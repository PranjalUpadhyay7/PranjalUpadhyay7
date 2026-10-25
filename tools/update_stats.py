#!/usr/bin/env python3
"""Write assets/github-stats.svg from the GitHub API. Standard library only.

In CI: GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER are set by the workflow.
Locally: GITHUB_TOKEN=... python3 tools/update_stats.py [login]
Without a token only repo and star counts are filled (REST, unauthenticated);
contribution tiles show "--" because contribution data needs GraphQL.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_assets import MONO, OUT, P, SANS, svg, write  # noqa: E402

QUERY = """
query($login:String!, $after:String) {
  user(login:$login) {
    contributionsCollection { contributionCalendar { totalContributions
      weeks { contributionDays { date contributionCount } } } }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, after: $after) {
      totalCount pageInfo { hasNextPage endCursor } nodes { stargazerCount } }
  }
}"""


def graphql(login, token):
    days, repos, stars, after = [], 0, 0, None
    while True:
        body = json.dumps({"query": QUERY, "variables": {"login": login, "after": after}}).encode()
        req = urllib.request.Request("https://api.github.com/graphql", body,
                                     {"Authorization": f"bearer {token}", "User-Agent": "profile-stats"})
        data = json.load(urllib.request.urlopen(req, timeout=30))
        if "errors" in data:
            raise RuntimeError(data["errors"])
        u = data["data"]["user"]
        if after is None:
            cal = u["contributionsCollection"]["contributionCalendar"]
            total = cal["totalContributions"]
            days = [d for w in cal["weeks"] for d in w["contributionDays"]]
        repos = u["repositories"]["totalCount"]
        stars += sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
        page = u["repositories"]["pageInfo"]
        if not page["hasNextPage"]:
            return total, days, repos, stars
        after = page["endCursor"]


def rest(login):
    repos, stars, page = 0, 0, 1
    while True:
        url = f"https://api.github.com/users/{login}/repos?per_page=100&page={page}&type=owner"
        batch = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "profile-stats"}), timeout=30))
        own = [r for r in batch if not r["fork"]]
        repos += len(own)
        stars += sum(r["stargazers_count"] for r in own)
        if len(batch) < 100:
            return repos, stars
        page += 1


def streaks(days, today=None):
    """days: [{'date','contributionCount'}] oldest first. Current streak may end yesterday."""
    today = today or dt.date.today().isoformat()
    counts = [(d["date"], d["contributionCount"]) for d in days if d["date"] <= today]
    longest = run = 0
    for _, c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i][1] == 0:  # today not contributed yet: streak is still alive
        i -= 1
    while i >= 0 and counts[i][1]:
        cur, i = cur + 1, i - 1
    return cur, longest


def render(total, cur, longest, repos, stars, stamp, source):
    tiles = [("CONTRIBUTIONS", total, "last 12 months"), ("CURRENT STREAK", cur, "days"),
             ("LONGEST STREAK", longest, "days, last 12 months"), ("STARS EARNED", stars, "on own repos")]
    gap = 12
    w = (716 - gap * 3) / 4
    body = ""
    for i, (label, val, sub) in enumerate(tiles):
        x = 2 + i * (w + gap)
        c = P["teal"] if i % 2 == 0 else P["amber"]
        v = "--" if val is None else f"{val:,}"
        body += (
            f'<rect x="{x:.1f}" y="2" width="{w:.1f}" height="104" rx="12" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<rect x="{x:.1f}" y="2" width="{w:.1f}" height="5" rx="2" fill="{c}"/>'
            f'<text x="{x + w / 2:.1f}" y="24" text-anchor="middle" font-family="{SANS}" font-size="9.5" letter-spacing="1.8" fill="{P["muted"]}">{label}</text>'
            f'<text x="{x + w / 2:.1f}" y="66" text-anchor="middle" font-family="{MONO}" font-size="{34 if len(v) < 5 else 28}" font-weight="700" fill="{c}">{v}</text>'
            f'<text x="{x + w / 2:.1f}" y="90" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{P["muted"]}">{sub}</text>'
        )
    body += (f'<text x="718" y="130" text-anchor="end" font-family="{SANS}" font-size="10.5" fill="{P["muted"]}">'
             f"updated {stamp} UTC {source}</text>")
    alt = (f"Live GitHub stats, updated {stamp} UTC: " + ", ".join(
        f"{l.lower()} {'unavailable' if v is None else v} ({s})" for l, v, s in tiles) + ".")
    write("github-stats.svg", svg(720, 138, "Live GitHub stats", alt, body))


def main():
    login = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "PranjalUpadhyay7"))
    token = os.environ.get("GITHUB_TOKEN")
    total = cur = longest = None
    if token:
        total, days, repos, stars = graphql(login, token)
        cur, longest = streaks(days)
    else:
        repos, stars = rest(login)
    source = "by a GitHub Action from the GitHub API" if token else "from public repo data; contributions arrive with the first Action run"
    render(total, cur, longest, repos, stars, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M"), source)
    print("wrote github-stats.svg", dict(total=total, cur=cur, longest=longest, repos=repos, stars=stars))


if __name__ == "__main__":
    main()

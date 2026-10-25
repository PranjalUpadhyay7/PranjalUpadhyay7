<div align="center">
<img src="assets/banner.gif" alt="Pranjal Upadhyay, Machine Learning Engineer, IISER Bhopal, expected May 2027. Machine learning systems that are measured, guarded and deployed on real hardware." width="100%">
</div>

<p align="center"><a href="https://www.linkedin.com/in/pranjal-upadhyay7">LinkedIn</a> · <a href="#quests">Quest log</a> · <a href="#achievements">Achievements</a> · <a href="#contact">Contact</a></p>

<p align="center"><img src="assets/journey.svg" alt="Flight log of my journey, animated as a drone flying a mission route. 1. Launch · Iiser Bhopal: BS-MS, Computer Science + Data Science (graduating May 2027). 2. First Reps: Learned to think fast in contests (645 problems · CodeChef max 1644). 3. First Research: Made a transformer forget less (forgetting 18.7% → 14.8%). 4. Tcs Research · 2025: Taught a robot gripper to pick, in simulation (PPO policy · 20 object categories). 5. Moon Lab: Flew drones where GPS can't reach (VIO 1.76–2.10x faster · flights at 50–80 m). 6. Thesis · Apr 2026: Rebuilt OpenVINS in Python, made it hover-aware (both repos open source). 7. Ap-Copilot · 2026: Built an LLM that can't write to the drone (60 tasks · 0 unsafe writes). 8. Next Waypoint: Your team. (full-time ML Engineer · India)." width="100%"></p>

<p align="center"><img src="assets/hud.svg" alt="Player 1: Pranjal. Class: ML engineer. Guild: IISER Bhopal. Quests: 9. Achievements unlocked: 6 of 9. Status: open to work." width="100%"></p>

<h2 id="quests"><img src="assets/section-quest-log.svg" alt="Quest log" width="100%"></h2>

<p align="center">
<a href="https://github.com/PranjalUpadhyay7/AP-Copilot"><img src="assets/card-ap-copilot.svg" alt="AP-Copilot, public repo. A safety-critical LLM agent that configures ArduPilot/Pixhawk parameters from plain-language requests; the model has no write tool, and deterministic validation plus a human-approval gate decide. Hybrid RAG with BM25, embeddings and RRF. On a 60-task benchmark the full system passed 59/60 for gpt-oss-20b versus 31/60 with retrieval and validation removed; no model produced an unsafe write on the full system. 480 tests, 219/219 mutants killed in the validation layer." width="100%"></a><br>
<a href="https://github.com/PranjalUpadhyay7/Detection_algo_benchmark"><img src="assets/card-nidar.svg" alt="NIDAR 2.0, team lead of 6. Building an 8-drone disaster-search swarm; validated in simulation with 2 recon and 4 delivery drones over 10 hectares; the full mission is the planned target. LEAF-YOLO-s at 4.5 to 4.6 FPS on a Jetson Nano; GNSS-denied navigation flight-validated at 50 to 80 m." width="100%"></a><br>
<a href="https://github.com/Shafwansafi06/vio_pipeline_cpp"><img src="assets/card-dodvins.svg" alt="DODVins, a data-oriented C++ reimplementation of the OpenVINS MSCKF visual-inertial odometry pipeline, by Shafwan Safi, Nikhil Vashisht and Pranjal Upadhyay (project lead). Same filter equations, different memory layout. On ten public sequences in the same toolchain container it matches OpenVINS accuracy (mean ATE 0.156 m vs 0.158 m, better on 4 of 10) while running 1.76 to 2.10x faster end to end, and it is faster on all ten on a Jetson Orin Nano. Paper and presentation are in the repo." width="100%"></a><br>
<img src="assets/card-liquid-nn.svg" alt="Liquid neural network adaptive controller with online parameter updates on a background thread; about 340x lower control-loop latency and about 19% lower tracking error than a DNN plus ODE-solver baseline. Journal paper in preparation." width="100%"><br>
<a href="https://github.com/PranjalUpadhyay7/dytox_modification"><img src="assets/card-dytox.svg" alt="Two extensions to the DyTox continual-learning transformer on CIFAR-100. The Task-Aware Encoder cut forgetting from 18.7% to 14.8%. Dynamic Contextual Positional Embeddings cost 3.2 to 3.3 points, which I report." width="100%"></a><br>
<a href="https://github.com/PranjalUpadhyay7/openvins-python-hovering-aware-msckf"><img src="assets/card-openvins-python.svg" alt="A Python port of the OpenVINS MSCKF visual-inertial estimator, plus a hovering-aware extension that implements the motion-classification algorithm of Kottas, Wu and Roumeliotis (IROS 2014), for which no reference code was published. It is the implementation behind my BS thesis at IISER Bhopal (April 2026). Validated on a Jetson Orin Nano UAV against the KAIST VIO benchmark and a custom hovering flight dataset." width="100%"></a><br>
<a href="https://github.com/PranjalUpadhyay7/DROID-SLAM-on-OAKD_pro-realtime"><img src="assets/card-droid-slam.svg" alt="My fork of DROID-SLAM (Teed and Deng) that adds a real-time demo driven by a live OAK-D camera stream." width="100%"></a><br>
<a href="https://github.com/PranjalUpadhyay7/Federated_Learning"><img src="assets/card-federated.svg" alt="Federated Mood Prediction for Early Depression Screening. Flower pipeline predicting 5-class mood from smartphone behavioural signals, DiversityOne dataset, non-IID clients. TabM 69.95%, LSTM 68.28%, within 2% of centralized." width="100%"></a><br>
<a href="https://devpost.com/software/novalearn-ty2b3k"><img src="assets/card-novalearn.svg" alt="NovaLearn. Planner plus executor multi-agent study companion on four Amazon Nova models through an AWS Bedrock layer; a 4-scene parallel pipeline produces a 24 second animation in about 4 minutes; shipped as a Chrome extension." width="100%"></a>
</p>

<details>
<summary><b>AP-Copilot: how a parameter change gets written</b></summary>

The model can read, search and propose. It has no write tool. Every stage after the proposal is ordinary deterministic code.

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#111832','primaryTextColor':'#E6EDF7','primaryBorderColor':'#2DD4BF','lineColor':'#8FA0C0'}}}%%
flowchart TD
    U([You ask in plain language]) --> L[LLM agent<br/>read, search, propose]
    L -->|proposal| V[Validation Layer<br/>exists, type, range, enum]
    V -->|rejected| L
    V -->|accepted| H[/Human approval<br/>critical: cooldown + type the name/]
    H -->|confirmed| W[Write-time checks<br/>fresh values, disarmed, rate limit]
    W -->|pass| P[Write + read-back ack]
    P --> A[(Hash-chained audit log)]
    H -.->|rejected| L
    W -.->|blocked| L
```
</details>

<details>
<summary><b>All repos and links</b></summary>

Code: <a href="https://github.com/PranjalUpadhyay7/AP-Copilot">AP-Copilot</a> · <a href="https://github.com/Shafwansafi06/vio_pipeline_cpp">vio_pipeline_cpp</a> (DODVins, with Shafwan Safi and Nikhil Vashisht) · <a href="https://github.com/PranjalUpadhyay7/openvins-python-msckf">openvins-python-msckf</a> · <a href="https://github.com/PranjalUpadhyay7/openvins-python-hovering-aware-msckf">openvins-python-hovering-aware-msckf</a> (thesis, GPL-3.0, derived from <a href="https://github.com/rpng/open_vins">OpenVINS</a>) · <a href="https://github.com/PranjalUpadhyay7/Federated_Learning">Federated_Learning</a> · <a href="https://github.com/PranjalUpadhyay7/dytox_modification">dytox_modification</a> (built on <a href="https://github.com/arthurdouillard/dytox">DyTox</a> by Douillard et al.) · <a href="https://github.com/PranjalUpadhyay7/Detection_algo_benchmark">Detection_algo_benchmark</a> · <a href="https://github.com/PranjalUpadhyay7/DROID-SLAM-on-OAKD_pro-realtime">DROID-SLAM-on-OAKD_pro-realtime</a> · <a href="https://devpost.com/software/novalearn-ty2b3k">NovaLearn on DevPost</a>
</details>

<details>
<summary><b>How these numbers were measured</b></summary>

- AP-Copilot: my own 60-task benchmark, machine-checked against what a fake vehicle received (no LLM judge). "Unsafe write" means a value the project's own validator would reject. 31/60 to 59/60 is one model (gpt-oss-20b), one repeat, with safety layers removed cumulatively; the 0 unsafe writes covers five models at 3 repeats on the full system. The 219 mutants cover the validation layer only. Free-tier models and author-written tasks: see the repo's caveats.
- OpenVINS in Python: a port that mirrors OpenVINS's structure and is GPL-3.0 as a derivative work; static initialisation only, ROS 1 required, a thesis artifact rather than a production estimator.
- TCS results are simulation only. The NIDAR swarm is simulation-validated; the 8-drone mission is the planned target and has not flown. GNSS-denied flights were validated at 50 to 80 m.
- DODVins: numbers from the team's paper (`paper/main.tex` in the repo; authors Shafwan Safi, Nikhil Vashisht, Pranjal Upadhyay). Ten public sequences (EuRoC, KAIST) run through the same transport and toolchain container as official OpenVINS: mean ATE 0.156 m vs 0.158 m (better on 4 of 10), 1.76 to 2.10x faster end to end. On a Jetson Orin Nano it is faster on all ten, with a narrower margin. Same filter equations as OpenVINS; the change is memory layout.
- Detector benchmark: 11 public detectors, VisDrone2019-DET validation set (person class), mAP@0.5 0.487 for LEAF-YOLO-s vs 0.438 for YOLOv8x on a PC CPU. The Jetson Nano figure is end to end for LEAF-YOLO-s only.
- Achievements: unlocked ones are the measured results above; locked ones are planned or in progress and have not happened. The 219 mutants cover the validation layer only.
- The Liquid NN result is from my own experiments; the paper is in preparation. Federated results are as reported in that repo; clients ran as Flower processes, not on phones.
</details>

<h2 id="achievements"><img src="assets/section-achievements.svg" alt="Achievements" width="100%"></h2>

<p align="center"><img src="assets/achievements.svg" alt="Achievements. Unlocked: Zero Unsafe Writes (60 tasks, 5 models); 100% Mutants Killed (219/219, validation layer); Honest Reporter (DCPE cost 3.2 pts, shown); Outpaced Openvins (1.76–2.10x, same accuracy); Light On A Nano (LEAF-YOLO-s, 4.5 FPS); Off The Grid (GNSS-denied, 50–80 m flights). Locked, planned or in progress: Full Swarm Flight (planned target: 8 drones); Paper Published (liquid-NN paper in prep); First Ml Role (full-time, India: you?)." width="100%"></p>

<h2 id="training"><img src="assets/section-training-grounds.svg" alt="Training grounds" width="100%"></h2>

<p align="center"><a href="https://github.com/PranjalUpadhyay7/My_certificates/blob/main/2924342-Pranjal%20Upadhyay%C2%A0.pdf"><img src="assets/experience-tcs.svg" alt="TCS Research and Innovation, Research Intern in AI and Robotics, 12 May to 31 Aug 2025 (certificate linked). Robotic Mobile Manipulation Platform for Retail and Warehouses: PyBullet platform with 4 warehouse scenarios and 20 object categories, RGB-D 6-DoF grasp pose prediction in clutter, PPO policy trained over a 48-hour simulation run, 15 to 30 s per-object pick cycles. Simulation only." width="100%"></a></p>
<p align="center"><img src="assets/experience-moon.svg" alt="MOON Lab, IISER Bhopal, undergraduate researcher for two years, advised by Dr. P. B. Sujit. Perception, state estimation, adaptive control and GNSS-denied navigation; algorithms deployed on Jetson edge devices and drones; Python implementation of OpenVINS." width="100%"></p>

<h2 id="inventory"><img src="assets/section-inventory.svg" alt="Inventory" width="100%"></h2>

<p align="center"><img src="assets/skills.svg" alt="Skills. ML and deep learning: PyTorch, TabM, LSTM, Transformers, Continual learning, Federated learning, RL (PPO), Object detection. Robotics: VIO (OpenVINS, MSCKF, EKF), Visual SLAM, GNSS-denied navigation, PyBullet, Adaptive control, ROS 2, Drone and edge hardware. GenAI and NLP: LangGraph, Hybrid RAG, Agent guardrails, AWS Bedrock, Whisper. Languages: Python, C++, TypeScript, Rust. Deployment: FastAPI, TensorRT FP16, Jetson Nano and Orin Nano, ArduPilot, pytest and mutmut." width="100%"></p>

<p align="center"><a href="https://codolio.com/profile/PranjalUpadhyay"><img src="assets/coding.svg" alt="Competitive programming on Codolio. Max ratings: CodeChef 1644 (3 star), CodeStudio 1741, CodeForces 1128. 645 questions solved, 42 contests attended, longest streak 28 days." width="100%"></a></p>

<h2 id="contact"><img src="assets/section-contact.svg" alt="Contact" width="100%"></h2>

<p align="center">Open to full-time ML Engineer roles in India. Message me on <a href="https://www.linkedin.com/in/pranjal-upadhyay7"><b>LinkedIn</b></a>.</p>
<p align="center"><img src="assets/github-stats.svg" alt="Live GitHub stats, refreshed daily by a GitHub Action: contributions and streaks over the last 12 months, and stars earned. Open github.com/PranjalUpadhyay7 for the current numbers." width="100%"></p>
<p align="center"><img src="assets/footer.svg" alt="Pranjal Upadhyay, Bhopal, India" width="100%"></p>

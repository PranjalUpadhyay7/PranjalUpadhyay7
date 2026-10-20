<div align="center">
<img src="assets/banner.svg" alt="Pranjal Upadhyay, Machine Learning Engineer, IISER Bhopal, expected May 2027. Machine learning systems that are measured, guarded and deployed on real hardware." width="100%">
</div>

<p align="center"><a href="https://www.linkedin.com/in/pranjal-upadhyay7">LinkedIn</a> · <a href="#selected-work">Selected work</a> · <a href="#contact">Contact</a></p>

<p align="center"><img src="assets/stats.svg" alt="0 unsafe writes on the 30-task AP-Copilot benchmark; 2x faster OpenVINS update at accuracy parity; about 340x lower control-loop latency for the liquid neural network controller; 3.9 percentage points less forgetting from the DyTox Task-Aware Encoder." width="100%"></p>

I build LLM agents with safety guardrails, deep-learning systems, and robotics that runs on real hardware (Jetson, drones). Two years in a robotics lab, TCS Research intern, BS-MS at IISER Bhopal (exp. May 2027), looking for full-time ML Engineer roles in India.

<h2 id="selected-work"><img src="assets/section-selected-work.svg" alt="Selected work" width="100%"></h2>

<p align="center"><img src="assets/card-ap-copilot.svg" alt="AP-Copilot, public release soon. A safety-critical LLM agent that configures ArduPilot/Pixhawk parameters from plain-language requests; deterministic guardrails and a human-approval gate block unsafe changes. Hybrid RAG with BM25, embeddings and RRF. 20/30 to 30/30 tasks, 0 unsafe writes, 219/219 mutants killed." width="100%"></p>
<p align="center"><a href="https://github.com/PranjalUpadhyay7/Federated_Learning"><img src="assets/card-federated.svg" alt="Federated Mood Prediction for Early Depression Screening. Flower pipeline predicting 5-class mood from smartphone behavioural signals, DiversityOne dataset, non-IID clients. TabM 69.95%, LSTM 68.28%, within 2% of centralized." width="100%"></a></p>
<p align="center"><a href="https://devpost.com/software/novalearn-ty2b3k"><img src="assets/card-novalearn.svg" alt="NovaLearn. Planner plus executor multi-agent study companion on four Amazon Nova models through an AWS Bedrock layer; a 4-scene parallel pipeline produces a 24 second animation in about 4 minutes; shipped as a Chrome extension." width="100%"></a></p>
<p align="center"><a href="https://github.com/PranjalUpadhyay7/dytox_modification"><img src="assets/card-dytox.svg" alt="Two extensions to the DyTox continual-learning transformer on CIFAR-100. The Task-Aware Encoder cut forgetting from 18.7% to 14.8%. Dynamic Contextual Positional Embeddings cost 3.2 to 3.3 points, which I report." width="100%"></a></p>
<p align="center"><img src="assets/card-liquid-nn.svg" alt="Liquid neural network adaptive controller with online parameter updates on a background thread; about 340x lower control-loop latency and about 19% lower tracking error than a DNN plus ODE-solver baseline. Journal paper in preparation." width="100%"></p>
<p align="center"><a href="https://github.com/PranjalUpadhyay7/Detection_algo_benchmark"><img src="assets/card-nidar.svg" alt="NIDAR 2.0, team lead of 6. Building an 8-drone disaster-search swarm; validated in simulation with 2 recon and 4 delivery drones over 10 hectares; the full mission is the planned target. OpenVINS backend update 7.5 ms to 3.7 to 4.0 ms; LEAF-YOLO-s at 4.5 to 4.6 FPS on a Jetson Nano; GNSS-denied navigation flight-validated at 50 to 80 m." width="100%"></a></p>
<p align="center"><img src="assets/card-openvins-python.svg" alt="My Python implementation of the OpenVINS visual-inertial estimator, written with data-oriented design. Public release soon." width="100%"></p>
<p align="center"><a href="https://github.com/PranjalUpadhyay7/DROID-SLAM-on-OAKD_pro-realtime"><img src="assets/card-droid-slam.svg" alt="My fork of DROID-SLAM (Teed and Deng) that adds a real-time demo driven by a live OAK-D camera stream." width="100%"></a></p>

<p align="center">Code: <a href="https://github.com/PranjalUpadhyay7/Federated_Learning">Federated_Learning</a> · <a href="https://github.com/PranjalUpadhyay7/dytox_modification">dytox_modification</a> (built on <a href="https://github.com/arthurdouillard/dytox">DyTox</a> by Douillard et al.) · <a href="https://github.com/PranjalUpadhyay7/Detection_algo_benchmark">Detection_algo_benchmark</a> · <a href="https://github.com/PranjalUpadhyay7/DROID-SLAM-on-OAKD_pro-realtime">DROID-SLAM-on-OAKD_pro-realtime</a> · <a href="https://devpost.com/software/novalearn-ty2b3k">NovaLearn on DevPost</a></p>

<details>
<summary><b>How these numbers were measured</b></summary>

- AP-Copilot: my own 30-task benchmark, machine-checked against what a fake vehicle received (no LLM judge). "Unsafe write" means a value the project's own validator would reject. The 219 mutants cover the validation layer only.
- TCS results are simulation only. The NIDAR swarm is simulation-validated; the 8-drone mission is the planned target and has not flown. GNSS-denied flights were validated at 50 to 80 m. The OpenVINS C++ speed-up was a 3-person effort at accuracy parity.
- Detector benchmark: 11 public detectors, VisDrone2019-DET validation set (person class), mAP@0.5 0.487 for LEAF-YOLO-s vs 0.438 for YOLOv8x on a PC CPU. The Jetson Nano figure is end to end for LEAF-YOLO-s only.
- The Liquid NN result is from my own experiments; the paper is in preparation. Federated results are as reported in that repo; clients ran as Flower processes, not on phones.
</details>

<h2 id="experience"><img src="assets/section-experience.svg" alt="Experience" width="100%"></h2>

<p align="center"><a href="https://github.com/PranjalUpadhyay7/My_certificates/blob/main/2924342-Pranjal%20Upadhyay%C2%A0.pdf"><img src="assets/experience-tcs.svg" alt="TCS Research and Innovation, Research Intern in AI and Robotics, 12 May to 31 Aug 2025 (certificate linked). Robotic Mobile Manipulation Platform for Retail and Warehouses: PyBullet platform with 4 warehouse scenarios and 20 object categories, RGB-D 6-DoF grasp pose prediction in clutter, PPO policy trained over a 48-hour simulation run, 15 to 30 s per-object pick cycles. Simulation only." width="100%"></a></p>
<p align="center"><img src="assets/experience-moon.svg" alt="MOON Lab, IISER Bhopal, undergraduate researcher for two years, advised by Dr. P. B. Sujit. Perception, state estimation, adaptive control and GNSS-denied navigation; algorithms deployed on Jetson edge devices and drones; Python implementation of OpenVINS." width="100%"></p>

<h2 id="skills"><img src="assets/section-skills.svg" alt="Skills" width="100%"></h2>

<p align="center"><img src="assets/skills.svg" alt="Skills. ML and deep learning: PyTorch, TabM, LSTM, Transformers, Continual learning, Federated learning, RL (PPO), Object detection. Robotics: VIO (OpenVINS, MSCKF, EKF), Visual SLAM, GNSS-denied navigation, PyBullet, Adaptive control, ROS 2, Drone and edge hardware. GenAI and NLP: LangGraph, Hybrid RAG, Agent guardrails, AWS Bedrock, Whisper. Languages: Python, C++, TypeScript, Rust. Deployment: FastAPI, TensorRT FP16, Jetson Nano and Orin Nano, ArduPilot, pytest and mutmut." width="100%"></p>

<sub>ISRO Hackathon '24 and '25 and Google AI Builder Lab are certificates, not awards. NovaLearn was submitted to the Amazon Nova Hackathon 2025 (no win claimed). CodeChef max rating 1644 (3 star).</sub>

<h2 id="contact"><img src="assets/section-contact.svg" alt="Contact" width="100%"></h2>

<p align="center"><a href="https://www.linkedin.com/in/pranjal-upadhyay7">linkedin.com/in/pranjal-upadhyay7</a></p>
<p align="center"><img src="assets/footer.svg" alt="Pranjal Upadhyay, Bhopal, India" width="100%"></p>

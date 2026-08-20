# Reinforcement Learning-Based Adaptive Traffic Signal Control

A research project that applies **Reinforcement Learning (RL)** to adaptive traffic signal control using **SUMO (Simulation of Urban MObility)**.

The project investigates and implements multiple reinforcement learning approaches for traffic signal control, including:

* **Q-Learning**
* **Double Q-Learning**
* **Multi-Agent Double Q-Learning**

The objective is to enable traffic lights to adapt their signal phases based on the current traffic conditions and learn policies that help improve traffic flow.

---

## Overview

Traditional traffic signal systems often rely on predefined timing plans. However, traffic conditions can change dynamically depending on vehicle density, congestion, and traffic flow.

In this project, traffic signal control is formulated as a **Reinforcement Learning problem**, where an agent interacts with a simulated traffic environment and learns which traffic signal action to take based on the current state of the intersection.

The general learning process consists of:

1. Observing the current traffic state.
2. Selecting a traffic signal action.
3. Applying the action in the SUMO simulation.
4. Receiving a reward based on traffic conditions.
5. Updating the learning policy.
6. Repeating the process over multiple simulation steps and episodes.

---

## Implemented Algorithms

### 1. Q-Learning

Located in:

```text id="yvmkxq"
traffic_simulator_qleaning/
```

This implementation uses a traditional **Q-Learning agent** to learn the expected value of each action for a given traffic state.

The Q-value is updated using the Bellman equation:

```text id="fvcieq"
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

The Q-Learning implementation includes:

* State-based traffic control.
* ε-greedy exploration.
* Q-table learning.
* Agent training and model saving.
* Simulation result analysis and visualization.

---

### 2. Double Q-Learning

Located in:

```text id="yif2z9"
traffic_simulator_dbq/
```

The Double Q-Learning implementation uses two separate Q-tables:

```text id="cmiv6c"
Q1
Q2
```

During training, one Q-table is updated while the other is used to estimate the value of the next state.

This approach helps reduce the **overestimation bias** that may occur in traditional Q-Learning.

The agent supports:

* Two Q-tables (`Q1` and `Q2`).
* ε-greedy exploration.
* Adaptive exploration decay.
* Learning rate adjustment during training.
* Model saving and loading using JSON.
* Training statistics tracking.
* Evaluation using the combined values of `Q1` and `Q2`.

The agent selects actions based on:

```text id="7o3jxu"
argmax(Q1(s, a) + Q2(s, a))
```

---

### 3. Multi-Agent Double Q-Learning

Located in:

```text id="g5cwxm"
traffic_simulator_mdbq/
```

This implementation extends Double Q-Learning to a **multi-agent traffic control scenario**.

Multiple agents are used to control different traffic signals or intersections within the simulated traffic network.

The goal is to explore how reinforcement learning agents can operate in a more complex traffic environment compared with a single-agent setting.

The implementation includes:

* Multiple learning agents.
* Double Q-Learning-based decision making.
* Independent or distributed traffic signal control.
* Multi-intersection traffic simulation.
* Training and performance analysis.

---

# Project Structure

```text id="x6lmbt"
traffic_simulation/
│
├── traffic_simulator_qleaning/
│   ├── qlearning_agent.py
│   ├── traffic_brain.py
│   ├── simulation.py
│   ├── train_q.py
│   └── analysis.py
│
├── traffic_simulator_dbq/
│   ├── configs/
│   │   └── large_intersection.sumocfg
│   │
│   ├── models/
│   │   └── agent checkpoints
│   │
│   ├── double_qlearning_agent.py
│   ├── traffic_brain.py
│   ├── simulation.py
│   ├── train_db.py
│   └── analysis.py
│
├── traffic_simulator_mdbq/
│   ├── multi_double_qlearning_agent.py
│   ├── traffic_brain.py
│   ├── simulation.py
│   ├── train_mdb.py
│   └── analysis.py
│
├── .gitignore
└── README.md
```

---

# Requirements

The project requires:

* **Python 3.x**
* **SUMO Simulator**
* NumPy
* Pandas
* Matplotlib

Install the Python dependencies:

```bash id="9z4d7q"
pip install numpy pandas matplotlib
```

---

# SUMO Installation

The project uses **SUMO (Simulation of Urban MObility)** as the traffic simulation environment.

After installing SUMO, make sure the `SUMO_HOME` environment variable is configured correctly.

For example:

### Windows

```text id="1x4i1s"
SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo
```

The exact path may differ depending on your SUMO installation.

You can verify the installation using:

```bash id="0zj4al"
sumo --version
```

---

# Running the Project

Each implementation contains its own training and simulation scripts.

## Q-Learning

Navigate to:

```bash id="eq5e6t"
cd traffic_simulator_qleaning
```

Run training:

```bash id="3zzy3b"
python train_q.py
```

---

## Double Q-Learning

Navigate to:

```bash id="zhrqaa"
cd traffic_simulator_dbq
```

Run training:

```bash id="31h3vk"
python train_db.py
```

The trained agent can be saved as a JSON file containing:

* Q1 table.
* Q2 table.
* Current exploration rate.
* Learning rate.
* Training statistics.
* Number of training steps.

Example model files:

```text id="0u1y6j"
models/
├── agent_ep10_*.json
├── agent_ep50_*.json
└── agent_ep100_*.json
```

---

## Multi-Agent Double Q-Learning

Navigate to:

```bash id="h9ghp9"
cd traffic_simulator_mdbq
```

Run training:

```bash id="d6ud6z"
python train_mdb.py
```

---

# Traffic Simulation

The simulation environment is implemented using SUMO.

The main simulation components include:

```text id="ogfw1c"
simulation.py
```

Responsible for running the SUMO simulation and collecting traffic information.

```text id="wdqmcm"
traffic_brain.py
```

Responsible for connecting the reinforcement learning agent with the traffic environment and making traffic signal decisions.

```text id="9nr0e6"
*_agent.py
```

Contains the implementation of the corresponding reinforcement learning algorithm.

---

# Training

During training, the agent repeatedly interacts with the traffic environment.

A typical training episode follows the process:

```text id="xipuqn"
Traffic State
      │
      ▼
Reinforcement Learning Agent
      │
      ▼
Select Traffic Signal Action
      │
      ▼
SUMO Simulation
      │
      ▼
Observe Traffic Conditions
      │
      ▼
Calculate Reward
      │
      └───────────────► Update Agent
```

The agent gradually learns a policy for selecting traffic signal actions based on the observed traffic state.

---

# Model Persistence

The Double Q-Learning implementation supports saving and loading trained agents.

The saved model contains:

```text id="xtpfmx"
{
    "q1": "...",
    "q2": "...",
    "epsilon": "...",
    "learning_rate": "...",
    "episode_rewards": "...",
    "training_steps": "..."
}
```

This allows a trained agent to be reused without starting the learning process from scratch.

---

# Analysis and Visualization

Each implementation provides an `analysis.py` script for analyzing simulation results.

The analysis tools can visualize several traffic metrics, including:

* Average waiting time.
* Maximum waiting time.
* Minimum waiting time.
* Waiting time distribution.
* Queue length.
* Number of active vehicles.

For example, the Double Q-Learning analysis module can compare simulation results between different intersection configurations, such as:

```text id="l74cth"
Small Intersection
        vs
Large Intersection
```

The analysis results can be displayed and saved as figures.

Run:

```bash id="xuxbgd"
python analysis.py
```

---

# Research Objective

The main objective of this project is to investigate the effectiveness of different reinforcement learning approaches for adaptive traffic signal control.

The project explores the following progression:

```text id="nbcrfg"
Q-Learning
    │
    ▼
Double Q-Learning
    │
    ▼
Multi-Agent Double Q-Learning
```

The implementations allow experiments to be conducted on increasingly complex traffic control scenarios.

---

# Technologies

* **Python**
* **SUMO**
* **TraCI**
* **NumPy**
* **Pandas**
* **Matplotlib**
* **Reinforcement Learning**

---


# Author

Developed as part of a **scientific research project on applying Reinforcement Learning to adaptive traffic signal control**.

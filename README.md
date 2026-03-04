# Next-Gen-Autonomous-vehicle-iot-raspberry-pi
IoT-based autonomous vehicle system using Raspberry Pi, OpenCV &amp; sensors for real-time traffic signal detection, ambulance recognition, obstacle avoidance &amp; alcohol detection.


## Overview

This project presents the development of a next-generation autonomous vehicle system that leverages the **Internet of Things (IoT)** to enhance real-time detection of traffic signals, pedestrians, obstacles, and emergency vehicles. Built on a **Raspberry Pi**, the system integrates multiple sensors and a camera module to continuously gather and process live environmental data, enabling the vehicle to make safe and intelligent driving decisions without human intervention.


## Problem Statement

Current autonomous vehicles in India or any place which is crowded with lousy traffic following rule cities often struggle to accurately detect and respond to traffic signals, pedestrians, and obstacles in complex urban environments. This system addresses those limitations by combining IoT sensors, computer vision, and real-time data processing to significantly improve vehicle situational awareness and road safety.

---

## Hardware Components

| Component | Purpose |
|---|---|
| Raspberry Pi | Central processing unit and controller |
| HC-SR04 Ultrasonic Sensor | Obstacle distance measurement |
| Raspberry Pi Camera Module | Visual detection of signals and emergency vehicles |
| MQ-3 Gas / Alcohol Sensor | Alcohol detection — disables vehicle if triggered |
| Relay Module | Controls vehicle motor (ON / OFF) |
| Buzzer | Audio alert system |
| LCD Display | Real-time status display |
| DHT11 Sensor | Temperature and humidity monitoring |

---

## System Logic

The system operates in a continuous real-time loop, evaluating sensor inputs on every cycle and taking immediate action based on the following conditions:

| Condition | Action |
|---|---|
| Red signal detected | Relay OFF — vehicle stops, Buzzer ON |
| White / ambulance detected | Relay OFF — vehicle yields |
| Obstacle within 15 cm | Relay OFF — emergency stop, Buzzer ON |
| Alcohol / gas detected | Relay OFF, Buzzer ON — driver safety override |
| All conditions clear | Relay ON — vehicle operates normally |

Color detection is implemented using **HSV color space** via OpenCV to identify red traffic signals and white ambulance markings from the live camera feed.

---

## Tech Stack

- **Language:** Python
- **Libraries:** OpenCV, RPi.GPIO, NumPy
- **IDE:** Geany (Raspberry Pi OS)
- **Hardware Platform:** Raspberry Pi
- **Communication Protocol:** GPIO | V2X (planned for future scope)

---

## Project Structure

```
├── san2.py              # Main program — all detection and control logic
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation

```

---

## Setup and Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/autonomous-vehicle-iot-raspberry-pi.git
cd autonomous-vehicle-iot-raspberry-pi
```

**2. Install dependencies**
```bash
pip install opencv-python RPi.GPIO numpy
```

**3. Run on Raspberry Pi**
```bash
python san2.py
```
> Press `q` to exit the live video window.

---

## Key Features

- Real-time traffic signal detection using computer vision
- Emergency vehicle (ambulance) recognition via colour detection
- Ultrasonic obstacle detection with automatic vehicle stop
- Alcohol and gas detection for driver safety enforcement
- Live video feed with on-screen status overlay
- Modular and extensible IoT sensor architecture

---

## Future Scope

- Integration of advanced LiDAR and radar sensors for wider environment coverage
- Vehicle-to-Everything (V2X) communication for coordinated traffic management
- Cloud platform integration for data logging and algorithm refinement
- Enhanced AI/ML models for pedestrian and cyclist behaviour prediction
- System testing and optimisation for adverse weather conditions

---

## Team

| Name | Role |
| Ruchira Ravindra Karle | Developer & Researcher |


---

## License

© 2025 Ruchira Karle. All rights reserved.  
This project is made publicly available for viewing and academic reference only.  
No part of this project may be copied, modified, distributed, or used without  
explicit written permission from the authors.

# 🚦 Density-Based Traffic Light Simulation (AIoT & Computer Vision)

A smart AIoT system designed to optimize traffic flow by dynamically adjusting traffic light timings based on real-time vehicle density, thereby reducing commuter waiting time, fuel consumption, and emissions.

This project combines **Computer Vision** on an edge device with **IoT communication** to create a responsive and data-driven solution for urban traffic management.

---

## ✨ Key Features & Impact

* **Dynamic Optimization:** Uses real-time vehicle density data to adjust traffic light durations, replacing static, inefficient timers.
* **Emissions Reduction:** Demonstrably reduces vehicle idle time and fuel consumption, contributing to lower urban emissions.
* **End-to-End AIoT Pipeline:** Integrates live data processing (density count), cloud logging (Google Sheets), and physical hardware actuation (Raspberry Pi Pico control).
* **Technology Showcase:** Combines advanced **Python** libraries for computer vision with IoT/Embedded programming.

---

## 🏗️ Project Architecture & Workflow

The system operates in two main loops:

1.  **Density Calculation (Host PC):** A Python script uses the webcam/stream to perform real-time **Computer Vision** analysis, counting the number of vehicles (density). This data is logged to Google Sheets via the API.
2.  **Light Control (Raspberry Pi Pico):** The Pico device constantly retrieves the latest density data from Google Sheets and uses that information to control the attached traffic light LEDs, switching between long, medium, and short cycles.



[Image of Project Workflow Diagram]


---

## 💻 Repository Files & Purpose

| File Name | Purpose | Technology/Platform |
| :--- | :--- | :--- |
| `rd.py` | **Density Counting & Data Sending.** This is the main Python script that runs the Computer Vision model, detects real-time vehicle density, and sends the calculated data to the Google Sheets log via API. | Python (OpenCV, Google Sheets API) |
| `retrieve_lcd.py` | **Traffic Light Control Logic.** The MicroPython script that runs on the Raspberry Pi Pico. It retrieves the latest density data from Google Sheets and contains the core logic to dynamically adjust the LED light sequence (the simulation of the traffic lights). | MicroPython (Thonny), RPi Pico |
| `pico_lcd.py` | **LCD Panel Driver.** Contains the foundational MicroPython code for interfacing and controlling the attached LCD screen, enabling the Pico to display status/density. | MicroPython, RPi Pico |
| `pico_i2c_lcd.py` | **I2C LCD Library.** Necessary driver file to handle I2C communication between the Raspberry Pi Pico and the LCD module. | MicroPython, RPi Pico (I2C) |
| `index.html` | **Live Dashboard Frontend.** The front-end code for the live dashboard used to visualize the real-time density data logged to Google Sheets. (Visible at the live link). | HTML, CSS, JavaScript |

---

## 🛠️ Technology Stack

* **Programming:** Python, MicroPython (Thonny)
* **Machine Learning/Vision:** OpenCV (for Computer Vision/Vehicle Detection)
* **IoT/Hardware:** Raspberry Pi Pico W, LEDs, LCD Panel
* **Data/Cloud:** Google Sheets API
* **Frontend:** HTML, CSS, JavaScript

---

## 🔗 Live Demonstration

* **Project Video Demo:** [https://www.linkedin.com/posts/yaswanthkumar-katari_aiot-smarttrafficsystem-computervision-activity-7315552305984995328-TaKm?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEytyXkBBLbIYF8e-7DS0nRHiqxemizkRBg](https://www.linkedin.com/posts/yaswanthkumar-katari_aiot-smarttrafficsystem-computervision-activity-7315552305984995328-TaKm?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEytyXkBBLbIYF8e-7DS0nRHiqxemizkRBg)
* **Live Dashboard:** [https://livetrafficdensity.netlify.app/](https://livetrafficdensity.netlify.app/)

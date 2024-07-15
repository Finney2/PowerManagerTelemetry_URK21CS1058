# PowerManagerTelemetry_URK21CS1058
# System Telemetry Dashboard

## Introduction

This project provides a web-based dashboard to monitor various system telemetry data, including CPU usage, memory usage, network interface controller (NIC) telemetry, and thermal design power (TDP). The dashboard allows users to simulate CPU load and observe how the system responds over time.

## Features

- Real-time monitoring of CPU, memory, NIC, and TDP telemetry.
- Simulate CPU load and visualize the impact on system telemetry.
- User-friendly web interface with interactive charts.

## Prerequisites

- Python 3.x
- Flask
- psutil
- multiprocessing
- random
- datetime
- Bootstrap (for frontend styling)
- Chart.js (for data visualization)

## Installation

1. Clone the repository:
    sh
    git clone https://github.com/yourusername/system-telemetry-dashboard.git
    cd system-telemetry-dashboard
    

2. Create a virtual environment (optional but recommended):
    sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    

3. Install the required packages:
    sh
    pip install flask psutil
    

## Running the Application

1. Start the Flask application:
    sh
    python app.py
    

2. Open your web browser and navigate to:
    
    http://127.0.0.1:5000
    

## Usage

1. Open the application in your web browser.
2. Enter the desired CPU utilization percentage and duration in seconds.
3. Click the "Start" button to simulate the load and begin telemetry data collection.
4. Observe the telemetry data displayed in the interactive charts.

## Code Overview

### app.py

- *Flask Application*: The main Flask application is defined here, with routes for the homepage (/) and the start of the telemetry data collection (/start).
- *Telemetry Functions*: Functions to collect CPU, memory, NIC, and TDP telemetry data using the psutil library.
- *Load Simulation Functions*: Functions to simulate CPU load and generate system stress.

### Templates

- *index()*: The HTML template for the main dashboard. It includes a form to input the CPU utilization percentage and duration, and placeholders for the telemetry data charts.

### Static Files

- *CSS*: Bootstrap for styling the frontend.
- *JavaScript*: jQuery for handling form submissions and AJAX requests, and Chart.js for data visualization.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

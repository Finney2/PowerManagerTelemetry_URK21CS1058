import time
import psutil
import multiprocessing
from datetime import datetime
from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)

# Function to get CPU telemetry data
def get_cpu_telemetry():
    cpu_times = psutil.cpu_times_percent(interval=1, percpu=False)
    cpu_data = {
        "user": cpu_times.user,
        "system": cpu_times.system,
        "idle": cpu_times.idle,
    }
    return cpu_data

# Function to get memory telemetry data
def get_memory_telemetry():
    mem = psutil.virtual_memory()
    memory_data = {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "free": mem.free,
        "percent": mem.percent,
    }
    return memory_data

# Function to get NIC telemetry data
def get_nic_telemetry():
    nic = psutil.net_io_counters(pernic=True)
    nic_data = {iface: {"bytes_sent": data.bytes_sent, "bytes_recv": data.bytes_recv} for iface, data in nic.items()}
    return nic_data

# Function to get TDP telemetry data (simulate dynamic changes)
def get_tdp_telemetry():
    current_tdp = random.uniform(10.0, 20.0)  # Simulate dynamic TDP values
    max_tdp = 25.0
    tdp_data = {
        "current_tdp": round(current_tdp, 2),
        "max_tdp": max_tdp,
    }
    return tdp_data

# Function to simulate CPU load
def cpu_load(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pass

# Function to generate load
def generate_load(utilization_percentage, duration_seconds):
    num_cores = multiprocessing.cpu_count()
    num_processes = int(num_cores * utilization_percentage / 100)
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=cpu_load, args=(duration_seconds,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

# Function to measure system power utilization
def measure_power_utilization(utilization_percentage, duration_seconds):
    telemetry_data = []
    start_time = datetime.now()

    load_process = multiprocessing.Process(target=generate_load, args=(utilization_percentage, duration_seconds))
    load_process.start()

    while (datetime.now() - start_time).seconds < duration_seconds:
        cpu_data = get_cpu_telemetry()
        memory_data = get_memory_telemetry()
        nic_data = get_nic_telemetry()
        tdp_data = get_tdp_telemetry()

        telemetry_data.append({
            "timestamp": datetime.now().isoformat(),
            "cpu": cpu_data,
            "memory": memory_data,
            "nic": nic_data,
            "tdp": tdp_data,
        })

        time.sleep(1)

    load_process.join()
    return telemetry_data

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>System Telemetry Dashboard</title>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
        <style>
            body {
                padding-top: 50px;
            }
            .container {
                max-width: 800px;
            }
            .chart-container {
                position: relative;
                height: 400px;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center">System Telemetry Dashboard</h1>
            <form id="telemetry-form" class="mb-4">
                <div class="form-group">
                    <label for="utilization">CPU Utilization (%)</label>
                    <input type="number" class="form-control" id="utilization" name="utilization" min="0" max="100" required>
                </div>
                <div class="form-group">
                    <label for="duration">Duration (seconds)</label>
                    <input type="number" class="form-control" id="duration" name="duration" min="1" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Start</button>
            </form>

            <div id="charts">
                <h2>Telemetry Data</h2>
                <div class="chart-container">
                    <canvas id="cpuChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="memoryChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="nicChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="tdpChart"></canvas>
                </div>
            </div>
        </div>

        <script>
            $(document).ready(function () {
                $('#telemetry-form').on('submit', function (e) {
                    e.preventDefault();

                    var utilization = $('#utilization').val();
                    var duration = $('#duration').val();

                    $.ajax({
                        url: '/start',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ utilization: utilization, duration: duration }),
                        success: function (data) {
                            console.log(data);
                            updateCharts(data);
                        },
                        error: function (error) {
                            console.error('Error:', error);
                        }
                    });
                });

                function updateCharts(data) {
                    var timestamps = data.map(entry => new Date(entry.timestamp).toLocaleTimeString());

                    var cpuData = {
                        labels: timestamps,
                        datasets: [
                            { label: 'User', data: data.map(entry => entry.cpu.user), borderColor: 'rgba(75, 192, 192, 1)', fill: false },
                            { label: 'System', data: data.map(entry => entry.cpu.system), borderColor: 'rgba(54, 162, 235, 1)', fill: false },
                            { label: 'Idle', data: data.map(entry => entry.cpu.idle), borderColor: 'rgba(153, 102, 255, 1)', fill: false }
                        ]
                    };

                    var memoryData = {
                        labels: timestamps,
                        datasets: [
                            { label: 'Used', data: data.map(entry => entry.memory.used), borderColor: 'rgba(255, 99, 132, 1)', fill: false },
                            { label: 'Available', data: data.map(entry => entry.memory.available), borderColor: 'rgba(255, 206, 86, 1)', fill: false }
                        ]
                    };

                    var nicData = {
                        labels: timestamps,
                        datasets: Object.keys(data[0].nic).map((nic, index) => ({
                            label: nic + ' - Bytes Sent', data: data.map(entry => entry.nic[nic].bytes_sent),
                            borderColor: 'rgba(75, 192, 192, 1)', fill: false
                        }))
                    };

                    var tdpData = {
                        labels: timestamps,
                        datasets: [
                            { label: 'Current TDP', data: data.map(entry => entry.tdp.current_tdp), borderColor: 'rgba(54, 162, 235, 1)', fill: false },
                            { label: 'Max TDP', data: data.map(entry => entry.tdp.max_tdp), borderColor: 'rgba(153, 102, 255, 1)', fill: false }
                        ]
                    };

                    var ctx1 = $('#cpuChart')[0].getContext('2d');
                    var ctx2 = $('#memoryChart')[0].getContext('2d');
                    var ctx3 = $('#nicChart')[0].getContext('2d');
                    var ctx4 = $('#tdpChart')[0].getContext('2d');

                    new Chart(ctx1, { type: 'line', data: cpuData });
                    new Chart(ctx2, { type: 'line', data: memoryData });
                    new Chart(ctx3, { type: 'line', data: nicData });
                    new Chart(ctx4, { type: 'line', data: tdpData });
                }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    utilization_percentage = int(data['utilization'])
    duration_seconds = int(data['duration'])
    telemetry_data = measure_power_utilization(utilization_percentage, duration_seconds)
    return jsonify(telemetry_data)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template_string
import psutil
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>System Monitor</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            background: #0f0f0f;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            display: flex;
            justify-content: center;
            padding: 40px;
        }
        .container { width: 600px; }
        h1 { text-align: center; color: #00ff88; }
        .card {
            background: #1a1a1a;
            border: 1px solid #00ff88;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }
        .label { color: #888; font-size: 13px; }
        .value { font-size: 28px; font-weight: bold; }
        .bar-bg {
            background: #333;
            border-radius: 10px;
            height: 12px;
            margin-top: 8px;
        }
        .bar-fill {
            height: 12px;
            border-radius: 10px;
            background: #00ff88;
        }
        .high { background: #ff4444; }
        .medium { background: #ffaa00; }
        .timestamp {
            text-align: center;
            color: #555;
            font-size: 13px;
            margin-top: 20px;
        }
        table { width: 100%; border-collapse: collapse; }
        td { padding: 6px 0; border-bottom: 1px solid #222; }
    </style>
</head>
<body>
<div class="container">
    <h1>📊 System Monitor</h1>

    <div class="card">
        <div class="label">🖥️ CPU USAGE</div>
        <div class="value">{{ cpu }}%</div>
        <div class="bar-bg">
            <div class="bar-fill {% if cpu > 80 %}high{% elif cpu > 60 %}medium{% endif %}"
                 style="width: {{ cpu }}%"></div>
        </div>
    </div>

    <div class="card">
        <div class="label">🧠 RAM USAGE</div>
        <div class="value">{{ ram }}%</div>
        <div class="bar-bg">
            <div class="bar-fill {% if ram > 80 %}high{% elif ram > 60 %}medium{% endif %}"
                 style="width: {{ ram }}%"></div>
        </div>
        <div class="label" style="margin-top:8px">{{ ram_used }}MB / {{ ram_total }}MB</div>
    </div>

    <div class="card">
        <div class="label">💾 DISK USAGE</div>
        <div class="value">{{ disk }}%</div>
        <div class="bar-bg">
            <div class="bar-fill {% if disk > 80 %}high{% elif disk > 60 %}medium{% endif %}"
                 style="width: {{ disk }}%"></div>
        </div>
        <div class="label" style="margin-top:8px">{{ disk_used }}GB / {{ disk_total }}GB</div>
    </div>

    <div class="card">
        <div class="label">🌐 NETWORK</div>
        <table>
            <tr><td>⬆️ Sent</td><td>{{ net_sent }} MB</td></tr>
            <tr><td>⬇️ Received</td><td>{{ net_recv }} MB</td></tr>
        </table>
    </div>

    <div class="card">
        <div class="label">⚙️ TOP PROCESSES</div>
        <table>
            {% for p in processes %}
            <tr>
                <td>{{ p.name }}</td>
                <td>{{ p.cpu }}%</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="timestamp">🔄 Auto-refreshes every 5 seconds | {{ timestamp }}</div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    processes = sorted(
        psutil.process_iter(['name', 'cpu_percent']),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )[:5]

    return render_template_string(HTML,
        cpu=psutil.cpu_percent(interval=1),
        ram=ram.percent,
        ram_used=ram.used // (1024**2),
        ram_total=ram.total // (1024**2),
        disk=disk.percent,
        disk_used=disk.used // (1024**3),
        disk_total=disk.total // (1024**3),
        net_sent=net.bytes_sent // (1024**2),
        net_recv=net.bytes_recv // (1024**2),
        processes=[{"name": p.info['name'][:25], "cpu": p.info['cpu_percent']} for p in processes],
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
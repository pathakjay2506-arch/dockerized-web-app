# 🐳 Dockerized System Monitor Web App

A real-time system monitoring web app built with Flask and containerized with Docker.

## 🚀 Run with Docker (One Command!)

```bash
docker-compose up
```
Then open: **http://localhost:5000**

## 🖥️ Run without Docker

```bash
pip install -r requirements.txt
python app.py
```

## ✨ Features
- Real-time CPU, RAM, Disk & Network monitoring
- Auto-refreshes every 5 seconds
- Color-coded alerts (🟢 Normal 🟡 Medium 🔴 High)
- Top 5 running processes
- Fully containerized with Docker

## 🛠️ Tech Stack
- Python 3 + Flask
- psutil
- Docker + Docker Compose
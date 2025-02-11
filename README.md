# 🚀 Chat with Logs

Welcome to **Chat with Logs**, your AI-powered debugging assistant! This tool analyzes production logs, detects issues, and helps you debug like a pro. Whether you're a lead engineer guiding your team or a hobbyist fixing bugs, we've got your back.

---

## 🛠️ Setup Guide

### 1️⃣ Create Your `.env` File

Before we start, let's set up your environment variables. Copy the sample file:

```bash
cp sample.env .env
```

### 2️⃣ Make Scripts Executable

Ensure all scripts in `src/scripts/` are ready to roll:

```bash
chmod +x src/scripts/*
```

### 3️⃣ Install Docker

This project runs on **Docker**. If you haven't installed it yet, grab it [here](https://www.docker.com/). This was built using Docker **20.10.17**, but newer versions should work fine.

---

## 🐳 Running with Docker

Time to get this ship sailing! 🚢

### 🏗️ 1. Build & Start the Docker Container

Run the following command to build and start everything:

```bash
docker compose up --build
```

This will pull dependencies, build the image, and fire up the container.

### 🛠️ 2. Enter the App Container

Need to peek inside the container? No problem!

```bash
docker compose exec app bash
```

Now you have full access to the running environment.

### ✅ 3. Run Code Checks

Keep your code clean and formatted:

```bash
format-checks
code-checks
```

---

## 💬 Chat with Logs CLI

To start debugging via the command line:

```bash
python app/chat_with_logs.py
```

This will let you chat with your logs and uncover hidden bugs! 🕵️‍♂️

---

## 🎨 Running the Streamlit App

Want a slick web UI instead? We've got you covered! 🚀

### 🌍 1. Start the Streamlit App

Run the following command inside the container:

```bash
docker compose up --build
```

### 🌐 2. Open in Your Browser

Once it's running, head over to:

```
http://localhost:8501
```
or for FastAPI UI

```
http://localhost:8000
```

Enjoy the visual debugging experience!

---

## 📊 Data Sources

- **Fake Data**: The app uses generated logs from `fake_data.py`. Feel free to tweak it!
- **Log Data**: The real logs are stored in the `data/` folder. Modify or add your own logs for testing!

---

🔧 Happy Debugging! 🚀


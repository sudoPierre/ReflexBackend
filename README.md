# ReflexBackend

**ReflexBackend** is a simple Python-based utility that listens to GitHub webhooks and automatically pulls, stops, and restarts your backend project every time a push is detected on a specific branch.

---

## ✅ Prerequisites

- A **clean machine or VM** with Python 3 installed (if not, it will be installed automatically).
- **Port 9898 must be free** (or you must change it in `config.json`).
- `git` must be installed.

---

## 🛠 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/ReflexBackend.git
   cd ReflexBackend
   ```

2. **Configure the project**: Edit `config.json` and set the following fields:

   - `branch`: the branch to listen for (e.g. "main").
   - `backend_path`: the path to your local repo (e.g. "~/MyProject").
   - `port`: the port ReflexBackend should listen on (default is `9898`).
   - `stop_commands`: an array of shell commands to stop your backend.
   - `start_commands`: an array of shell commands to start your backend.

3. **Start the loader**:

   ```bash
   sudo bash ./start.sh
   ```

---

## 📛 Stopping ReflexBackend

To stop the webhook listener and background process:

```bash
sudo bash ./stop.sh
```

---

## 📁 Files Overview

- `start.sh`: Installs dependencies, sets up the virtual environment, and starts the webhook listener.
- `stop.sh`: Stops the background process using the stored PID.
- `main.py`: The core Python script that handles webhook requests.
- `config.json`: Configuration file with GitHub link, branch, port, and commands.

---

## 📝 Example `config.json`

```json
{
  // Branch to watch for webhook pushes
  "branch": "main",
  
  // Path to your local repo
  "backend_path": "path/to/my/backend",

  // Port ReflexBackend will listen on
  "port": 9898

  // Commands to stop the current backend
  "stop_commands": [
    "pkill -f 'your-backend-process'"
  ],

  // Commands to start the backend
  "start_commands": [
    "cd yourproject",
    "python3 app.py"
  ],
}
```

---

## 🚀 Use Case

Use this tool if you want your backend server to:

- Automatically update after each push to GitHub.
- Be restarted with custom stop/start logic.
- Run on a lightweight VM or server without Docker or CI/CD tools.

---

## 🛠 License

MIT – Feel free to use and adapt.


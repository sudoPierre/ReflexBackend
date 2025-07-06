# ReflexBackend

**ReflexBackend** is a lightweight webhook listener that automatically updates and restarts your backend server when a `push` event is triggered on a specific GitHub branch.

---

## 📌 Requirements

Make sure your environment meets the following conditions before starting:

- A **clean machine or VM** (no service running on port `9898`, or update the port in `config.json`).
- The **GitHub repository must already be cloned locally** on the machine.
- **Git is installed** on the system.
- The machine is **authenticated with GitHub** (via username/password or SSH key), especially if the repository is private.
- A **GitHub webhook** must be created with the following settings:
  - **URL**: `http://<your-ip>:9898/webhook`
  - **Content type**: `application/json`
  - **SSL**: disabled
  - **Secret**: none
  - **Events**: only `push`
- If your machine is on a **local network**, you must configure **port forwarding** on your router to redirect traffic from port `9898` to the machine’s local IP.

---

## ⚙️ Setup

1. **Clone ReflexBackend** to your machine:
   ```bash
   git clone https://github.com/sudoPierre/ReflexBackend
   cd ReflexBackend
   ```

2. **Fill in `config.json`** with the following information:
   - Branch to monitor.
   - Path to your local project folder.
   - Port to listen on (default is 9898).
   - Commands to stop and restart your backend (can be multiple).

3. **Start the loader**:
   ```bash
   sudo bash ./start.sh
   ```

---

## 🛑 Stop ReflexBackend

To stop the webhook listener:
```bash
sudo bash ./stop.sh
```

---

## 🧪 Example `config.json`

```json
{
  "branch": "main",
  "backend_path": "path/to/my/backend",
  "port": 9898,
  "start_commands": [
    "echo Starting backend...",
    "cd path/to/my/backend",
    "nohup python3 main.py &"
  ],
  "stop_commands": [
    "echo Stopping backend...",
    "pkill -f my-backend"
  ]
}
```

---

## 📂 Notes

- All logs are written to `webhook.log`.
- If you change the listening port, make sure to also update the webhook on GitHub and any port forwarding on your router.
- `start.sh` creates a virtual environment and installs dependencies automatically.

---

## ✅ License

MIT – Use it freely, modify it, and contribute if you'd like!

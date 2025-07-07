from flask import Flask, request, abort
import json
import subprocess
import hmac
import hashlib
import os
import os.path
import datetime

path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(path, "config.json")) as config_file:
    config = json.load(config_file)

app = Flask(__name__)
startCommands = config["start_commands"]
stopCommands = config["stop_commands"]
port = config["port"]
pathServer = config["backend_path"]
branch = config["branch"]

def logger(status, content):
    completePath = os.path.join(path, "webhook.log")
    if not os.path.exists(completePath):
        with open(completePath, "w") as file:
            file.write("Log file created.\n")
    file = open(completePath, "r")
    currentContent = file.read()
    file.close()
    file = open(completePath, "w")
    file.write(f"{datetime.datetime.now()} - {status} : {content}\n{currentContent}")
    file.close()

def run(cmd):
    try:
        logger("INFO", f"Command '{cmd[0]} {cmd[1]}' successfuly executed")
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logger("WARNING", f"Failed to execute command '{cmd[0]} {cmd[1]}'.")
    
def startServer():
    try:
        for cmd in startCommands:
            run(cmd)
            logger("ACTION", "Starting server with commands: " + str(startCommands))
    except Exception as e:
        logger("ERROR", f"Failed to start server: {e}")
        return
    return

def stopServer():
    try:
        for cmd in stopCommands:
            run(cmd)
            logger("ACTION", "Stopping server with commands: " + str(stopCommands))
    except Exception as e:
        logger("ERROR", f"Failed to stop server: {e}")
        return
    return

def updateRepo():
    try:
        run(["git", "fetch", "origin", branch])
        run(["git", "reset", "--hard", f"origin/{branch}"])
        run(["git", "clean", "-fd"])
        logger("ACTION", "Local repository updated to the latest commit on branch: " + branch)
    except Exception as e:
        logger("ERROR", f"Failed to update local repo: {e}")
        return
    return

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    if payload['ref'] == 'refs/heads/' + branch:
        logger("ACTION", "Push detected on " + branch + ". Pulling latest changes.")
        if stopServer():
            if updateRepo():
                if startServer():
                    logger("INFO", "Server restarted successfully after push on " + branch + " branch.")
            else:
                logger("ERROR", "Failed to update repository.")
                return 'Failed to update repository', 500
        else:
            logger("ERROR", "Failed to stop server before updating repository.")
            return 'Failed to stop server', 500
        return 'OK', 200
    else:
        logger("INFO", "Push detected. Not on " + branch + " branch.")
        return 'Not ' + branch + ' branch', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
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
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=pathServer, shell=False)
    cmd_str = ' '.join(cmd)
    if result.returncode == 0:
        logger("INFO", f"Command '{cmd_str}' executed successfully.")
        return True
    else:
        logger("ERROR", f"Command '{cmd_str}' failed.")
        return False

def startServer():
    for cmd in startCommands:
        cmd = cmd.split(" ")
        if run(cmd):
            return True
        else:
            return False

def stopServer():
    for cmd in stopCommands:
        cmd = cmd.split(" ")
        if run(cmd):
            return True
        else:
            return False
    return True

def updateRepo():
    if run(["git", "fetch", "origin", branch]):
        if run(["git", "reset", "--hard", f"origin/{branch}"]):
            if run(["git", "clean", "-fd"]):
                logger("ACTION", "Local repository updated to the latest commit on branch: " + branch)
                return True
            else:
                return False
        else:
            return False
    else:
        return False

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
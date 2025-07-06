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
    completePath = os.path.join(path, "commands.log")
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

def updateRepo():
    try:
        for cmd in startCommands:
            run(cmd)
            logger("ACTION", "Starting server with commands: " + str(startCommands))
        for cmd in stopCommands:
            run(cmd)
            logger("ACTION", "Stopping server with commands: " + str(stopCommands))
    except Exception as e:
        logger("ERROR", f"Failed to start server: {e}")
        return

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    if payload['ref'] == 'refs/heads/' + branch:
        logger("ACTION", "Push detected on " + branch + ". Pulling latest changes.")
        updateRepo()
        return 'OK', 200
    else:
        logger("INFO", "Push detected. Not on " + branch + " branch.")
        return 'Not ' + branch + ' branch', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
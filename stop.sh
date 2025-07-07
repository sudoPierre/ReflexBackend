#!/bin/bash

if [ -f starter.pid ]; then
  sudo kill $(cat starter.pid)
  sudo rm starter.pid
  echo "webhook-reloader stopped."
else
  echo "No PID file found. Is it running?"
fi

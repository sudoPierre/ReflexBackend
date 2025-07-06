#!/bin/bash

if [ -f starter.pid ]; then
  kill $(cat starter.pid)
  rm starter.pid
  echo "webhook-reloader stopped."
else
  echo "No PID file found. Is it running?"
fi

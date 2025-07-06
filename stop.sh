#!/bin/bash

if [ -f webhook.pid ]; then
  kill $(cat webhook.pid)
  rm webhook.pid
  echo "webhook-reloader stopped."
else
  echo "No PID file found. Is it running?"
fi

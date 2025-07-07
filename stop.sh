#!/bin/bash

if [ -f rb.pid ]; then
  sudo kill $(cat rb.pid)
  sudo rm rb.pid
  sudo rm -f starter.log
  echo "ReflexBackend stopped."
else
  echo "No PID file found. Is it running?"
fi

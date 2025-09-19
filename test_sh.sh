#!/bin/bash

# ----------------------------------------
# test_main.sh
# ----------------------------------------
# Bash script to test the Route AI FastAPI backend
# ----------------------------------------

# Exit immediately if a command exits with a non-zero status
set -e

# Server host and port
HOST="127.0.0.1"
PORT="8000"

echo "Starting FastAPI server..."
# Run uvicorn in the background
uvicorn main:app --host $HOST --port $PORT --reload &
SERVER_PID=$! &

# Give the server a few seconds to start
sleep 5

echo "Testing /demo endpoint..."
curl -s "http://$HOST:$PORT/demo?num_cars=5" | jq

echo "Testing /optimise endpoint..."
curl -s -X POST "http://$HOST:$PORT/optimise" | jq

echo "Tests completed."

# Stop the server
kill $SERVER_PID
echo "Server stopped."

#!/usr/bin/env bash
# Optional helper: starts 3 backends + the load balancer (Linux / macOS / Git-Bash)
python backend_server.py 1 5001 &
python backend_server.py 2 5002 &
python backend_server.py 3 5003 &
sleep 2
python load_balancer.py

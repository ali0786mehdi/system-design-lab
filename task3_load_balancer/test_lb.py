"""Sends 9 requests to the load balancer. Start the 3 backends + load_balancer.py first."""
import requests

LB_URL = "http://127.0.0.1:8000/"

for i in range(1, 10):
    r = requests.get(LB_URL)
    print(f"Request {i}: {r.text}")

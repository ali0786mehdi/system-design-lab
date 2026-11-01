"""Quick test client for Task 2. Start app.py first, then run:  python test_task2.py"""
import requests

URL = "http://127.0.0.1:5001/data"

print("--- user_1 sends 7 requests (limit = 5 per minute) ---")
for i in range(1, 8):
    r = requests.get(URL, headers={"X-User-ID": "user_1"})
    print(f"Request {i}: HTTP {r.status_code} -> {r.json()}")

print("\n--- user_2 sends 1 request (has its own separate counter) ---")
r = requests.get(URL, headers={"X-User-ID": "user_2"})
print(f"Request 1: HTTP {r.status_code} -> {r.json()}")

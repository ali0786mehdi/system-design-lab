"""Quick test client for Task 1. Start app.py first, then run:  python test_task1.py"""
import json

import requests

BASE = "http://127.0.0.1:5000"

print("=== 1. POST /shorten (valid URL) ===")
r = requests.post(f"{BASE}/shorten", json={"url": "https://www.google.com/search?q=system+design"})
print("Status:", r.status_code)
print("Body  :", json.dumps(r.json(), indent=2))
short_id = r.json()["short_id"]

print("\n=== 2. GET /{shortId} (should redirect) ===")
r = requests.get(f"{BASE}/{short_id}", allow_redirects=False)
print("Status  :", r.status_code)
print("Location:", r.headers["Location"])

print("\n=== 3. POST /shorten (second URL gets a new ID) ===")
r = requests.post(f"{BASE}/shorten", json={"url": "https://github.com/ali0786mehdi"})
print("Status:", r.status_code)
print("Body  :", json.dumps(r.json(), indent=2))

print("\n=== 4. GET unknown short ID ===")
r = requests.get(f"{BASE}/doesnotexist", allow_redirects=False)
print("Status:", r.status_code, "|", r.json())

print("\n=== 5. POST /shorten (invalid URL) ===")
r = requests.post(f"{BASE}/shorten", json={"url": "not-a-url"})
print("Status:", r.status_code, "|", r.json())

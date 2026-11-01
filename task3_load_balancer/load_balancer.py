"""
Task 3 - Round Robin Load Balancer
----------------------------------
Listens on port 8000 and forwards every incoming request to the next
backend server in a fixed cycle:  S1 -> S2 -> S3 -> S1 -> S2 -> ...

Uses the `requests` library to forward the call to the chosen backend.
Bonus: if a backend is down, the balancer skips to the next one.
"""
import itertools
import threading

import requests
from flask import Flask, Response, request

app = Flask(__name__)

BACKENDS = [
    "http://127.0.0.1:5001",   # Server 1
    "http://127.0.0.1:5002",   # Server 2
    "http://127.0.0.1:5003",   # Server 3
]

_counter = itertools.count()       # 0, 1, 2, 3, ...
_counter_lock = threading.Lock()   # make "next index" thread-safe


def next_start_index() -> int:
    with _counter_lock:
        return next(_counter) % len(BACKENDS)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def balance(path):
    start = next_start_index()

    # try the chosen server first; if it is down, try the following ones in order
    for attempt in range(len(BACKENDS)):
        backend = BACKENDS[(start + attempt) % len(BACKENDS)]
        try:
            resp = requests.request(
                method=request.method,
                url=f"{backend}/{path}",
                params=request.args,
                data=request.get_data(),
                headers={k: v for k, v in request.headers if k.lower() != "host"},
                timeout=3,
            )
            print(f"[LB] {request.method} /{path}  ->  {backend}  ({resp.status_code})", flush=True)
            return Response(resp.content, status=resp.status_code,
                            content_type=resp.headers.get("Content-Type"))
        except requests.exceptions.RequestException:
            print(f"[LB] {backend} is DOWN, trying next server...", flush=True)

    return Response("503 Service Unavailable: all backend servers are down.", status=503)


if __name__ == "__main__":
    print("Round Robin Load Balancer running on http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=False, threaded=True)

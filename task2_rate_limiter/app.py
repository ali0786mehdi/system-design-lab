"""
Task 2 - Rate Limiter Mini
--------------------------
GET /data  -> returns data, but each user may only make 5 requests per 60 seconds.

Algorithm : Sliding Window Log
Storage   : in-memory dictionary  { user_id: [timestamp1, timestamp2, ...] }
User ID   : taken from the 'X-User-ID' header, ?user_id= query param,
            or falls back to the client IP address.
"""
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

MAX_REQUESTS = 5          # allowed requests ...
WINDOW_SECONDS = 60       # ... per this many seconds

request_log: dict[str, list[float]] = {}   # user_id -> list of request timestamps
lock = threading.Lock()                    # Flask can serve requests in parallel threads


def get_user_id() -> str:
    return (
        request.headers.get("X-User-ID")
        or request.args.get("user_id")
        or request.remote_addr
        or "anonymous"
    )


def is_allowed(user_id: str):
    """Return (allowed: bool, retry_after_seconds: int, remaining: int)."""
    now = time.time()
    window_start = now - WINDOW_SECONDS

    with lock:
        # keep only the timestamps that are still inside the 60-second window
        timestamps = [t for t in request_log.get(user_id, []) if t > window_start]

        if len(timestamps) >= MAX_REQUESTS:
            request_log[user_id] = timestamps
            retry_after = int(timestamps[0] + WINDOW_SECONDS - now) + 1
            return False, retry_after, 0

        timestamps.append(now)
        request_log[user_id] = timestamps
        return True, 0, MAX_REQUESTS - len(timestamps)


@app.route("/data", methods=["GET"])
def get_data():
    user_id = get_user_id()
    allowed, retry_after, remaining = is_allowed(user_id)

    if not allowed:
        response = jsonify(error="Too Many Requests: Try again later.")
        response.status_code = 429
        response.headers["Retry-After"] = str(retry_after)
        response.headers["X-RateLimit-Remaining"] = "0"
        return response

    response = jsonify(
        user=user_id,
        message="Here is your data!",
        requests_remaining=remaining,
    )
    response.headers["X-RateLimit-Limit"] = str(MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)

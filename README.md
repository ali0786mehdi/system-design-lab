# System Design Lab

Three system design concepts built from scratch in Python with Flask: a **URL shortener**, a **rate limiter** and a **round robin load balancer**.

🎮 **Live simulation (no install needed): [https://sd-labb.netlify.app/](https://sd-labb.netlify.app/)**

The simulation runs in your browser and uses the same logic as the Python code in this repo. Shorten links, spam the rate limiter, and switch servers off to see failover, then run the real versions below.

## What's inside

| Project | Concept | Port |
|---|---|---|
| `task1_url_shortener` | Base62 short IDs, SQLite, HTTP 302 redirects | 5000 |
| `task2_rate_limiter` | Sliding window log, HTTP 429 with `Retry-After` | 5001 |
| `task3_load_balancer` | Round robin across 3 servers, with failover | 8000 (backends 5001 to 5003) |

## Setup

    python -m venv venv
    venv\Scripts\activate          (macOS/Linux: source venv/bin/activate)
    pip install -r requirements.txt

## Task 1 - URL Shortener (port 5000)

    cd task1_url_shortener
    python app.py                  # terminal 1
    python test_task1.py           # terminal 2
    python show_db.py              # see stored rows

**How it works:** `POST /shorten` validates the URL, saves it in SQLite and turns the row ID into a Base62 short ID. `GET /<short_id>` looks it up and replies `302 Found` with the original URL, or `404` if it doesn't exist. Bad input returns `400`.

## Task 2 - Rate Limiter (port 5001)

    cd task2_rate_limiter
    python app.py                  # terminal 1
    python test_task2.py           # terminal 2

**How it works:** each user (from the `X-User-ID` header) has a list of request timestamps. Timestamps older than 60 seconds are dropped. If 5 or more remain, the server returns `429 Too Many Requests` with a `Retry-After` header. Each user is tracked separately.

## Task 3 - Load Balancer (backends 5001-5003, balancer 8000)

Stop Task 2 first (port 5001). Then, in four terminals inside `task3_load_balancer`:

    python backend_server.py 1 5001
    python backend_server.py 2 5002
    python backend_server.py 3 5003
    python load_balancer.py

Then in a fifth terminal:  `python test_lb.py`

**How it works:** the balancer on port 8000 forwards each request to server `counter % 3` (1, 2, 3, 1, 2, 3...). If a server is down or times out, it tries the next one, so the client still gets a response. Note that browsers also request `/favicon.ico`, which uses up a turn in the rotation.

## Limitations

These are deliberate simplifications, and each one points to the next thing to build:

- **URL shortener:** the same URL gets a new short ID every time, and sequential IDs are guessable.
- **Rate limiter:** counts live in one process's memory, so they reset on restart and don't work across multiple servers (a shared store like Redis fixes this).
- **Load balancer:** no health checks, so a dead server is only found when a request to it fails. It also ignores server load.

## Author

Ali Mehdi Mirza ([@ali0786mehdi](https://github.com/ali0786mehdi))

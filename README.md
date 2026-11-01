# System Design Assignment - Ali Mehdi Mirza

Three mini-projects: URL Shortener Lite, Rate Limiter Mini, Round Robin Load Balancer.

## Setup
    python -m venv venv
    venv\Scripts\activate          (macOS/Linux: source venv/bin/activate)
    pip install -r requirements.txt

## Task 1 - URL Shortener (port 5000)
    cd task1_url_shortener
    python app.py                  # terminal 1
    python test_task1.py           # terminal 2
    python show_db.py              # see stored rows

## Task 2 - Rate Limiter (port 5001)
    cd task2_rate_limiter
    python app.py                  # terminal 1
    python test_task2.py           # terminal 2

## Task 3 - Load Balancer (backends 5001-5003, balancer 8000)
Stop Task 2 first (port 5001). Then, in four terminals inside task3_load_balancer:
    python backend_server.py 1 5001
    python backend_server.py 2 5002
    python backend_server.py 3 5003
    python load_balancer.py
Then in a fifth terminal:  python test_lb.py

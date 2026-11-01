"""
Task 3 - Mock backend server
----------------------------
Usage:  python backend_server.py <server_number> <port>
Example: python backend_server.py 1 5001   -> "Hello from Server 1!"
"""
import sys

from flask import Flask

if len(sys.argv) != 3:
    print("Usage: python backend_server.py <server_number> <port>")
    sys.exit(1)

SERVER_NUMBER = sys.argv[1]
PORT = int(sys.argv[2])

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def hello(path):
    return f"Hello from Server {SERVER_NUMBER}!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=False)

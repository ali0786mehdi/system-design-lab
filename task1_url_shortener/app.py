"""
Task 1 - URL Shortener Lite
---------------------------
POST /shorten      -> accepts a long URL, returns a unique short URL ID
GET  /<short_id>   -> redirects (HTTP 302) to the original URL

Storage : SQLite (file: urls.db) - survives server restarts
Short ID: Base62 encoding of the row's auto-increment integer ID
"""
import os
import sqlite3
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "urls.db")

# 0-9, a-z, A-Z  -> 62 characters
BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(num: int) -> str:
    """Convert a positive integer into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    chars = []
    while num > 0:
        num, remainder = divmod(num, 62)
        chars.append(BASE62_ALPHABET[remainder])
    return "".join(reversed(chars))


def base62_decode(text: str) -> int:
    """Convert a Base62 string back to an integer (used to sanity check)."""
    num = 0
    for ch in text:
        num = num * 62 + BASE62_ALPHABET.index(ch)
    return num


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id  TEXT UNIQUE,
                long_url  TEXT NOT NULL
            )
            """
        )


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True) or {}
    long_url = (data.get("url") or "").strip()

    if not long_url:
        return jsonify(error="Field 'url' is required"), 400
    if not is_valid_url(long_url):
        return jsonify(error="Invalid URL. It must start with http:// or https://"), 400

    conn = get_db()
    try:
        # 1) insert the row to obtain a unique integer ID
        cur = conn.execute("INSERT INTO urls (long_url) VALUES (?)", (long_url,))
        # 2) encode that unique integer in Base62 -> guaranteed-unique short ID
        short_id = base62_encode(cur.lastrowid)
        conn.execute("UPDATE urls SET short_id = ? WHERE id = ?", (short_id, cur.lastrowid))
        conn.commit()
    finally:
        conn.close()

    return (
        jsonify(
            short_id=short_id,
            short_url=f"{request.host_url}{short_id}",
            long_url=long_url,
        ),
        201,
    )


@app.route("/<short_id>", methods=["GET"])
def redirect_to_original(short_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT long_url FROM urls WHERE short_id = ?", (short_id,)
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return jsonify(error="Short URL not found"), 404
    return redirect(row["long_url"], code=302)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)

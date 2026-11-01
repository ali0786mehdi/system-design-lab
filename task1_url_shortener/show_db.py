"""Prints every row stored in urls.db (id, short_id, long_url)."""
import sqlite3

for row in sqlite3.connect("urls.db").execute("SELECT * FROM urls"):
    print(row)

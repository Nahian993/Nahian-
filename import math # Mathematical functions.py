import math                  # Mathematical functions
import sys                   # System-specific parameters and functions
import os                    # Operating system interfaces
import datetime              # Date and time operations
import random                # Generate pseudo-random numbers
import json                  # JSON encoding and decoding
import re                    # Regular expressions
import urllib.request        # Opening URLs
import itertools             # Iterator building functions
import functools             # Higher-order functions
import collections           # Specialized container datatypes
import statistics            # Mathematical statistics functions
import logging               # Logging facilitypip
import argparse              # Command-line argument parsing
import csv                   # CSV file reading and writing
import sqlite3               # SQLite database module
import hashlib               # Secure hash and message digest algorithms
import threading             # Thread-based parallelism
import time                  # Time-related functions

def main():
    # Math demo: square root of 16
    print("Square root of 16:", math.sqrt(16))
    
    # OS demo: current working directory
    print("Current working directory:", os.getcwd())
    
    # Date & time: current datetime
    print("Current date and time:", datetime.datetime.now())
    
    # JSON: encode a dictionary to JSON string
    data = {"name": "Alice", "age": 30}
    print("JSON data:", json.dumps(data))
    
    # Random: random integer between 1 and 10
    print("Random number [1,1000]:", random.randint(1, 1000))
    
    # Regex: search for digits in a string
    match = re.search(r"\d+", "There are 42 apples")
    if match:
        print("Regex found number:", match.group())
    
    # URLlib: fetching headers from a webpage (commented out to avoid delays)
    # response = urllib.request.urlopen("https://www.example.com")
    # print("Fetched page with status code:", response.getcode())
    
    # Itertools: Generate a short sequence
    print("First three numbers from itertools.count:")
    for i, num in zip(range(3), itertools.count(1)):
        print(num, end=" ")
    print()
    
    # Functools: Sum a list using reduce
    total = functools.reduce(lambda a, b: a + b, [1, 2, 3, 4])
    print("Sum of [1,2,3,4] with reduce:", total)
    
    # Collections: Counter for a string
    counter = collections.Counter("hello world")
    print("Counter for 'hello world':", counter)
    
    # Statistics: Mean of a list
    print("Mean of [1,2,3,4,5]:", statistics.mean([1, 2, 3, 4, 5]))
    
    # Logging: Basic configuration and info-level logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging is configured!")
    
    # Argparse: Parse a simple command-line argument
    parser = argparse.ArgumentParser(description="Simple demo script")
    parser.add_argument("--greet", help="Greeting to show", default="Hello")
    args = parser.parse_args()
    print(args.greet, "world!")
    
    # CSV: Write a simple CSV file
    with open("sample.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Age"])
        writer.writerow(["Alice", 30])
    print("CSV file 'sample.csv' created.")
    
    # SQLite3: Create an in-memory database and insert a row
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    cur.execute("INSERT INTO test (value) VALUES ('sample data')")
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM test").fetchone()[0]
    print("SQLite in-memory database, row count:", count)
    
    # Hashlib: Compute SHA256 hash of a string
    hash_obj = hashlib.sha256(b"hello")
    print("SHA256 hash of 'hello':", hash_obj.hexdigest())
    
    # Threading: Run a simple thread worker
    def worker():
        print("Thread worker is running.")

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    
    # Time: Sleep for 1 second
    print("Sleeping for 1 second...")
    time.sleep(1)
    print("Awake now.")

if __name__ == "__main__":
    main()
from flask import Flask, jsonify
import socket
import logging
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env if present
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello():
    logger.info("Root endpoint was called")
    return "Hello, Docker + Jenkins + Python!"

@app.route('/info')
def info():
    logger.info("Info endpoint was called")
    return jsonify({
        "message": "This is a simple Flask app running in Docker",
        "hostname": socket.gethostname(),
        "custom_env": os.getenv("MY_ENV", "Not Set")
    })

@app.route('/joke')
def joke():
    """Fetch a random joke from an external API using requests"""
    logger.info("Joke endpoint was called")
    try:
        resp = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        data = resp.json()
        return jsonify({
            "setup": data.get("setup", "No setup"),
            "punchline": data.get("punchline", "No punchline")
        })
    except Exception as e:
        logger.error(f"Error fetching joke: {e}")
        return jsonify({"error": "Could not fetch a joke"}), 500

if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)

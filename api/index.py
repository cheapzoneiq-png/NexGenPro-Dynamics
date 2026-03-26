/
├── api/
│   └── index.py     ← your full Flask code here
├── requirements.txt
└── vercel.json     ← add this next{
  "version": 2,
  "builds": ,
  "routes": [
    { "src": "/(.*)", "dest": "/api/index.py" }
  ]
}from flask import Flask, request, jsonify
import requests
# GEOCODIO_KEY = ... (use env var!)

app = Flask(__name__)

@app.route('/scan', methods= )
def scan():
    # your fixed code here...

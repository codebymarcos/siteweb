from flask import Flask, jsonify, render_template
from log_analyzer import analyze_logs

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/logs")
def logs():
    return jsonify(analyze_logs())

app.run(host="0.0.0.0", port=5000)

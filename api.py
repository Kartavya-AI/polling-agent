# api.py
from flask import Flask, request, jsonify
from datetime import datetime
from src.polling_agent.crew import PollingAgent
import os
import json

app = Flask(__name__)

@app.route("/polling-agent", methods=["POST"])
def polling_agent():
    data = request.get_json()
    if not data or "topic" not in data:
        return jsonify({"error": "Missing 'topic' in request body"}), 400

    inputs = {
        'topic': data["topic"],
        'current_year': str(datetime.now().year)
    }

    try:
        PollingAgent().crew().kickoff(inputs=inputs)

        result = {
            "message": "Polling Agent executed successfully.",
        }

        for filename in ["poll.json", "twitter_post.json", "linkdin_post.json"]:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    result[filename] = json.load(f)
            else:
                result[filename] = f"{filename} not found."

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8087)

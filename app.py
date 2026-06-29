from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from detector import llm_signal, style_signal
import uuid
from datetime import datetime

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

audit_log = []


@app.route("/")
def home():
    return "Provenance Guard API is running!"


@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():

    data = request.get_json()

    text = data.get("text", "")
    creator_id = data.get("creator_id", "")

    content_id = str(uuid.uuid4())

    # Detection signals
    llm_score = llm_signal(text)
    style_score = style_signal(text)

    confidence = round((llm_score + style_score) / 2, 2)

    if confidence >= 0.70:
        attribution = "likely_ai"
        label = (
            "Likely AI-generated. "
            "Our system has high confidence this content was generated with AI."
        )
    elif confidence <= 0.30:
        attribution = "likely_human"
        label = (
            "Likely human-written. "
            "Our system has high confidence this content was written by a person."
        )
    else:
        attribution = "uncertain"
        label = (
            "Uncertain. "
            "The system cannot confidently determine whether this content is AI-generated or human-written."
        )

    entry = {
        "content_id": content_id,
        "creator_id": creator_id,
        "timestamp": datetime.utcnow().isoformat(),
        "text": text,
        "llm_score": llm_score,
        "style_score": style_score,
        "confidence": confidence,
        "attribution": attribution,
        "label": label,
        "status": "classified",
        "appeal_reasoning": None
    }

    audit_log.append(entry)

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "llm_score": llm_score,
        "style_score": style_score
    })


@app.route("/appeal", methods=["POST"])
def appeal():

    data = request.get_json()

    content_id = data.get("content_id")
    reasoning = data.get("creator_reasoning")

    for entry in audit_log:
        if entry["content_id"] == content_id:
            entry["status"] = "under_review"
            entry["appeal_reasoning"] = reasoning

            return jsonify({
                "message": "Appeal received.",
                "content_id": content_id,
                "status": "under_review"
            })

    return jsonify({"error": "Content not found"}), 404


@app.route("/log", methods=["GET"])
def log():
    return jsonify({"entries": audit_log})


if __name__ == "__main__":
    app.run(debug=True)
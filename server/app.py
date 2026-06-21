import json
import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import mariadb

from models.user import User

from models.report import Report
from services.database import Database
from services.ollama import Ollama

import schemes.report

load_dotenv()

app = Flask(__name__)


# Database setup
connection = mariadb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

database = Database(connection)

user_model = User(database)
report_model = Report(database)

ollama = Ollama(
    bearer_token=os.getenv("OLLAMA_API_KEY"),
    base_url=os.getenv("OLLAMA_BASE_URL")
)

# Create
@app.post("/user")
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password or not username:
        return jsonify({
            "error": "email, password and username are required"
        }), 400

    try:
        user_model.create(
            email=email,
            password=password,
            username=username
        )

        return jsonify({
            "message": "User created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Retrieve
@app.get("/user/<email>")
def get_user(email):
    try:
        user = user_model.get(email)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "email": user[1],
            "password": user[2],
            "username": user[3]
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Update
@app.put("/user/<email>")
def update_user(email):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    allowed_fields = {
        "email",
        "password",
        "username"
    }

    update_params = {
        key: value
        for key, value in data.items()
        if key in allowed_fields
    }

    if not update_params:
        return jsonify({
            "error": "No valid fields provided"
        }), 400

    try:
        user = user_model.get(email)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        user_model.update(
            email=email,
            params=update_params
        )

        return jsonify({
            "message": "User updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Delete
@app.delete("/user/<email>")
def delete_user(email):
    try:
        user = user_model.get(email)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        user_model.delete(email)

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.post("/report")
def analyze_claim():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    claim = data.get("claim")
    user_email = data.get("email")

    if not claim:
        return jsonify({
            "error": "claim is required"
        }), 400

    if not user_email:
        return jsonify({
            "error": "user_id is required"
        }), 400

    try:
        result = ollama.generate(
            model=os.getenv("OLLAMA_MODEL"),
            system_prompt="""
 You are a fact-checking app.

    Return:
    - score (0-100)
    - reason
    - confidence (0-10)
    
    You respond in a plain text json, just that.
    
    Response example:
    {
        "score": 80,
        "reason": "It makes no sense",
        "confidence": 9
    }
    
    Respond only with plain json, no special characters, quotes, colon, etc.
    
    JUST PLAIN JSON
""",
            prompt=claim,
            schema=schemes.report.ReportScheme.model_json_schema()
        )

        schemes.report.ReportScheme.model_validate_json(result)
        report = json.loads(result)

        # Replace this section with your actual schema fields
        score = int(report["score"])
        reason = str(report["reason"])
        confidence = int(report["confidence"])

        print(score, reason, confidence)

        report_model.create(
            claim=claim,
            score=score,
            reason=reason,
            confidence=confidence,
            user_email=user_email
        )

        return jsonify({
            "claim": claim,
            "score": score,
            "reason": reason,
            "confidence": confidence
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.teardown_appcontext
def shutdown(exception):
    pass


if __name__ == "__main__":
    app.run(debug=True)
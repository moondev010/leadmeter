import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from ollama import chat
from ollama import ChatResponse

from pydantic import BaseModel

from typing import Literal

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class Report(BaseModel):
    score: int
    message: Literal['Completely misled',
                     'Partially misled', 'Completely misled']
    reason: str
    confidence: int


initial_prompt = """
You're a fact-checking software. You will be provided with a text and you will 
score how accurate it is in its assertions.

The format you have to follow is the following:
score: (from 0 to 100)
message: One of the given options
reason: Reason why you gave that score
confidence: How confident you are of the your score and reason (from 0 to 100)

IMPORTANT -> Be flexible and DO NOT penalize too much if the text is not that accurate.

The text is the following:
"""


@app.route("/", methods=["POST"])
def main():
    if request.method == "POST":
        req = request.get_json()

        final_prompt = initial_prompt + req["claim"]

        print(req)

        response: ChatResponse = chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt,
                }
            ],
            format=Report.model_json_schema(),
            options={'temperature': 0}
        )

        # print(response.message.content)

        res = json.loads(response.message.content)

        return jsonify(res)
    else:
        return {'message': 'Method not accepted'}

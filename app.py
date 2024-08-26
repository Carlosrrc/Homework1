import os
import requests
from flask import Flask, render_template, request
from google.auth import default

app = Flask(__name__)

# Set up authentication for Google AI
API_KEY = os.getenv("GOOGLE_AI_API_KEY")  # Make sure to set this environment variable in Render

def get_google_ai_response(prompt):
    """
    Function to send a request to Google AI Studio (PaLM API) and return the response.
    """
    url = "https://YOUR_GOOGLE_AI_ENDPOINT_HERE"  # Replace with actual Google AI endpoint URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "models/chat-bison-001",  # Replace with your model name
        "max_tokens": 100  # Adjust based on your needs
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an error if the request failed
    return response.json().get("response_text", "")  # Adjust based on the actual response structure

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")

@app.route("/ai_agent_reply", methods=["GET", "POST"])
def ai_agent_reply():
    q = request.form.get("q")

    # Get response from Google AI Studio
    try:
        r = get_google_ai_response(q)
    except requests.RequestException as e:
        r = f"Error occurred: {str(e)}"

    return render_template("ai_agent_reply.html", r=r)

if __name__ == "__main__":
    app.run()

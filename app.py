from flask import Flask, render_template, request
import os
import google.generativeai as palm
import random

# Fetch the API key from environment variables
api_key = os.getenv('API_KEY')
if api_key:
    palm.configure(api_key=api_key)
else:
    raise ValueError("API_KEY environment variable is not set.")

model = {"model": "models/chat-bison-001"}

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")

@app.route("/ai_agent_reply", methods=["GET", "POST"])
def ai_agent_reply():
    q = request.form.get("q")
    if q:
        try:
            r = palm.chat(messages=q, **model)
            reply = r.last  # Assuming `r.last` is the intended response
        except Exception as e:
            reply = f"Error processing your request: {e}"
    else:
        reply = "No input provided."
    return render_template("ai_agent_reply.html", r=reply)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    # Placeholder for future functionality
    return "Prediction functionality is not implemented yet."

@app.route("/joke", methods=["GET", "POST"])
def joke():
    jokes = [
        "The only thing faster than Singapore's MRT during peak hours is the way we ""chope"" seats with a tissue packet.",
        "Jay Powell has signalled he is ready to cut US interest rates in September, as he warned that “downside risks” to the labour market had increased."
    ]
    selected_joke = random.choice(jokes)
    return render_template("joke.html", joke=selected_joke)

if __name__ == "__main__":
    app.run(debug=True)

import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")

@app.route("/ai_agent_reply", methods=["GET", "POST"])
def ai_agent_reply():
    q = request.form.get("q")
    
    # Create a chat completion using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": q}]
    )

    # Extract the response content correctly
    r = response['choices'][0]['message']['content']
    
    return render_template("ai_agent_reply.html", r=r)

if __name__ == "__main__":
    app.run()

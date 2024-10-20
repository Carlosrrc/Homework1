from flask import Flask, render_template, request, jsonify
import textblob
from transformers import pipeline
import os
import google.generativeai as genai
import random
import tensorflow as tf

api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

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
            r = model.generate_content(q)
            reply = r.text
        except Exception as e:
            reply = f"Error processing your request: {e}"
    else:
        reply = "No input provided."
    return render_template("ai_agent_reply.html", r=reply)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    return "Prediction functionality is not working yet."

# Route to render sentiment.html
@app.route("/SA", methods=["GET", "POST"])
def sentiment_page():
    return render_template("sentiment.html")

# Route to handle sentiment analysis
@app.route('/analyze_sentiment', methods=['POST'])
def sentiment_analysis():
    # Get the text from the form input
    text = request.form.get('text')

    # Check if input text is provided
    if not text:
        return render_template("sentiment.html", sentiment_error="No text provided for sentiment analysis.")

    # Perform sentiment analysis using TextBlob
    textblob_sentiment = textblob.TextBlob(text).sentiment

    # Perform sentiment analysis using transformers model
    model = pipeline("sentiment-analysis")
    transformer_sentiment = model(text)

    # Pass the sentiment result back to sentiment.html
    return render_template("sentiment.html", 
                           textblob_polarity=textblob_sentiment.polarity,
                           textblob_subjectivity=textblob_sentiment.subjectivity,
                           transformer_sentiment=transformer_sentiment[0]['label'],
                           transformer_score=transformer_sentiment[0]['score'])

@app.route("/joke", methods=["GET", "POST"])
def joke():
    jokes = [
        "The only thing faster than Singapore's MRT during peak hours is the way we ""chope"" seats with a tissue packet.",
        "Jay Powell has signalled he is ready to cut US interest rates in September, as he warned that “downside risks” to the labour market had increased."
    ]
    selected_joke = random.choice(jokes)
    return render_template("joke.html", joke=selected_joke)


@app.route("/paynow", methods=["GET", "POST"])
def paynow():
    return (render_template("paynow.html"))


if __name__ == "__main__":
    app.run(debug=True)
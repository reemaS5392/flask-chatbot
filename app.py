from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API Key (Replace with your own if deploying)
openai.api_key = "your_openai_api_key"

# Predefined answers
PREDEFINED_RESPONSES = {
    "which courses offered?": "📚 Jazan University offers a variety of programs, including Engineering, Medicine, Business, and IT. You can find more details at [Jazan University](https://jazanu.edu.sa).",
    "where are the institute located?": "📍 Jazan University is located in Jazan, Saudi Arabia. You can visit us at our main campus or check our website for directions!",
    "what is the duration of the degrees?": "🎓 Bachelor's degrees typically take 4 years, Master's degrees 2 years, and PhD programs vary based on research requirements.",
    "how many faculties?": "🏛️ Jazan University has multiple faculties including Engineering, Medicine, Business, Sciences, and more! Visit our website for the full list."
}

# Function to get response from OpenAI if no predefined response exists
def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "⚠️ Sorry, I am unable to fetch a response right now. Please try again later."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    
    # Check if we have a predefined response
    response = PREDEFINED_RESPONSES.get(user_message, None)
    if not response:
        response = get_openai_response(user_message)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0")

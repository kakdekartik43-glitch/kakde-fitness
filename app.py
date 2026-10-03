
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Gym information
GYM_NAME = "Kakde Fitness"
LOCATION = "Narhe Gaon, near Zeal Chowk, Pune"
PHONE_1 = "8999250652"
PHONE_2 = "9767910652"

MEMBERSHIP_PLANS = """
Monthly membership: Rs. 1000
6-month membership: Rs. 5000
Yearly membership: Rs. 10000
"""

GYM_TIMINGS = """
Morning: 5:00 AM to 11:00 AM
Evening: 5:00 PM to 10:00 PM
"""

# Website pages
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/facilities")
def facilities():
    return render_template("facilities.html")


@app.route("/plans")
def plans():
    return render_template("plans.html")


@app.route("/trainers")
def trainers():
    return render_template("trainers.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# AI Chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please type your question."
        }), 400

    prompt = f"""
You are the friendly AI assistant for {GYM_NAME}.

Answer in the same language as the customer.
Keep answers clear, polite and short.
Do not invent information.

Gym name: {GYM_NAME}
Location: {LOCATION}
Phone numbers: {PHONE_1}, {PHONE_2}

Membership plans:
{MEMBERSHIP_PLANS}

Gym timings:
{GYM_TIMINGS}

Facilities:
Weight training, cardio, personal training,
fitness guidance and goal-based workouts.

If you do not know an answer,
ask the customer to contact the gym.

Customer question:
{user_message}
"""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        answer = result.get("response", "").strip()

        if not answer:
            answer = "Sorry, I could not prepare an answer."

        return jsonify({"reply": answer})

    except requests.RequestException as error:
        print("Ollama connection error:", error)

        return jsonify({
            "reply": "AI service is unavailable. Please check whether Ollama is running."
        }), 503

    except (ValueError, KeyError) as error:
        print("AI response error:", error)

        return jsonify({
            "reply": "Sorry, I received an invalid response from the AI."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
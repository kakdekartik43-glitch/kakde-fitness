
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Gym Information
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

# Website Pages
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


# AI Chatbot using Gemini
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

    # Read API key securely from environment
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        print("Gemini API error: GEMINI_API_KEY is missing")
        return jsonify({
            "reply": "AI service is not configured."
        }), 503

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-2.5-flash:generateContent"
    )

    try:
        response = requests.post(
            url,
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json"
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            },
            timeout=60
        )

        # Log API response for debugging
        print("Gemini status:", response.status_code)

        if not response.ok:
            print("Gemini response:", response.text[:2000])
            response.raise_for_status()

        result = response.json()

        candidates = result.get("candidates", [])

        if not candidates:
            print("Gemini response has no candidates:", result)
            return jsonify({
                "reply": "Sorry, the AI could not generate an answer."
            }), 502

        parts = candidates[0].get("content", {}).get("parts", [])

        answer = " ".join(
            part.get("text", "")
            for part in parts
            if part.get("text")
        ).strip()

        if not answer:
            answer = "Sorry, I could not prepare an answer."

        return jsonify({
            "reply": answer
        })

    except requests.HTTPError as error:
        print("Gemini HTTP error:", error)
        return jsonify({
            "reply": "AI service rejected the request. Please try again."
        }), 503

    except requests.RequestException as error:
        print("Gemini connection error:", error)
        return jsonify({
            "reply": "Sorry, I could not connect to the AI. Please try again."
        }), 503

    except (ValueError, KeyError, IndexError, TypeError) as error:
        print("Gemini response error:", error)
        return jsonify({
            "reply": "Sorry, I received an invalid response from the AI."
        }), 500


# Run Flask app
if __name__ == "__main__":
    app.run(debug=False)

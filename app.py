
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# ==============================
# GYM INFORMATION
# ==============================

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

FACILITIES = """
Weight training
Cardio
Personal training
Fitness guidance
Goal-based workouts
"""


# ==============================
# WEBSITE PAGES
# ==============================

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


# ==============================
# AI CHATBOT USING GROQ
# ==============================

@app.route("/chat", methods=["POST"])
def chat():

    # Get customer message
    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "")

    if not isinstance(user_message, str):
        return jsonify({
            "reply": "Invalid message."
        }), 400

    user_message = user_message.strip()

    if not user_message:
        return jsonify({
            "reply": "Please type your question."
        }), 400

    # Get API key from environment
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if not api_key:
        print("Error: GROQ_API_KEY is missing")

        return jsonify({
            "reply": "AI service is not configured."
        }), 503

    # AI prompt
    prompt = f"""
You are a friendly and helpful AI assistant
for {GYM_NAME}.

Your job is to answer customer questions
about this gym.

IMPORTANT RULES:
1. Answer in the same language as the customer.
2. Keep answers short, clear and polite.
3. Do not invent information.
4. Use only the gym information provided below.
5. If information is unavailable, ask the
   customer to contact the gym.
6. Do not provide medical diagnoses.
7. Be welcoming and professional.

GYM INFORMATION:

Gym name: {GYM_NAME}

Location:
{LOCATION}

Contact numbers:
{PHONE_1}
{PHONE_2}

Membership plans:
{MEMBERSHIP_PLANS}

Gym timings:
{GYM_TIMINGS}

Facilities:
{FACILITIES}

CUSTOMER QUESTION:
{user_message}
"""

    # Groq API URL
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Request data
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:

        # Send request to Groq
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        print("Groq status:", response.status_code)

        # Handle API errors
        if not response.ok:
            print(
                "Groq response:",
                response.text[:2000]
            )

            response.raise_for_status()

        # Read response
        result = response.json()

        choices = result.get("choices", [])

        if not choices:
            print("Groq returned no choices:", result)

            return jsonify({
                "reply": "Sorry, the AI could not generate an answer."
            }), 502

        # Extract AI answer
        answer = (
            choices[0]
            .get("message", {})
            .get("content", "")
        )

        if not isinstance(answer, str):
            answer = ""

        answer = answer.strip()

        if not answer:
            answer = "Sorry, I could not prepare an answer."

        # Send answer to website
        return jsonify({
            "reply": answer
        })

    except requests.HTTPError as error:

        print("Groq HTTP error:", error)

        return jsonify({
            "reply": "AI service rejected the request. Please try again."
        }), 503

    except requests.Timeout as error:

        print("Groq timeout:", error)

        return jsonify({
            "reply": "The AI is taking too long. Please try again."
        }), 504

    except requests.RequestException as error:

        print("Groq connection error:", error)

        return jsonify({
            "reply": "Sorry, I could not connect to the AI. Please try again."
        }), 503

    except (ValueError, KeyError, IndexError, TypeError) as error:

        print("Groq response error:", error)

        return jsonify({
            "reply": "Sorry, I received an invalid response from the AI."
        }), 500


# ==============================
# RUN FLASK APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=False)

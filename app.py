from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import requests
import os


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

database_url = os.environ.get("DATABASE_URL", "sqlite:///gym.db")

# Render/PostgreSQL compatibility
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================================================
# GYM INFORMATION
# =========================================================

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


# =========================================================
# DATABASE MODELS
# =========================================================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    membership = db.Column(
        db.String(50),
        default="No Membership"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Booking(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    booking_date = db.Column(
        db.String(30),
        nullable=False
    )

    booking_type = db.Column(
        db.String(50),
        default="Free Trial"
    )

    plan = db.Column(
        db.String(50),
        default=""
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Review(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================================
# LOGIN MANAGER
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# =========================================================
# ADMIN
# =========================================================

def admin_required(function):

    @wraps(function)
    @login_required
    def wrapper(*args, **kwargs):

        admin_email = os.environ.get(
            "ADMIN_EMAIL",
            "admin@kakdefitness.com"
        )

        if current_user.email != admin_email:

            flash(
                "Admin access required.",
                "error"
            )

            return redirect(
                url_for("home")
            )

        return function(*args, **kwargs)

    return wrapper


# =========================================================
# DATABASE STARTUP
# =========================================================

with app.app_context():

    try:

        db.create_all()

        print(
            "DATABASE CONNECTED - TABLES READY"
        )

    except Exception as error:

        print(
            "DATABASE ERROR:",
            repr(error)
        )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return "OK", 200


# =========================================================
# WEBSITE PAGES
# =========================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


@app.route("/facilities")
def facilities():

    return render_template(
        "facilities.html"
    )


@app.route("/plans")
def plans():

    return render_template(
        "plans.html"
    )


@app.route("/trainers")
def trainers():

    return render_template(
        "trainers.html"
    )


@app.route("/gallery")
def gallery():

    return render_template(
        "gallery.html"
    )


@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not phone or not password:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email is already registered.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password
        )

        try:

            db.session.add(user)
            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "REGISTRATION DATABASE ERROR:",
                repr(error)
            )

            flash(
                "Could not create account. Please try again.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# =========================================================
# USER DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    bookings = Booking.query.filter_by(
        phone=current_user.phone
    ).order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "dashboard.html",
        bookings=bookings
    )


# =========================================================
# MEMBERSHIP
# =========================================================

@app.route("/join/<plan>")
@login_required
def join_plan(plan):

    valid_plans = {
        "monthly": "Monthly",
        "six-month": "6 Months",
        "yearly": "Yearly"
    }

    selected_plan = valid_plans.get(plan)

    if not selected_plan:

        flash(
            "Invalid membership plan.",
            "error"
        )

        return redirect(
            url_for("plans")
        )

    try:

        current_user.membership = selected_plan

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "MEMBERSHIP DATABASE ERROR:",
            repr(error)
        )

        flash(
            "Could not update membership.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    flash(
        f"{selected_plan} membership selected successfully!",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# =========================================================
# FREE TRIAL / BOOKING
# =========================================================

@app.route(
    "/booking",
    methods=["GET", "POST"]
)
def booking():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        booking_date = request.form.get(
            "booking_date",
            ""
        ).strip()

        booking_type = request.form.get(
            "booking_type",
            "Free Trial"
        )

        plan = request.form.get(
            "plan",
            ""
        )

        if not name or not phone or not booking_date:

            flash(
                "Please fill all booking details.",
                "error"
            )

            return redirect(
                url_for("booking")
            )

        new_booking = Booking(
            name=name,
            phone=phone,
            booking_date=booking_date,
            booking_type=booking_type,
            plan=plan
        )

        try:

            db.session.add(new_booking)
            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "BOOKING DATABASE ERROR:",
                repr(error)
            )

            flash(
                "Could not submit booking. Please try again.",
                "error"
            )

            return redirect(
                url_for("booking")
            )

        flash(
            "Your booking request has been submitted!",
            "success"
        )

        return redirect(
            url_for("booking")
        )

    return render_template(
        "booking.html"
    )


# =========================================================
# BMI
# =========================================================

@app.route("/bmi")
def bmi():

    return render_template(
        "bmi.html"
    )


# =========================================================
# WORKOUT
# =========================================================

@app.route("/workout")
def workout():

    return render_template(
        "workout.html"
    )


# =========================================================
# REVIEWS
# =========================================================

@app.route(
    "/reviews",
    methods=["GET", "POST"]
)
def reviews():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()

        try:

            rating = int(
                request.form.get(
                    "rating",
                    5
                )
            )

        except (ValueError, TypeError):

            rating = 5

        if not name or not message:

            flash(
                "Please enter your name and review.",
                "error"
            )

            return redirect(
                url_for("reviews")
            )

        if rating < 1 or rating > 5:

            rating = 5

        review = Review(
            name=name,
            rating=rating,
            message=message
        )

        try:

            db.session.add(review)
            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "REVIEW DATABASE ERROR:",
                repr(error)
            )

            flash(
                "Could not submit review.",
                "error"
            )

            return redirect(
                url_for("reviews")
            )

        flash(
            "Thank you for your review!",
            "success"
        )

        return redirect(
            url_for("reviews")
        )

    all_reviews = Review.query.order_by(
        Review.id.desc()
    ).all()

    return render_template(
        "reviews.html",
        reviews=all_reviews
    )


# =========================================================
# SEARCH
# =========================================================

@app.route("/search")
def search():

    query = request.args.get(
        "q",
        ""
    ).strip().lower()

    search_data = [

        {
            "title": "About Kakde Fitness",
            "description": "Information about Kakde Fitness gym.",
            "url": url_for("about")
        },

        {
            "title": "Membership Plans",
            "description": "Monthly, 6-month and yearly membership plans.",
            "url": url_for("plans")
        },

        {
            "title": "Gym Facilities",
            "description": "Weight training, cardio and personal training.",
            "url": url_for("facilities")
        },

        {
            "title": "Trainers",
            "description": "Meet the trainers at Kakde Fitness.",
            "url": url_for("trainers")
        },

        {
            "title": "Gallery",
            "description": "View Kakde Fitness gym photos.",
            "url": url_for("gallery")
        },

        {
            "title": "Contact",
            "description": "Contact Kakde Fitness in Narhe, Pune.",
            "url": url_for("contact")
        },

        {
            "title": "BMI Calculator",
            "description": "Calculate your BMI.",
            "url": url_for("bmi")
        },

        {
            "title": "Workout Schedule",
            "description": "View a basic weekly workout schedule.",
            "url": url_for("workout")
        },

        {
            "title": "Free Trial",
            "description": "Book a free gym trial.",
            "url": url_for("booking")
        },

        {
            "title": "Reviews",
            "description": "Read and submit gym reviews.",
            "url": url_for("reviews")
        }
    ]

    if query:

        results = [
            item
            for item in search_data
            if query in (
                item["title"]
                + " "
                + item["description"]
            ).lower()
        ]

    else:

        results = search_data

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================================================
# ADMIN PANEL
# =========================================================

@app.route("/admin")
@admin_required
def admin():

    users = User.query.order_by(
        User.id.desc()
    ).all()

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    reviews = Review.query.order_by(
        Review.id.desc()
    ).all()

    return render_template(
        "admin.html",
        users=users,
        bookings=bookings,
        reviews=reviews
    )


# =========================================================
# AI CHATBOT USING GROQ
# =========================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json(
        silent=True
    ) or {}

    user_message = data.get(
        "message",
        ""
    )

    if not isinstance(
        user_message,
        str
    ):

        return jsonify({
            "reply": "Invalid message."
        }), 400

    user_message = user_message.strip()

    if not user_message:

        return jsonify({
            "reply": "Please type your question."
        }), 400

    api_key = os.environ.get(
        "GROQ_API_KEY",
        ""
    ).strip()

    if not api_key:

        return jsonify({
            "reply": "AI service is not configured."
        }), 503

    prompt = f"""
You are a friendly AI assistant for {GYM_NAME}.

Answer the customer using only the information below.

Rules:
1. Answer in the same language as the customer.
2. Keep answers short and clear.
3. Do not invent gym information.
4. Do not provide medical diagnosis.
5. If information is unavailable, tell the customer to contact the gym.
6. Be friendly and professional.

Gym:
{GYM_NAME}

Location:
{LOCATION}

Phone:
{PHONE_1}
{PHONE_2}

Plans:
{MEMBERSHIP_PLANS}

Timings:
{GYM_TIMINGS}

Facilities:
{FACILITIES}

Customer question:
{user_message}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

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

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        print(
            "Groq status:",
            response.status_code
        )

        if not response.ok:

            print(
                "Groq response:",
                response.text[:2000]
            )

            response.raise_for_status()

        result = response.json()

        choices = result.get(
            "choices",
            []
        )

        if not choices:

            return jsonify({
                "reply": "Sorry, the AI could not generate an answer."
            }), 502

        answer = (
            choices[0]
            .get("message", {})
            .get("content", "")
        )

        if not isinstance(
            answer,
            str
        ):

            answer = ""

        answer = answer.strip()

        if not answer:

            answer = "Sorry, I could not prepare an answer."

        return jsonify({
            "reply": answer
        })

    except requests.HTTPError:

        return jsonify({
            "reply": "AI service rejected the request. Please try again."
        }), 503

    except requests.Timeout:

        return jsonify({
            "reply": "The AI is taking too long. Please try again."
        }), 504

    except requests.RequestException:

        return jsonify({
            "reply": "Sorry, I could not connect to the AI."
        }), 503

    except Exception as error:

        print(
            "Chatbot error:",
            error
        )

        return jsonify({
            "reply": "Sorry, something went wrong."
        }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as error:
    print("Dotenv error:", error)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "temporary-development-key")

from werkzeug.security import generate_password_hash, check_password_hash

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

try:
    from supabase import create_client
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as error:
    print("Supabase error:", error)


# Career recommendations
CAREERS = {
    "Arts": [
        "Graphic Designer", "Artist", "Photographer", "Animator"
    ],
    "Technology": [
        "Software Developer", "Web Developer",
        "Data Scientist", "AI Engineer"
    ],
    "Business": [
        "Business Manager", "Entrepreneur", "Marketing Manager"
    ],
    "Healthcare": [
        "Doctor", "Nurse", "Pharmacist", "Dentist"
    ],
    "Social Work": [
        "Social Worker", "Counsellor"
    ],
    "Teaching": [
        "School Teacher", "University Lecturer"
    ],
    "Finance": [
        "Accountant", "Financial Analyst", "Auditor"
    ],
    "Law": [
        "Lawyer", "Legal Advisor", "Judge"
    ]
}

EDUCATION_JOBS = {
    "O Levels": ["Office Assistant", "Retail Assistant"],
    "A Levels": ["Customer Service Assistant", "Content Writer"],
    "Matric": ["Data Entry Operator", "Receptionist"],
    "Intermediate": ["Teaching Assistant", "Sales Assistant"],
    "Bachelor's": [
        "Marketing Executive", "Research Assistant", "Junior Developer"
    ]
}


@app.route("/", methods=["GET", "POST"])
def home():
        if "user_id" not in session:
        return render_template("TI.html", mode="choice")
    result = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        interest = request.form.get("interest")
        education = request.form.get("education")

        if name and age.isdigit() and interest in CAREERS and education in EDUCATION_JOBS:
            result = {
                "name": name,
                "age": age,
                "interest": interest,
                "education": education,
                "careers": CAREERS[interest],
                "jobs": EDUCATION_JOBS[education]
            }
        else:
            flash("Please complete all fields correctly.")

    return render_template(
        "index.html",
        interests=CAREERS.keys(),
        education_levels=EDUCATION_JOBS.keys(),
        result=result
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not database_ready():
        return "Supabase is not connected yet. We need to configure it first."

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 8:
            flash("Enter your name, a valid email and a password of at least 8 characters.")
            return redirect(url_for("signup"))

        try:
            existing = supabase.table("users").select("id").eq("email", email).execute()

            if existing.data:
                flash("An account with this email already exists.")
                return redirect(url_for("signup"))

            password_hash = generate_password_hash(password)

            response = supabase.table("users").insert({
                "full_name": name,
                "email": email,
                "password_hash": password_hash
            }).execute()

            if response.data:
                session["user_id"] = response.data[0]["id"]
                session["user_name"] = name
                return redirect(url_for("home"))

            flash("Could not create your account. Please try again.")

        except Exception as error:
            print("Signup error:", error)
            flash("There was a database error. Please check your Supabase setup.")

    return render_template("TI.html", mode="signup")


@app.route("/login", methods=["GET", "POST"])
def login():
    if not database_ready():
        return "Supabase is not connected yet. We need to configure it first."

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        try:
            response = supabase.table("users").select("*").eq(
                "email", email
            ).execute()

            if response.data:
                user = response.data[0]

                if check_password_hash(user["password_hash"], password):
                    session["user_id"] = user["id"]
                    session["user_name"] = user["full_name"]
                    return redirect(url_for("home"))

            flash("Incorrect email or password.")

        except Exception as error:
            print("Login error:", error)
            flash("There was a database error. Please try again.")

    return render_template("TI.html", mode="login")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        plans=[]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

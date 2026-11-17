@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return render_template("TI.html", mode="choice")

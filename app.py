from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    file_exists = os.path.isfile("leads.csv")
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "E-Mail", "Telefon"])
        writer.writerow([name, email, phone])

    return render_template("thanks.html")

if __name__ == "__main__":
    app.run(debug=True)

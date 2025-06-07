import re
from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    vorname = request.form['vorname'].strip()
    nachname = request.form['nachname'].strip()
    email = request.form['email'].strip()
    phone = request.form['phone'].strip()

    # Validierungsmuster
    name_pattern = re.compile(r"^[A-Za-zÄÖÜäöüß\s\-]{2,30}$")
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    phone_pattern = re.compile(r"^\+?[0-9\s\-]{7,20}$")

    if not name_pattern.match(vorname):
        return "Ungültiger Vorname", 400
    if not name_pattern.match(nachname):
        return "Ungültiger Nachname", 400
    if not email_pattern.match(email):
        return "Ungültige E-Mail-Adresse", 400
    if not phone_pattern.match(phone):
        return "Ungültige Telefonnummer", 400

    # Speichern in leads.csv
    file_exists = os.path.isfile('leads.csv')
    with open('leads.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Vorname', 'Nachname', 'Email', 'Telefon'])
        writer.writerow([vorname, nachname, email, phone])

    return render_template('thanks.html')

@app.route('/admin')
def admin():
    leads = []
    if os.path.exists('leads.csv'):
        with open('leads.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            for row in reader:
                leads.append(row)
    return render_template('admin.html', leads=leads)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)  # Wichtig für Replit


import re
from flask import Flask, render_template, request, send_file, Response
import csv
import os
from functools import wraps

app = Flask(__name__)

# Zugangsdaten für Admin-Seite
USERNAME = 'admin'
PASSWORD = '12345'

# Authentifizierung
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Zugriff verweigert. Bitte Benutzername & Passwort angeben.', 401,
        {'WWW-Authenticate': 'Basic realm="Login erforderlich"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ✅ Pre-Landing
@app.route('/pre')
def pre_landing():
    return render_template('pre-landing.html')

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Formular absenden
@app.route('/submit', methods=['POST'])
def submit():
    vorname = request.form['vorname'].strip()
    nachname = request.form['nachname'].strip()
    email = request.form['email'].strip()
    phone = request.form['phone'].strip()

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

    file_exists = os.path.isfile('leads.csv')
    with open('leads.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Vorname', 'Nachname', 'Email', 'Telefon'])
        writer.writerow([vorname, nachname, email, phone])

    return render_template('thanks.html')

# Admin-Bereich
@app.route('/admin')
@requires_auth
def admin():
    leads = []
    if os.path.exists('leads.csv'):
        with open('leads.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                leads.append(row)
    return render_template('admin.html', leads=leads)

# CSV-Download
@app.route('/download')
@requires_auth
def download_leads():
    return send_file('leads.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)

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

    file_exists = os.path.isfile('leads.csv')
    with open('leads.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Vorname', 'Nachname', 'E-Mail', 'Telefon'])
        writer.writerow([vorname, nachname, email, phone])

    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)

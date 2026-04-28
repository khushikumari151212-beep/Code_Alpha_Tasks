from flask import Flask, request, redirect, render_template
import sqlite3
import string, random

app = Flask(__name__)

# Generate random short code
def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Initialize DB
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (code TEXT, url TEXT)')
    conn.commit()
    conn.close()

init_db()

# Home page (frontend)
@app.route('/')
def home():
    return render_template('index.html')

# API to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    code = generate_code()

    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls VALUES (?, ?)", (code, long_url))
    conn.commit()
    conn.close()

    short_url = f"http://127.0.0.1:5000/{code}"
    return f"<h3>Short URL: <a href='{short_url}'>{short_url}</a></h3>"

# Redirect route
@app.route('/<code>')
def redirect_url(code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT url FROM urls WHERE code=?", (code,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    return "<h3>URL not found!</h3>"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import sqlite3
import re

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('event.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS events (
                                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       name TEXT,
                                                       date TEXT,
                                                       description TEXT
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
                                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                              name TEXT,
                                                              email TEXT,
                                                              event_id INTEGER
                 )''')

    conn.commit()
    conn.close()

init_db()

# Home (with registered count)
@app.route('/')
def home():
    conn = sqlite3.connect('event.db')
    c = conn.cursor()

    c.execute("""
              SELECT events.*, COUNT(registrations.id)
              FROM events
                       LEFT JOIN registrations
                                 ON events.id = registrations.event_id
              GROUP BY events.id
              """)

    events = c.fetchall()
    conn.close()

    return render_template('index.html', events=events)

# Register page
@app.route('/register/<int:event_id>')
def register_page(event_id):
    return render_template('register.html', event_id=event_id)

# Submit form
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    event_id = request.form['event_id']

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "<h3>❌ Invalid Email!</h3><a href='/'>Go Back</a>"

    conn = sqlite3.connect('event.db')
    c = conn.cursor()
    c.execute("INSERT INTO registrations (name,email,event_id) VALUES (?,?,?)",
              (name, email, event_id))
    conn.commit()
    conn.close()

    return redirect('/success')

# Success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
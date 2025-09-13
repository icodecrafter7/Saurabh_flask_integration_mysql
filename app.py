from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ----------------------
# Database connection
# ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="5055",        # your MySQL password
        database="mini_project"
    )

# ----------------------
# Home route
# ----------------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------
# Signup route
# ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(buffered=True)  # buffered cursor
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('dashboard'))
    return render_template('signup.html')

# ----------------------
# Login route
# ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(buffered=True)  # buffered cursor
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

# ----------------------
# Dashboard route
# ----------------------
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(buffered=True)  # buffered cursor
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('dashboard.html', users=users)

# ----------------------
# Run app
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)

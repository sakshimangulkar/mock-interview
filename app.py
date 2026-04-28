from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"   # required for login sessions

# -------- DATABASE -------- #
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        score INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# -------- QUESTIONS -------- #
questions_data = {
    "python": [
        {"q": "What is Python?", "a": "programming language"},
        {"q": "What is list?", "a": "collection"}
    ],
    "java": [
        {"q": "What is OOP?", "a": "object oriented"},
        {"q": "What is inheritance?", "a": "inherit"}
    ],
    "hr": [
        {"q": "Tell me about yourself", "a": "yourself"},
        {"q": "Why should we hire you?", "a": "skills"}
    ]
}

# -------- AUTH ROUTES -------- #

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# -------- MAIN ROUTES -------- #

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    return render_template("index.html", user=session['user'])


@app.route('/interview/<category>', methods=['GET', 'POST'])
def interview(category):
    if 'user' not in session:
        return redirect('/login')

    questions = questions_data.get(category, [])

    if request.method == 'POST':
        answers = request.form.getlist('answers')
        score = 0

        for i, ans in enumerate(answers):
            if i < len(questions) and questions[i]['a'] in ans.lower():
                score += 1

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO results (username, category, score) VALUES (?, ?, ?)",
            (session['user'], category, score)
        )

        conn.commit()
        conn.close()

        return render_template("result.html", score=score, total=len(questions))

    return render_template("interview.html", questions=questions, category=category)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
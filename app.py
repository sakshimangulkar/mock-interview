from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        score INTEGER
    )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_result(category, score):
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (category, score) VALUES (?, ?)", (category, score))
    conn.commit()
    conn.close()

# ---------------- QUESTIONS ---------------- #
questions_data = {
    "python": [
        {"q": "What is Python?", "a": "programming language"},
        {"q": "What is a list?", "a": "collection"}
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

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/interview/<category>', methods=['GET', 'POST'])
def interview(category):
    questions = questions_data.get(category, [])

    if request.method == 'POST':
        answers = request.form.getlist('answers')
        score = 0

        for i, ans in enumerate(answers):
            if i < len(questions) and questions[i]['a'] in ans.lower():
                score += 1

        save_result(category, score)

        return render_template(
            "result.html",
            score=score,
            total=len(questions),
            category=category
        )

    return render_template("interview.html", questions=questions, category=category)

# ---------------- RUN ---------------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
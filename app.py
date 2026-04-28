from flask import Flask, render_template, request, redirect
import sqlite3

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    score INTEGER
)
''')

app = Flask(__name__)

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
                
        return render_template("result.html", score=score)
    
    return render_template("interview.html", questions=questions, category=category)

def give_feedback(score):
    if score == 0:
        return "Needs improvement"
    elif score == 1:
        return "Good attempt"
    else:
        return "Excellent"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
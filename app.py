# ✅ FILE: app.py (Flask backend for gesture-based quiz)

from flask import Flask, render_template, request, jsonify
import subprocess
import threading

app = Flask(__name__)

# ✅ Predefined quiz questions
questions = [
    {
        "question": "1. What is the capital of India?",
        "options": {"A": "Mumbai", "B": "Delhi", "C": "Chennai", "D": "Kolkata"},
        "answer": "B"
    },
    {
        "question": "2. Which is the largest planet?",
        "options": {"A": "Mars", "B": "Earth", "C": "Jupiter", "D": "Saturn"},
        "answer": "C"
    },
    {
        "question": "3. What color is the sky on a clear day?",
        "options": {"A": "Green", "B": "Blue", "C": "Red", "D": "Yellow"},
        "answer": "B"
    },
    {
        "question": "4. Who wrote 'Hamlet'?",
        "options": {"A": "Shakespeare", "B": "Wordsworth", "C": "Keats", "D": "Milton"},
        "answer": "A"
    },
    {
        "question": "5. What is the chemical symbol for water?",
        "options": {"A": "O2", "B": "H2O", "C": "CO2", "D": "NaCl"},
        "answer": "B"
    },
    {
        "question": "6. What is 15 + 10?",
        "options": {"A": "20", "B": "25", "C": "30", "D": "35"},
        "answer": "B"
    },
    {
        "question": "7. Which is the smallest continent?",
        "options": {"A": "Africa", "B": "Europe", "C": "Australia", "D": "Antarctica"},
        "answer": "C"
    },
    {
        "question": "8. Who invented the telephone?",
        "options": {"A": "Einstein", "B": "Newton", "C": "Graham Bell", "D": "Tesla"},
        "answer": "C"
    },
    {
        "question": "9. What is the boiling point of water?",
        "options": {"A": "80°C", "B": "90°C", "C": "100°C", "D": "110°C"},
        "answer": "C"
    },
    {
        "question": "10. What language is used for styling webpages?",
        "options": {"A": "HTML", "B": "Java", "C": "Python", "D": "CSS"},
        "answer": "D"
    }
]

# ✅ Stores user's gesture-based answers
user_answers = []


@app.route('/')
def index():
    return render_template('index.html')  # Must exist in templates/index.html


@app.route('/get_questions')
def get_questions():
    return jsonify({"questions": questions})


@app.route('/get_answers')
def get_answers():
    return jsonify({"answers": user_answers})


@app.route('/get_score')
def get_score():
    score = 0
    for i in range(min(len(user_answers), len(questions))):
        if user_answers[i] == questions[i]["answer"]:
            score += 1
    return jsonify({"score": score, "total": len(questions)})


@app.route('/reset')
def reset():
    global user_answers
    user_answers = []
    return jsonify({"status": "reset"})


@app.route('/post_gesture', methods=['POST'])
def post_gesture():
    """
    Endpoint to receive gesture answers from alica.py
    """
    global user_answers
    data = request.get_json()
    answer = data.get("gesture")

    # Only allow one answer per question
    if answer and len(user_answers) < len(questions):
        user_answers.append(answer.upper())  # Store uppercase A/B/C/D
        print(f"✅ Gesture answer recorded: {answer}")
        return jsonify({"status": "received"})

    return jsonify({"status": "ignored or quiz complete"}), 400


@app.route('/start_alica')
def start_alica():
    """
    Launch alica.py (gesture detection) when Start Test button is clicked
    """
    def run_alica():
        subprocess.run(["python", "alica.py"], check=True)

    threading.Thread(target=run_alica, daemon=True).start()
    return jsonify({"status": "alica started"})


if __name__ == '__main__':
    app.run(debug=True)

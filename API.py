"""
from flask import Flask, request, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:FNhn4282#@127.0.0.1/NETquizapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

# Define Quiz model
class Quiz(db.Model):
    __tablename__ = 'quiz'

    uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'), primary_key=True)
    quizId = db.Column(db.String(255))
    quizType = db.Column(db.String(255))
    quizSubject = db.Column(db.String(255))
    quizTotalMcqs = db.Column(db.String(255))
    quizExpectedTime = db.Column(db.String(255))
    quizTakenTime = db.Column(db.String(255))

# Define QuizMcqs model
class QuizMcqs(db.Model):
    __tablename__ = 'quizMcqs'

    mcqId = db.Column(db.String(255), primary_key=True)
    quizId = db.Column(db.String(255), db.ForeignKey('quiz.quizId'))
    quizMcqsID = db.Column(db.String(255), index=True)

# Define Mcqs model
class Mcqs(db.Model):
    __tablename__ = 'Mcqs'

    mcqID = db.Column(db.String(255), db.ForeignKey('quizMcqs.mcqId'), primary_key=True)
    mcqSubject = db.Column(db.String(255))
    mcqTitle = db.Column(db.String(255))
    mcqTopic = db.Column(db.String(255))
    opt1 = db.Column(db.String(255))
    opt2 = db.Column(db.String(255))
    opt3 = db.Column(db.String(255))
    opt4 = db.Column(db.String(255))
    solution = db.Column(db.String(255))

    quiz_mcq = db.relationship('QuizMcqs', backref='mcqs')

# Define UserAnalytics model
class UserAnalytics(db.Model):
    __tablename__ = 'userAnalytics'

    uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'), primary_key=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Welcome to the Quiz App!'})

@app.route("/generate_mcqs", methods=["GET", "POST"])
def generate_mcqs():
    if request.method == "POST":
        subject = request.json.get("subject")
        num_mcqs = request.json.get("num_mcqs")

        mcqs = (
            Mcqs.query.filter_by(mcqSubject=subject)
            .order_by(func.rand())
            .limit(num_mcqs)
            .all()
        )

        if not mcqs:
            return jsonify({"message": f"No MCQs found for subject '{subject}'."}), 404

        mcq_list = [
            {
                "mcqID": mcq.mcqID,
                "mcqSubject": mcq.mcqSubject,
                "mcqTitle": mcq.mcqTitle,
                "mcqTopic": mcq.mcqTopic,
                "opt1": mcq.opt1,
                "opt2": mcq.opt2,
                "opt3": mcq.opt3,
                "opt4": mcq.opt4,
                "solution": mcq.solution,
            }
            for mcq in mcqs
        ]
        print(mcq_list)  # This will print the generated MCQs list to your console


        return jsonify({"mcqs": mcq_list})
    else:
        return "Please use a POST request to generate MCQs.", 405
@app.route("/example", methods=["GET", "POST"])
def example():
    if request.method == "GET":
        return "This is a GET request."
    elif request.method == "POST":
        return "This is a POST request."
    else:
        return "Method Not Allowed", 405

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
"""
from flask_login import LoginManager, current_user, login_user, UserMixin
from flask import Flask, request, session,jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import desc,asc
from collections import defaultdict
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:FNhn4282#@127.0.0.1/NETquizapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    education = db.Column(db.String(255))

# Define Quiz model
class Quiz(db.Model):
    __tablename__ = 'quiz'

    uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'), primary_key=True)
    quizId = db.Column(db.String(255))
    quizType = db.Column(db.String(255))
    quizSubject = db.Column(db.String(255))
    quizTotalMcqs = db.Column(db.String(255))
    quizExpectedTime = db.Column(db.String(255))
    quizTakenTime = db.Column(db.String(255))

# Define QuizMcqs model
class QuizMcqs(db.Model):
    __tablename__ = 'quizMcqs'

    mcqId = db.Column(db.String(255), primary_key=True)
    quizId = db.Column(db.String(255), db.ForeignKey('quiz.quizId'))
    quizMcqsID = db.Column(db.String(255), index=True)

# Define Mcqs model
class Mcqs(db.Model):
    __tablename__ = 'Mcqs'

    mcqID = db.Column(db.String(255), db.ForeignKey('quizMcqs.mcqId'), primary_key=True)
    mcqSubject = db.Column(db.String(255))
    mcqTitle = db.Column(db.String(255))
    difficultyLevel=db.Column(db.String(255))
    mcqTopic = db.Column(db.String(255))
    opt1 = db.Column(db.String(255))
    opt2 = db.Column(db.String(255))
    opt3 = db.Column(db.String(255))
    opt4 = db.Column(db.String(255))
    time_spent = db.Column(db.Integer) 
    solution = db.Column(db.String(255))

    quiz_mcq = db.relationship('QuizMcqs', backref='mcqs')

class UserAttemptedQuiz(db.Model):
    __tablename__ = 'user_attempted_quiz'

    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'))
    quiz_id = db.Column(db.Integer)
    mcqID = db.Column(db.String(255), db.ForeignKey('Mcqs.mcqID'))
    time_taken = db.Column(db.Integer)
    selected_option = db.Column(db.String(255))
    accuracy = db.Column(db.Float)
    # Relationships
    user = db.relationship('User', backref='attempted_quizzes')
    mcq = db.relationship('Mcqs', backref='user_quiz_attempts')
# Define UserAnalytics model
class UserAnalytics(db.Model):
    __tablename__ = 'userAnalytics'

    uuid = db.Column(db.String(255), db.ForeignKey('users.uuid'), primary_key=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Welcome to the Quiz App!'})


@app.route("/generate_mcqs", methods=["GET", "POST"])
def generate_mcqs():
    if request.method == "GET":
        # Handle GET request
        return "This is a GET request."

    elif request.method == "POST":
        # Handle POST request
        subject = request.json.get("subject")
        num_mcqs = request.json.get("num_mcqs")
        difficulty_level = request.json.get("difficultyLevel")  # Get difficulty level from request

        mcqs = (
            Mcqs.query.filter_by(mcqSubject=subject, difficultyLevel=difficulty_level)  # Filter by difficulty level
            .order_by(func.rand())
            .limit(num_mcqs)
            .all()
        )

        if not mcqs:
            return jsonify({"message": f"No MCQs found for subject '{subject}' and difficulty '{difficulty_level}'."}), 404

        mcq_list = [
            {
                "mcqID": mcq.mcqID,
                "mcqSubject": mcq.mcqSubject,
                "mcqTitle": mcq.mcqTitle,
                "mcqTopic": mcq.mcqTopic,
                "opt1": mcq.opt1,
                "opt2": mcq.opt2,
                "opt3": mcq.opt3,
                "opt4": mcq.opt4,
                "solution": mcq.solution,
                "difficultyLevel": mcq.difficultyLevel  # Include the MCQ's difficulty level
            }
            for mcq in mcqs
        ]

        return jsonify({"mcqs": mcq_list})

    else:
        return "Method Not Allowed", 405

@app.route("/send_requests", methods=["GET"])
def send_requests():
    # Example of sending GET and POST requests within your Flask app
    get_response = requests.get('http://127.0.0.1:5000/generate_mcqs')

    payload = {"subject": "Math", "num_mcqs": 10}
    headers = {"Content-Type": "application/json"}
    post_response = requests.post('http://127.0.0.1:5000/generate_mcqs', data=json.dumps(payload), headers=headers)

    return jsonify({
        "GET_Response": get_response.text,
        "POST_Response": post_response.text
    })

@app.route("/example", methods=["GET", "POST"])
def example():
    if request.method == "GET":
        return "This is a GET request."
    elif request.method == "POST":
        return "This is a POST request."
    else:
        return "Method Not Allowed", 405
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        uuid=data['uuid'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        #have to add education
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User signed up successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Invalid credentials"}), 401

    user = User.query.filter_by(email=auth.username).first()

    if not user or not check_password_hash(user.password, auth.password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Logged in successfully"}), 200

@app.route("/start_question_timer", methods=["POST"])
def start_question_timer():
    # Store the start time for each question in the session
    mcq_id = request.json.get("mcq_id")
    if mcq_id not in session:
        session[mcq_id] = datetime.now()
        return jsonify({"message": f"Timer started for MCQ ID: {mcq_id}"})
    else:
        return jsonify({"message": f"Timer already started for MCQ ID: {mcq_id}"})

@app.route("/end_question_timer", methods=["POST"])
def end_question_timer():
    # Calculate time spent for each MCQ and store it in the database
    mcq_id = request.json.get("mcq_id")
    if mcq_id in session:
        start_time = session.pop(mcq_id)
        end_time = datetime.now()
        time_spent = int((end_time - start_time).total_seconds())  # Calculate time spent in seconds

        # Store time_spent in the database for the MCQ in the current quiz attempt
        quiz_id = request.json.get("quiz_id")  # Assuming you can identify the quiz attempt
        if quiz_id:
            user_attempted_quiz = UserAttemptedQuiz(
                user_uuid=current_user.uuid,
                quiz_id=quiz_id,
                mcqID=mcq_id,
                time_taken=time_spent
            )
            db.session.add(user_attempted_quiz)
            db.session.commit()
            return jsonify({"mcq_id": mcq_id, "time_spent": time_spent, "message": "Time spent saved in database"})
        else:
            return jsonify({"message": "Quiz ID not provided"})
    else:
        return jsonify({"message": f"No timer found for MCQ ID: {mcq_id}"})
def generate_quiz(subject, num_questions):
    # Fetch questions based on specific criteria from the database
    selected_questions = (
        db.session.query(Mcqs)
        .filter_by(mcqSubject=subject)
        .order_by(asc(Mcqs.time_spent),desc(Mcqs.accuracy))  # Order by time spent and accuracy
        .limit(num_questions)
        .all()
    )

    # Create a list of dictionaries with selected question details
    quiz_questions = [
        {
            "mcqID": question.mcqID,
            "mcqSubject": question.mcqSubject,
            "mcqTitle": question.mcqTitle,
            # Add other details you want to include in the quiz
        }
        for question in selected_questions
    ]

    return quiz_questions
def fetch_attempted_mcqs_for_quiz(quiz_id):
    # Fetch attempted MCQs for a specific quiz ID from your database
    attempted_mcqs = UserAttemptedQuiz.query.filter_by(quiz_id=quiz_id).all()
    return attempted_mcqs

# Function to calculate accuracy for each topic in a quiz and save it to the database
def calculate_and_save_accuracy_for_quiz(quiz_id):
    attempted_mcqs = fetch_attempted_mcqs_for_quiz(quiz_id)

    # Group attempted MCQs by topic
    mcqs_by_topic = defaultdict(list)
    for mcq_attempt in attempted_mcqs:
        mcqs_by_topic[mcq_attempt.mcq.mcqTopic].append(mcq_attempt)

    # Calculate accuracy for each topic
    accuracy_by_topic = {}
    for topic, mcqs in mcqs_by_topic.items():
        total_attempts_topic = len(mcqs)
        correct_attempts_topic = sum(1 for attempt in mcqs if attempt.selected_option == attempt.mcq.solution)

        if total_attempts_topic > 0:
            accuracy_by_topic[topic] = (correct_attempts_topic / total_attempts_topic) * 100
        else:
            accuracy_by_topic[topic] = 0  # If there are no attempts, set accuracy to 0

        # Save accuracy to the database for each topic
        # Assuming you have a model called TopicAccuracy to store accuracy for each topic
        topic_accuracy = accuracy(
            quiz_id=quiz_id,
            topic=topic,
            accuracy=accuracy_by_topic[topic]
        )
        db.session.add(topic_accuracy)
        db.session.commit()

    return accuracy_by_topic

# Endpoint to save the quiz attempts and calculate accuracy for each topic
@app.route("/save_quiz_attempts", methods=["POST"])
def save_quiz_attempts():
    # Assume you receive quiz attempts data in the request
    # Save the quiz attempts to the database

    # Calculate and save accuracy for the quiz
    quiz_id = "your_quiz_id_here"  # Replace with the actual quiz ID from the request data
    accuracy_for_quiz = calculate_and_save_accuracy_for_quiz(quiz_id)

    return jsonify({"message": "Quiz attempts saved. Accuracy calculated and saved for each topic.", "accuracy": accuracy_for_quiz})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
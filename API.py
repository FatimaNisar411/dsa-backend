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
from flask import Flask, request, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import json
import requests

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
    if request.method == "GET":
        # Handle GET request
        return "This is a GET request."

    elif request.method == "POST":
        # Handle POST request
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import mysql.connector
from similarity import find_most_similar
import os

app = Flask(__name__)

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="qasystem"
)
cursor = db.cursor()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return "File uploaded successfully"

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    file_path = request.form['file']

    filepath = os.path.join(UPLOAD_FOLDER, file_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        context = f.read()

    cursor.execute("SELECT question, answer FROM qa")
    data = cursor.fetchall()

    similar_question, answer = find_most_similar(question, data)
    if similar_question:
        return jsonify({"answer": answer, "source": "database"})

    result = qa_pipeline({'context': context, 'question': question})
    answer = result['answer']
    cursor.execute("INSERT INTO qa (question, answer) VALUES (%s, %s)", (question, answer))
    db.commit()

    return jsonify({"answer": answer, "source": "model"})

if __name__ == '__main__':
    app.run(debug=True)

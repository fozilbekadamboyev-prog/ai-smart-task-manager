from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DB_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def analyze_priority(text):
    text = text.lower()
    if any(word in text for word in ['tezkor', 'bugun', 'shoshilinch', 'urgent', 'asap', 'muhim']):
        return 'Yuqori (High)'
    elif any(word in text for word in ['ertaga', 'hafta', 'korib chiqish', 'later']):
        return 'O\'rta (Medium)'
    else:
        return 'Past (Low)'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error': 'Vazifa matni kiritilmadi'}), 400
    
    tasks = load_tasks()
    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'priority': analyze_priority(data['title']),
        'completed': False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

if __name__ == '__main__':
    app.run(debug=True)

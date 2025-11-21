from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

app = Flask(__name__)

# Data file path
DATA_FILE = 'workout_data.json'

def load_data():
    """Load workout data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'workouts': []}

def save_data(data):
    """Save workout data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/add-workout', methods=['POST'])
def add_workout():
    """Add a new workout entry"""
    try:
        data = request.json
        workout_data = load_data()
        
        new_workout = {
            'id': len(workout_data['workouts']) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'exercise': data.get('exercise'),
            'sets': int(data.get('sets', 0)),
            'reps': int(data.get('reps', 0)),
            'weight': float(data.get('weight', 0)),
            'notes': data.get('notes', '')
        }
        
        workout_data['workouts'].append(new_workout)
        save_data(workout_data)
        
        return jsonify({'success': True, 'message': 'Workout logged successfully!', 'workout': new_workout})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/get-workouts')
def get_workouts():
    """Get all workouts"""
    data = load_data()
    return jsonify(data['workouts'])

@app.route('/get-weekly-stats')
def get_weekly_stats():
    """Get workout stats for the current week"""
    data = load_data()
    workouts = data['workouts']
    
    # Get the start of the current week (Monday)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    
    weekly_data = defaultdict(lambda: {'exercises': 0, 'total_weight': 0, 'total_reps': 0})
    
    for workout in workouts:
        workout_date = datetime.strptime(workout['date'], '%Y-%m-%d %H:%M:%S')
        if workout_date >= start_of_week:
            day_name = workout_date.strftime('%A')
            weekly_data[day_name]['exercises'] += 1
            weekly_data[day_name]['total_weight'] += workout['weight'] * workout['sets']
            weekly_data[day_name]['total_reps'] += workout['reps'] * workout['sets']
    
    return jsonify(dict(weekly_data))

@app.route('/get-exercise-stats')
def get_exercise_stats():
    """Get stats by exercise type"""
    data = load_data()
    workouts = data['workouts']
    
    exercise_stats = defaultdict(lambda: {'count': 0, 'total_weight': 0})
    
    for workout in workouts:
        exercise = workout['exercise']
        exercise_stats[exercise]['count'] += 1
        exercise_stats[exercise]['total_weight'] += workout['weight']
    
    return jsonify(dict(exercise_stats))

@app.route('/delete-workout/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout entry"""
    try:
        data = load_data()
        data['workouts'] = [w for w in data['workouts'] if w['id'] != workout_id]
        save_data(data)
        return jsonify({'success': True, 'message': 'Workout deleted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/get-trends')
def get_trends():
    """Get weight trends for each exercise"""
    data = load_data()
    workouts = data['workouts']
    
    trends = defaultdict(list)
    
    for workout in workouts:
        exercise = workout['exercise']
        trends[exercise].append({
            'date': workout['date'],
            'weight': workout['weight'],
            'reps': workout['reps'],
            'sets': workout['sets']
        })
    
    # Sort each exercise's trends by date
    for exercise in trends:
        trends[exercise] = sorted(trends[exercise], key=lambda x: x['date'])
    
    return jsonify(dict(trends))

if __name__ == '__main__':
    app.run(debug=True, port=5002)

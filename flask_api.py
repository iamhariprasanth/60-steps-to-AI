from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory data store (replace with a real DB like SQLite in production)
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
]
next_id = 3  # For auto-incrementing IDs

# GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET: Retrieve a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

# POST: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    new_user = {
        'id': next_id,
        'name': request.json.get('name'),
        'email': request.json.get('email')
    }
    if not new_user['name'] or not new_user['email']:
        return jsonify({'error': 'Name and email are required'}), 400
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201

# PUT: Update an existing user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    return jsonify(user)

# DELETE: Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)



#### GET http://127.0.0.1:5000/users
#### POST curl -X POST -H "Content-Type: application/json" -d '{"name":"Charlie","email":"charlie@example.com"}' http://127.0.0.1:5000/users
#### PUT  curl -X PUT -H "Content-Type: application/json" -d '{"name":"Charlie Updated"}' http://127.0.0.1:5000/users/3
### DELETE curl -X DELETE http://127.0.0.1:5000/users/3
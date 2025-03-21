from flask import Flask, render_template, jsonify, Response, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messaging
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Mock data
mock_users = {
    #1: {'userID': 1, 'username': 'testuser', 'password': 'password', 'role': 'admin', 'weight': 70},
    1: {'userID': 123, 'username': 'asdf', 'password': 'asdf', 'role': 'admin', 'weight': 70},
}

mock_sessions = {
    1: [
        {'sessionID': 1, 'steps': 5000, 'calories': 200},
        {'sessionID': 2, 'steps': 6000, 'calories': 250},
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        # Mock login check
        for user_id, user_info in mock_users.items():
            if user_info['username'] == username and user_info['password'] == password:
                return redirect(url_for('user_homepage', user_id=user_id))

        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['Name']
        password = request.form['Password']
        weight = int(request.form['Weight'])
        role = 'admin'  # Assuming role is always 'admin' for now

        # Mock user creation
        new_user_id = max(mock_users.keys(), default=0) + 1
        mock_users[new_user_id] = {
            'userID': new_user_id,
            'username': username,
            'password': password,
            'role': role,
            'weight': weight
        }
        mock_sessions[new_user_id] = []

        return redirect(url_for('user_homepage', user_id=new_user_id))

    return render_template('signup.html')

@app.route('/login/<int:user_id>/')
def user_homepage(user_id):
    user_info = mock_users.get(user_id)
    sessions = mock_sessions.get(user_id, [])
    session_count = len(sessions)

    return render_template('user_homepage.html', user_id=user_id, user_info=user_info, session_count=session_count, sessions=sessions)

@app.route('/login/<int:user_id>/<int:session_id>')
def session_info(user_id, session_id):
    sessions = mock_sessions.get(user_id, [])
    session = next((s for s in sessions if s['sessionID'] == session_id), None)

    return render_template('session.html', user_id=user_id, session=session)

@app.route('/login/<int:user_id>/<int:session_id>/delete', methods=['POST'])
def delete_session(user_id, session_id):
    sessions = mock_sessions.get(user_id, [])
    mock_sessions[user_id] = [s for s in sessions if s['sessionID'] != session_id]
    print(f'DELETED SESSION WITH ID: {session_id}')
    return Response(status=202)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    emit('response', {'data': 'Message received'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)


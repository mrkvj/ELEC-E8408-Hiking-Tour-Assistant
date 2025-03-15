from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import db
import hike

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['Password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username and password match an existing user
        cursor.execute("SELECT userID FROM user_info WHERE name = ? AND password = ?", (name, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id = user['userID']
            return redirect(url_for('user_homepage', user_id=user_id))
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        weight = int(request.form['Weight'])
        role = 'admin'  # Assuming role is always 'admin' for now

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM user_info WHERE name = ?", (name,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists. Please choose a different username."

        # Generate a new user ID
        cursor.execute("SELECT MAX(userID) FROM user_info")
        max_id = cursor.fetchone()[0]
        new_user_id = (max_id if max_id is not None else 0) + 1

        # Insert the new user into the database
        cursor.execute("INSERT INTO user_info (userID, password, name, role, weight) VALUES (?, ?, ?, ?, ?)",
                       (new_user_id, password, name, role, weight))
        conn.commit()
        conn.close()

        return redirect(url_for('user_homepage', user_id=new_user_id))

    return render_template('signup.html')

@app.route('/login/<int:user_id>/')
def user_homepage(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve user information
    cursor.execute("SELECT * FROM user_info WHERE userID = ?", (user_id,))
    user_info = cursor.fetchone()

    # Count the number of sessions for the user
    cursor.execute("SELECT COUNT(*) as session_count FROM Session WHERE userID = ?", (user_id,))
    session_count = cursor.fetchone()['session_count']

    # Retrieve the list of sessions for the user
    cursor.execute("SELECT sessionID, steps, calories FROM Session WHERE userID = ?", (user_id,))
    sessions = cursor.fetchall()

    conn.close()

    return render_template('user_homepage.html', user_id=user_id, user_info=user_info, session_count=session_count, sessions=sessions)


@app.route('/login/<int:user_id>/<int:session_id>')
def session_info(user_id, session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve session information
    cursor.execute("SELECT * FROM Session WHERE sessionID = ? AND userID = ?", (session_id, user_id))
    session = cursor.fetchone()

    conn.close()

    return render_template('session.html', user_id=user_id, session=session)

@app.route('/login/<int:user_id>/<int:session_id>/delete', methods=['POST'])
def delete_session(user_id, session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the session from the database
    cursor.execute("DELETE FROM Session WHERE sessionID = ? AND userID = ?", (session_id, user_id))
    conn.commit()
    conn.close()

    print(f'DELETED SESSION WITH ID: {session_id}')
    return redirect(url_for('user_homepage', user_id=user_id))

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

from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from databaseAPI import DatabaseAPI
import hike

DB_FILE_NAME = "test.db"

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

################################################################
# Choose to login or signup
@app.route('/')
def home():

    return render_template('home.html')
################################################################

################################################################
# Login option for existing users
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['Password']
        
        db = DatabaseAPI(DB_FILE_NAME)  # SQLite file database
        if db.connect():
            db.create_tables()


        # Check if user and password pair exists
        #cursor.execute("SELECT userID FROM user_info WHERE name = ? AND password = ?", (name, password))
        user = db.select_user_by_credentials(name,password)
        db.disconnect()

        if user:
            user_id = int(user[0])
            return redirect(url_for('user_homepage', user_id=user_id))
        else:
            #flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')
################################################################

################################################################
# Signup page for new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        weight = int(request.form['Weight'])
        role = 'admin'  # Admin as a default for now
        watchID = None

        db = DatabaseAPI(DB_FILE_NAME)  # SQLite file database
        if db.connect():
            db.create_tables()


            # Check if username exists
            #cursor.execute("SELECT * FROM user_info WHERE name = ?", (name,))
            existing_user = db.select_user_by_username(name)

            if existing_user:
                return "Username already exists. Please choose a different username."

            # Generate user ID
            #cursor.execute("SELECT MAX(userID) FROM user_info")
            max_id = db.select_max_userID()[0]
            new_user_id = (max_id if max_id is not None else 0) + 1

            # Insert the new user into the database
            #cursor.execute("INSERT INTO user_info (userID, password, name, role, weight) VALUES (?, ?, ?, ?, ?)",
            user_info_data = [new_user_id, name, watchID, password, role, weight]
            db.insert_user_info(user_info_data)
            #conn.commit()
            db.disconnect()

        return redirect(url_for('user_homepage', user_id=new_user_id))

    return render_template('signup.html')

################################################################
# Backend for user homepage
@app.route('/login/<int:user_id>/')
def user_homepage(user_id):

    db = DatabaseAPI(DB_FILE_NAME)  # SQLite file database
    if db.connect():
        db.create_tables()
        #conn = get_db_connection()
        #cursor = conn.cursor()

        # Get user information
        #cursor.execute("SELECT * FROM user_info WHERE userID = ?", (user_id,))
        #user_info = cursor.fetchone()
        user_info = db.select_user_by_userID(user_id)

        # User session count
        #cursor.execute("SELECT COUNT(*) as session_count FROM Session WHERE userID = ?", (user_id,))
        #cursor.fetchone()['session_count']
        session_count = db.count_sessions_by_userID(user_id)#['session_count'] 

        # List of sessions
        #cursor.execute("SELECT sessionID, steps, calories FROM Session WHERE userID = ?", (user_id,))
        sessions = db.select_sessions_by_userID(user_id)

        db.disconnect()
        
    user_keys = ['userID','username','watchID', 'password', 'role', 'weight'] 
    user_info = db.cast_tuple_to_dict(user_info,user_keys)
    #session_keys = ['sessionID','userID','watchID','start_time','end_time', 'session_length', 'distance', 'steps', 'calories']
    session_keys = ['sessionID','steps', 'calories'] 
    sessions = [db.cast_tuple_to_dict(tup, session_keys) for tup in sessions]

    return render_template('user_homepage.html', user_id=user_id, user_info=user_info, session_count=session_count, sessions=sessions)
################################################################


################################################################
# Backend for session info page
@app.route('/login/<int:user_id>/<int:session_id>')
def session_info(user_id, session_id):

    db = DatabaseAPI(DB_FILE_NAME)  # SQLite file database
    if db.connect():
        db.create_tables()

    # Get session information
    #cursor.execute("SELECT * FROM Session WHERE sessionID = ? AND userID = ?", (session_id, user_id))
    session = db.select_session_by_sessionID_and_userID(session_id, user_id)

    db.disconnect()

    return render_template('session.html', user_id=user_id, session=session)

################################################################
# Backend for deleting a session
@app.route('/login/<int:user_id>/<int:session_id>/delete', methods=['POST'])
def delete_session(user_id, session_id):

    #conn = get_db_connection()
    #cursor = conn.cursor()
    db = DatabaseAPI(DB_FILE_NAME)  # SQLite file database
    if db.connect():
        db.create_tables()

    # Delete current session from the database
    #cursor.execute("DELETE FROM Session WHERE sessionID = ? AND userID = ?", (session_id, user_id))
    db.delete_session(session_id, user_id)
    #conn.commit()
    db.disconnect()

    print(f'DELETED SESSION WITH ID: {session_id}')
    return redirect(url_for('user_homepage', user_id=user_id))
################################################################

################################################################
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
################################################################

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

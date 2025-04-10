from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from databaseAPI import DatabaseAPI
import hike


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home():
    ''' Choose to login or signup '''

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login option for existing users '''

    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['Password']
        
        db = DatabaseAPI()  # SQLite file database
        if db.connect():
            db.create_tables()


        # Check if user and password pair exists
        user = db.select_user_by_credentials(name,password)
        db.disconnect()

        if user:
            user_id = int(user[0])
            return redirect(url_for('user_homepage', user_id=user_id))
        else:
            #flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' Signup page for new users '''

    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        weight = int(request.form['Weight'])
        role = 'user'  # user as a default for now
        watchID = None

        db = DatabaseAPI()  # SQLite file database
        if db.connect():
            db.create_tables()


            # Check if username exists
            existing_user = db.select_user_by_username(name)

            if existing_user:
                return "Username already exists. Please choose a different username."

            # Generate user ID
            max_id = db.select_max_userID()[0]
            new_user_id = (max_id if max_id is not None else 0) + 1

            # Insert the new user into the database
            user_info_data = [new_user_id, name, watchID, password, role, weight]
            db.insert_user_info(user_info_data)
            db.disconnect()

        return redirect(url_for('user_homepage', user_id=new_user_id))

    return render_template('signup.html')

@app.route('/login/<int:user_id>/')
def user_homepage(user_id):
    ''' Backend for user homepage '''

    db = DatabaseAPI()  # SQLite file database
    if db.connect():
        db.create_tables()

        # Get user information
        user_info = db.select_user_by_userID(user_id)

        # User session count
        session_count = db.count_sessions_by_userID(user_id)#['session_count'] 

        # List of sessions
        sessions = db.select_sessions_by_userID(user_id)

        db.disconnect()
    user_keys = ['userID','username','watchID', 'password', 'role', 'weight'] 
    user_info = db.cast_tuple_to_dict(user_info,user_keys)
    session_keys = ['sessionID','start_time' , 'end_time', 'session_length', 'distance', 'steps', 'calories'] 
    sessions = [db.cast_tuple_to_dict(tup, session_keys) for tup in sessions]

    return render_template('user_homepage.html', user_id=user_id, user_info=user_info, session_count=session_count, sessions=sessions)


@app.route('/login/<int:user_id>/<int:session_id>')
def session_info(user_id, session_id):
    ''' Backend for session info page '''

    db = DatabaseAPI()  # SQLite file database
    if db.connect():
        db.create_tables()

    # Get session information
    session = db.select_session_by_sessionID_and_userID(session_id, user_id)
    session_keys = ['sessionID','userID','watchID','start_time','end_time', 'session_length', 'distance', 'steps', 'calories']
    session = db.cast_tuple_to_dict(session, session_keys)
    db.disconnect()

    return render_template('session.html', user_id=user_id, session=session)


@app.route('/login/<int:user_id>/<int:session_id>/delete', methods=['POST'])
def delete_session(user_id, session_id):
    ''' Backend for deleting a session '''

    db = DatabaseAPI()  # SQLite file database
    if db.connect():
        db.create_tables()

    # Delete current session from the database
    db.delete_session(session_id, user_id)
    db.disconnect()

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

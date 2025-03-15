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
        # Handle login logic here
        user_id = request.form['user_id']
        return redirect(url_for('user_homepage', user_id=user_id))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        user_id = request.form['user_id']
        return redirect(url_for('user_homepage', user_id=user_id))
    return render_template('signup.html')

@app.route('/login/<user_id>/')
def user_homepage(user_id):
    #sessions = hdb.get_sessions(user_id)
    return render_template('user_homepage.html', user_id=user_id, sessions=sessions)

@app.route('/login/<user_id>/<session_id>')
def session_info(user_id, session_id):
    #session = hdb.get_session(session_id)
    return jsonify(hike.to_list(session))

@app.route('/login/<user_id>/<session_id>/delete', methods=['POST'])
def delete_session(user_id, session_id):
    #hdb.delete(session_id)
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

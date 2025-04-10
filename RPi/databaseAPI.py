import sqlite3
from sqlite3 import Error
import threading
import hike
import datetime

DB_FILE_NAME = "database.db"

# lock object so multithreaded use of the same

class DatabaseAPI:
    
    '''
    lock: lock object so multithreaded use of the same HubDatabase object
            is safe. sqlite3 does not allow the same cursor object to be
            used concurrently.
    '''          
    lock = threading.Lock()
    
    def __init__(self):
        """Initialize the DatabaseAPI class with the database file."""
        self.db_file = DB_FILE_NAME
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to the database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
        return True

    def disconnect(self):
        """Close the connection to the database."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Disconnected from the database.")

    def execute_query(self, query, params=None):
        """Execute a single SQL query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetch all results for a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Fetch a single result for a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchone()
            return row
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    def cast_tuple_to_dict(self, tup, keys):
        """
        This method casts the contents of a tuple into a dictionary with keys from the `keys` list and
        ensures all values are converted to strings.

        :param tup: The input tuple with data.
        :param keys: A list of keys corresponding to the tuple's elements.
        :return: A dictionary with string values.
        """
        if len(tup) != len(keys):
            raise ValueError("The length of the tuple and keys list must be the same.")
        
        # Create a dictionary by zipping the keys with the tuple and casting each value to a string
        return {key: str(value) for key, value in zip(keys, tup)}

        
    def create_tables(self):
        """Create the necessary tables in the database."""
        try:
            # Create Session table
            self.execute_query('''CREATE TABLE IF NOT EXISTS Session (
                sessionID INTEGER,
                userID INTEGER,
                watchID TEXT,
                start_time DATETIME,
                end_time DATETIME,
                session_length DATETIME,
                distance INTEGER,
                steps INTEGER,
                calories INTEGER,
                PRIMARY KEY (sessionID, userID)
            )''')

            # Create user_info table
            self.execute_query('''CREATE TABLE IF NOT EXISTS user_info (
                userID INTEGER,
                username TEXT,
                watchID TEXT,
                password TEXT,
                role TEXT,
                weight INTEGER,
                PRIMARY KEY (userID, username)
            )''')

            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")
            
    def insert_session(self, session_data):
        """Insert data into the Session table."""
        #try:
            #self.lock.acquire()
        query = '''INSERT INTO Session (sessionID, userID, watchID, start_time, end_time, distance, steps, calories)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute_query(query, session_data)
        #finally:
            #self.lock.release()


    def insert_user_info(self, user_info_data):
        """Insert data into the user_info table."""
        #try:
        self.lock.acquire()
        query = '''INSERT INTO user_info (userID, username, watchID, password, role, weight)
                VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute_query(query, user_info_data)
        #finally:
        #    self.lock.release()
        
        
    # SELECT Queries

    def select_all_user_info(self):
        """Select all data from user_info."""
        query = "SELECT * FROM user_info"
        return self.fetch_all(query)
    
    def select_user_by_username(self, username):
        """Fetch a user by their username."""
        query = "SELECT * FROM user_info WHERE username = ?"
        return self.fetch_one(query, (username,))

    def select_user_by_userID(self, userID):
        """Fetch a user by their userID."""
        query = "SELECT * FROM user_info WHERE userID = ?"
        return self.fetch_one(query, (userID,))
    
    def select_userID_by_username(self, username):
        """Fetch a userID by their username."""
        query = "SELECT userID FROM user_info WHERE username = ?"
        return self.fetch_one(query, (username,))
    
    def select_userinfo_by_watchID(self, watchID):
        """Fetch a userinfo by their watchID."""
        query = "SELECT userID, username, weight FROM user_info WHERE watchID = ?"
        return self.fetch_one(query, (watchID,))

    def select_max_userID(self):
        """Select the max userID from user_info."""
        query = "SELECT MAX(userID) FROM user_info"
        return self.fetch_one(query)
    
    def select_max_sessionID(self):
        """Select the max sessionID from Session."""
        query = "SELECT MAX(sessionID) FROM Session"
        return self.fetch_one(query)

    def select_user_by_credentials(self, username, password):
        """Select userID from user_info where username and password match."""
        query = "SELECT userID FROM user_info WHERE username = ? AND password = ?"
        return self.fetch_one(query, (username, password))

    def select_exists_user(self, userID):
        """Check if a user exists with the given userID."""
        query = '''SELECT EXISTS(
                       SELECT 1
                       FROM user_info
                       WHERE userID = ?
                       ORDER BY userID ASC
                   )'''
        return self.fetch_one(query, (userID,))

    def select_sessions_by_userID(self, userID):
        """get sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories for a specific userID."""
        query = '''SELECT sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories 
                   FROM Session 
                   WHERE userID = ?'''
        result = self.fetch_all(query, (userID,))
        return result  # Returns a list of tuples (sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories)

    def select_session_by_sessionID(self, sessionID):
        """Select session data by sessionID."""
        query = '''SELECT sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories
                   FROM Session
                   WHERE sessionID = ?'''
        return self.fetch_one(query, (sessionID,))

    def select_session_by_sessionID_and_userID(self, sessionID, userID):
        """Select session data by sessionID and userID."""
        query = '''SELECT sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories
                   FROM Session
                   WHERE sessionID = ? AND userID = ?'''
        return self.fetch_one(query, (sessionID, userID))
    
    def select_user_exists(self, userID):
        """Select userID and username from user_info if user exists."""
        query = '''SELECT userID, username
                   FROM user_info
                   WHERE EXISTS (
                       SELECT 1
                       FROM user_info
                       WHERE userID = ?
                   )
                   LIMIT 1'''
        return self.fetch_one(query, (userID,))
    
    def count_sessions_by_userID(self, userID):
        """Get the count of sessions for a specific userID."""
        query = "SELECT COUNT(*) as session_count FROM Session WHERE userID = ?"
        result = self.fetch_one(query, (userID,))
        if result:
            return result[0]  # Return the session count
        return 0  # Return 0 if no result is found
    
    def count_sessions(self):
        """Gets the count of sessions"""
        query = "SELECT COUNT(*) as session_count FROM Session"
        result = self.fetch_one(query)
        if result:
            return result  # Return the session count
        return 0  # Return 0 if no result is found
    

    def update_session_steps_calories(self, steps, calories, sessionID, userID):
        """Update steps and calories in Session table."""
        query = '''UPDATE Session
                   SET steps = ?, calories = ?
                   WHERE sessionID = ? AND userID = ?'''
        self.execute_query(query, (steps, calories, sessionID, userID))

    def update_user_weight(self, weight, userID, username):
        """Update user weight in user_info table."""
        query = '''UPDATE user_info
                   SET weight = ?
                   WHERE userID = ? AND username = ?'''
        self.execute_query(query, (weight, userID, username))

    def delete_user_info(self, userID, username):
        """Delete user info from user_info table."""
        query = '''DELETE FROM user_info
                   WHERE userID = ? AND username = ?'''
        self.execute_query(query, (userID, username))

    def delete_session(self, sessionID, userID):
        """Delete a session from the Session table."""
        query = '''DELETE FROM Session
                   WHERE sessionID = ? AND userID = ?'''
        self.execute_query(query, (sessionID, userID))

    def update_session_length1(self):
        """Update session length in the Session table."""
        query = '''UPDATE Session
                   SET session_length = strftime('%H:%M:%S', end_time) - strftime('%H:%M:%S', start_time)'''
        self.execute_query(query)

    def select_sessions_with_session_length(self):
        """Select session data with session length calculated."""
        query = '''SELECT sessionID, userID, watchID, start_time, end_time, 
                          strftime('%H:%M:%S', end_time) - strftime('%H:%M:%S', start_time) AS session_length
                   FROM Session'''
        return self.fetch_all(query)
    
    
    def update_session_length2(self, end_time,  start_time, sessionID):
        # Execute the UPDATE query
        query = '''
        UPDATE Session
        SET session_length = 
            strftime('%H:%M:%S', 
                datetime('1970-01-01 00:00:00', 
                '+' || (strftime('%s', ?) - strftime('%s', ?)) || ' seconds'))
        WHERE sessionID = ?;
        '''
        # Execute the query with the sessionID parameter
        self.execute_query(query, (end_time, start_time, sessionID,))
        
    def update_all_session_lengths(self, end_time, start_time, sessionID):
        # Execute the UPDATE query
        query = '''
        UPDATE Session
        SET session_length = 
            strftime('%H:%M:%S', 
                datetime('1970-01-01 00:00:00', 
                '+' || (strftime('%s', end_time) - strftime('%s', start_time)) || ' seconds'))
        WHERE ? IS NOT NULL AND ? IS NOT NULL;
        '''
        # Execute the query with the sessionID parameter
        self.execute_query(query, (end_time, start_time, sessionID, start_time, end_time,))
    
    def select_session_length(self,sessionID):
        # Execute the SELECT query
        query = '''
        SELECT session_length
        FROM Session
        WHERE sessionID = ?;
        '''
        # Execute the query with the sessionID parameter
        session_length = self.fetch_one(query, (sessionID,))
        return session_length


    def update_session_end_time(self, sessionID, userID, end_time):
        """Update end time for a specific session."""
        query = '''UPDATE Session
                   SET end_time = ?
                   WHERE sessionID = ? AND userID = ?'''
        self.execute_query(query, (end_time, sessionID, userID))

    def update_session_distance(self, distance, sessionID, userID):
        """Update distance for a specific session."""
        query = '''UPDATE Session
                   SET distance = ?
                   WHERE sessionID = ? AND userID = ?'''
        self.execute_query(query, (distance, sessionID, userID))


    def save_session_from_bt(self, hs: hike.HikeSession):
        session_count = int(self.count_sessions()[0])

        if session_count > 0:
            hs.sessionID = session_count + 1
        else:
            hs.sessionID = 1
            
        #(sessionID, userID, watchID, start_time, end_time, session_length, distance, steps, calories)  hs.duration,
        session_data = [hs.sessionID, int(self.select_userID_by_username(hs.username)[0]), hs.watchID , hs.start_time, hs.end_time, hs.distance, hs.steps, hs.calories] 

        try:
            self.insert_session(session_data)
            self.update_session_length2(hs.end_time, hs.start_time, hs.sessionID)
            
        except sqlite3.IntegrityError:
            print("WARNING: Session ID already exists in database! Aborting saving current session.")

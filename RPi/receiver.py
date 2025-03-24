import time
import sqlite3

import hike
from databaseAPI import DatabaseAPI
import bt

hubbt = bt.HubBluetooth()

def process_sessions(sessions: list[hike.HikeSession]):
    """Callback function to process sessions.

    Calculates the calories for a hiking session.
    Saves the session into the database.

    Args:
        sessions: list of `hike.HikeSession` objects to process
    """
    db = DatabaseAPI()  # SQLite file database
    if db.connect():
        db.create_tables()
        
        for hs in sessions:
            hs.calc_kcal()
            db.save_session_from_bt(hs)
            
        db.disconnect()
        

def main():
    print("Starting Bluetooth receiver.")
    try:
        while True:
            hubbt.wait_for_connection()
            hubbt.synchronize(callback=process_sessions)
            
    except KeyboardInterrupt:
        print("CTRL+C Pressed. Shutting down the server...")

    except Exception as e:
        print(f"Unexpected shutdown...")
        print(f"ERROR: {e}")
        hubbt.sock.close()
        raise e

if __name__ == "__main__":
    main()
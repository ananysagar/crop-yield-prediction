"""
createdb.py

This script creates (or connects to) the SQLite database 'agricultureuser.db'.
It creates the agriuser table for user management if it doesn't exist.
"""

import sqlite3

def create_database(db_name='agricultureuser.db'):
    """
    Creates the SQLite database and necessary tables.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create agriuser table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agriuser (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phono TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

if __name__ == '__main__':
    create_database()

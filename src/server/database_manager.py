import sqlite3

def initialize_db():
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS friends (
        user_id INTEGER,
        friend_id INTEGER,
        status TEXT CHECK(status IN ('pending', 'accepted')) NOT NULL,
        UNIQUE(user_id, friend_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(friend_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Username or email already exists.")
    finally:
        conn.close()

def send_friend_request(user_id, friend_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, 'pending')", (user_id, friend_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Friend request already sent or users are already friends.")
    finally:
        conn.close()

def accept_friend_request(user_id, friend_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE friends SET status = 'accepted' 
    WHERE user_id = ? AND friend_id = ? AND status = 'pending'
    """, (user_id, friend_id))
    conn.commit()
    conn.close()

def reject_friend_request(user_id, friend_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM friends WHERE status = 'pending' AND user_id = ? AND friend_id = ?
    """, (user_id, friend_id))
    conn.commit()
    conn.close()

def get_friends(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.id, users.username FROM users 
    JOIN friends ON users.id = friends.friend_id 
    WHERE friends.user_id = ? AND friends.status = 'accepted'
    """, (user_id,))
    friends = cursor.fetchall()
    conn.close()
    return friends

# Initialize database
initialize_db()

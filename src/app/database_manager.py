import sqlite3
import re

from argon2 import PasswordHasher
ph = PasswordHasher()


def initialize_db():
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        tokens INTEGER DEFAULT 100,
        rating INTEGER DEFAULT 8
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
    hash = ph.hash(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hash))
        conn.commit()    
    except sqlite3.IntegrityError:
        print("Username or email already exists.")
        conn.close()
        return 1
    finally:
        conn.close()
    return 0

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

def get_user_info(username):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    conn.close()
    if user_info:
        return {
            'id': user_info[0],
            'username': user_info[1],
            'email': user_info[2],
            'password': user_info[3]
        }
    return None

def get_user_id(username):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    conn.close()
    if user_info:
        int(user_info[0])
    return None

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

def change_password(user_id, new_password):
    if not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
        print("Password must contain at least one uppercase letter, one lowercase letter, and one special character.")
        return

    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()
    print("Password updated successfully.")

def delete_account(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM friends WHERE user_id = ? OR friend_id = ?", (user_id, user_id))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    print("Account deleted successfully.")

def check_user(username, password):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password from users where username = ?", (username,))
    hash = cursor.fetchall()
    if not hash:
        print("User not found.")
        return None
    else :
        test_password = hash[0][0]
        try:
            ph.verify(test_password, password)
            print("Password is correct.")
        except:
            print("Password is incorrect.")
            return None
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    if user_info:
        user = {
            'id': user_info[0],
            'username': user_info[1],
            'email': user_info[2],
            'password': user_info[3]
        }
    else:
        print("User not found.2")
        return None
    conn.close()
    return user

def forgot_password(email, new_password):
    if not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
        print("Password must contain at least one uppercase letter, one lowercase letter, and one special character.")
        return

    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    if cursor.rowcount == 0:
        print("No account found with the provided email.")
    else:
        print("Password reset successfully.")
    conn.commit()
    conn.close()

# Initialize database
initialize_db()

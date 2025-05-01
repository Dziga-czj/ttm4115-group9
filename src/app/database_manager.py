import sqlite3
import re
import random
import json
import time

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

    cursor.execute('''
    DROP TABLE IF EXISTS scooters
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scooters (
        scooter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        renter_id INTEGER DEFAULT -1,
        battery INTEGER DEFAULT 100,
        lattitude REAL,
        longitude REAL,
        running INTEGER DEFAULT 0,
        reservation_time INTEGER DEFAULT 0
    )''')
    
    
    conn.commit()
    conn.close()
    add_random_scooter()
    add_random_scooter()
    add_random_scooter()

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
    friends = get_friends(user_id)
    if friend_id in [friend[0] for friend in friends]:
        return
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

    friends = get_friends(user_id)
    if friend_id in [friend[0] for friend in friends]:
        conn = sqlite3.connect("social_network.db")
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM friends WHERE status = 'pending' AND user_id = ? AND friend_id = ?
        """, (user_id, friend_id))
        conn.commit()

        conn.close()
        return

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

def get_pending_requests(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT user_id FROM friends where friend_id = ? AND friends.status = 'pending'
    """, (user_id,))
    pending_requests = cursor.fetchall()

    res = []

    for id in pending_requests :
        cursor.execute("""
        SELECT username FROM users where id = ?
        """, (id[0],))
        username = cursor.fetchall()[0]
        res.append((id[0], username[0]))
    
    print(res)
    conn.close()
    return res

def get_sent_requests(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT friend_id FROM friends where user_id = ? AND friends.status = 'pending'
    """, (user_id,))
    pending_requests = cursor.fetchall()

    res = []
    for id in pending_requests :
        cursor.execute("""
        SELECT username FROM users where id = ?
        """, (id[0],))
        username = cursor.fetchall()[0]
        res.append((id[0], username[0]))
    
    print(res)
    conn.close()
    return res

def get_username(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    username = cursor.fetchone()
    conn.close()
    if username:
        return username[0]
    return None

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

def get_user_by_id(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_info = cursor.fetchone()
    conn.close()
    if user_info:
        return {
            'username': user_info[1],
            'email': user_info[2],
            'coquilles': user_info[4],
        }
    return None

def get_user_id(username):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    id = user_info[0] if user_info else None
    conn.close()
    return id

def get_friends(user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.username, u.email 
    FROM users u 
    JOIN friends f ON (u.id = f.friend_id AND f.user_id = ? AND f.status = 'accepted') 
                   OR (u.id = f.user_id AND f.friend_id = ? AND f.status = 'accepted')
    """, (user_id, user_id,))
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

def update_user_password(user_id, new_password):
    hash = ph.hash(new_password)
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hash, user_id))
    conn.commit()
    conn.close()
    


def update_user_username(user_id, new_username):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    conn.commit()
    conn.close()

def get_available_scooters(user_id = None):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    if user_id:
        data = cursor.execute('''SELECT 
        json_group_array(
            json_object(
                'scooter_id', scooter_id, 
                'battery', battery, 
                'lattitude', lattitude,
                'longitude', longitude,
                'reserved', CASE WHEN renter_id = -1 THEN 0 ELSE 1 END,
                'running', running,
                'reservation_time', CASE WHEN renter_id = -1 THEN 0 ELSE reservation_time END
                )
            )
        FROM scooters WHERE renter_id = -1 OR renter_id = ?''', (user_id,))
    else:
        data = cursor.execute('''SELECT 
        json_group_array(
            json_object(
                'scooter_id', scooter_id, 
                'battery', battery, 
                'lattitude', lattitude,
                'longitude', longitude,
                'reserved', CASE WHEN renter_id = -1 THEN 0 ELSE 1 END,
                'running', running,
                'reservation_time', CASE WHEN renter_id = -1 THEN 0 ELSE reservation_time END
                )
            )
        FROM scooters WHERE renter_id = -1''')
    scooters = json.loads(data.fetchall()[0][0])
    conn.close()
    return scooters

def add_random_scooter():
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scooters (battery, lattitude, longitude) VALUES (?, ?, ?)", (random.randint(10,100), random.uniform(63.41, 63.419), random.uniform(10.403, 10.405)))
    conn.commit()
    conn.close()

def reserve_scooter(scooter_id, user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE scooters SET renter_id = ?, reservation_time = ? WHERE scooter_id = ?", (user_id, int(time.time()), scooter_id))
    conn.commit()
    conn.close()

def unlock_reserved_scooter(scooter_id, user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE scooters SET running = ? WHERE scooter_id = ? AND renter_id = ?", (int(time.time()), scooter_id, user_id))
    conn.commit()
    conn.close()

def unlock_scooter(scooter_id, user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE scooters SET running = ?, renter_id = ? WHERE scooter_id = ?", (int(time.time()), user_id, scooter_id))
    conn.commit()
    conn.close()

def lock_scooter(scooter_id, user_id):
    conn = sqlite3.connect("social_network.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE scooters SET running = 0, renter_id = -1, reservation_time = 0 WHERE scooter_id = ? AND renter_id = ?", (scooter_id, user_id))
    conn.commit()
    conn.close()

# Initialize database
initialize_db()

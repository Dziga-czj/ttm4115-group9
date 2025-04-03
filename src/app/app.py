from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


import database_manager


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def on_login():
    None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f'login for user {username} with password {password}')
        user = database_manager.check_user(username, password)    
        print(user)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else :
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        res = database_manager.add_user(username, email, password)
        if res == 0:
            return redirect(url_for('login'))
        elif res == 1:
            return render_template('register.html', error='Username or email already exists.')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        return render_template('forgotPassword.html', message='If the email is registered, you will receive a reset link.')
    return render_template('forgotPassword.html')

@app.route('/return_to_login')
def return_to_login():
    return redirect(url_for('login'))

@app.route('/friend_request', methods=['GET','POST'])
def friend_requests():
    user_id = session['user_id']
        
    pending_requests = database_manager.get_pending_requests(user_id)



    message = request.args.get('message')
    message = message if message else ""
    error = request.args.get('error')
    error = error if error else ""

    return render_template('friend_request.html', pending_requests=pending_requests, message=message, error=error)


@app.route('/send_friend_request', methods=['POST'])
def send_friend_requests():
    if request.method == 'POST':
        friend_username = request.form['friend_username']
        user_id = session['user_id']
        friend_id = database_manager.get_user_id(friend_username)
        if friend_id == user_id:
            return redirect(url_for('.friend_requests', error='You cannot send a friend request to yourself.'))
        if friend_id:
            database_manager.send_friend_request(user_id, friend_id)
            return redirect(url_for('.friend_requests', message='Friend request sent.'))
        else:
            return redirect(url_for('.friend_requests', error='User not found.'))
        

    return render_template('friend_request.html')

@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request():
    if request.method == 'POST':
        user_id = session['user_id']
        friend_id = request.form['friend_id']
        database_manager.accept_friend_request(user_id, friend_id)
        return redirect(url_for('.friend_requests', message='Friend request accepted.'))
    return render_template('friend_request.html')

@app.route('/reject_friend_request', methods=['POST'])
def reject_friend_request():
    if request.method == 'POST':
        user_id = session['user_id']
        friend_id = request.form['friend_id']
        database_manager.reject_friend_request(friend_id, user_id)
        return redirect(url_for('.friend_requests', error='Friend request rejected.'))
    return render_template('friend_request.html')

@app.route('/updateProfile')
def account_management():
    return render_template('updateProfile.html')

@app.route('/passwordChange')
def change_password():
    return render_template('passwordChange.html')

@app.route('/account_deletion')
def account_deletion():
    
    return render_template('account_deletion.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        user_id = session['user_id']
        database_manager.delete_account(user_id)
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('account_deletion.html')

@app.route('/rentScooter')
def rent_scooter():
    return render_template('rentScooter.html')

if __name__ == '__main__':
    app.run(debug=True)
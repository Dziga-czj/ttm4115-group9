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

    return render_template('login.html', error='Invalid credentials')

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
            return render_template('register.html')

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
        client.send_message(MQTT_GENERAL, {
            'command': 'forgot_password',
            'email': email
        })
        return render_template('forgotPassword.html', message='If the email is registered, you will receive a reset link.')
    return render_template('forgotPassword.html')

@app.route('/return_to_login')
def return_to_login():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
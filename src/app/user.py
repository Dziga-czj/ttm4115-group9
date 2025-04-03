from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import paho.mqtt.client as mqtt

from user_mqtt import Mqtt_client
from user_mqtt import User

MQTT_BROKER = 'mqtt20.iik.ntnu.no'
MQTT_PORT = 1883

MQTT_GENERAL = 'ttm4115/escargot/general'
MQTT_GENERAL_RESPONSE = 'ttm4115/escargot/general_response'


client = Mqtt_client()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('social_network.db')
    conn.row_factory = sqlite3.Row
    return conn

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

        client.send_message(MQTT_GENERAL, {
            'command': 'login',
            'username': username,
            'password': password
        })

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
        print("sending register request")
        client.send_message(MQTT_GENERAL, {
            'command': 'register',
            'username': username,
            'password': password,
            'email': email
        })

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

if __name__ == '__main__':
    app.run(debug=True)
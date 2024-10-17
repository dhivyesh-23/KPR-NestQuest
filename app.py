from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import bcrypt

app = Flask(__name__)

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="REALESTATE_USER",
        user="first",
        password="anirudhh"
    )
    return conn

# Home route
@app.route('/')
def home():
    return render_template('home_login_final.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        print(f"Form data received: {data}")

        # Ensure username, password, and other fields are provided
        if not username or not password :
            return jsonify({'message': 'All fields are required'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)", 
                        (username, hashed_password.decode('utf-8'), name, email))
            conn.commit()
            return redirect(url_for('login'))  # Redirect to login after successful registration
        except psycopg2.IntegrityError:
            conn.rollback()
            return jsonify({'message': 'Username already exists'}), 409
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_hashed_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return redirect(url_for('user_dashboard'))  # Redirect to dashboard after login
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

        cursor.close()
        conn.close()

    return render_template('login.html')

# Placeholder route for user dashboard
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('properties_dashboard.html')  # Ensure you have properties_dashboard.html

if __name__ == '__main__':
    app.run(debug=True)

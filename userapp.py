from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import bcrypt
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/real_estate"
mongo = PyMongo(app)
client = MongoClient("mongodb://localhost:27017/")
db = client['real_estate']
properties_collection = db['properties']



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
def userhome():
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

    return render_template('userregister.html')

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
                return redirect(url_for('property_list'))  # Redirect to dashboard after login
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

        cursor.close()
        conn.close()

    return render_template('userlogin.html')

@app.route('/view_properties', methods=['GET'])
def view_properties():
    # Get the filter values from the query string
    search_query = request.args.get('search_query', '').lower()
    location = request.args.get('location', 'any')
    property_type = request.args.get('property_type', 'all')
    budget = int(request.args.get('budget', 10000))
    
    # Build the query dynamically based on filters
    query = {}
    
    # Search query (location or property name/type)
    if search_query:
        query['$or'] = [
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'location': {'$regex': search_query, '$options': 'i'}},
            {'property_type': {'$regex': search_query, '$options': 'i'}}
        ]
    
    # Location filter
    if location != 'any':
        query['location'] = location

    # Property type filter
    if property_type != 'all':
        query['property_type'] = property_type

    # Budget filter (price_per_cent <= budget)
    query['price_per_cent'] = {'$lte': budget}

    # Fetch properties that match the filters from the database
    properties = list(properties_collection.find(query))
    
    # Render the properties on the frontend
    return render_template('property_listing.html', properties=properties)
@app.route('/properties', methods=['GET'])

def property_list():
    # Fetch all properties from MongoDB
    properties = mongo.db.properties.find()
    # Pass the properties to the template
    return render_template('property_listing.html', properties=properties)


# Placeholder route for user dashboard
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('property_listing.html')  # Ensure you have properties_dashboard.html

if __name__ == '__main__':
    app.run(debug=True,port=5001)

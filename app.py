from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import os
from dotenv import load_dotenv
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL*+-
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
def staffhome():
    return render_template('home.html')

# Login route
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

        # Fetch the password for the given username
        cursor.execute("SELECT password FROM staffs WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            # Compare stored password (plaintext) with entered password (plaintext)
            if password == stored_password:
                return redirect(url_for('choice'))  # Redirect to choice page after login
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

        cursor.close()
        conn.close()

    return render_template('login.html')

# Choice route
@app.route('/choice', methods=['GET', 'POST'])
def choice():
    return render_template('choice.html')


# Load environment variables
load_dotenv()


# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/real_estate"
mongo = PyMongo(app)

# Path to save uploaded images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/properties', methods=['GET'])
def property_list():
    # Fetch all properties from MongoDB
    properties = mongo.db.properties.find()
    # Pass the properties to the template
    return render_template('property_listing.html', properties=properties)


@app.route('/edit_choice', methods=['GET'])
def edit_choice():
   
    properties = mongo.db.properties.find()
    return render_template('edit_choicefi.html', properties=properties)


@app.route('/edit_property/<property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    if request.method == 'POST':
        # Handle form submission and update
        name = request.form.get('name')
        area = request.form.get('area')
        location = request.form.get('location')
        year_of_construction = request.form.get('year_of_construction')
        landmarks = request.form.get('landmarks')
        cd = request.form.get('Contact_Details')
        image = request.files.get('image')

        update_data = {
            'name': name,
            'area': area,
            'location': location,
            'year_of_construction': year_of_construction,
            'landmarks': landmarks,
            "Contact_Details": cd,
        }

        # If an image is provided, save it and add to the update data
        if image and image.filename != '':
            image_filename = image.filename  # Extract the filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)  # Save the image to the upload folder
            update_data['image'] = image_filename  # Add image filename to update data

        # Update the property in MongoDB
        mongo.db.properties.update_one({'_id': ObjectId(property_id)}, {'$set': update_data})

        return redirect('/properties')

    # Fetch the property details from MongoDB
    property = mongo.db.properties.find_one({'_id': ObjectId(property_id)})

    if property is None:
        # Handle the case where the property is not found (optional)
        return "Property not found", 404

    # Render the edit property template with the property details
    return render_template('edit_property.html', property=property)

@app.route('/delete_choice', methods=['GET'])
def delete_choice():
   
    properties = mongo.db.properties.find()
    return render_template('delete_choice.html', properties=properties)

@app.route('/delete_property/<property_id>', methods=['POST'])
def delete_property(property_id):
   
    mongo.db.properties.delete_one({'_id': ObjectId(property_id)})
    return redirect(url_for('property_list'))
@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))
@app.route('/add_property', methods=['GET'])
def types():
     return render_template('add_choice.html')
@app.route('/add_land', methods=['GET'])
def land():
     return render_template('staff_add_land.html')
@app.route('/add_villa', methods=['GET'])
def villa():
     return render_template('staff_add_villa.html')
@app.route('/add_apartment', methods=['GET'])
def apartment():
     return render_template('staff_add_apartment.html')

@app.route('/add_land_details', methods=['GET','POST'])
def land_details():
    if request.method == 'POST':
        # Get form data safely with .get() to avoid KeyError
        name = request.form.get('name')
        price_per_cent = request.form.get('price_per_cent')
        area = request.form.get('area')
        location = request.form.get('location')
        year_of_construction = request.form.get('year_of_construction')
        landmarks = request.form.get('landmarks')
        cd=request.form.get('Contact_Details')
        image = request.files.get('image')

        
      
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            mongo.db.properties.insert_one({
                'name': name,
                'price_per_cent': price_per_cent,
                'area': area,
                'location': location,
                'year_of_construction': year_of_construction,
                'landmarks': landmarks,
                "Contact_Details":cd,
                'image': image_filename
            })

        return redirect(url_for('choice'))  # Redirect to the property list after successful submission
    return render_template('staff_add_land.html')


@app.route('/add_villa_details', methods=['GET','POST'])
def villa_details():
    if request.method == 'POST':
        # Get form data safely with .get() to avoid KeyError
        name = request.form.get('name')
        price_per_cent = request.form.get('price_per_cent')
        area = request.form.get('area')
        location = request.form.get('location')
        year_of_construction = request.form.get('year_of_construction')
        landmarks = request.form.get('landmarks')
        amenities=request.form.get('amenities')
        no_of_bedrooms=request.form.get('no_of_bedrooms')
        cd=request.form.get('Contact_Details')
        image = request.files.get('image')

        
      
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            mongo.db.properties.insert_one({
                'name': name,
                'price_per_cent': price_per_cent,
                'area': area,
                'location': location,
                'year_of_construction': year_of_construction,
                'landmarks': landmarks,
                'amenities':amenities,
                'no_of_bedrooms':no_of_bedrooms,
                "Contact_Details":cd,
                'image': image_filename
            })

        return redirect(url_for('choice'))  # Redirect to the property list after successful submission
    return render_template('staff_add_villa.html')


@app.route('/add_apartment_details', methods=['GET','POST'])
def apartment_details():
    if request.method == 'POST':
        # Get form data safely with .get() to avoid KeyError
        name = request.form.get('name')
        price_per_cent = request.form.get('price_per_cent')
        area = request.form.get('area')
        location = request.form.get('location')
        year_of_construction = request.form.get('year_of_construction')
        landmarks = request.form.get('landmarks')
        amenities=request.form.get('amenities')
        no_of_bedrooms=request.form.get('no_of_bedrooms')
        cd=request.form.get('Contact_Details')
        image = request.files.get('image')

        
      
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            mongo.db.properties.insert_one({
                'name': name,
                'price_per_cent': price_per_cent,
                'area': area,
                'location': location,
                'year_of_construction': year_of_construction,
                'landmarks': landmarks,
                'amenities':amenities,
                'no_of_bedrooms':no_of_bedrooms,
                "Contact_Details":cd,
                'image': image_filename
            })

        return redirect(url_for('choice'))  # Redirect to the property list after successful submission
    return render_template('staff_add_apartment.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
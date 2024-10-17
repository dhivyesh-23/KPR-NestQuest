from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client['realestate']
properties = db['properties']
employees = db['employees']

# Employee model (for authentication)
def create_employee(username, password):
    password_hash = generate_password_hash(password)
    employees.insert_one({'username': username, 'password': password_hash})

def get_employee(username):
    return employees.find_one({'username': username})

# Property model
def add_property(data):
    properties.insert_one(data)

def get_properties():
    return list(properties.find())

def get_property_by_id(property_id):
    return properties.find_one({'_id': property_id})

def delete_property(property_id):
    properties.delete_one({'_id': property_id})

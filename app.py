from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb
import json
import mysql.connector

app = Flask(__name__)

#allow cors for all origins and allow post requests
CORS(app, resources={r"/*": {"origins": "*", "methods":["POST"]}})

# MariaDB Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "patient",
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome to Flask API connect Database"

@app.route('/create_record', methods=['POST', 'GET'])
def create_record():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        required_keys = ["patientid", "dateofvisit", "doctorname", "clinicalimpression", "diagnosis", "icd10code"]
        
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing key: {key}"}), 400
            
        cursor.execute(
                "INSERT INTO patient_visits (patientid, dateofvisit, doctorname, clinicalimpression, diagnosis, icd10code) VALUES (%s, %s, %s, %s, %s, %s)",
                (data["patientid"], data["dateofvisit"], data["doctorname"], data["clinicalimpression"], data["diagnosis"], data["icd10code"])
            )
        conn.commit()
        return jsonify({"message": "Patient Record created successfully"}), 201
    
    except mariadb.Error as e:
        print(f"Error executing SQL: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to create the record"}), 500

if __name__ == '__main__':
    app.run()

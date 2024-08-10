from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allows requests from any origin

# Database connection
conn = psycopg2.connect(
    host="dpg-cqqck656l47c73as78gg-a.oregon-postgres.render.com",
    database="healthdb_nkst",
    user="healthdb_nkst_user",
    password="8efpuuEvJJTFWJWLEclkgEAZFpfllwvs"
)
cursor = conn.cursor()

@app.route('/')
def home():
    return "Welcome to the Health API!"

# Endpoint to get all diseases
@app.route('/diseases', methods=['GET'])
def get_diseases():
    cursor.execute("SELECT * FROM diseases")
    diseases = cursor.fetchall()
    return jsonify(diseases)

# Endpoint to get treatments based on disease_id
@app.route('/treatments/<int:disease_id>', methods=['GET'])
def get_treatments(disease_id):
    cursor.execute("SELECT * FROM treatments WHERE disease_id = %s", (disease_id,))
    treatments = cursor.fetchall()
    return jsonify(treatments)

# Endpoint to get both diseases and treatments based on symptoms
@app.route('/get-disease-info', methods=['POST'])
def get_disease_info():
    data = request.json
    symptoms = data.get('symptoms')
    
    try:
        # Query to find diseases based on symptoms
        cursor.execute("""
            SELECT d.disease_id, d.disease_name 
            FROM diseases d 
            JOIN symptoms s ON d.disease_id = s.disease_id 
            WHERE s.symptom_name ILIKE %s
        """, ('%' + symptoms + '%',))
        
        diseases = cursor.fetchall()
        
        if not diseases:
            return jsonify({"error": "No diseases found for the given symptoms."}), 404
        
        # Get treatments for each disease
        disease_info = []
        for disease in diseases:
            cursor.execute("SELECT * FROM treatments WHERE disease_id = %s", (disease[0],))
            treatments = cursor.fetchall()
            
            disease_info.append({
                "disease_id": disease[0],
                "disease_name": disease[1],
                "treatments": [{"type": t[2], "description": t[3]} for t in treatments]
            })
        
        return jsonify({"result": disease_info})

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

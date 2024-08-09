from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

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

@app.route('/diseases', methods=['GET'])
def get_diseases():
    cursor.execute("SELECT * FROM diseases")
    diseases = cursor.fetchall()
    return jsonify(diseases)

@app.route('/treatments/<int:disease_id>', methods=['GET'])
def get_treatments(disease_id):
    cursor.execute("SELECT * FROM treatments WHERE disease_id = %s", (disease_id,))
    treatments = cursor.fetchall()
    return jsonify(treatments)

if __name__ == "__main__":
    app.run(debug=True)

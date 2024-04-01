from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/cyber_threats"
mongo = PyMongo(app)

# Function to fetch cyber threats by type
def get_threats_by_type(threat_type):
    # Connect to the 'resources' collection in MongoDB
    collection = mongo.db.resources
    
    # Fetch documents with the specified threat type
    threats = list(collection.find({'type': threat_type}))
    
    # Convert ObjectId to string for JSON serialization
    for threat in threats:
        threat['_id'] = str(threat['_id'])
    
    return threats

# Endpoint to fetch cyber threats by type
@app.route('/cyberthreats/type', methods=['GET'])
def get_cyber_threats_by_type():
    threat_type = request.args.get('type')
    
    if not threat_type:
        return jsonify({"error": "Threat type parameter is missing"}), 400
    
    threats = get_threats_by_type(threat_type)
    
    return jsonify(threats), 200

# Function to fetch cyber threats by severity
def get_threats_by_severity(severity):
    # Connect to the 'resources' collection in MongoDB
    collection = mongo.db.resources
    
    # Fetch documents with the specified severity
    threats = list(collection.find({'severity': severity}))
    
    # Convert ObjectId to string for JSON serialization
    for threat in threats:
        threat['_id'] = str(threat['_id'])
    
    return threats

# Endpoint to fetch cyber threats by severity
@app.route('/cyberthreats/severity', methods=['GET'])
def get_cyber_threats_by_severity():
    severity = request.args.get('severity')
    
    if not severity:
        return jsonify({"error": "Severity parameter is missing"}), 400
    
    threats = get_threats_by_severity(severity)
    
    return jsonify(threats), 200

# Endpoint to fetch all cyber threat resources
@app.route('/cyberthreats', methods=['GET'])
def get_cyber_threats():
    # Connect to the 'resources' collection in MongoDB
    collection = mongo.db.resources
    
    # Fetch all documents from the collection
    threats = list(collection.find({}))
    
    # Convert ObjectId to string for JSON serialization
    for threat in threats:
        threat['_id'] = str(threat['_id'])
    
    return jsonify(threats), 200

# Endpoint to fetch a specific cyber threat resource by ID
@app.route('/cyberthreats/<string:threat_id>', methods=['GET'])
def get_cyber_threat(threat_id):
    # Connect to the 'resources' collection in MongoDB
    collection = mongo.db.resources
    
    # Fetch the document with the specified ID
    threat = collection.find_one({'_id': threat_id})
    
    # Check if the document exists
    if threat:
        # Convert ObjectId to string for JSON serialization
        threat['_id'] = str(threat['_id'])
        return jsonify(threat), 200
    else:
        return jsonify({"error": "Resource not found"}), 404

# Code to add a new cyber threat
@app.route('/cyberthreats/add', methods=['POST'])
def add_cyber_threat():
    data = request.json
    print(f"Received data: {data}")  # Debugging statement

    # Validate required fields
    if not data or 'type' not in data or 'severity' not in data or 'description' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Connect to the 'resources' collection in MongoDB
    collection = mongo.db.resources
    
    # Insert new cyber attack data into MongoDB
    result = collection.insert_one(data)
    
    # Check if insertion was successful
    if result.inserted_id:
        return jsonify({"message": "Cyber threat added successfully", "id": str(result.inserted_id)}), 201
    else:
        return jsonify({"error": "Failed to add cyber threat"}), 500

if __name__ == '__main__':
    # Run the Flask app on host '0.0.0.0' and port 5000
    app.run(host='0.0.0.0', port=5000)

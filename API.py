from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/cyber_threats"
mongo = PyMongo(app)

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

if __name__ == '__main__':
    app.run(debug=True)


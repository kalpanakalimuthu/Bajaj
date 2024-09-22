from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import base64
import os

app = Flask(__name__)

# Enable CORS for the entire application
CORS(app)

# Helper function to decode Base64 string and get file info
def decode_file(file_b64):
    try:
        # Decode the Base64 string
        file_data = base64.b64decode(file_b64)
        # Save to a temporary file to get file size and MIME type
        temp_file_path = "temp_file"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_data)
        
        # Check file size in KB
        file_size_kb = os.path.getsize(temp_file_path) / 1024
        
        # Get MIME type (basic logic, can use other libraries if needed)
        mime_type = "image/png"  # Assuming image/png, this can be made more flexible
        
        # Delete the temp file after use
        os.remove(temp_file_path)
        
        return True, mime_type, file_size_kb
    except Exception as e:
        return False, None, 0

# POST endpoint to handle the request
@app.route('/bfhl', methods=['POST'])
def process_data():
    try:
        # Extract data from the request
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64', None)

        # Extract numbers and alphabets
        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]
        
        # Find the highest lowercase alphabet
        lowercase_alphabets = [item for item in alphabets if item.islower()]
        highest_lowercase = max(lowercase_alphabets) if lowercase_alphabets else None
        
        # Handle file (if present)
        file_valid, file_mime_type, file_size_kb = decode_file(file_b64) if file_b64 else (False, None, 0)
        
        # Response
        response = {
            "is_success": True,
            "user_id": "john_doe_17091999",
            "email": "john@xyz.com",
            "roll_number": "ABCD123",
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else [],
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": file_size_kb
        }
    except Exception as e:
        response = {
            "is_success": False,
            "message": "Error processing request: " + str(e)
        }
    
    return jsonify(response)

# GET endpoint to return an operation code
@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    response = {
        "operation_code": "1"  # You can replace this with any logic you want
    }
    return jsonify(response)



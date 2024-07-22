import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    if not request.json:
        raise APIException("You must send information in the body", status_code=400)
    
    required_fields = ['first_name', 'age', 'lucky_numbers']
    if not all(field in request.json for field in required_fields):
        raise APIException("Missing required fields", status_code=400)

    new_member = {
        "first_name": request.json['first_name'],
        "age": request.json['age'],
        "lucky_numbers": request.json['lucky_numbers']
    }
    
    added_member = jackson_family.add_member(new_member)
    return jsonify(added_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted_member = jackson_family.delete_member(member_id)
    if deleted_member:
        return jsonify({"done": True}), 200
    return jsonify({"message": "Member not found"}), 404

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if not request.json:
        raise APIException("You must send information to update", status_code=400)
    
    updated_member = jackson_family.update_member(member_id, request.json)
    if updated_member:
        return jsonify(updated_member), 200
    return jsonify({"message": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

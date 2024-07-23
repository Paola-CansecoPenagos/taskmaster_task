from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from utils.jwt_utils import decode_access_token

client = MongoClient("mongodb://localhost:27017/")
db_not = client["taskMasterNot"]
notifications_collection = db_not["notifications"]

notifications_blueprint = Blueprint('notifications', __name__)

@notifications_blueprint.route('/notifications', methods=['GET'])
def get_notifications():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        return jsonify({"error": "Authorization header is missing"}), 401

    token = auth_header.split(" ")[1]  # Assuming the header is in the format "Bearer <token>"

    try:
        decoded_token = decode_access_token(token)
        if decoded_token is None:
            return jsonify({"error": "Invalid or expired token"}), 401
        user_id = decoded_token['user_id']
        print(f"User ID: {user_id}")  # Print user ID to console
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    notifications = list(notifications_collection.find({"user_id": user_id}))
    for notification in notifications:
        notification["_id"] = str(notification["_id"])  # Convert ObjectId to string

    return jsonify(notifications), 200

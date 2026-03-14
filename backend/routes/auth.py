from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data     = request.get_json()
        username = data.get('username', '').strip()
        email    = data.get('email', '').strip()
        password = data.get('password', '')

        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400

        user = User(
            username      = username,
            email         = email,
            password_hash = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data     = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()
        user    = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
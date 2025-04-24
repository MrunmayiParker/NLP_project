from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter((User.email == data['email']) | (User.username == data['username'])).first():
        return jsonify({"message": "User already exists"}), 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
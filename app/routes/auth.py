from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from app.models.user import User
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not email or not password:
                return jsonify({"message": "All fields are required"}), 400

            if User.query.filter((User.username == username) | (User.email == email)).first():
                return jsonify({"message": "User already exists"}), 409

            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            return jsonify({"message": "User registered successfully!"}), 201  # ✅ respond with JSON

        return jsonify({"message": "Request must be JSON"}), 400

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            login_user(user, remember=True) #change
            if request.is_json:
                return jsonify({"message": "Logged in successfully!"}), 200
            else:
                return redirect(url_for('home.homepage'))  # (after login redirect)

        if request.is_json:
            return jsonify({"message": "Invalid credentials"}), 401
        else:
            return render_template("login.html", message="Invalid credentials.")

    return render_template("login.html")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

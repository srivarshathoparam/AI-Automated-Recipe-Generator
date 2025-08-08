from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from models import db, User  # Import db & User model from models.py

# ✅ Create Blueprint
login_blueprint = Blueprint("login", __name__)

# ✅ Authentication Decorator (For Protected Routes)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = token.split("Bearer ")[1]  # Extract token if prefixed with 'Bearer '
            decoded_data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(decoded_data['user_id'])

            if not current_user:
                return jsonify({"error": "User not found!"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return f(current_user, *args, **kwargs)

    return decorated

# ✅ Register User
@login_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Username, email, and password are required!"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered!"}), 409

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# ✅ Login & Get JWT Token
@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Email and password are required!"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            current_app.config['SECRET_KEY'], algorithm="HS256"
        )
        return jsonify({"message": "Login successful!", "token": f"Bearer {token}"})

    return jsonify({"error": "Invalid email or password!"}), 401

# ✅ Get Profile (Protected)
@login_blueprint.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        "username": current_user.username,
        "email": current_user.email
    })

# ✅ Update Password (Protected)
@login_blueprint.route('/update-password', methods=['PUT'])
@token_required
def update_password(current_user):
    data = request.get_json()

    if not data or 'password' not in data:
        return jsonify({"error": "New password is required!"}), 400

    current_user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"})

# ✅ Delete Account (Protected)
@login_blueprint.route('/delete-account', methods=['DELETE'])
@token_required
def delete_account(current_user):
    db.session.delete(current_user)
    db.session.commit()

    return jsonify({"message": "User account deleted successfully!"})

@login_blueprint.route('/logout', methods=['POST'])
def logout():
    # This can be just a frontend-assisted logout. Server-side token blacklisting is optional.
    return jsonify({"message": "Logged out successfully!"}), 200

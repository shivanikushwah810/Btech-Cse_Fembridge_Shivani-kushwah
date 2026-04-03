"""
FemBridge - Authentication Routes
Handles user registration and login
"""

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db_setup import get_connection

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registers a new user."""
    data = request.get_json()

    name     = data.get('name', '').strip()
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')
    skills   = data.get('skills', '').strip()
    location = data.get('location', '').strip()

    # Basic validation
    if not name or not email or not password:
        return jsonify({"success": False, "message": "Name, email, and password are required."}), 400

    hashed_pw = generate_password_hash(password)

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password, skills, location) VALUES (?,?,?,?,?)",
            (name, email, hashed_pw, skills, location)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Registration successful! Please login."}), 201
    except Exception:
        return jsonify({"success": False, "message": "Email already registered."}), 409
    finally:
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    """Logs in a user and creates a session."""
    data = request.get_json()

    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    # Store user info in session
    session['user_id'] = user['id']
    session['user_name'] = user['name']

    return jsonify({
        "success": True,
        "message": f"Welcome back, {user['name']}!",
        "user": {
            "id":       user['id'],
            "name":     user['name'],
            "email":    user['email'],
            "skills":   user['skills'],
            "location": user['location']
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clears the user session."""
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@auth_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    """Gets or updates the current user's profile."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Not logged in."}), 401

    conn = get_connection()

    if request.method == 'GET':
        user = conn.execute("SELECT id, name, email, skills, location FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404
        return jsonify({"success": True, "user": dict(user)})

    # PUT - update profile
    data     = request.get_json()
    skills   = data.get('skills', '').strip()
    location = data.get('location', '').strip()
    name     = data.get('name', '').strip()

    conn.execute(
        "UPDATE users SET name=?, skills=?, location=? WHERE id=?",
        (name, skills, location, user_id)
    )
    conn.commit()
    conn.close()
    session['user_name'] = name
    return jsonify({"success": True, "message": "Profile updated successfully."})
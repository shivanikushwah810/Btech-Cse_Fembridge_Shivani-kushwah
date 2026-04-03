"""
FemBridge - Main Flask Application
Entry point for the backend server
"""

import os
from flask import Flask, jsonify, session, request
from flask_cors import CORS

# ── Import Blueprints ─────────────────────────────────────────────────────────
from routes.auth         import auth_bp
from routes.jobs         import jobs_bp
from routes.applications import applications_bp
from routes.ai           import ai_bp
from routes.chatbot      import chatbot_bp

# ── Import DB initializer ─────────────────────────────────────────────────────
from models.db_setup import init_db, get_connection
from utils.resume_parser import analyze_resume

# ── App Factory ───────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "fembridge_secret_key_2024"  # Change in production

# Allow cross-origin requests from the frontend
CORS(app, supports_credentials=True, origins=["*"])

# ── Register Blueprints ───────────────────────────────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(chatbot_bp)


# ── Resume Upload Endpoint ────────────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/resume', methods=['POST'])
def upload_resume():
    """Handles resume upload and analysis."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login first."}), 401

    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No file uploaded."}), 400

    file = request.files['resume']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Invalid file. Please upload .txt, .pdf, or .docx"}), 400

    # Save file temporarily
    filepath = os.path.join(UPLOAD_FOLDER, f"user_{user_id}_resume{os.path.splitext(file.filename)[1]}")
    file.save(filepath)

    # Analyze
    result = analyze_resume(filepath)

    # Store result in database
    conn = get_connection()
    conn.execute("""
        INSERT INTO resume (user_id, score, suggestions)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET score=excluded.score, suggestions=excluded.suggestions
    """, (user_id, result['score'], "; ".join(result['suggestions'])))
    conn.commit()
    conn.close()

    return jsonify({"success": True, **result})


@app.route('/resume/score', methods=['GET'])
def get_resume_score():
    """Returns the stored resume score for the current user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login."}), 401

    conn = get_connection()
    rec  = conn.execute("SELECT * FROM resume WHERE user_id=?", (user_id,)).fetchone()
    conn.close()

    if not rec:
        return jsonify({"success": True, "score": 0, "suggestions": [], "has_resume": False})

    return jsonify({
        "success":     True,
        "score":       rec['score'],
        "suggestions": rec['suggestions'].split("; ") if rec['suggestions'] else [],
        "has_resume":  True
    })


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Returns aggregated dashboard data for the current user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login."}), 401

    conn = get_connection()

    # Applied jobs count
    app_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM applications WHERE user_id=?", (user_id,)
    ).fetchone()['cnt']

    # Resume score
    resume_row = conn.execute(
        "SELECT score FROM resume WHERE user_id=?", (user_id,)
    ).fetchone()
    resume_score = resume_row['score'] if resume_row else 0

    # Total jobs available
    total_jobs = conn.execute("SELECT COUNT(*) as cnt FROM jobs").fetchone()['cnt']

    conn.close()

    return jsonify({
        "success":       True,
        "applied_count": app_count,
        "resume_score":  resume_score,
        "total_jobs":    total_jobs,
        "user_name":     session.get('user_name', 'User')
    })


# ── Health Check ──────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "FemBridge API is running 🌸", "version": "1.0"})


# ── Initialize DB and Start Server ───────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("🌸 FemBridge Backend Starting on http://localhost:5000")
    app.run(debug=True, port=5000)
"""
FemBridge - Jobs Routes
Handles job listing, filtering, and applications
"""

from flask import Blueprint, request, jsonify, session
from models.db_setup import get_connection

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """
    Returns all jobs. Optionally filters by:
    - location (query param)
    - type (query param: Full-time / Part-time)
    - search (query param: keyword in title or company)
    Always includes Remote jobs when location filter is active.
    """
    location_filter = request.args.get('location', '').strip()
    type_filter     = request.args.get('type', '').strip()
    search_query    = request.args.get('search', '').strip().lower()

    conn   = get_connection()
    query  = "SELECT * FROM jobs WHERE 1=1"
    params = []

    # Location filter: show user's city + Remote jobs
    if location_filter:
        query += " AND (LOWER(location) = ? OR LOWER(location) = 'remote')"
        params.append(location_filter.lower())

    # Type filter
    if type_filter:
        query += " AND LOWER(type) = ?"
        params.append(type_filter.lower())

    # Keyword search in title or company
    if search_query:
        query += " AND (LOWER(title) LIKE ? OR LOWER(company) LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    jobs = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify({"success": True, "jobs": [dict(j) for j in jobs]})


@jobs_bp.route('/apply', methods=['POST'])
def apply_job():
    """Applies the logged-in user to a job."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login to apply."}), 401

    data   = request.get_json()
    job_id = data.get('job_id')

    if not job_id:
        return jsonify({"success": False, "message": "Job ID is required."}), 400

    conn = get_connection()

    # Check if already applied
    existing = conn.execute(
        "SELECT id FROM applications WHERE user_id=? AND job_id=?", (user_id, job_id)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({"success": False, "message": "You have already applied for this job."}), 409

    conn.execute(
        "INSERT INTO applications (user_id, job_id, status) VALUES (?,?,'Pending')",
        (user_id, job_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Application submitted successfully! 🎉"})


@jobs_bp.route('/my-applications', methods=['GET'])
def my_applications():
    """Returns all job applications for the logged-in user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login."}), 401

    conn = get_connection()
    apps = conn.execute("""
        SELECT a.id, a.status, j.title, j.company, j.location, j.type, j.salary
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        WHERE a.user_id = ?
        ORDER BY a.id DESC
    """, (user_id,)).fetchall()
    conn.close()

    return jsonify({"success": True, "applications": [dict(a) for a in apps]})
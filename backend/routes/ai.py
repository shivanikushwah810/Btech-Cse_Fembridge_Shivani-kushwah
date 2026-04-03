"""
FemBridge - AI Routes
Job recommendation based on user skills (NLP keyword matching)
"""

from flask import Blueprint, jsonify, session
from models.db_setup import get_connection
from utils.recommender import recommend_jobs

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/recommend', methods=['GET'])
def recommend():
    """
    Returns AI-recommended jobs based on the user's skill set.
    Uses keyword matching between user skills and job descriptions.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please login to get recommendations."}), 401

    conn = get_connection()
    user = conn.execute("SELECT skills, location FROM users WHERE id = ?", (user_id,)).fetchone()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()

    if not user or not user['skills']:
        return jsonify({
            "success": False,
            "message": "Please update your profile with your skills to get recommendations."
        })

    ranked = recommend_jobs(user['skills'], [dict(j) for j in jobs])

    return jsonify({
        "success": True,
        "recommendations": ranked,
        "skills_used": user['skills']
    })
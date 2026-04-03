"""
FemBridge - Applications Routes
Dedicated route file for application management
(core logic lives in jobs.py; this file exposes status updates)
"""

from flask import Blueprint, request, jsonify, session
from models.db_setup import get_connection

applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/applications/status', methods=['PUT'])
def update_status():
    """Updates the status of an application (admin/employer use)."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized."}), 401

    data   = request.get_json()
    app_id = data.get('application_id')
    status = data.get('status')

    valid_statuses = ['Pending', 'Reviewed', 'Shortlisted', 'Rejected']
    if status not in valid_statuses:
        return jsonify({"success": False, "message": f"Invalid status. Choose from: {valid_statuses}"}), 400

    conn = get_connection()
    conn.execute("UPDATE applications SET status=? WHERE id=?", (status, app_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"Application status updated to '{status}'."})
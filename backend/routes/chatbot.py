"""
FemBridge - Chatbot Routes
Rule-based chatbot for user assistance
"""

from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)

# ── Rule-based response map ───────────────────────────────────────────────────
RULES = [
    (["hello", "hi", "hey", "namaste"],
     "👋 Hello! Welcome to FemBridge! I'm here to help you find your dream job. How can I assist you?"),

    (["apply", "application", "how to apply"],
     "📝 To apply for a job: Go to the Jobs page → Find a job you like → Click the 'Apply Now' button. It's that simple!"),

    (["recommend", "recommendation", "suggest", "suggestion"],
     "🤖 Our AI recommends jobs based on your skills! Update your skills in your Profile, then click 'Get Recommendations' on the Dashboard."),

    (["resume", "cv", "upload"],
     "📄 Upload your resume on the Profile page. Our AI will analyze it and give you a score plus improvement tips!"),

    (["register", "sign up", "create account"],
     "✅ Click 'Register' on the top menu. Fill in your name, email, password, skills, and location. It's free!"),

    (["login", "sign in", "log in"],
     "🔐 Click 'Login' on the top menu and enter your email and password."),

    (["job", "jobs", "listing", "openings", "vacancy"],
     "💼 Browse all available jobs on the Jobs page. You can filter by location and job type!"),

    (["location", "remote", "city"],
     "📍 FemBridge shows jobs in your city AND remote jobs automatically. Update your location in your Profile."),

    (["dashboard", "home", "portal"],
     "🏠 Your Dashboard shows your applied jobs, AI recommendations, and resume score all in one place!"),

    (["profile", "update", "edit", "skills"],
     "👤 Go to your Profile to update your name, skills, and location. Adding skills improves your job recommendations!"),

    (["salary", "pay", "compensation"],
     "💰 Each job listing shows the salary range. Browse the Jobs page to compare compensation packages."),

    (["help", "support", "assist"],
     "🆘 I'm here to help! You can ask me about: applying for jobs, recommendations, resume upload, profile setup, or anything about FemBridge."),

    (["thank", "thanks", "great", "awesome"],
     "🌸 You're welcome! FemBridge is rooting for you. Best of luck with your job search! 💪"),

    (["bye", "goodbye", "exit", "quit"],
     "👋 Goodbye! Come back anytime. FemBridge is always here for you! 🌸"),
]


def get_bot_response(message: str) -> str:
    """
    Matches user message against rules and returns the appropriate response.
    Falls back to a default message if no rule matches.
    """
    msg_lower = message.lower().strip()

    for keywords, response in RULES:
        if any(kw in msg_lower for kw in keywords):
            return response

    # Default fallback
    return (
        "🤔 I'm not sure about that. Try asking me about: "
        "job applications, AI recommendations, resume upload, "
        "your profile, or how to navigate FemBridge!"
    )


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Processes a chat message and returns a bot response."""
    data    = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"success": False, "message": "Please enter a message."}), 400

    response = get_bot_response(message)
    return jsonify({"success": True, "response": response})
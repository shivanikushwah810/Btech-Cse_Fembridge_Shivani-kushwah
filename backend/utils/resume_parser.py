"""
FemBridge - Resume Parser & Analyzer
Extracts text from uploaded resume files and calculates a match score
"""

import re
import os

# Keywords that make a strong resume
STRONG_KEYWORDS = [
    # Technical
    "python", "java", "javascript", "sql", "html", "css", "react", "flask",
    "django", "machine learning", "data analysis", "tensorflow", "pytorch",
    "aws", "docker", "git", "api", "rest", "microservices",
    # Soft / professional
    "leadership", "communication", "teamwork", "management", "agile",
    "scrum", "problem solving", "analytical", "creative",
    # Resume sections
    "experience", "education", "projects", "achievements", "certifications",
    "internship", "volunteer", "skills", "summary", "objective"
]

SECTION_KEYWORDS = ["experience", "education", "skills", "projects", "certifications", "achievements"]


def extract_text_from_file(filepath: str) -> str:
    """
    Extracts plain text from a resume file.
    Supports: .txt, .pdf (basic), .docx (basic)
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.txt':
        with open(filepath, 'r', errors='ignore') as f:
            return f.read()

    elif ext == '.pdf':
        try:
            import PyPDF2
            text = ""
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            return f"PDF parsing error: {e}"

    elif ext in ['.doc', '.docx']:
        try:
            import docx
            doc  = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"DOCX parsing error: {e}"

    return ""


def analyze_resume(filepath: str) -> dict:
    """
    Analyzes a resume file and returns:
    - score (0–100)
    - list of matched keywords
    - improvement suggestions
    """
    text = extract_text_from_file(filepath).lower()

    if not text or "error" in text[:20]:
        return {
            "score": 0,
            "suggestions": ["Could not read file. Please upload a .txt, .pdf, or .docx file."],
            "matched_keywords": []
        }

    # Count keyword matches
    matched = [kw for kw in STRONG_KEYWORDS if kw in text]
    base_score = min(len(matched) * 3, 70)  # max 70 from keywords

    # Bonus points for having proper sections
    section_bonus = sum(5 for sec in SECTION_KEYWORDS if sec in text)
    section_bonus = min(section_bonus, 20)

    # Bonus for length (longer resume = more detail)
    word_count   = len(text.split())
    length_bonus = min(int(word_count / 50), 10)

    score = min(base_score + section_bonus + length_bonus, 100)

    # ── Generate suggestions ──────────────────────────────────────────────────
    suggestions = []

    if score < 40:
        suggestions.append("Your resume needs significant improvement. Add more relevant skills and experience details.")
    elif score < 70:
        suggestions.append("Good start! Adding more technical keywords will improve visibility.")
    else:
        suggestions.append("Excellent resume! You have strong keyword coverage.")

    missing_sections = [sec for sec in SECTION_KEYWORDS if sec not in text]
    if missing_sections:
        suggestions.append(f"Add these sections: {', '.join(missing_sections).title()}.")

    if word_count < 200:
        suggestions.append("Your resume seems short. Add more detail about your experience and projects.")

    if "objective" not in text and "summary" not in text:
        suggestions.append("Add a professional summary/objective at the top of your resume.")

    if len(matched) < 5:
        suggestions.append("Include more technical skills relevant to your target roles.")

    if not suggestions:
        suggestions.append("Great resume! Keep it updated with your latest projects.")

    return {
        "score":            score,
        "suggestions":      suggestions,
        "matched_keywords": matched,
        "word_count":       word_count
    }
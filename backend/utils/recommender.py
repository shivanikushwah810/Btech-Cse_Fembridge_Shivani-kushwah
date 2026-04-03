"""
FemBridge - AI Job Recommender
Keyword-based skill matching between user skills and job descriptions
"""

import re
from typing import List, Dict


def tokenize(text: str) -> List[str]:
    """Splits text into lowercase word tokens."""
    return re.findall(r'\b[a-z]+\b', text.lower())


def recommend_jobs(user_skills: str, jobs: List[Dict], top_n: int = 6) -> List[Dict]:
    """
    Scores each job by counting how many of the user's skills
    appear in the job description / title, then returns the top N.

    Algorithm:
    - Extract skill tokens from user profile
    - For each job, count token matches in description + title
    - Compute a 0–100 match score
    - Sort descending and return top_n results
    """
    skill_tokens = set(tokenize(user_skills))

    if not skill_tokens:
        return jobs[:top_n]  # No skills → return first N jobs

    scored_jobs = []

    for job in jobs:
        job_text   = f"{job.get('title', '')} {job.get('description', '')}".lower()
        job_tokens = set(tokenize(job_text))

        # Count matching skills
        matches    = skill_tokens & job_tokens
        match_count = len(matches)

        # Normalise to 0–100 (cap at 100)
        score = min(int((match_count / max(len(skill_tokens), 1)) * 100), 100)

        if match_count > 0:
            job_copy = dict(job)
            job_copy['match_score']    = score
            job_copy['matched_skills'] = sorted(matches)
            scored_jobs.append(job_copy)

    # Sort by match score descending
    scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)

    return scored_jobs[:top_n]
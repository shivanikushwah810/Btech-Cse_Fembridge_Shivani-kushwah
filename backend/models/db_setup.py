"""
FemBridge - Database Setup
Creates all tables for the application
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'fembridge.db')


def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dict-style access
    return conn


def init_db():
    """Initializes the database with all required tables and sample data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # ── USERS TABLE ──────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            skills   TEXT    DEFAULT '',
            location TEXT    DEFAULT ''
        )
    """)

    # ── JOBS TABLE ────────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            company     TEXT NOT NULL,
            location    TEXT NOT NULL,
            type        TEXT DEFAULT 'Full-time',
            salary      TEXT DEFAULT 'Competitive',
            description TEXT DEFAULT ''
        )
    """)

    # ── APPLICATIONS TABLE ────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_id  INTEGER NOT NULL,
            status  TEXT    DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (job_id)  REFERENCES jobs(id)
        )
    """)

    # ── RESUME TABLE ──────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL UNIQUE,
            score       INTEGER DEFAULT 0,
            suggestions TEXT    DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ── SEED SAMPLE JOBS ──────────────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        sample_jobs = [
            ("Python Developer", "TechCorp", "Mumbai", "Full-time", "₹8-12 LPA",
             "python flask django sql machine learning data analysis backend development"),
            ("Frontend Developer", "WebWorks", "Bangalore", "Full-time", "₹6-10 LPA",
             "html css javascript react bootstrap responsive design ui ux frontend"),
            ("Data Analyst", "DataHub", "Remote", "Full-time", "₹7-11 LPA",
             "python sql data analysis excel tableau machine learning statistics"),
            ("UX Designer", "DesignCo", "Delhi", "Part-time", "₹4-8 LPA",
             "figma ui ux design wireframing prototyping adobe xd user research"),
            ("HR Manager", "PeopleFirst", "Hyderabad", "Full-time", "₹6-9 LPA",
             "human resources recruitment management communication leadership excel"),
            ("Machine Learning Engineer", "AI Labs", "Remote", "Full-time", "₹15-25 LPA",
             "python machine learning deep learning tensorflow pytorch nlp data science"),
            ("Content Writer", "MediaHouse", "Pune", "Part-time", "₹3-5 LPA",
             "writing content seo blogging communication english creative copywriting"),
            ("Digital Marketing", "GrowthCo", "Mumbai", "Full-time", "₹5-8 LPA",
             "digital marketing seo sem google ads social media analytics communication"),
            ("Java Developer", "SoftSol", "Chennai", "Full-time", "₹9-14 LPA",
             "java spring boot microservices sql rest api backend development"),
            ("Product Manager", "ProductLab", "Bangalore", "Full-time", "₹18-30 LPA",
             "product management agile scrum leadership communication analytics strategy"),
        ]
        cursor.executemany(
            "INSERT INTO jobs (title, company, location, type, salary, description) VALUES (?,?,?,?,?,?)",
            sample_jobs
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")


if __name__ == "__main__":
    init_db()
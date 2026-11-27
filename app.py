
import os
import sqlite3
import uuid
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, abort, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


# ==========================================
# 1. FLASK APPLICATION CONFIGURATION
# ==========================================



app = Flask(__name__)

APP_ENV = os.environ.get("APP_ENV", "development").lower()
SECRET_KEY = os.environ.get("SECRET_KEY")

if APP_ENV == "production" and not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY must be configured before production deployment."
    )

app.config["SECRET_KEY"] = SECRET_KEY or (
    "skillbridge-development-key-change-before-deployment"
)


# ==========================================
# DATABASE AND FILE STORAGE CONFIGURATION
# ==========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database storage
DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(app.instance_path, "skillbridge.db")
)

os.makedirs(os.path.dirname(os.path.abspath(DATABASE_PATH)), exist_ok=True)

app.config["DATABASE"] = DATABASE_PATH

# Certificate upload storage
UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER",
    os.path.join(BASE_DIR, "static", "uploads")
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed certificate file types
ALLOWED_EXTENSIONS = {"pdf"}

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# ==========================================
# 2. DATABASE CONNECTION
# ==========================================


def get_db():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row

    # Enforce database foreign-key relationships
    connection.execute("PRAGMA foreign_keys = ON")

    return connection



# ==========================================
# 3. CREATE DATABASE TABLES
# ==========================================

def init_db():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            country TEXT NOT NULL,
            location TEXT NOT NULL,
            professional_field TEXT NOT NULL,
            qualification TEXT NOT NULL,
            experience TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            career_goals TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # Add administrator role support

    user_columns = [
        column["name"]
        for column in connection.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    if "role" not in user_columns:
        connection.execute("""
            ALTER TABLE users
            ADD COLUMN role TEXT NOT NULL DEFAULT 'user'
        """)


    connection.execute("""
        CREATE TABLE IF NOT EXISTS qualifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            qualification_name TEXT NOT NULL,
            institution TEXT NOT NULL,
            year_obtained INTEGER NOT NULL,
            certificate_filename TEXT NOT NULL,
            verification_status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

        # ==========================================
    # QUALIFICATION REVIEW FIELD MIGRATION
    # ==========================================

    qualification_columns = [
        column["name"]
        for column in connection.execute(
            "PRAGMA table_info(qualifications)"
        ).fetchall()
    ]

    new_qualification_columns = {
        "reviewer_notes": "TEXT DEFAULT ''",
        "reviewed_at": "TEXT"
    }

    for column, data_type in new_qualification_columns.items():
        if column not in qualification_columns:
            connection.execute(
                f"ALTER TABLE qualifications ADD COLUMN {column} {data_type}"
            )


    # ==========================================
    # CERTIFICATE VERIFICATION HISTORY
    # ==========================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS certificate_verification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            qualification_id INTEGER NOT NULL,

            admin_id INTEGER NOT NULL,

            verification_status TEXT NOT NULL
                CHECK (
                    verification_status IN ('Verified', 'Rejected')
                ),

            decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (qualification_id)
                REFERENCES qualifications(id),

            FOREIGN KEY (admin_id)
                REFERENCES users(id)
        )
    """)

        # ==========================================
    # CERTIFICATE AUDIT HISTORY FIELD MIGRATION
    # ==========================================

    history_columns = [
        column["name"]
        for column in connection.execute(
            "PRAGMA table_info(certificate_verification_history)"
        ).fetchall()
    ]

    new_history_columns = {
        "previous_status": "TEXT",
        "reviewer_notes": "TEXT DEFAULT ''"
    }

    for column, data_type in new_history_columns.items():
        if column not in history_columns:
            connection.execute(
                f"ALTER TABLE certificate_verification_history "
                f"ADD COLUMN {column} {data_type}"
            )


    connection.execute("""
        CREATE TABLE IF NOT EXISTS mentorship_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            professional_field TEXT NOT NULL,
            mentorship_area TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()

 # Initialize database tables when the application starts
init_db()   


# ==========================================
# 4. USER AUTHENTICATION DECORATOR
# ==========================================

def login_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return wrapper

# ==========================================
# ADMINISTRATOR ACCESS DECORATOR
# ==========================================

def admin_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))

        connection = get_db()

        user = connection.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        connection.close()

        if user is None or user["role"] != "admin":
            abort(403)

        return route_function(*args, **kwargs)

    return wrapper

# ==========================================
# 5. HELPER FUNCTION TO GET CURRENT USER
# ==========================================

def get_current_user():

    if "user_id" not in session:
        return None

    connection = get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    connection.close()

    return user


# ==========================================
# 6. CHECK ALLOWED FILE TYPES
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================================
# 7. HOMEPAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# 8. USER REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        country = request.form.get("country", "").strip()
        location = request.form.get("location", "").strip()
        professional_field = request.form.get(
            "professional_field", ""
        ).strip()
        qualification = request.form.get(
            "qualification", ""
        ).strip()

        if not all([
            full_name, email, password, country,
            location, professional_field, qualification
        ]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        connection = get_db()

        try:

            connection.execute("""
                INSERT INTO users (
                    full_name, email, password, country,
                    location, professional_field, qualification
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                full_name, email, hashed_password, country,
                location, professional_field, qualification
            ))

            connection.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash("This email address is already registered.", "error")

        finally:
            connection.close()

    return render_template("register.html")


# ==========================================
# 9. USER LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_db()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            flash("Welcome to SkillBridge!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email address or password.", "error")

    return render_template("login.html")


# ==========================================
# 10. USER LOGOUT
# ==========================================

@app.route("/logout")
@login_required
def logout():

    session.clear()

    flash("You have successfully logged out.", "success")

    return redirect(url_for("home"))


# ==========================================
# 11. USER DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    connection = get_db()

    qualifications_count = connection.execute(
        "SELECT COUNT(*) FROM qualifications WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    mentorship_count = connection.execute(
        "SELECT COUNT(*) FROM mentorship_requests WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        qualifications_count=qualifications_count,
        mentorship_count=mentorship_count
    )


# ==========================================
# 12. PROFESSIONAL PROFILE
# ==========================================

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    connection = get_db()

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        professional_field = request.form.get(
            "professional_field", ""
        ).strip()
        qualification = request.form.get(
            "qualification", ""
        ).strip()
        experience = request.form.get("experience", "").strip()
        skills = request.form.get("skills", "").strip()
        career_goals = request.form.get("career_goals", "").strip()

        if not full_name:
            connection.close()
            flash("Full name is required.", "error")
            return redirect(url_for("profile"))

        connection.execute("""
            UPDATE users
            SET full_name = ?,
                professional_field = ?,
                qualification = ?,
                experience = ?,
                skills = ?,
                career_goals = ?
            WHERE id = ?
        """, (
            full_name, professional_field, qualification,
            experience, skills, career_goals,
            session["user_id"]
        ))

        connection.commit()

        session["user_name"] = full_name

        connection.close()

        flash("Your professional profile has been updated.", "success")

        return redirect(url_for("profile"))

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    connection.close()

    return render_template("profile.html", user=user)


# ==========================================
# CERTIFICATE DOWNLOAD
# ==========================================

@app.route("/certificates/<int:qualification_id>")
@login_required
def view_certificate(qualification_id):

    connection = get_db()

    certificate = connection.execute("""
        SELECT certificate_filename
        FROM qualifications
        WHERE id = ? AND user_id = ?
    """, (
        qualification_id,
        session["user_id"]
    )).fetchone()

    connection.close()

    if certificate is None:
        abort(404)

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        certificate["certificate_filename"],
        as_attachment=True
    )



# ==========================================
# ADMINISTRATOR CERTIFICATE DASHBOARD
# SEARCH AND FILTER
# ==========================================

@app.route("/admin/certificates")
@admin_required
def admin_certificates():

    search_query = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()

    connection = get_db()

    # Base query
    query = """
        SELECT
            qualifications.*,
            users.full_name,
            users.email
        FROM qualifications
        JOIN users
            ON qualifications.user_id = users.id
        WHERE 1 = 1
    """

    parameters = []

    # Search applicant, email, qualification or institution
    if search_query:
        query += """
            AND (
                users.full_name LIKE ?
                OR users.email LIKE ?
                OR qualifications.qualification_name LIKE ?
                OR qualifications.institution LIKE ?
            )
        """

        search_pattern = f"%{search_query}%"

        parameters.extend([
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        ])

    # Filter by verification status
    if status_filter in ["Pending", "Verified", "Rejected"]:
        query += """
            AND qualifications.verification_status = ?
        """
        parameters.append(status_filter)

    query += """
        ORDER BY qualifications.created_at DESC
    """

    qualifications = connection.execute(
        query,
        parameters
    ).fetchall()

    # Certificate statistics (independent of filters)
    statistics = connection.execute("""
        SELECT
            COUNT(*) AS total,

            COALESCE(SUM(
                CASE
                    WHEN verification_status = 'Pending'
                    THEN 1 ELSE 0
                END
            ), 0) AS pending,

            COALESCE(SUM(
                CASE
                    WHEN verification_status = 'Verified'
                    THEN 1 ELSE 0
                END
            ), 0) AS verified,

            COALESCE(SUM(
                CASE
                    WHEN verification_status = 'Rejected'
                    THEN 1 ELSE 0
                END
            ), 0) AS rejected

        FROM qualifications
    """).fetchone()

    connection.close()

    return render_template(
        "admin_certificates.html",
        qualifications=qualifications,
        statistics=statistics,
        search_query=search_query,
        status_filter=status_filter
    )


# ==========================================
# ADMINISTRATOR CERTIFICATE DOWNLOAD
# ==========================================

@app.route("/admin/certificates/<int:qualification_id>/download")
@admin_required
def admin_view_certificate(qualification_id):

    connection = get_db()

    certificate = connection.execute("""
        SELECT certificate_filename
        FROM qualifications
        WHERE id = ?
    """, (qualification_id,)).fetchone()

    connection.close()

    if certificate is None:
        abort(404)

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        certificate["certificate_filename"],
        as_attachment=True
    )


# ==========================================
# UPDATE CERTIFICATE STATUS, REVIEW NOTES
# AND AUDIT HISTORY
# ==========================================

@app.route(
    "/admin/certificates/<int:qualification_id>/verify",
    methods=["POST"]
)
@admin_required
def update_certificate_status(qualification_id):

    status = request.form.get(
        "verification_status", ""
    ).strip()

    reviewer_notes = request.form.get(
        "reviewer_notes", ""
    ).strip()

    # Accept only valid verification decisions
    if status not in ["Verified", "Rejected"]:
        flash("Invalid verification status.", "error")
        return redirect(url_for("admin_certificates"))

    connection = get_db()

    try:
        # Retrieve the existing certificate status
        certificate = connection.execute("""
            SELECT id, verification_status
            FROM qualifications
            WHERE id = ?
        """, (qualification_id,)).fetchone()

        if certificate is None:
            abort(404)

        previous_status = certificate["verification_status"]

        # Update qualification status and reviewer feedback
        connection.execute("""
            UPDATE qualifications
            SET verification_status = ?,
                reviewer_notes = ?,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            status,
            reviewer_notes,
            qualification_id
        ))

        # Record the complete audit history
        connection.execute("""
            INSERT INTO certificate_verification_history (
                qualification_id,
                admin_id,
                verification_status,
                previous_status,
                reviewer_notes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            qualification_id,
            session["user_id"],
            status,
            previous_status,
            reviewer_notes
        ))

        # Save both operations together
        connection.commit()

        flash(
            f"Certificate successfully marked as {status}.",
            "success"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("admin_certificates"))


# ==========================================
# ADMINISTRATOR CERTIFICATE VERIFICATION HISTORY
# ==========================================

@app.route("/admin/certificates/history")
@admin_required
def certificate_verification_history():

    connection = get_db()

    history = connection.execute("""
        SELECT
            certificate_verification_history.id,
            certificate_verification_history.qualification_id,
            certificate_verification_history.verification_status,
            certificate_verification_history.decided_at,

            qualifications.qualification_name,
            qualifications.institution,

            users.full_name AS applicant_name,
            admins.full_name AS admin_name

        FROM certificate_verification_history

        JOIN qualifications
            ON certificate_verification_history.qualification_id =
               qualifications.id

        JOIN users
            ON qualifications.user_id = users.id

        JOIN users AS admins
            ON certificate_verification_history.admin_id = admins.id

        ORDER BY certificate_verification_history.decided_at DESC
    """).fetchall()

    connection.close()

    return render_template(
        "admin_certificate_history.html",
        history=history
    )



# ==========================================
# 13. CREDENTIAL RECOGNITION AND SKILLS
# ==========================================

@app.route("/skills", methods=["GET", "POST"])
@login_required
def skills():

    if request.method == "POST":

        qualification_name = request.form.get(
            "qualification_name", ""
        ).strip()

        institution = request.form.get(
            "institution", ""
        ).strip()

        year_obtained = request.form.get(
            "year_obtained", ""
        ).strip()

        certificate = request.files.get("certificate")

        if not all([
            qualification_name,
            institution,
            year_obtained,
            certificate
        ]):
            flash("Please complete all qualification fields.", "error")
            return redirect(url_for("skills"))

        if not year_obtained.isdigit():
            flash("Please enter a valid qualification year.", "error")
            return redirect(url_for("skills"))

        if not 1950 <= int(year_obtained) <= 2100:
            flash("Please enter a year between 1950 and 2100.", "error")
            return redirect(url_for("skills"))

        if certificate.filename == "":
            flash("Please select a certificate to upload.", "error")
            return redirect(url_for("skills"))

        if not allowed_file(certificate.filename):
            flash("Only PDF certificates are accepted.", "error")
            return redirect(url_for("skills"))

        original_name = secure_filename(certificate.filename)

        if not original_name:
            flash("Invalid filename.", "error")
            return redirect(url_for("skills"))

        unique_name = f"{uuid.uuid4().hex}_{original_name}"

        save_path = os.path.join(
            app.config["UPLOAD_FOLDER"], unique_name
        )

        try:
            certificate.save(save_path)

            connection = get_db()

            connection.execute("""
                INSERT INTO qualifications (
                    user_id, qualification_name, institution,
                    year_obtained, certificate_filename
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                qualification_name,
                institution,
                int(year_obtained),
                unique_name
            ))

            connection.commit()
            connection.close()

            flash(
                "Your qualification has been submitted for review.",
                "success"
            )

        except Exception:
            if os.path.exists(save_path):
                os.remove(save_path)

            flash("Unable to save your qualification. Please try again.", "error")

        return redirect(url_for("skills"))

    return render_template("skills.html")


# ==========================================
# 14. EMPLOYMENT OPPORTUNITIES
# ==========================================

@app.route("/opportunities")
def opportunities():

    opportunities_list = [
        {
            "title": "Junior Software Developer",
            "field": "Information Technology",
            "type": "Full-time",
            "description": "An opportunity to develop and maintain software applications."
        },
        {
            "title": "IT Support Assistant",
            "field": "Information Technology",
            "type": "Internship",
            "description": "Gain practical experience in technical support."
        },
        {
            "title": "Education Assistant",
            "field": "Education",
            "type": "Full-time",
            "description": "Support teaching, learning and educational activities."
        },
        {
            "title": "Healthcare Support",
            "field": "Healthcare",
            "type": "Full-time",
            "description": "Explore healthcare support and development opportunities."
        },
        {
            "title": "Remote Business Assistant",
            "field": "Business",
            "type": "Remote",
            "description": "Support business administration and remote operations."
        },
        {
            "title": "Engineering Intern",
            "field": "Engineering",
            "type": "Internship",
            "description": "Gain practical engineering experience."
        }
    ]

    selected_field = request.args.get("field", "").strip()
    selected_type = request.args.get("type", "").strip()

    filtered_opportunities = [
        opportunity for opportunity in opportunities_list
        if (not selected_field or opportunity["field"] == selected_field)
        and (not selected_type or opportunity["type"] == selected_type)
    ]

    return render_template(
        "opportunities.html",
        opportunities=filtered_opportunities
    )


# ==========================================
# 15. PROFESSIONAL MENTORSHIP
# ==========================================

@app.route("/mentorship", methods=["GET", "POST"])
@login_required
def mentorship():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        professional_field = request.form.get(
            "professional_field", ""
        ).strip()
        mentorship_area = request.form.get(
            "mentorship_area", ""
        ).strip()
        message = request.form.get("message", "").strip()

        if not all([
            full_name, email, professional_field, mentorship_area
        ]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("mentorship"))

        connection = get_db()

        connection.execute("""
            INSERT INTO mentorship_requests (
                user_id, full_name, email,
                professional_field, mentorship_area, message
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            full_name,
            email,
            professional_field,
            mentorship_area,
            message
        ))

        connection.commit()
        connection.close()

        flash("Your mentorship request has been submitted.", "success")

        return redirect(url_for("mentorship"))

    return render_template("mentorship.html")


# ==========================================
# 16. CAREER PROGRESS
# ==========================================

@app.route("/progress")
@login_required
def progress():

    connection = get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    qualifications_count = connection.execute(
        "SELECT COUNT(*) FROM qualifications WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    mentorship_count = connection.execute(
        "SELECT COUNT(*) FROM mentorship_requests WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    connection.close()

    profile_fields = [
        user["full_name"],
        user["country"],
        user["location"],
        user["professional_field"],
        user["qualification"],
        user["experience"],
        user["skills"],
        user["career_goals"]
    ]

    completed_fields = sum(
        1 for field in profile_fields if field and field.strip()
    )

    profile_completion = round(
        completed_fields / len(profile_fields) * 100
    )

    return render_template(
        "progress.html",
        profile_completion=profile_completion,
        skills_completed=0,
        qualifications_count=qualifications_count,
        mentorship_count=mentorship_count
    )


# ==========================================
# 17. ERROR HANDLING
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return "Page not found. Please check the URL.", 404


@app.errorhandler(413)
def file_too_large(error):

    return "File is too large. Maximum upload size is 5 MB.", 413


# ==========================================
# 18. START APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

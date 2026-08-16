from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)



# MySQL Database Connection

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kajale@2211",
        database="job_tracker"
    )



# Home Route

@app.route("/")
def home():
    return "Job Application Tracker API is running!"



# GET - Fetch all applications

@app.route("/api/application", methods=["GET"])
def get_application():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM job_application
        ORDER BY date_applied DESC
    """)

    application = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(application)



# POST - Add application

@app.route("/api/application", methods=["POST"])
def add_application():
    data = request.get_json()

    company = data.get("company")
    role = data.get("role")
    date_applied = data.get("date_applied")
    status = data.get("status")
    job_link = data.get("job_link")
    notes = data.get("notes")

    if not company or not role or not date_applied or not status:
        return jsonify({
            "error": "Company, role, date applied and status are required."
        }), 400

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO job_application
        (company, role, date_applied, status, job_link, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        company,
        role,
        date_applied,
        status,
        job_link,
        notes
    )

    cursor.execute(query, values)
    db.commit()

    new_id = cursor.lastrowid

    cursor.close()
    db.close()

    return jsonify({
        "message": "Application added successfully.",
        "id": new_id
    }), 201


# PUT - Update application

@app.route("/api/application/<int:id>", methods=["PUT"])
def update_application(id):
    data = request.get_json()

    company = data.get("company")
    role = data.get("role")
    date_applied = data.get("date_applied")
    status = data.get("status")
    job_link = data.get("job_link")
    notes = data.get("notes")

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        UPDATE job_application
        SET company = %s,
            role = %s,
            date_applied = %s,
            status = %s,
            job_link = %s,
            notes = %s
        WHERE id = %s
    """

    values = (
        company,
        role,
        date_applied,
        status,
        job_link,
        notes,
        id
    )

    cursor.execute(query, values)
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "error": "Application not found."
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Application updated successfully."
    })



# DELETE - Delete application

@app.route("/api/application/<int:id>", methods=["DELETE"])
def delete_application(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM job_application WHERE id = %s",
        (id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "error": "Application not found."
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Application deleted successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)
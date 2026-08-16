from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kajale@2211",
    database="job_tracker"
)

print("MySQL database connected successfully!")


@app.route("/")
def home():
    return "Job Application Tracker API is running!"


if __name__ == "__main__":
    app.run(debug=True)
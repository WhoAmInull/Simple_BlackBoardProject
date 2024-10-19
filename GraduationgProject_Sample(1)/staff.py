import smtplib
import uuid
import psycopg2
from psycopg2 import OperationalError, IntegrityError
import bcrypt
from email.mime.text import MIMEText
import random
import os

# Database configuration
DB_HOST = "localhost"
DB_NAME = "course_management"
DB_USER = "postgres"
DB_PASSWORD = "21619062"

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "alzahrani0566359@gmail.com"  # Your email
EMAIL_PASSWORD = "uoqdnridnxnctkhy"  # Your app password

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(EMAIL_USER, EMAIL_PASSWORD)  # Authenticate
            server.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email and app password.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Database connection
def connect_db():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# User model
class User:
    def __init__(self, user_id, email, user_type, verified):
        self.user_id = user_id
        self.email = email
        self.user_type = user_type
        self.verified = verified

# System class to manage users and courses
class System:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    # Drop tables with CASCADE to remove dependencies
                    cur.execute("DROP TABLE IF EXISTS submissions CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS assignments CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS enrollments CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS logs CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS courses CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS password_resets CASCADE;")  # Drop password_resets first
                    cur.execute("DROP TABLE IF EXISTS users CASCADE;")  # Now drop users

                    # Create users table
                    cur.execute("""
                    CREATE TABLE users (
                        user_id VARCHAR PRIMARY KEY,
                        email VARCHAR UNIQUE NOT NULL,
                        password VARCHAR NOT NULL,
                        user_type VARCHAR NOT NULL,
                        verified BOOLEAN DEFAULT FALSE
                    );
                    """)
                    # Create password reset table
                    cur.execute("""
                    CREATE TABLE password_resets (
                        reset_id UUID PRIMARY KEY,
                        user_id VARCHAR REFERENCES users(user_id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        pin_code VARCHAR
                    );
                    """)
                    # Create courses table
                    cur.execute("""
                    CREATE TABLE courses (
                        course_id VARCHAR PRIMARY KEY,
                        title VARCHAR UNIQUE NOT NULL,
                        instructor_id VARCHAR REFERENCES users(user_id)
                    );
                    """)
                    # Create enrollments table
                    cur.execute("""
                    CREATE TABLE enrollments (
                        user_id VARCHAR REFERENCES users(user_id),
                        course_id VARCHAR REFERENCES courses(course_id),
                        PRIMARY KEY (user_id, course_id)
                    );
                    """)
                    # Create assignments table
                    cur.execute("""
                    CREATE TABLE assignments (
                        assignment_id SERIAL PRIMARY KEY,
                        course_id VARCHAR REFERENCES courses(course_id),
                        title VARCHAR NOT NULL,
                        due_date TIMESTAMP
                    );
                    """)
                    # Create submissions table
                    cur.execute("""
                    CREATE TABLE submissions (
                        submission_id SERIAL PRIMARY KEY,
                        assignment_id INTEGER REFERENCES assignments(assignment_id),
                        user_id VARCHAR REFERENCES users(user_id),
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        content TEXT,
                        grade FLOAT
                    );
                    """)
                    # Create logs table
                    cur.execute("""
                    CREATE TABLE logs (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR REFERENCES users(user_id),
                        action VARCHAR NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """)
                conn.commit()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def register_user(self, user_id, email, password, user_type):
        hashed_password = self.hash_password(password)

        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO users (user_id, email, password, user_type) VALUES (%s, %s, %s, %s)",
                                    (user_id, email, hashed_password.decode(), user_type))
                        conn.commit()
                        print(f"User {email} registered successfully.")
                    except IntegrityError:
                        print(f"User {email} already exists.")
                        conn.rollback()

    def verify_user(self, token):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM password_resets WHERE reset_id = %s", (token,))
                    user = cur.fetchone()
                    if user:
                        cur.execute("UPDATE users SET verified = TRUE WHERE user_id = %s", (user[0],))
                        cur.execute("DELETE FROM password_resets WHERE reset_id = %s", (token,))
                        conn.commit()
                        print("Email verified successfully!")
                        return True
                    else:
                        print("Invalid or expired token.")
                        return False

    def login(self, identifier, password):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id, email, password, user_type, verified FROM users WHERE (email = %s OR user_id = %s)", (identifier, identifier))
                    user = cur.fetchone()
                    if user and self.check_password(password, user[2]):
                        return User(user[0], user[1], user[3], user[4])
                    else:
                        print("Invalid email or password.")
                        return None

    def create_course(self, course_id, title, instructor_id):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO courses (course_id, title, instructor_id) VALUES (%s, %s, %s)", (course_id, title, instructor_id))
                        conn.commit()
                        print(f"Course {title} created successfully.")
                    except IntegrityError:
                        print(f"Course {course_id} already exists.")
                        conn.rollback()

    def enroll_student(self, user_id, course_id):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
                        conn.commit()
                        print(f"Student {user_id} enrolled in course {course_id}.")
                    except IntegrityError:
                        print(f"Enrollment failed: Student {user_id} is already enrolled in course {course_id}.")
                        conn.rollback()

    def view_all_users(self):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id, email, user_type, verified FROM users")
                    users = cur.fetchall()
                    for user in users:
                        print(user)

    def reset_password_request(self, email):
        token = str(uuid.uuid4())
        pin_code = str(random.randint(100000, 999999))  # Generate a random 6-digit PIN
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                    user = cur.fetchone()
                    if user:
                        cur.execute("INSERT INTO password_resets (reset_id, user_id, pin_code) VALUES (%s, %s, %s)", (token, user[0], pin_code))
                        conn.commit()
                        reset_link = f"http://localhost:5000/reset_password?token={token}"
                        send_email(email, "Password Reset", f"Reset your password by clicking the link: {reset_link}\nYour PIN Code: {pin_code}")
                        print("Password reset email sent.")
                    else:
                        print("Email not found.")

    def reset_password(self, token, new_password, pin_input):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id, pin_code FROM password_resets WHERE reset_id = %s", (token,))
                    reset_info = cur.fetchone()
                    if reset_info and reset_info[1] == pin_input:  # Validate PIN
                        hashed_password = self.hash_password(new_password)
                        cur.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_password.decode(), reset_info[0]))
                        cur.execute("DELETE FROM password_resets WHERE reset_id = %s", (token,))
                        conn.commit()
                        print("Password reset successfully!")
                    else:
                        print("Invalid token or PIN.")

    def add_assignment(self, course_id, title, due_date):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO assignments (course_id, title, due_date) VALUES (%s, %s, %s)", (course_id, title, due_date))
                    conn.commit()
                    print(f"Assignment '{title}' added to Course ID: {course_id}.")

    def submit_assignment(self, assignment_id, user_id, content):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO submissions (assignment_id, user_id, content) VALUES (%s, %s, %s)", (assignment_id, user_id, content))
                    conn.commit()
                    print("Assignment submitted successfully.")

    def view_assignments(self, course_id):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT assignment_id, title, due_date FROM assignments WHERE course_id = %s", (course_id,))
                    assignments = cur.fetchall()
                    for assignment in assignments:
                        print(f"Assignment ID: {assignment[0]}, Title: {assignment[1]}, Due Date: {assignment[2]}")

    def view_submissions(self, assignment_id):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id, content, submitted_at FROM submissions WHERE assignment_id = %s", (assignment_id,))
                    submissions = cur.fetchall()
                    for submission in submissions:
                        print(f"User ID: {submission[0]}, Content: {submission[1]}, Submitted At: {submission[2]}")

    def grade_submission(self, submission_id, grade):
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE submissions SET grade = %s WHERE submission_id = %s", (grade, submission_id))
                    conn.commit()
                    print("Submission graded successfully.")

# Initial Setup for Super Admin
def create_initial_admin(system):
    with connect_db() as conn:
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM users")
                count = cur.fetchone()[0]
                
                if count == 0:
                    user_id = "admin"
                    email = "phunder055207@gmail.com"
                    password = "123"  # Use a secure password
                    user_type = "Super Admin"
                    system.register_user(user_id, email, password, user_type)
                    print("Initial Super Admin user created.")
                    print(f"Super Admin credentials - Email: {email}, Password: {password}")

# Admin Menu
def admin_menu(system):
    while True:
        print("\nAdmin Menu:")
        print("1. Add User")
        print("2. Create Course")
        print("3. View All Users")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            user_id = input("Enter user ID: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            user_type = input("Enter user type (Admin/Instructor/Student): ")
            system.register_user(user_id, email, password, user_type)

        elif choice == '2':
            course_id = input("Enter course ID: ")
            title = input("Enter course title: ")
            instructor_id = input("Enter instructor user ID: ")
            system.create_course(course_id, title, instructor_id)

        elif choice == '3':
            system.view_all_users()

        elif choice == '4':
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")

# Student Menu Function
def student_menu(system, current_user):
    while True:
        print("\nStudent Menu:")
        print("1. View Courses")
        print("2. Enroll in a Course")
        print("3. View Enrolled Courses")
        print("4. Submit Assignment")
        print("5. View Submitted Assignments")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            print("Available Courses:")
            with connect_db() as conn:
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT course_id, title FROM courses")
                        courses = cur.fetchall()
                        for course in courses:
                            print(f"Course ID: {course[0]}, Title: {course[1]}")

        elif choice == '2':
            course_id = input("Enter Course ID to enroll: ")
            system.enroll_student(current_user.user_id, course_id)

        elif choice == '3':
            print("Enrolled Courses:")
            with connect_db() as conn:
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT course_id FROM enrollments WHERE user_id = %s", (current_user.user_id,))
                        enrolled_courses = cur.fetchall()
                        for course in enrolled_courses:
                            print(f"Course ID: {course[0]}")

        elif choice == '4':
            assignment_id = input("Enter Assignment ID to submit: ")
            content = input("Enter your submission content: ")
            system.submit_assignment(assignment_id, current_user.user_id, content)

        elif choice == '5':
            assignment_id = input("Enter Assignment ID to view submissions: ")
            system.view_submissions(assignment_id)

        elif choice == '6':
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")

# Instructor Menu Function
def instructor_menu(system, current_user):
    while True:
        print("\nInstructor Menu:")
        print("1. View Courses")
        print("2. Add Assignment")
        print("3. View Students Enrolled in Your Courses")
        print("4. View Assignments")
        print("5. Grade Submissions")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            print("Your Courses:")
            with connect_db() as conn:
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT course_id, title FROM courses WHERE instructor_id = %s", (current_user.user_id,))
                        courses = cur.fetchall()
                        for course in courses:
                            print(f"Course ID: {course[0]}, Title: {course[1]}")

        elif choice == '2':
            course_id = input("Enter Course ID to add an assignment: ")
            title = input("Enter Assignment Title: ")
            due_date = input("Enter Due Date (YYYY-MM-DD HH:MM:SS): ")
            system.add_assignment(course_id, title, due_date)

        elif choice == '3':
            print("Students Enrolled in Your Courses:")
            with connect_db() as conn:
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                        SELECT e.user_id, u.email 
                        FROM enrollments e
                        JOIN users u ON e.user_id = u.user_id
                        WHERE e.course_id IN (SELECT course_id FROM courses WHERE instructor_id = %s)
                        """, (current_user.user_id,))
                        students = cur.fetchall()
                        for student in students:
                            print(f"Student ID: {student[0]}, Email: {student[1]}")

        elif choice == '4':
            course_id = input("Enter Course ID to view assignments: ")
            system.view_assignments(course_id)

        elif choice == '5':
            submission_id = input("Enter Submission ID to grade: ")
            grade = float(input("Enter Grade: "))
            system.grade_submission(submission_id, grade)

        elif choice == '6':
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")

# Function to handle password reset flow
def reset_password_flow(system):
    token = input("Enter your reset token from the email: ")
    pin_input = input("Enter the PIN code sent to your email: ")
    new_password = input("Enter your new password: ")
    
    # Call the reset_password method with the token, new password, and PIN input
    system.reset_password(token, new_password, pin_input)

# Updated main menu to include this flow
def main_menu(system):
    while True:
        print("\nWelcome to the Course Management System")
        print("1. Login")
        print("2. Request Password Reset")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            identifier = input("Enter email or user ID: ")
            password = input("Enter password: ")
            current_user = system.login(identifier, password)
            if current_user:
                print(f"Logged in as {current_user.user_type}")
                if current_user.user_type in ['Admin', 'Super Admin']:
                    admin_menu(system)
                elif current_user.user_type == 'Student':
                    student_menu(system, current_user)
                elif current_user.user_type == 'Instructor':
                    instructor_menu(system, current_user)

        elif choice == '2':
            email = input("Enter your email: ")
            system.reset_password_request(email)
            reset_password_flow(system)  # Prompt for token, PIN, and new password

        elif choice == '3':
            print("Exiting the system...")
            break

        else:
            print("Invalid choice. Please try again.")

# Entry point for the application
if __name__ == "__main__":
    system = System()
    create_initial_admin(system)  # Create initial Super Admin if not exists
    main_menu(system)  # Start the main menu
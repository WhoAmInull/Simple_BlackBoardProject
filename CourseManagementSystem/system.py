import uuid
import bcrypt
import random
from db_connection import connect_db, create_tables
from email_service import send_email
from models.user import User
from models.course import Course
from models.assignment import Assignment

class System:
    def __init__(self):
        """Initialize the System and create necessary tables."""
        self.create_tables()

    def create_tables(self):
        """Create necessary tables in the database."""
        with connect_db() as conn:
            if conn:
                create_tables(conn)

    def hash_password(self, password):
        """Hash a password for storage."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password, hashed):
        """Check a password against a hashed password."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def register_user(self, user_id, email, password, user_type):
        """Register a new user in the database."""
        hashed_password = self.hash_password(password)

        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO users (user_id, email, password, user_type) VALUES (%s, %s, %s, %s)",
                                    (user_id, email, hashed_password.decode(), user_type))
                        conn.commit()
                        print(f"User {email} registered successfully.")
                    except Exception as e:
                        print(f"Error registering user: {e}")

    def create_course(self, course_id, title, instructor_id):
        """Create a new course in the database."""
        with connect_db() as conn:
            if conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO courses (course_id, title, instructor_id) VALUES (%s, %s, %s)",
                                    (course_id, title, instructor_id))
                        conn.commit()
                        print(f"Course {title} created successfully.")
                    except Exception as e:
                        print(f"Error creating course: {e}")

    # Additional methods for assignment handling, user retrieval, etc. can be added here
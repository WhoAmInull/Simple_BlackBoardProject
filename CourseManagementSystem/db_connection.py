import psycopg2
from psycopg2 import OperationalError
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def connect_db():
    """Establish a connection to the database."""
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables(conn):
    """Create necessary tables in the database."""
    with conn.cursor() as cur:
        # Drop tables with CASCADE to remove dependencies
        cur.execute("DROP TABLE IF EXISTS submissions CASCADE;")
        cur.execute("DROP TABLE IF EXISTS assignments CASCADE;")
        cur.execute("DROP TABLE IF EXISTS enrollments CASCADE;")
        cur.execute("DROP TABLE IF EXISTS logs CASCADE;")
        cur.execute("DROP TABLE IF EXISTS courses CASCADE;")
        cur.execute("DROP TABLE IF EXISTS password_resets CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        
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

        # Create courses table
        cur.execute("""
        CREATE TABLE courses (
            course_id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            instructor_id VARCHAR REFERENCES users(user_id)
        );
        """)

        # Create assignments table
        cur.execute("""
        CREATE TABLE assignments (
            assignment_id VARCHAR PRIMARY KEY,
            course_id VARCHAR REFERENCES courses(course_id),
            title VARCHAR NOT NULL,
            due_date DATE NOT NULL
        );
        """)

        # Create enrollments table
        cur.execute("""
        CREATE TABLE enrollments (
            enrollment_id SERIAL PRIMARY KEY,
            user_id VARCHAR REFERENCES users(user_id),
            course_id VARCHAR REFERENCES courses(course_id)
        );
        """)

        # Create submissions table
        cur.execute("""
        CREATE TABLE submissions (
            submission_id SERIAL PRIMARY KEY,
            assignment_id VARCHAR REFERENCES assignments(assignment_id),
            user_id VARCHAR REFERENCES users(user_id),
            content TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Create logs table
        cur.execute("""
        CREATE TABLE logs (
            log_id SERIAL PRIMARY KEY,
            user_id VARCHAR REFERENCES users(user_id),
            action VARCHAR NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    conn.commit()
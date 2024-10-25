class Course:
    def __init__(self, course_id, title, instructor_id):
        """Initialize a Course object."""
        self.course_id = course_id  # Unique identifier for the course
        self.title = title  # Title of the course
        self.instructor_id = instructor_id  # User ID of the instructor
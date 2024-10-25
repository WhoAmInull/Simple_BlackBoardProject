class Assignment:
    def __init__(self, assignment_id, course_id, title, due_date):
        """Initialize an Assignment object."""
        self.assignment_id = assignment_id  # Unique identifier for the assignment
        self.course_id = course_id  # ID of the course to which the assignment belongs
        self.title = title  # Title of the assignment
        self.due_date = due_date  # Due date for the assignment
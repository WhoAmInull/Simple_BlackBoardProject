class User:
    def __init__(self, user_id, email, user_type, verified):
        """Initialize a User object."""
        self.user_id = user_id  # Unique identifier for the user
        self.email = email  # User's email address
        self.user_type = user_type  # Type of user (Admin, Instructor, Student)
        self.verified = verified  # Verification status of the user
# Semi-Blackboard System Project

## Overview
This project is a simplified simulation of a blackboard system used for managing courses, assignments, and communication between instructors and students.

The system is designed with roles (Student, Instructor) and basic functionalities like login, course management, and assignment submissions. The system follows object-oriented design principles.

## Features

### User
- **Attributes**:
  - `userID`: String
  - `name`: String
  - `email`: String
  - `role`: String

- **Methods**:
  - `login()`: Allows users to log in
  - `logout()`: Logs out the current user
  - `register()`: Registers a new user

### Course
- **Attributes**:
  - `courseID`: String
  - `title`: String
  - `description`: String
  - `credits`: Integer

- **Methods**:
  - `addAssignment()`: Add assignments to the course
  - `viewMaterials()`: View course materials

### Assignment
- **Attributes**:
  - `assignmentID`: String
  - `title`: String
  - `dueDate`: Date

- **Methods**:
  - `submit()`: Allows students to submit assignments
  - `grade()`: Allows instructors to grade assignments

### Communication
- **Attributes**:
  - `messageID`: String
  - `senderID`: String
  - `receiverID`: String
  - `content`: String

- **Methods**:
  - `send()`: Sends a message
  - `receive()`: Receives a message

### Student Role
- **Methods**:
  - `viewGrades()`: Allows students to view their grades

### Instructor Role
- **Methods**:
  - `gradeAssignment()`: Allows instructors to grade student assignments

## UML Diagram
The system design is represented in the UML diagram (insert diagram here).

## How to Use
1. Clone the repository:
    ```bash
    git clone https://github.com/WhoAmInull/Simple_BlackBoardProject.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Simple_BlackBoardProject
    ```

3. Follow installation instructions (if any).

## Future Enhancements
- **Role Management**: Add more roles like Admin.
- **Notification System**: Add email notifications for assignments and grades.
- **Assignment Submissions**: Support for file uploads.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

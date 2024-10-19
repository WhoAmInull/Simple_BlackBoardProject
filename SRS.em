---

# Software Requirements Specification (SRS)

## 1. **Introduction**

### 1.1 **Purpose**
The purpose of this document is to define the requirements for the **Semi-Blackboard System**, a simplified platform designed for students and instructors to manage courses, assignments, and communication.

### 1.2 **Scope**
The Semi-Blackboard System is a lightweight version of traditional Learning Management Systems (LMS). It provides core functionalities such as user authentication, course management, assignment handling, and online classes, tailored for basic educational needs.

### 1.3 **Intended Users**
- **Students**: Can log in, enroll in courses, view course content, attend virtual classes, and submit assignments.
- **Instructors**: Can log in, create and manage courses, post assignments, and review submissions.

---

## 2. **System Overview**

The Semi-Blackboard System supports two primary user roles: **Students** and **Instructors**. It facilitates streamlined operations such as logging in, course and assignment management, virtual class attendance, and tracking submissions.

---

## 3. **Functional Requirements**

### 3.1 **User Roles and Permissions**

- **Students**: 
  - Can log in to their account.
  - View available courses and course content.
  - Attend virtual (online) classes.
  - View, complete, and submit assignments through the system.

- **Instructors**:
  - Can log in to their account.
  - Create, view, and manage their courses.
  - Post and manage assignments.
  - Review, grade, and provide feedback on student submissions.

### 3.2 **Login System**
- Each user (student or instructor) will have a unique login with role-specific access.
- The system will authenticate users based on credentials and display functionalities appropriate to their role.

### 3.3 **Course Management**

- **For Instructors**:
  - Ability to create new courses and manage existing ones.
  - Upload course content and provide access to enrolled students.
  - Set up virtual classes for online learning sessions.

- **For Students**:
  - Ability to view and enroll in available courses.
  - Access course content and participate in virtual classes.
  - View assignments related to the enrolled courses.

### 3.4 **Assignment Management**

- **For Instructors**:
  - Upload and manage assignments for each course.
  - Review and grade student submissions.
  - Provide feedback on submitted assignments.

- **For Students**:
  - View and download assignments from enrolled courses.
  - Submit assignments by attaching completed work to the system.

---

## 4. **Non-Functional Requirements**

### 4.1 **Usability**
- The system should be user-friendly, ensuring that both students and instructors can easily navigate through the functionalities without prior technical knowledge.

### 4.2 **Performance**
- The system must perform smoothly under normal usage conditions, handling user logins, course navigation, and assignment submissions without significant delays.

### 4.3 **Security**
- User login details (like passwords) should be securely encrypted.
- Access to features should be role-based, ensuring that students cannot access instructor-specific functionalities and vice versa.

---

## 5. **System Design**

### 5.1 **Object-Oriented Design**
- The system will use object-oriented principles to ensure code reusability, maintainability, and flexibility for future updates.

### 5.2 **Database**
- A relational database will store essential data such as user profiles, course details, assignment submissions, and virtual class schedules.

---

## 6. **Conclusion**

The **Semi-Blackboard System** is a straightforward, user-friendly solution aimed at managing essential educational activities, including course and assignment management. Its simplicity makes it an ideal tool for instructors and students who need a reliable and easy-to-use platform.

---

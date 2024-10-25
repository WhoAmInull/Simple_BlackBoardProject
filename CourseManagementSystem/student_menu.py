def student_menu(system, current_user):
    """Display the student menu and handle user input."""
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
            # Placeholder for viewing courses
            print("Viewing courses is not yet implemented.")

        elif choice == '2':
            # Placeholder for enrolling in a course
            print("Enrolling in a course is not yet implemented.")

        elif choice == '3':
            # Placeholder for viewing enrolled courses
            print("Viewing enrolled courses is not yet implemented.")

        elif choice == '4':
            # Placeholder for submitting an assignment
            print("Submitting an assignment is not yet implemented.")

        elif choice == '5':
            # Placeholder for viewing submitted assignments
            print("Viewing submitted assignments is not yet implemented.")

        elif choice == '6':
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.") 

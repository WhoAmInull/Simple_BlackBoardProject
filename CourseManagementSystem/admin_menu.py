def admin_menu(system):
    """Display the admin menu and handle user input."""
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
            # Placeholder for viewing all users
            print("Viewing all users is not yet implemented.")

        elif choice == '4':
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")
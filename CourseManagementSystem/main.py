from system import System
from admin_menu import admin_menu
from student_menu import student_menu

def main():
    """Main function to run the Course Management System."""
    system = System()
    
    # Create initial admin user if needed
    # Uncomment the following lines to create an initial admin user
    # admin_email = "admin@example.com"
    # admin_password = "admin_password"
    # system.register_user("admin", admin_email, admin_password, "Admin")

    while True:
        print("\nWelcome to the Course Management System")
        print("1. Login as Admin")
        print("2. Login as Student")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            # Admin login logic can be implemented here
            print("Admin login is not yet implemented.")

        elif choice == '2':
            # Student login logic can be implemented here
            print("Student login is not yet implemented.")

        elif choice == '3':
            print("Exiting the system...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
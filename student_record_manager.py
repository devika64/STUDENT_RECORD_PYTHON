"""
Student Record Manager
A console-based application to manage student records using Core Python only.
"""

import re

STUDENTS_FILE = "students.txt"


def display_menu():
    """Display the main menu options to the user."""
    print("\n===== Student Record Manager =====")
    print("\n1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Exit")
    print()


def validate_email(email):
    """Validate email format using regular expressions."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def get_existing_ids():
    """Read all student IDs from the file to prevent duplicates."""
    ids = set()
    try:
        with open(STUDENTS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    student_id = line.split(",")[0].strip()
                    ids.add(student_id)
    except FileNotFoundError:
        pass
    return ids


def save_student(student_id, name, email, age, course):
    """Append a student record to students.txt."""
    with open(STUDENTS_FILE, "a") as file:
        file.write(f"{student_id},{name},{email},{age},{course}\n")


def read_students():
    """Read all student records from the file."""
    students = []
    try:
        with open(STUDENTS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 5:
                    students.append({
                        "id": parts[0].strip(),
                        "name": parts[1].strip(),
                        "email": parts[2].strip(),
                        "age": parts[3].strip(),
                        "course": parts[4].strip()
                    })
    except FileNotFoundError:
        pass
    return students


def add_student():
    """Add a new student record with input validation."""
    print("\n--- Add Student ---")
    existing_ids = get_existing_ids()

    while True:
        try:
            student_id = input("Enter Student ID: ").strip()
            if not student_id:
                print("Error: Student ID cannot be empty. Please try again.")
                continue
            if student_id in existing_ids:
                print("Error: Student ID already exists. Please enter a unique ID.")
                continue
            break
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return

    while True:
        try:
            name = input("Enter Student Name: ").strip()
            if not name:
                print("Error: Name cannot be empty. Please try again.")
                continue
            break
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return

    while True:
        try:
            email = input("Enter Email: ").strip()
            if validate_email(email):
                break
            print("Error: Invalid email format. Please enter a valid email (e.g., student@gmail.com).")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return

    while True:
        try:
            age = int(input("Enter Age: ").strip())
            if age <= 0 or age > 150:
                print("Error: Please enter a valid age (1-150).")
                continue
            break
        except ValueError:
            print("Error: Age must be a number. Please try again.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return

    while True:
        try:
            course = input("Enter Course: ").strip()
            if not course:
                print("Error: Course cannot be empty. Please try again.")
                continue
            break
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return

    try:
        save_student(student_id, name, email, age, course)
        print("\nStudent added successfully!")
    except IOError as e:
        print(f"\nError: Could not save student record. {e}")


def view_all_students():
    """Read and display all students in a formatted table."""
    print("\n--- All Students ---")
    try:
        students = read_students()
        if not students:
            print("No student records found.")
            return

        print(f"\n{'ID':<6} {'Name':<14} {'Email':<22} {'Age':<6} {'Course':<10}")
        print("-" * 60)
        for student in students:
            print(
                f"{student['id']:<6} {student['name']:<14} "
                f"{student['email']:<22} {student['age']:<6} {student['course']:<10}"
            )
    except Exception as e:
        print(f"\nError: Could not read student records. {e}")


def search_student():
    """Search for a student by ID or Name."""
    print("\n--- Search Student ---")
    try:
        search_by = input("Search by (1) ID or (2) Name: ").strip()

        if search_by == "1":
            search_term = input("Enter Student ID: ").strip()
            students = read_students()
            found = next((s for s in students if s["id"] == search_term), None)
        elif search_by == "2":
            search_term = input("Enter Student Name: ").strip()
            students = read_students()
            found = next((s for s in students if s["name"].lower() == search_term.lower()), None)
        else:
            print("Error: Invalid search option. Please enter 1 or 2.")
            return

        if found:
            print("\n--- Student Found ---")
            print(f"ID     : {found['id']}")
            print(f"Name   : {found['name']}")
            print(f"Email  : {found['email']}")
            print(f"Age    : {found['age']}")
            print(f"Course : {found['course']}")
        else:
            print("\nStudent not found.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\nError: {e}")


def main():
    """Main function to run the Student Record Manager application."""
    print("Welcome to Student Record Manager!")

    while True:
        try:
            display_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                print("\nThank you for using Student Record Manager. Goodbye!")
                break
            else:
                print("\nError: Invalid option. Please choose 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

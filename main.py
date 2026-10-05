
from database import (
    add_student as save_student,
)
from database import (
    close_database,
    get_student_by_id,
    get_students,
    search_students,
    student_exists,
)
from database import (
    delete_student as remove_student,
)
from database import (
    update_student as save_updated_student,
)


# Display student records
def display_students(students):
    for student in students:
        print(
            f"ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Course: {student[2]} | "
            f"Email: {student[3]}"
        )


# Get a valid positive student ID
def get_student_id():
    while True:
        try:
            student_id = int(input("Enter student ID: "))

            if student_id <= 0:
                print("Student ID must be a positive number.")
                continue

            return student_id

        except ValueError:
            print("Invalid input. Please enter a whole number.")


# Basic email validation
def validate_email(email):
    if not email or email.count("@") != 1:
        return False

    local_part, domain = email.split("@")

    if not local_part or not domain:
        return False

    if "." not in domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return " " not in email


# Collect and validate student details
def get_student_details():
    while True:
        name = input("Enter student name: ").strip()

        if name:
            break

        print("Name cannot be empty. Please try again.")

    while True:
        course = input("Enter course: ").strip()

        if course:
            break

        print("Course cannot be empty. Please try again.")

    while True:
        email = input("Enter email: ").strip()

        if validate_email(email):
            break

        print("Invalid email address. Please try again.")

    return name, course, email


# Add a student
def add_student():
    name, course, email = get_student_details()

    success = save_student(name, course, email)

    if success:
        print("Student added successfully.")
    else:
        print("Could not add student. Please try again.")


# View all students
def view_students():
    students = get_students()

    if students is None:
        print("Could not retrieve students because of a database error.")

    elif students:
        display_students(students)

    else:
        print("No students found.")


# Search students
def search_student():
    while True:
        name = input("Enter student name to search: ").strip()

        if name:
            break

        print("Search name cannot be empty. Please try again.")

    students = search_students(name)

    if students is None:
        print("Search failed because of a database error.")

    elif students:
        display_students(students)

    else:
        print("No matching students found.")


# Update a student
def update_student():
    student_id = get_student_id()
    student = get_student_by_id(student_id)

    if student is None:
        print(
            "Could not retrieve student details "
            "because of a database error."
        )
        return

    if student is False:
        print("Student ID not found.")
        return

    # Show the existing details
    print("\n===== Current Student Details =====")
    print(f"ID: {student[0]}")
    print(f"Name: {student[1]}")
    print(f"Course: {student[2]}")
    print(f"Email: {student[3]}")

    print("\nEnter the new details:")
    name, course, email = get_student_details()

    # Show the proposed changes
    print("\n===== Proposed Student Details =====")
    print(f"Student ID: {student_id}")
    print(f"New Name: {name}")
    print(f"New Course: {course}")
    print(f"New Email: {email}")

    confirmation = input(
        "Save these changes? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Update cancelled. Existing details remain unchanged.")
        return

    success = save_updated_student(
        student_id,
        name,
        course,
        email
    )

    if success:
        print("Student updated successfully.")
    else:
        print(
            "Student was not updated. "
            "Please check the ID and try again."
        )


# Delete a student
def delete_student():
    student_id = get_student_id()
    exists = student_exists(student_id)

    if exists is None:
        print("Could not verify the student ID.")
        return

    if not exists:
        print("Student ID not found.")
        return

    confirmation = input(
        f"Are you sure you want to delete student {student_id}? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion cancelled.")
        return

    success = remove_student(student_id)

    if success:
        print("Student deleted successfully.")
    else:
        print("Student was not deleted. Please try again.")


# Main menu
def main():
    try:
        while True:
            print("\n===== Student Management System =====")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_student()

            elif choice == "2":
                view_students()

            elif choice == "3":
                search_student()

            elif choice == "4":
                update_student()

            elif choice == "5":
                delete_student()

            elif choice == "6":
                print("Exiting Student Management System.")
                break

            else:
                print("Invalid choice. Please select 1–6.")

    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted. Exiting safely.")

    finally:
        close_database()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
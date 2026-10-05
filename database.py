
import sqlite3

# Connect to the database and create the table
try:
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT,
            email TEXT
        )
    """)

    conn.commit()

except sqlite3.Error as error:
    print(f"Database initialization failed: {error}")

    if "conn" in globals():
        conn.close()

    raise SystemExit(1)


# Display database errors and roll back failed changes
def handle_database_error(error, rollback=False):
    print(f"Database error: {error}")

    if rollback:
        try:
            conn.rollback()
        except sqlite3.Error as rollback_error:
            print(f"Rollback failed: {rollback_error}")


# Retrieve all students
def get_students():
    try:
        cur.execute("SELECT * FROM students")
        return cur.fetchall()

    except sqlite3.Error as error:
        handle_database_error(error)
        return None


# Retrieve one student by ID
# Returns the record, False if not found, or None on database error
def get_student_by_id(student_id):
    try:
        cur.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )
        student = cur.fetchone()

        if student is None:
            return False

        return student

    except sqlite3.Error as error:
        handle_database_error(error)
        return None


# Search students by name
def search_students(name):
    try:
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            (f"%{name}%",)
        )
        return cur.fetchall()

    except sqlite3.Error as error:
        handle_database_error(error)
        return None


# Check whether a student exists
def student_exists(student_id):
    try:
        cur.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        )
        student = cur.fetchone()

        return student is not None

    except sqlite3.Error as error:
        handle_database_error(error)
        return None


# Add a student
def add_student(name, course, email):
    try:
        cur.execute(
            """
            INSERT INTO students (name, course, email)
            VALUES (?, ?, ?)
            """,
            (name, course, email)
        )

        conn.commit()
        return True

    except sqlite3.Error as error:
        handle_database_error(error, rollback=True)
        return False


# Update a student
def update_student(student_id, name, course, email):
    try:
        cur.execute(
            """
            UPDATE students
            SET name = ?, course = ?, email = ?
            WHERE id = ?
            """,
            (name, course, email, student_id)
        )

        updated = cur.rowcount > 0
        conn.commit()

        return updated

    except sqlite3.Error as error:
        handle_database_error(error, rollback=True)
        return False


# Delete a student
def delete_student(student_id):
    try:
        cur.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        deleted = cur.rowcount > 0
        conn.commit()

        return deleted

    except sqlite3.Error as error:
        handle_database_error(error, rollback=True)
        return False


# Close the database connection
def close_database():
    try:
        conn.close()
        return True

    except sqlite3.Error as error:
        print(f"Could not close database: {error}")
        return False
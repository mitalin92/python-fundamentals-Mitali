from models import Base
from db_engine import ENGINE
from queries import get_all_students, get_student_by_name, add_student, update_student

if __name__ == "__main__":
    Base.metadata.create_all(ENGINE)  # Ensure table exists

    print("\n--- Running Database Operations ---")

    # Retrieve all students
    print("\nAll Students:")
    for s in get_all_students():
        print(s.name, s.email, s.course_name, s.semester, s.age)

    # Find a student by name
    print("\nSearching for 'Mitali':")
    student = get_student_by_name("Mitali")
    if student:
        print(
            student.name,
            student.email,
            student.course_name,
            student.semester,
            student.age,
        )
    else:
        print("Student not found.")

    # Insert new student
    print("\nInserting new student 'Ravi'...")
    add_student("Ravi", "ravi@example.com", "Physics", 2, 21)

    # Update student information
    print("\nUpdating 'Rushi' semester to 6...")
    target = get_student_by_name("Rushi")
    if target:
        update_student(target.student_id, semester=6)

    # Show all students again
    print("\nUpdated Students:")
    for s in get_all_students():
        print(s.name, s.email, s.course_name, s.semester, s.age)

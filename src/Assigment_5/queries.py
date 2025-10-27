from sqlalchemy.orm import Session
from models import Student
from db_engine import ENGINE
from sqlalchemy.exc import SQLAlchemyError


def get_all_students():
    with Session(ENGINE) as session:
        return session.query(Student).all()


# Where clause Question 9


def get_student_by_name(name):
    with Session(ENGINE) as session:
        return session.query(Student).filter(Student.name == name).first()


# Question 10


def add_student(name, email, course_name, semester, age):
    try:
        with Session(ENGINE) as session:
            new_student = Student(
                name=name,
                email=email,
                course_name=course_name,
                semester=semester,
                age=age,
            )
            session.add(new_student)
            session.commit()
            return True
    except SQLAlchemyError as e:
        print("Error inserting student:", e)
        return False


# Question 11


def update_student(
    student_id, name=None, email=None, course_name=None, semester=None, age=None
):
    try:
        with Session(ENGINE) as session:
            student = (
                session.query(Student).filter(Student.student_id == student_id).first()
            )
            if student:
                if name:
                    student.name = name
                if email:
                    student.email = email
                if course_name:
                    student.course_name = course_name
                if semester:
                    student.semester = semester
                if age:
                    student.age = age
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print("Error updating student:", e)
        return False

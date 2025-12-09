from sqlalchemy.orm import Session
from models import Student
from db_engine import ENGINE


def get_all_students():
    with Session(ENGINE) as session:
        return session.query(Student).all()


# Where clause


def get_student_by_name(name):
    with Session(ENGINE) as session:
        return session.query(Student).filter(Student.name == name).first()

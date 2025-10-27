from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, UniqueConstraint


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("email", name="uq_student_email"),)

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    course_name = Column(String(100))
    semester = Column(Integer)
    age = Column(Integer)

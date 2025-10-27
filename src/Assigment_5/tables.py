from sqlalchemy import MetaData, Table, Column, Integer, String, UniqueConstraint

metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("student_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), unique=True, nullable=False),
    Column("course_name", String(100)),
    Column("semester", Integer),
    Column("age", Integer),
    UniqueConstraint("email", name="uq_student_email"),
)

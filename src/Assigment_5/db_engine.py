from sqlalchemy import create_engine, text
import os

DB_USER = os.getenv("DB_USER", "myuser")
DB_PASS = os.getenv("DB_PASS", "mypassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "college_db")

CONN_STR = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ENGINE = create_engine(
    CONN_STR,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
    future=True,
)


def test_connection():
    with ENGINE.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB test result:", result.scalar())


if __name__ == "__main__":
    test_connection()

-- Create database for students
CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    course_name VARCHAR(100),
    semester INT,
    age INT
);

-- Insert data

INSERT INTO students (name, email, course_name, semester, age) VALUES
('Mitali', 'mitali@example.com', 'Data Science', 3, 24),
('Rushi', 'rushi@example.com', 'Computer Science', 5, 22),
('Rucha', 'rucha@example.com', 'Biotechnology', 4, 23),
('Yukthi', 'yukthi@example.com', 'AI and Robotics', 2, 21),
('Nilesh', 'nilesh@example.com', 'Mechanical Engineering', 6, 25),
('Geeta', 'geeta@example.com', 'Electrical Engineering', 1, 20);

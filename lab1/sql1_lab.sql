-- SQL Exercises (With Answers)
-- Assuming I can assume the tables and column names? (I got sick w/ covid)

-- 1. Retrieve all students who enrolled in 2023.
 SELECT * FROM enrollments WHERE YEAR(EnrollmentDate) = 2023;

-- 2. Find students whose email contains 'gmail.com'.
 SELECT * FROM students WHERE Email like "%gmail.com%";

-- 3. Count how many students are enrolled in the database.
 SELECT COUNT(*) FROM students;

-- 4. Find students born between 2000 and 2005.
 SELECT * FROM students WHERE Year(DateOfBirth) BETWEEN 2000 and 2005;

-- 5. List students sorted by last name in descending order.
 SELECT * FROM students ORDER BY LastName DESC;


-- 6. Find the names of students and the courses they are enrolled in.
SELECT s.FirstName, s.LastName, c.CourseName
 FROM students s 
 JOIN enrollments e ON s.StudentID = e.StudentID
 JOIN courses c ON e.CourseID = c.CourseID;

-- 7. List all students and their courses, ensuring students without courses are included (LEFT JOIN).
SELECT s.FirstName, s.LastName, c.CourseName
 FROM students s 
 LEFT JOIN enrollments e ON s.StudentID = e.StudentID
 LEFT JOIN courses c ON e.CourseID = c.CourseID;

-- 8. Find all courses with no students enrolled (LEFT JOIN).

select c.CourseName from courses c LEFT JOIN enrollments e ON e.CourseID = c.CourseID WHERE e.studentID IS NULL;


-- 10. List courses and show the number of students enrolled in each course.

select c.CourseName, Count(e.StudentID) from courses c LEFT JOIN enrollments e ON e.CourseID = c.CourseID GROUP BY c.CourseID;


"""
AI-Powered School Database System
This module provides a comprehensive database system for school management
with AI-powered natural language query capabilities.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
import re


class SchoolDatabase:
    """
    AI-Powered School Database System
    
    Features:
    - Student, Teacher, Course, and Grade management
    - Natural language query interface
    - Intelligent search and filtering
    - Automated recommendations
    """
    
    def __init__(self, db_path: str = "school.db"):
        """Initialize the database connection and create tables if needed."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary database tables."""
        cursor = self.conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade_level INTEGER,
                email TEXT UNIQUE,
                enrollment_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Teachers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT,
                email TEXT UNIQUE,
                years_experience INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT,
                teacher_id INTEGER,
                capacity INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id)
            )
        """)
        
        # Grades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                grade REAL,
                semester TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)
        
        # Enrollments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id),
                UNIQUE(student_id, course_id)
            )
        """)
        
        self.conn.commit()
    
    # === CRUD Operations for Students ===
    
    def add_student(self, name: str, age: int, grade_level: int, email: str, 
                    enrollment_date: str = None) -> int:
        """Add a new student to the database."""
        if enrollment_date is None:
            enrollment_date = datetime.now().strftime("%Y-%m-%d")
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, age, grade_level, email, enrollment_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, grade_level, email, enrollment_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_student(self, student_id: int) -> Optional[Dict]:
        """Get a student by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    def update_student(self, student_id: int, **kwargs) -> bool:
        """Update student information."""
        allowed_fields = ['name', 'age', 'grade_level', 'email', 'enrollment_date']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [student_id]
        
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE students SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_student(self, student_id: int) -> bool:
        """Delete a student."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # === CRUD Operations for Teachers ===
    
    def add_teacher(self, name: str, subject: str, email: str, 
                    years_experience: int = 0) -> int:
        """Add a new teacher to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (name, subject, email, years_experience)
            VALUES (?, ?, ?, ?)
        """, (name, subject, email, years_experience))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_teacher(self, teacher_id: int) -> Optional[Dict]:
        """Get a teacher by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_teachers(self) -> List[Dict]:
        """Get all teachers."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM teachers ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    # === CRUD Operations for Courses ===
    
    def add_course(self, name: str, subject: str, teacher_id: int, 
                   capacity: int = 30) -> int:
        """Add a new course to the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO courses (name, subject, teacher_id, capacity)
            VALUES (?, ?, ?, ?)
        """, (name, subject, teacher_id, capacity))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_course(self, course_id: int) -> Optional[Dict]:
        """Get a course by ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.*, t.name as teacher_name 
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.id
            WHERE c.id = ?
        """, (course_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_courses(self) -> List[Dict]:
        """Get all courses."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.*, t.name as teacher_name 
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.id
            ORDER BY c.name
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    # === CRUD Operations for Grades ===
    
    def add_grade(self, student_id: int, course_id: int, grade: float, 
                  semester: str) -> int:
        """Add a grade for a student in a course."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO grades (student_id, course_id, grade, semester)
            VALUES (?, ?, ?, ?)
        """, (student_id, course_id, grade, semester))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_student_grades(self, student_id: int) -> List[Dict]:
        """Get all grades for a student."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT g.*, c.name as course_name, s.name as student_name
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            JOIN students s ON g.student_id = s.id
            WHERE g.student_id = ?
            ORDER BY g.semester, c.name
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_course_grades(self, course_id: int) -> List[Dict]:
        """Get all grades for a course."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT g.*, s.name as student_name, c.name as course_name
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN courses c ON g.course_id = c.id
            WHERE g.course_id = ?
            ORDER BY s.name
        """, (course_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # === Enrollment Operations ===
    
    def enroll_student(self, student_id: int, course_id: int) -> int:
        """Enroll a student in a course."""
        enrollment_date = datetime.now().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO enrollments (student_id, course_id, enrollment_date)
            VALUES (?, ?, ?)
        """, (student_id, course_id, enrollment_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_student_courses(self, student_id: int) -> List[Dict]:
        """Get all courses a student is enrolled in."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.*, t.name as teacher_name, e.enrollment_date
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            LEFT JOIN teachers t ON c.teacher_id = t.id
            WHERE e.student_id = ?
            ORDER BY c.name
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_course_students(self, course_id: int) -> List[Dict]:
        """Get all students enrolled in a course."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.*, e.enrollment_date
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            WHERE e.course_id = ?
            ORDER BY s.name
        """, (course_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # === AI-Powered Features ===
    
    def natural_language_query(self, query: str) -> Dict[str, Any]:
        """
        AI-powered natural language query interface.
        Interprets natural language queries and returns appropriate data.
        """
        query_lower = query.lower()
        
        # Student queries
        if "student" in query_lower or "students" in query_lower:
            if "all" in query_lower or "list" in query_lower:
                return {
                    "query": query,
                    "interpretation": "List all students",
                    "results": self.get_all_students()
                }
            
            # Search for specific student by name
            name_match = re.search(r'named? ([A-Za-z\s]+)', query_lower)
            if name_match:
                name = name_match.group(1).strip()
                return {
                    "query": query,
                    "interpretation": f"Search for student named '{name}'",
                    "results": self.search_students(name)
                }
        
        # Teacher queries
        if "teacher" in query_lower or "teachers" in query_lower:
            if "all" in query_lower or "list" in query_lower:
                return {
                    "query": query,
                    "interpretation": "List all teachers",
                    "results": self.get_all_teachers()
                }
            
            # Search by subject
            subject_match = re.search(r'teach(?:ing|es)? ([A-Za-z\s]+)', query_lower)
            if subject_match:
                subject = subject_match.group(1).strip()
                return {
                    "query": query,
                    "interpretation": f"Search for teachers teaching '{subject}'",
                    "results": self.search_teachers_by_subject(subject)
                }
        
        # Course queries
        if "course" in query_lower or "courses" in query_lower or "class" in query_lower:
            if "all" in query_lower or "list" in query_lower:
                return {
                    "query": query,
                    "interpretation": "List all courses",
                    "results": self.get_all_courses()
                }
        
        # Grade queries
        if "grade" in query_lower or "grades" in query_lower or "performance" in query_lower:
            # Check for average or GPA
            if "average" in query_lower or "gpa" in query_lower:
                return {
                    "query": query,
                    "interpretation": "Calculate student averages",
                    "results": self.get_student_averages()
                }
        
        # Top performers
        if "top" in query_lower or "best" in query_lower or "highest" in query_lower:
            if "student" in query_lower:
                return {
                    "query": query,
                    "interpretation": "Get top performing students",
                    "results": self.get_top_students(limit=10)
                }
        
        # Default response
        return {
            "query": query,
            "interpretation": "Unable to interpret query",
            "suggestion": "Try queries like 'list all students', 'show all teachers', 'top students', etc.",
            "results": []
        }
    
    def search_students(self, name: str) -> List[Dict]:
        """Search for students by name."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM students 
            WHERE name LIKE ? 
            ORDER BY name
        """, (f"%{name}%",))
        return [dict(row) for row in cursor.fetchall()]
    
    def search_teachers_by_subject(self, subject: str) -> List[Dict]:
        """Search for teachers by subject."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM teachers 
            WHERE subject LIKE ? 
            ORDER BY name
        """, (f"%{subject}%",))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_student_averages(self) -> List[Dict]:
        """Calculate average grades for all students."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                s.id, 
                s.name, 
                s.grade_level,
                AVG(g.grade) as average_grade,
                COUNT(g.id) as total_grades
            FROM students s
            LEFT JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            ORDER BY average_grade DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_top_students(self, limit: int = 10) -> List[Dict]:
        """Get top performing students based on average grades."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                s.id, 
                s.name, 
                s.grade_level,
                AVG(g.grade) as average_grade,
                COUNT(g.id) as total_grades
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            HAVING COUNT(g.id) > 0
            ORDER BY average_grade DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def recommend_courses_for_student(self, student_id: int) -> List[Dict]:
        """
        AI-powered course recommendations based on student's performance and interests.
        Recommends courses in subjects where student performs well.
        """
        cursor = self.conn.cursor()
        
        # Get student's best performing subjects
        cursor.execute("""
            SELECT c.subject, AVG(g.grade) as avg_grade
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = ?
            GROUP BY c.subject
            ORDER BY avg_grade DESC
            LIMIT 3
        """, (student_id,))
        
        top_subjects = [row['subject'] for row in cursor.fetchall()]
        
        if not top_subjects:
            # No grades yet, recommend popular courses
            cursor.execute("""
                SELECT c.*, t.name as teacher_name, COUNT(e.id) as enrollment_count
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.id
                LEFT JOIN enrollments e ON c.id = e.course_id
                GROUP BY c.id
                ORDER BY enrollment_count DESC
                LIMIT 5
            """)
        else:
            # Recommend courses in top subjects not yet enrolled
            placeholders = ','.join(['?' for _ in top_subjects])
            cursor.execute(f"""
                SELECT c.*, t.name as teacher_name
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.id
                WHERE c.subject IN ({placeholders})
                AND c.id NOT IN (
                    SELECT course_id FROM enrollments WHERE student_id = ?
                )
                LIMIT 5
            """, top_subjects + [student_id])
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        cursor = self.conn.cursor()
        
        # Count totals
        cursor.execute("SELECT COUNT(*) as count FROM students")
        student_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM teachers")
        teacher_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM courses")
        course_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM grades")
        grade_count = cursor.fetchone()['count']
        
        # Average grade
        cursor.execute("SELECT AVG(grade) as avg_grade FROM grades")
        avg_grade = cursor.fetchone()['avg_grade'] or 0
        
        return {
            "total_students": student_count,
            "total_teachers": teacher_count,
            "total_courses": course_count,
            "total_grades": grade_count,
            "overall_average_grade": round(avg_grade, 2)
        }
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

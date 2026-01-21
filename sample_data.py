"""
Sample Data Generator for School Database
Creates realistic sample data for testing and demonstration
"""

from school_database import SchoolDatabase
import random


def generate_sample_data(db: SchoolDatabase):
    """Generate sample data for the school database."""
    
    print("Generating sample data...")
    
    # Sample student names
    student_names = [
        "Emma Johnson", "Liam Smith", "Olivia Brown", "Noah Davis",
        "Ava Wilson", "Elijah Martinez", "Sophia Anderson", "James Taylor",
        "Isabella Thomas", "William Jackson", "Mia White", "Benjamin Harris",
        "Charlotte Martin", "Lucas Thompson", "Amelia Garcia", "Mason Rodriguez",
        "Harper Lee", "Ethan Clark", "Evelyn Lewis", "Alexander Walker"
    ]
    
    # Sample teacher names and subjects
    teachers = [
        ("Dr. Sarah Mitchell", "Mathematics", "sarah.mitchell@school.edu", 10),
        ("Prof. John Peterson", "Science", "john.peterson@school.edu", 15),
        ("Ms. Emily Chen", "English", "emily.chen@school.edu", 7),
        ("Mr. David Lopez", "History", "david.lopez@school.edu", 12),
        ("Dr. Maria Garcia", "Physics", "maria.garcia@school.edu", 8),
        ("Mr. Robert Kim", "Chemistry", "robert.kim@school.edu", 6),
        ("Ms. Jennifer Brown", "Biology", "jennifer.brown@school.edu", 9),
        ("Prof. Michael Wong", "Computer Science", "michael.wong@school.edu", 11)
    ]
    
    # Add teachers
    print("\nAdding teachers...")
    teacher_ids = []
    for name, subject, email, years in teachers:
        tid = db.add_teacher(name, subject, email, years)
        teacher_ids.append(tid)
        print(f"  Added: {name} ({subject})")
    
    # Add students
    print("\nAdding students...")
    student_ids = []
    for i, name in enumerate(student_names):
        age = random.randint(14, 18)
        grade_level = random.randint(9, 12)
        email = f"{name.lower().replace(' ', '.')}@student.school.edu"
        sid = db.add_student(name, age, grade_level, email)
        student_ids.append(sid)
        print(f"  Added: {name} (Grade {grade_level})")
    
    # Add courses
    print("\nAdding courses...")
    courses = [
        ("Algebra I", "Mathematics", 0, 30),
        ("Geometry", "Mathematics", 0, 25),
        ("General Science", "Science", 1, 30),
        ("English Literature", "English", 2, 28),
        ("World History", "History", 3, 32),
        ("Physics I", "Physics", 4, 25),
        ("Chemistry I", "Chemistry", 5, 25),
        ("Biology I", "Biology", 6, 30),
        ("Introduction to Programming", "Computer Science", 7, 20),
        ("Advanced Mathematics", "Mathematics", 0, 20)
    ]
    
    course_ids = []
    for name, subject, teacher_idx, capacity in courses:
        cid = db.add_course(name, subject, teacher_ids[teacher_idx], capacity)
        course_ids.append(cid)
        print(f"  Added: {name} (Teacher: {teachers[teacher_idx][0]})")
    
    # Enroll students in courses
    print("\nEnrolling students in courses...")
    enrollment_count = 0
    for sid in student_ids:
        # Each student enrolls in 3-6 courses
        num_courses = random.randint(3, 6)
        selected_courses = random.sample(course_ids, num_courses)
        for cid in selected_courses:
            db.enroll_student(sid, cid)
            enrollment_count += 1
    print(f"  Created {enrollment_count} enrollments")
    
    # Add grades
    print("\nAdding grades...")
    semesters = ["Fall 2024", "Spring 2025"]
    grade_count = 0
    
    for sid in student_ids:
        # Get student's courses
        courses = db.get_student_courses(sid)
        for course in courses:
            for semester in semesters:
                # Generate realistic grades (70-100)
                grade = round(random.uniform(70, 100), 2)
                db.add_grade(sid, course['id'], grade, semester)
                grade_count += 1
    
    print(f"  Created {grade_count} grade records")
    print("\nSample data generation complete!")


if __name__ == "__main__":
    # Create and populate database
    with SchoolDatabase("school.db") as db:
        generate_sample_data(db)
        
        # Display statistics
        print("\n" + "="*50)
        print("DATABASE STATISTICS")
        print("="*50)
        stats = db.get_statistics()
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

#!/usr/bin/env python3
"""
AI-Powered School Database Demo
Demonstrates the natural language query and AI features
"""

from school_database import SchoolDatabase
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_results(results, max_items=5):
    """Print results in a formatted way."""
    if isinstance(results, list):
        if not results:
            print("  No results found.")
            return
        
        print(f"  Found {len(results)} result(s):")
        for i, item in enumerate(results[:max_items], 1):
            print(f"\n  {i}. {json.dumps(item, indent=4)}")
        
        if len(results) > max_items:
            print(f"\n  ... and {len(results) - max_items} more")
    elif isinstance(results, dict):
        print(f"  {json.dumps(results, indent=2)}")
    else:
        print(f"  {results}")


def demo_basic_operations(db):
    """Demonstrate basic CRUD operations."""
    print_section("BASIC DATABASE OPERATIONS")
    
    # Get all students
    print("\n1. Getting all students:")
    students = db.get_all_students()
    print(f"   Total students: {len(students)}")
    if students:
        print(f"   First student: {students[0]['name']} (Grade {students[0]['grade_level']})")
    
    # Get all teachers
    print("\n2. Getting all teachers:")
    teachers = db.get_all_teachers()
    print(f"   Total teachers: {len(teachers)}")
    if teachers:
        print(f"   First teacher: {teachers[0]['name']} ({teachers[0]['subject']})")
    
    # Get all courses
    print("\n3. Getting all courses:")
    courses = db.get_all_courses()
    print(f"   Total courses: {len(courses)}")
    if courses:
        print(f"   First course: {courses[0]['name']} - {courses[0]['teacher_name']}")


def demo_ai_queries(db):
    """Demonstrate AI-powered natural language queries."""
    print_section("AI-POWERED NATURAL LANGUAGE QUERIES")
    
    queries = [
        "List all students",
        "Show all teachers",
        "List all courses",
        "Show me the top students",
        "Get student averages",
        "Find teacher teaching Mathematics",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: '{query}'")
        result = db.natural_language_query(query)
        print(f"   Interpretation: {result['interpretation']}")
        
        if 'results' in result:
            results = result['results']
            if isinstance(results, list):
                print(f"   Results: {len(results)} item(s)")
                if results and len(results) <= 3:
                    for item in results:
                        if 'name' in item:
                            print(f"     - {item['name']}")
            else:
                print(f"   Results: {results}")
        
        if 'suggestion' in result:
            print(f"   Suggestion: {result['suggestion']}")


def demo_student_details(db):
    """Demonstrate detailed student information."""
    print_section("DETAILED STUDENT INFORMATION")
    
    students = db.get_all_students()
    if not students:
        print("  No students in database")
        return
    
    # Pick first student
    student = students[0]
    print(f"\nStudent: {student['name']} (ID: {student['id']})")
    print(f"Grade Level: {student['grade_level']}, Age: {student['age']}")
    print(f"Email: {student['email']}")
    
    # Get courses
    print(f"\nEnrolled Courses:")
    courses = db.get_student_courses(student['id'])
    for course in courses:
        print(f"  - {course['name']} (Teacher: {course['teacher_name']})")
    
    # Get grades
    print(f"\nGrades:")
    grades = db.get_student_grades(student['id'])
    if grades:
        total = sum(g['grade'] for g in grades)
        avg = total / len(grades)
        print(f"  Total grades: {len(grades)}, Average: {avg:.2f}")
        
        # Show a few grades
        for grade in grades[:5]:
            print(f"  - {grade['course_name']}: {grade['grade']:.2f} ({grade['semester']})")


def demo_ai_recommendations(db):
    """Demonstrate AI-powered course recommendations."""
    print_section("AI-POWERED COURSE RECOMMENDATIONS")
    
    students = db.get_all_students()
    if not students:
        print("  No students in database")
        return
    
    # Get recommendations for first student
    student = students[0]
    print(f"\nCourse Recommendations for: {student['name']}")
    
    recommendations = db.recommend_courses_for_student(student['id'])
    if recommendations:
        print(f"\nRecommended {len(recommendations)} course(s):")
        for i, course in enumerate(recommendations, 1):
            teacher = course.get('teacher_name', 'TBA')
            print(f"  {i}. {course['name']} ({course['subject']}) - {teacher}")
    else:
        print("  No recommendations available")


def demo_statistics(db):
    """Demonstrate database statistics."""
    print_section("DATABASE STATISTICS")
    
    stats = db.get_statistics()
    print("\nOverall Statistics:")
    for key, value in stats.items():
        label = key.replace('_', ' ').title()
        print(f"  {label}: {value}")
    
    print("\nTop Performing Students:")
    top_students = db.get_top_students(5)
    for i, student in enumerate(top_students, 1):
        print(f"  {i}. {student['name']}: {student['average_grade']:.2f} "
              f"(Grade {student['grade_level']}, {student['total_grades']} grades)")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("  AI-POWERED SCHOOL DATABASE SYSTEM")
    print("  Demonstration and Testing")
    print("="*60)
    
    # Open database
    with SchoolDatabase("school.db") as db:
        # Run demonstrations
        demo_basic_operations(db)
        demo_ai_queries(db)
        demo_student_details(db)
        demo_ai_recommendations(db)
        demo_statistics(db)
    
    print("\n" + "="*60)
    print("  DEMONSTRATION COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

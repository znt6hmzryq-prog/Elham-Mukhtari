# AI-Powered School Database System

A comprehensive, intelligent database system for managing school data with AI-powered natural language query capabilities.

## Features

### Core Database Management
- **Student Management**: Add, update, delete, and search students
- **Teacher Management**: Manage teacher profiles and assignments
- **Course Management**: Create and manage courses with teacher assignments
- **Grade Management**: Track and analyze student grades
- **Enrollment System**: Manage student course enrollments

### AI-Powered Features
- **Natural Language Queries**: Ask questions in plain English
- **Intelligent Search**: Find students, teachers, and courses with smart matching
- **Course Recommendations**: AI-powered course suggestions based on student performance
- **Performance Analytics**: Automatic calculation of averages and statistics
- **Top Performers**: Identify high-achieving students

## Installation

No external dependencies required! This system uses Python's built-in SQLite database.

### Requirements
- Python 3.6 or higher

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd Elham-Mukhtari
```

2. Generate sample data:
```bash
python3 sample_data.py
```

3. Run the demo:
```bash
python3 demo.py
```

## Usage

### Basic Usage

```python
from school_database import SchoolDatabase

# Create/open database
db = SchoolDatabase("school.db")

# Add a student
student_id = db.add_student(
    name="John Doe",
    age=16,
    grade_level=10,
    email="john.doe@student.school.edu"
)

# Add a teacher
teacher_id = db.add_teacher(
    name="Dr. Jane Smith",
    subject="Mathematics",
    email="jane.smith@school.edu",
    years_experience=5
)

# Add a course
course_id = db.add_course(
    name="Algebra I",
    subject="Mathematics",
    teacher_id=teacher_id,
    capacity=30
)

# Enroll student in course
db.enroll_student(student_id, course_id)

# Add a grade
db.add_grade(student_id, course_id, 95.5, "Fall 2024")

# Close database when done
db.close()
```

### Using Context Manager

```python
with SchoolDatabase("school.db") as db:
    students = db.get_all_students()
    for student in students:
        print(f"{student['name']} - Grade {student['grade_level']}")
```

### Natural Language Queries

The AI-powered query system understands natural language:

```python
# List all students
result = db.natural_language_query("List all students")
print(result['results'])

# Find teachers by subject
result = db.natural_language_query("Show me teachers teaching Mathematics")
print(result['results'])

# Get top performers
result = db.natural_language_query("Who are the top students?")
print(result['results'])

# Get averages
result = db.natural_language_query("Show student averages")
print(result['results'])
```

### AI-Powered Recommendations

Get personalized course recommendations:

```python
# Get recommendations for a student
recommendations = db.recommend_courses_for_student(student_id)
for course in recommendations:
    print(f"{course['name']} - {course['subject']}")
```

### Analytics and Statistics

```python
# Get overall statistics
stats = db.get_statistics()
print(f"Total Students: {stats['total_students']}")
print(f"Average Grade: {stats['overall_average_grade']}")

# Get top students
top_students = db.get_top_students(10)
for student in top_students:
    print(f"{student['name']}: {student['average_grade']:.2f}")

# Get student averages
averages = db.get_student_averages()
for student in averages:
    print(f"{student['name']}: {student['average_grade']:.2f}")
```

## Database Schema

### Students Table
- `id`: Primary key
- `name`: Student name
- `age`: Student age
- `grade_level`: Grade level (9-12)
- `email`: Student email (unique)
- `enrollment_date`: Date of enrollment
- `created_at`: Record creation timestamp

### Teachers Table
- `id`: Primary key
- `name`: Teacher name
- `subject`: Subject taught
- `email`: Teacher email (unique)
- `years_experience`: Years of teaching experience
- `created_at`: Record creation timestamp

### Courses Table
- `id`: Primary key
- `name`: Course name
- `subject`: Course subject
- `teacher_id`: Foreign key to teachers
- `capacity`: Maximum enrollment
- `created_at`: Record creation timestamp

### Grades Table
- `id`: Primary key
- `student_id`: Foreign key to students
- `course_id`: Foreign key to courses
- `grade`: Numeric grade
- `semester`: Semester identifier
- `created_at`: Record creation timestamp

### Enrollments Table
- `id`: Primary key
- `student_id`: Foreign key to students
- `course_id`: Foreign key to courses
- `enrollment_date`: Date of enrollment
- `created_at`: Record creation timestamp

## API Reference

### Student Operations
- `add_student(name, age, grade_level, email, enrollment_date=None)` - Add new student
- `get_student(student_id)` - Get student by ID
- `get_all_students()` - Get all students
- `update_student(student_id, **kwargs)` - Update student information
- `delete_student(student_id)` - Delete student
- `search_students(name)` - Search students by name

### Teacher Operations
- `add_teacher(name, subject, email, years_experience=0)` - Add new teacher
- `get_teacher(teacher_id)` - Get teacher by ID
- `get_all_teachers()` - Get all teachers
- `search_teachers_by_subject(subject)` - Search teachers by subject

### Course Operations
- `add_course(name, subject, teacher_id, capacity=30)` - Add new course
- `get_course(course_id)` - Get course by ID
- `get_all_courses()` - Get all courses

### Grade Operations
- `add_grade(student_id, course_id, grade, semester)` - Add grade
- `get_student_grades(student_id)` - Get all grades for a student
- `get_course_grades(course_id)` - Get all grades for a course

### Enrollment Operations
- `enroll_student(student_id, course_id)` - Enroll student in course
- `get_student_courses(student_id)` - Get courses for a student
- `get_course_students(course_id)` - Get students in a course

### AI-Powered Features
- `natural_language_query(query)` - Process natural language queries
- `recommend_courses_for_student(student_id)` - Get AI recommendations
- `get_student_averages()` - Calculate all student averages
- `get_top_students(limit=10)` - Get top performing students
- `get_statistics()` - Get database statistics

## Examples

### Example 1: Complete Workflow

```python
from school_database import SchoolDatabase

with SchoolDatabase("my_school.db") as db:
    # Create a teacher
    teacher_id = db.add_teacher(
        "Dr. Smith",
        "Physics",
        "dr.smith@school.edu",
        10
    )
    
    # Create a course
    course_id = db.add_course(
        "Physics 101",
        "Physics",
        teacher_id,
        25
    )
    
    # Add students and enroll them
    for i in range(5):
        student_id = db.add_student(
            f"Student {i+1}",
            15 + i,
            9 + (i % 4),
            f"student{i+1}@school.edu"
        )
        db.enroll_student(student_id, course_id)
        db.add_grade(student_id, course_id, 80 + i*3, "Fall 2024")
    
    # Get course statistics
    grades = db.get_course_grades(course_id)
    avg = sum(g['grade'] for g in grades) / len(grades)
    print(f"Course average: {avg:.2f}")
```

### Example 2: Natural Language Interface

```python
with SchoolDatabase("school.db") as db:
    # Interactive query loop
    queries = [
        "List all students",
        "Show top students",
        "Find teachers teaching Science",
        "Get student averages"
    ]
    
    for query in queries:
        result = db.natural_language_query(query)
        print(f"\nQuery: {query}")
        print(f"Found: {len(result['results'])} results")
```

## Testing

Run the demo script to see all features in action:

```bash
python3 demo.py
```

This will demonstrate:
- Basic CRUD operations
- Natural language queries
- Student details and grades
- AI-powered recommendations
- Database statistics

## License

This project is part of a school management system.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For questions or support, please open an issue in the repository.

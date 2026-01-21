# Elham-Mukhtari School Database

An AI-powered database system for school management with intelligent query capabilities.

## 🚀 Quick Start

```bash
# Generate sample data
python3 sample_data.py

# Run the interactive CLI
python3 interactive_cli.py

# Or run the full demo
python3 demo.py
```

## ✨ Features

- **Complete School Management**: Students, Teachers, Courses, Grades
- **AI-Powered Natural Language Queries**: Ask questions in plain English
- **Interactive CLI**: User-friendly command-line interface
- **Intelligent Recommendations**: Smart course suggestions based on performance
- **Analytics**: Automatic performance tracking and statistics
- **Zero External Dependencies**: Uses Python's built-in SQLite

## 🎮 Interactive Mode

The interactive CLI allows you to query the database using natural language:

```bash
$ python3 interactive_cli.py

🔍 Query: List all students
✓ Found 20 result(s)

🔍 Query: Show me the top students
✓ Found 10 result(s)

🔍 Query: Find teacher teaching Mathematics
✓ Found 1 result(s)
```

## 📚 Documentation

See [DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md) for complete API reference and examples.

## 🎯 Example Usage

```python
from school_database import SchoolDatabase

with SchoolDatabase("school.db") as db:
    # Natural language queries
    result = db.natural_language_query("Show me the top students")
    
    # Get AI recommendations
    recommendations = db.recommend_courses_for_student(student_id)
    
    # Get statistics
    stats = db.get_statistics()
```

## 🏗️ Project Structure

- `school_database.py` - Core database system with AI features
- `interactive_cli.py` - Interactive command-line interface
- `sample_data.py` - Sample data generator
- `demo.py` - Automated demonstration
- `DATABASE_DOCUMENTATION.md` - Complete documentation

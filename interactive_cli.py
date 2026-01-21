#!/usr/bin/env python3
"""
Interactive CLI for AI-Powered School Database
Provides a user-friendly interface for database queries
"""

from school_database import SchoolDatabase
import sys


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("  AI-POWERED SCHOOL DATABASE")
    print("  Interactive Query Interface")
    print("="*60)


def print_help():
    """Print help information."""
    print("\nAvailable Commands:")
    print("  - List all students")
    print("  - Show all teachers")
    print("  - List all courses")
    print("  - Show me the top students")
    print("  - Find teacher teaching [subject]")
    print("  - Search for student named [name]")
    print("  - Get statistics")
    print("  - Help - Show this help message")
    print("  - Exit/Quit - Exit the application")
    print("\nYou can also ask questions in natural language!")


def format_results(result):
    """Format query results for display."""
    if 'interpretation' in result:
        print(f"\n📊 Interpretation: {result['interpretation']}")
    
    if 'suggestion' in result:
        print(f"💡 Suggestion: {result['suggestion']}")
    
    if 'results' in result:
        results = result['results']
        if isinstance(results, list):
            if not results:
                print("   No results found.")
                return
            
            print(f"\n✓ Found {len(results)} result(s):\n")
            
            # Format based on content type
            for i, item in enumerate(results[:10], 1):
                if 'name' in item:
                    name = item['name']
                    details = []
                    
                    if 'subject' in item:
                        details.append(f"Subject: {item['subject']}")
                    if 'grade_level' in item:
                        details.append(f"Grade: {item['grade_level']}")
                    if 'average_grade' in item and item['average_grade']:
                        details.append(f"Average: {item['average_grade']:.2f}")
                    if 'teacher_name' in item:
                        details.append(f"Teacher: {item['teacher_name']}")
                    
                    detail_str = ', '.join(details) if details else ''
                    print(f"  {i}. {name}" + (f" ({detail_str})" if detail_str else ""))
            
            if len(results) > 10:
                print(f"\n  ... and {len(results) - 10} more")
        else:
            print(f"\n{results}")


def main():
    """Main interactive loop."""
    print_header()
    print("\nWelcome! Type 'help' for available commands or ask a question.")
    
    db = SchoolDatabase("school.db")
    
    try:
        while True:
            try:
                # Get user input
                query = input("\n🔍 Query: ").strip()
                
                if not query:
                    continue
                
                # Handle special commands
                query_lower = query.lower()
                
                if query_lower in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if query_lower in ['help', 'h', '?']:
                    print_help()
                    continue
                
                if 'statistic' in query_lower or query_lower == 'stats':
                    stats = db.get_statistics()
                    print("\n📈 Database Statistics:")
                    for key, value in stats.items():
                        label = key.replace('_', ' ').title()
                        print(f"   {label}: {value}")
                    continue
                
                # Process natural language query
                result = db.natural_language_query(query)
                format_results(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("   Please try again or type 'help' for assistance.")
    
    finally:
        db.close()


if __name__ == "__main__":
    main()

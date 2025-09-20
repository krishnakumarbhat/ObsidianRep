"""
Initialization service for automatic data ingestion on startup.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
import os
import asyncio
from typing import Optional
from repositories.interfaces import IVectorRepository
from repositories.vector_repository import DocumentIngestionService
import config


class InitializationService:
    """Service for handling application initialization and data ingestion."""
    
    def __init__(self, vector_repo: IVectorRepository):
        self.vector_repo = vector_repo
        self.ingestion_service = DocumentIngestionService(vector_repo)
    
    async def initialize_application(self) -> bool:
        """Initialize the application with automatic data ingestion if needed."""
        print("Initializing RecallMind application...")
        
        try:
            # Check if vector database is empty
            is_empty = await self.vector_repo.is_empty()
            
            if is_empty:
                print("Vector database is empty. Starting automatic data ingestion...")
                success = await self._ingest_data()
                if success:
                    print("Data ingestion completed successfully.")
                else:
                    print("Data ingestion failed. Application will continue with empty database.")
                    return False
            else:
                print("Vector database contains data. Skipping ingestion.")
            
            print("Application initialization completed successfully.")
            return True
            
        except Exception as e:
            print(f"Error during application initialization: {e}")
            return False
    
    async def _ingest_data(self) -> bool:
        """Ingest data from the configured data directory."""
        data_directory = config.DATA_DIRECTORY
        
        # Check if data directory exists
        if not os.path.exists(data_directory):
            print(f"Data directory does not exist: {data_directory}")
            print("Creating example data directory...")
            return await self._create_example_data()
        
        # Check if data directory has markdown files
        md_files = self._find_markdown_files(data_directory)
        if not md_files:
            print(f"No markdown files found in {data_directory}")
            print("Creating example data...")
            return await self._create_example_data()
        
        # Ingest existing data
        return await self.ingestion_service.ingest_from_directory(data_directory)
    
    async def _create_example_data(self) -> bool:
        """Create example data if no data directory or files exist."""
        data_directory = config.DATA_DIRECTORY
        
        try:
            # Create data directory
            os.makedirs(data_directory, exist_ok=True)
            
            # Create example markdown files
            example_files = [
                {
                    "filename": "welcome.md",
                    "content": """# Welcome to RecallMind

This is your personal study assistant powered by AI and vector search.

## Features

- **Flashcard Management**: Create and organize study decks
- **AI-Powered Q&A**: Ask questions about your study materials
- **Study Sessions**: Track your learning progress
- **Quiz Generation**: Test your knowledge with AI-generated quizzes

## Getting Started

1. Add your study materials as markdown files in this directory
2. Create flashcard decks in the application
3. Start studying and ask questions!

## Study Tips

- Break down complex topics into smaller chunks
- Review regularly using spaced repetition
- Use the AI assistant to clarify difficult concepts
- Track your progress to stay motivated
"""
                },
                {
                    "filename": "sample-notes.md",
                    "content": """# Sample Study Notes

## Python Programming

### Variables and Data Types
- **String**: Text data enclosed in quotes
- **Integer**: Whole numbers
- **Float**: Decimal numbers
- **Boolean**: True or False values

### Control Structures
- **If statements**: Conditional execution
- **Loops**: For and while loops for repetition
- **Functions**: Reusable code blocks

### Data Structures
- **Lists**: Ordered, mutable collections
- **Dictionaries**: Key-value pairs
- **Tuples**: Ordered, immutable collections

## Study Questions

1. What is the difference between a list and a tuple?
2. How do you create a function in Python?
3. What are the main data types in Python?
"""
                },
                {
                    "filename": "mathematics.md",
                    "content": """# Mathematics Fundamentals

## Algebra

### Linear Equations
A linear equation is an equation of the form: ax + b = 0

Where:
- a and b are constants
- x is the variable
- a ≠ 0

### Quadratic Equations
A quadratic equation is of the form: ax² + bx + c = 0

The quadratic formula is: x = (-b ± √(b² - 4ac)) / 2a

## Geometry

### Area Formulas
- **Rectangle**: A = length × width
- **Circle**: A = πr²
- **Triangle**: A = ½ × base × height

### Volume Formulas
- **Cube**: V = s³
- **Cylinder**: V = πr²h
- **Sphere**: V = (4/3)πr³

## Calculus

### Derivatives
The derivative of a function f(x) is f'(x) = lim(h→0) [f(x+h) - f(x)] / h

### Integration
The integral of a function f(x) is ∫f(x)dx = F(x) + C
"""
                }
            ]
            
            # Write example files
            for file_info in example_files:
                file_path = os.path.join(data_directory, file_info["filename"])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
            
            print(f"Created {len(example_files)} example files in {data_directory}")
            
            # Now ingest the example data
            return await self.ingestion_service.ingest_from_directory(data_directory)
            
        except Exception as e:
            print(f"Error creating example data: {e}")
            return False
    
    def _find_markdown_files(self, directory: str) -> list:
        """Find all markdown files in a directory recursively."""
        md_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        return md_files
    
    async def reingest_data(self) -> bool:
        """Force re-ingestion of all data."""
        print("Starting data re-ingestion...")
        
        try:
            # Clear existing data
            await self.vector_repo.clear()
            
            # Ingest fresh data
            return await self._ingest_data()
            
        except Exception as e:
            print(f"Error during data re-ingestion: {e}")
            return False
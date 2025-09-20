"""
Test service implementing business logic for quiz and test operations.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
from typing import List, Optional
from datetime import datetime
import uuid
from domain.entities import Test, TestType
from domain.value_objects import QuizQuestion
from repositories.interfaces import ITestRepository, IFlashcardRepository


class TestService:
    """Service for managing test business logic."""
    
    def __init__(self, test_repo: ITestRepository, flashcard_repo: IFlashcardRepository):
        self.test_repo = test_repo
        self.flashcard_repo = flashcard_repo
    
    async def create_test(self, deck_id: str, test_type: str, 
                         questions_count: int) -> Test:
        """Create a new test."""
        # Validate test type
        try:
            test_type_enum = TestType(test_type.lower())
        except ValueError:
            raise ValueError(f"Invalid test type: {test_type}")
        
        # Validate questions count
        if questions_count <= 0:
            raise ValueError("Questions count must be positive")
        
        # Get flashcards for the deck
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        if len(flashcards) < questions_count:
            raise ValueError("Not enough flashcards in deck for requested questions count")
        
        test = Test(
            id=str(uuid.uuid4()),
            deck_id=deck_id,
            test_type=test_type_enum,
            questions_count=questions_count,
            score=0,  # Will be updated when test is completed
            correct_answers=0,
            total_questions=questions_count,
            duration=0,  # Will be updated when test is completed
            completed_at=datetime.now()
        )
        
        return await self.test_repo.create(test)
    
    async def submit_test_results(self, test_id: str, correct_answers: int, 
                                 total_questions: int, duration: int) -> Optional[Test]:
        """Submit test results and calculate score."""
        if correct_answers < 0 or correct_answers > total_questions:
            raise ValueError("Invalid correct answers count")
        
        if total_questions <= 0:
            raise ValueError("Total questions must be positive")
        
        if duration < 0:
            raise ValueError("Duration must be non-negative")
        
        score = int((correct_answers / total_questions) * 100)
        
        update_data = {
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "duration": duration,
            "completed_at": datetime.now()
        }
        
        return await self.test_repo.update(test_id, update_data)
    
    async def get_tests_by_deck(self, deck_id: str) -> List[Test]:
        """Get all tests for a deck."""
        return await self.test_repo.get_by_deck_id(deck_id)
    
    async def get_test_by_id(self, test_id: str) -> Optional[Test]:
        """Get a test by ID."""
        return await self.test_repo.get_by_id(test_id)
    
    def calculate_test_score(self, correct_answers: int, total_questions: int) -> int:
        """Calculate test score as percentage."""
        if total_questions == 0:
            return 0
        return int((correct_answers / total_questions) * 100)
    
    def format_duration(self, duration_seconds: int) -> str:
        """Format duration in a human-readable format."""
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
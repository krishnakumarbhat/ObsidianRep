"""
Domain entities representing the core business objects.
Following the Single Responsibility Principle, each entity has a clear purpose.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class DifficultyLevel(Enum):
    """Enum for difficulty levels following the Open/Closed Principle."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class TestType(Enum):
    """Enum for test types following the Open/Closed Principle."""
    MULTIPLE_CHOICE = "multiple-choice"
    FLASHCARD = "flashcard"


class ReviewDifficulty(Enum):
    """Enum for card review difficulty following the Open/Closed Principle."""
    EASY = "easy"
    OKAY = "okay"
    DIFFICULT = "difficult"


@dataclass
class Deck:
    """Deck entity representing a collection of flashcards."""
    id: str
    name: str
    description: Optional[str]
    difficulty: DifficultyLevel
    card_count: int
    created_at: datetime
    last_studied: Optional[datetime] = None

    def __post_init__(self):
        """Validate deck data after initialization."""
        if not self.name.strip():
            raise ValueError("Deck name cannot be empty")
        if self.card_count < 0:
            raise ValueError("Card count cannot be negative")


@dataclass
class Flashcard:
    """Flashcard entity representing a question-answer pair."""
    id: str
    deck_id: str
    question: str
    answer: str
    created_at: datetime

    def __post_init__(self):
        """Validate flashcard data after initialization."""
        if not self.question.strip():
            raise ValueError("Question cannot be empty")
        if not self.answer.strip():
            raise ValueError("Answer cannot be empty")


@dataclass
class StudySession:
    """Study session entity representing a learning session."""
    id: str
    deck_id: str
    start_time: datetime
    end_time: Optional[datetime]
    cards_studied: int
    duration: int  # in seconds

    def __post_init__(self):
        """Validate study session data after initialization."""
        if self.cards_studied < 0:
            raise ValueError("Cards studied cannot be negative")
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")


@dataclass
class CardReview:
    """Card review entity representing a user's rating of a card."""
    id: str
    session_id: str
    card_id: str
    difficulty: ReviewDifficulty
    reviewed_at: datetime


@dataclass
class Test:
    """Test entity representing a quiz or test."""
    id: str
    deck_id: str
    test_type: TestType
    questions_count: int
    score: int  # percentage
    correct_answers: int
    total_questions: int
    duration: int  # in seconds
    completed_at: datetime

    def __post_init__(self):
        """Validate test data after initialization."""
        if not 0 <= self.score <= 100:
            raise ValueError("Score must be between 0 and 100")
        if self.correct_answers < 0:
            raise ValueError("Correct answers cannot be negative")
        if self.total_questions <= 0:
            raise ValueError("Total questions must be positive")


@dataclass
class ChatMessage:
    """Chat message entity representing a Q&A interaction."""
    id: str
    question: str
    answer: str
    relevant_cards: List[str]  # card IDs used for context
    created_at: datetime

    def __post_init__(self):
        """Validate chat message data after initialization."""
        if not self.question.strip():
            raise ValueError("Question cannot be empty")
        if not self.answer.strip():
            raise ValueError("Answer cannot be empty")


@dataclass
class UserStats:
    """User statistics entity representing learning progress."""
    id: str
    study_streak: int
    total_decks: int
    cards_studied: int
    study_time: int  # in seconds
    last_study_date: Optional[datetime]
    updated_at: datetime

    def __post_init__(self):
        """Validate user stats data after initialization."""
        if self.study_streak < 0:
            raise ValueError("Study streak cannot be negative")
        if self.total_decks < 0:
            raise ValueError("Total decks cannot be negative")
        if self.cards_studied < 0:
            raise ValueError("Cards studied cannot be negative")
        if self.study_time < 0:
            raise ValueError("Study time cannot be negative")
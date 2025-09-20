"""
Value objects representing concepts that are defined by their attributes.
Following the Single Responsibility Principle and Immutability principle.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class QuizQuestion:
    """Value object representing a quiz question."""
    question: str
    options: List[str]
    correct_answer: int  # index of correct option
    explanation: Optional[str] = None

    def __post_init__(self):
        """Validate quiz question data after initialization."""
        if not self.question.strip():
            raise ValueError("Question cannot be empty")
        if len(self.options) < 2:
            raise ValueError("Must have at least 2 options")
        if not 0 <= self.correct_answer < len(self.options):
            raise ValueError("Correct answer index out of range")


@dataclass(frozen=True)
class ChatResponse:
    """Value object representing a chat response."""
    answer: str
    relevant_cards: List[str]

    def __post_init__(self):
        """Validate chat response data after initialization."""
        if not self.answer.strip():
            raise ValueError("Answer cannot be empty")


@dataclass(frozen=True)
class StudyProgress:
    """Value object representing study progress."""
    current_card: int
    total_cards: int
    progress_percentage: float

    def __post_init__(self):
        """Validate study progress data after initialization."""
        if self.current_card < 0:
            raise ValueError("Current card cannot be negative")
        if self.total_cards <= 0:
            raise ValueError("Total cards must be positive")
        if not 0 <= self.progress_percentage <= 100:
            raise ValueError("Progress percentage must be between 0 and 100")


@dataclass(frozen=True)
class VectorSearchResult:
    """Value object representing a vector search result."""
    content: str
    metadata: dict
    similarity_score: float

    def __post_init__(self):
        """Validate vector search result data after initialization."""
        if not self.content.strip():
            raise ValueError("Content cannot be empty")
        if not 0 <= self.similarity_score <= 1:
            raise ValueError("Similarity score must be between 0 and 1")
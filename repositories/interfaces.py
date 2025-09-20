"""
Repository interfaces following the Dependency Inversion Principle.
These interfaces define contracts that concrete implementations must follow.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import (
    Deck, Flashcard, StudySession, CardReview, Test, 
    ChatMessage, UserStats
)
from domain.value_objects import QuizQuestion


class IDeckRepository(ABC):
    """Interface for deck data access operations."""
    
    @abstractmethod
    async def get_all(self) -> List[Deck]:
        """Get all decks."""
        pass
    
    @abstractmethod
    async def get_by_id(self, deck_id: str) -> Optional[Deck]:
        """Get deck by ID."""
        pass
    
    @abstractmethod
    async def create(self, deck: Deck) -> Deck:
        """Create a new deck."""
        pass
    
    @abstractmethod
    async def update(self, deck_id: str, deck_data: dict) -> Optional[Deck]:
        """Update an existing deck."""
        pass
    
    @abstractmethod
    async def delete(self, deck_id: str) -> bool:
        """Delete a deck."""
        pass


class IFlashcardRepository(ABC):
    """Interface for flashcard data access operations."""
    
    @abstractmethod
    async def get_by_deck_id(self, deck_id: str) -> List[Flashcard]:
        """Get all flashcards for a deck."""
        pass
    
    @abstractmethod
    async def create(self, flashcard: Flashcard) -> Flashcard:
        """Create a new flashcard."""
        pass
    
    @abstractmethod
    async def update(self, flashcard_id: str, flashcard_data: dict) -> Optional[Flashcard]:
        """Update an existing flashcard."""
        pass
    
    @abstractmethod
    async def delete(self, flashcard_id: str) -> bool:
        """Delete a flashcard."""
        pass


class IStudySessionRepository(ABC):
    """Interface for study session data access operations."""
    
    @abstractmethod
    async def create(self, session: StudySession) -> StudySession:
        """Create a new study session."""
        pass
    
    @abstractmethod
    async def update(self, session_id: str, session_data: dict) -> Optional[StudySession]:
        """Update an existing study session."""
        pass


class ICardReviewRepository(ABC):
    """Interface for card review data access operations."""
    
    @abstractmethod
    async def create(self, review: CardReview) -> CardReview:
        """Create a new card review."""
        pass


class ITestRepository(ABC):
    """Interface for test data access operations."""
    
    @abstractmethod
    async def create(self, test: Test) -> Test:
        """Create a new test."""
        pass
    
    @abstractmethod
    async def get_by_deck_id(self, deck_id: str) -> List[Test]:
        """Get all tests for a deck."""
        pass


class IChatMessageRepository(ABC):
    """Interface for chat message data access operations."""
    
    @abstractmethod
    async def get_all(self) -> List[ChatMessage]:
        """Get all chat messages."""
        pass
    
    @abstractmethod
    async def create(self, message: ChatMessage) -> ChatMessage:
        """Create a new chat message."""
        pass


class IUserStatsRepository(ABC):
    """Interface for user statistics data access operations."""
    
    @abstractmethod
    async def get(self) -> UserStats:
        """Get user statistics."""
        pass
    
    @abstractmethod
    async def update(self, updates: dict) -> UserStats:
        """Update user statistics."""
        pass


class IVectorRepository(ABC):
    """Interface for vector database operations."""
    
    @abstractmethod
    async def search_similar(self, query: str, limit: int = 5) -> List[dict]:
        """Search for similar content using vector similarity."""
        pass
    
    @abstractmethod
    async def add_documents(self, documents: List[dict]) -> bool:
        """Add documents to the vector database."""
        pass
    
    @abstractmethod
    async def is_empty(self) -> bool:
        """Check if the vector database is empty."""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all data from the vector database."""
        pass
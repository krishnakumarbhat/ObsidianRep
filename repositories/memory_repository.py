"""
In-memory repository implementation for development and testing.
Following the Single Responsibility Principle and Interface Segregation Principle.
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from repositories.interfaces import (
    IDeckRepository, IFlashcardRepository, IStudySessionRepository,
    ICardReviewRepository, ITestRepository, IChatMessageRepository,
    IUserStatsRepository
)
from domain.entities import (
    Deck, Flashcard, StudySession, CardReview, Test,
    ChatMessage, UserStats, DifficultyLevel, TestType, ReviewDifficulty
)


class MemoryDeckRepository(IDeckRepository):
    """In-memory implementation of deck repository."""
    
    def __init__(self):
        self._decks: Dict[str, Deck] = {}
    
    async def get_all(self) -> List[Deck]:
        return list(self._decks.values())
    
    async def get_by_id(self, deck_id: str) -> Optional[Deck]:
        return self._decks.get(deck_id)
    
    async def create(self, deck: Deck) -> Deck:
        if not deck.id:
            deck.id = str(uuid.uuid4())
        self._decks[deck.id] = deck
        return deck
    
    async def update(self, deck_id: str, deck_data: dict) -> Optional[Deck]:
        if deck_id not in self._decks:
            return None
        
        deck = self._decks[deck_id]
        for key, value in deck_data.items():
            if hasattr(deck, key):
                setattr(deck, key, value)
        return deck
    
    async def delete(self, deck_id: str) -> bool:
        if deck_id in self._decks:
            del self._decks[deck_id]
            return True
        return False


class MemoryFlashcardRepository(IFlashcardRepository):
    """In-memory implementation of flashcard repository."""
    
    def __init__(self):
        self._flashcards: Dict[str, Flashcard] = {}
    
    async def get_by_deck_id(self, deck_id: str) -> List[Flashcard]:
        return [card for card in self._flashcards.values() if card.deck_id == deck_id]
    
    async def create(self, flashcard: Flashcard) -> Flashcard:
        if not flashcard.id:
            flashcard.id = str(uuid.uuid4())
        self._flashcards[flashcard.id] = flashcard
        return flashcard
    
    async def update(self, flashcard_id: str, flashcard_data: dict) -> Optional[Flashcard]:
        if flashcard_id not in self._flashcards:
            return None
        
        flashcard = self._flashcards[flashcard_id]
        for key, value in flashcard_data.items():
            if hasattr(flashcard, key):
                setattr(flashcard, key, value)
        return flashcard
    
    async def delete(self, flashcard_id: str) -> bool:
        if flashcard_id in self._flashcards:
            del self._flashcards[flashcard_id]
            return True
        return False


class MemoryStudySessionRepository(IStudySessionRepository):
    """In-memory implementation of study session repository."""
    
    def __init__(self):
        self._sessions: Dict[str, StudySession] = {}
    
    async def create(self, session: StudySession) -> StudySession:
        if not session.id:
            session.id = str(uuid.uuid4())
        self._sessions[session.id] = session
        return session
    
    async def update(self, session_id: str, session_data: dict) -> Optional[StudySession]:
        if session_id not in self._sessions:
            return None
        
        session = self._sessions[session_id]
        for key, value in session_data.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session
    
    async def get_by_id(self, session_id: str) -> Optional[StudySession]:
        """Get study session by ID."""
        return self._sessions.get(session_id)


class MemoryCardReviewRepository(ICardReviewRepository):
    """In-memory implementation of card review repository."""
    
    def __init__(self):
        self._reviews: Dict[str, CardReview] = {}
    
    async def create(self, review: CardReview) -> CardReview:
        if not review.id:
            review.id = str(uuid.uuid4())
        self._reviews[review.id] = review
        return review


class MemoryTestRepository(ITestRepository):
    """In-memory implementation of test repository."""
    
    def __init__(self):
        self._tests: Dict[str, Test] = {}
    
    async def create(self, test: Test) -> Test:
        if not test.id:
            test.id = str(uuid.uuid4())
        self._tests[test.id] = test
        return test
    
    async def get_by_deck_id(self, deck_id: str) -> List[Test]:
        return [test for test in self._tests.values() if test.deck_id == deck_id]
    
    async def get_by_id(self, test_id: str) -> Optional[Test]:
        """Get test by ID."""
        return self._tests.get(test_id)
    
    async def update(self, test_id: str, test_data: dict) -> Optional[Test]:
        """Update test."""
        if test_id not in self._tests:
            return None
        
        test = self._tests[test_id]
        for key, value in test_data.items():
            if hasattr(test, key):
                setattr(test, key, value)
        return test


class MemoryChatMessageRepository(IChatMessageRepository):
    """In-memory implementation of chat message repository."""
    
    def __init__(self):
        self._messages: Dict[str, ChatMessage] = {}
    
    async def get_all(self) -> List[ChatMessage]:
        return list(self._messages.values())
    
    async def create(self, message: ChatMessage) -> ChatMessage:
        if not message.id:
            message.id = str(uuid.uuid4())
        self._messages[message.id] = message
        return message


class MemoryUserStatsRepository(IUserStatsRepository):
    """In-memory implementation of user stats repository."""
    
    def __init__(self):
        self._stats = UserStats(
            id=str(uuid.uuid4()),
            study_streak=0,
            total_decks=0,
            cards_studied=0,
            study_time=0,
            last_study_date=None,
            updated_at=datetime.now()
        )
    
    async def get(self) -> UserStats:
        return self._stats
    
    async def update(self, updates: dict) -> UserStats:
        for key, value in updates.items():
            if hasattr(self._stats, key):
                setattr(self._stats, key, value)
        self._stats.updated_at = datetime.now()
        return self._stats
"""
Deck service implementing business logic for deck operations.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
from typing import List, Optional
from datetime import datetime
import uuid
from domain.entities import Deck, DifficultyLevel
from repositories.interfaces import IDeckRepository, IFlashcardRepository


class DeckService:
    """Service for managing deck business logic."""
    
    def __init__(self, deck_repo: IDeckRepository, flashcard_repo: IFlashcardRepository):
        self.deck_repo = deck_repo
        self.flashcard_repo = flashcard_repo
    
    async def get_all_decks(self) -> List[Deck]:
        """Get all decks."""
        return await self.deck_repo.get_all()
    
    async def get_deck_by_id(self, deck_id: str) -> Optional[Deck]:
        """Get a deck by ID."""
        return await self.deck_repo.get_by_id(deck_id)
    
    async def create_deck(self, name: str, description: str = None, 
                         difficulty: str = "beginner") -> Deck:
        """Create a new deck with validation."""
        # Validate input
        if not name or not name.strip():
            raise ValueError("Deck name is required")
        
        # Convert difficulty string to enum
        try:
            difficulty_enum = DifficultyLevel(difficulty.lower())
        except ValueError:
            raise ValueError(f"Invalid difficulty level: {difficulty}")
        
        # Create deck
        deck = Deck(
            id=str(uuid.uuid4()),
            name=name.strip(),
            description=description.strip() if description else None,
            difficulty=difficulty_enum,
            card_count=0,
            created_at=datetime.now()
        )
        
        return await self.deck_repo.create(deck)
    
    async def update_deck(self, deck_id: str, name: str = None, 
                         description: str = None, difficulty: str = None) -> Optional[Deck]:
        """Update an existing deck."""
        # Validate input
        update_data = {}
        
        if name is not None:
            if not name.strip():
                raise ValueError("Deck name cannot be empty")
            update_data["name"] = name.strip()
        
        if description is not None:
            update_data["description"] = description.strip() if description else None
        
        if difficulty is not None:
            try:
                difficulty_enum = DifficultyLevel(difficulty.lower())
                update_data["difficulty"] = difficulty_enum
            except ValueError:
                raise ValueError(f"Invalid difficulty level: {difficulty}")
        
        return await self.deck_repo.update(deck_id, update_data)
    
    async def delete_deck(self, deck_id: str) -> bool:
        """Delete a deck and all its flashcards."""
        # Check if deck exists
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            return False
        
        # Delete all flashcards in the deck
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        for flashcard in flashcards:
            await self.flashcard_repo.delete(flashcard.id)
        
        # Delete the deck
        return await self.deck_repo.delete(deck_id)
    
    async def get_deck_with_cards(self, deck_id: str) -> Optional[dict]:
        """Get a deck with its flashcards."""
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            return None
        
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        
        return {
            "deck": deck,
            "flashcards": flashcards,
            "card_count": len(flashcards)
        }
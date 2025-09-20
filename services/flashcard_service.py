"""
Flashcard service implementing business logic for flashcard operations.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
from typing import List, Optional
from datetime import datetime
import uuid
from domain.entities import Flashcard
from repositories.interfaces import IFlashcardRepository, IDeckRepository


class FlashcardService:
    """Service for managing flashcard business logic."""
    
    def __init__(self, flashcard_repo: IFlashcardRepository, deck_repo: IDeckRepository):
        self.flashcard_repo = flashcard_repo
        self.deck_repo = deck_repo
    
    async def get_flashcards_by_deck(self, deck_id: str) -> List[Flashcard]:
        """Get all flashcards for a deck."""
        # Validate deck exists
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            raise ValueError("Deck not found")
        
        return await self.flashcard_repo.get_by_deck_id(deck_id)
    
    async def create_flashcard(self, deck_id: str, question: str, answer: str) -> Flashcard:
        """Create a new flashcard with validation."""
        # Validate deck exists
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            raise ValueError("Deck not found")
        
        # Validate input
        if not question or not question.strip():
            raise ValueError("Question is required")
        if not answer or not answer.strip():
            raise ValueError("Answer is required")
        
        # Create flashcard
        flashcard = Flashcard(
            id=str(uuid.uuid4()),
            deck_id=deck_id,
            question=question.strip(),
            answer=answer.strip(),
            created_at=datetime.now()
        )
        
        created_flashcard = await self.flashcard_repo.create(flashcard)
        
        # Update deck card count
        await self._update_deck_card_count(deck_id)
        
        return created_flashcard
    
    async def update_flashcard(self, flashcard_id: str, question: str = None, 
                              answer: str = None) -> Optional[Flashcard]:
        """Update an existing flashcard."""
        # Validate input
        update_data = {}
        
        if question is not None:
            if not question.strip():
                raise ValueError("Question cannot be empty")
            update_data["question"] = question.strip()
        
        if answer is not None:
            if not answer.strip():
                raise ValueError("Answer cannot be empty")
            update_data["answer"] = answer.strip()
        
        updated_flashcard = await self.flashcard_repo.update(flashcard_id, update_data)
        
        if updated_flashcard:
            # Update deck card count
            await self._update_deck_card_count(updated_flashcard.deck_id)
        
        return updated_flashcard
    
    async def delete_flashcard(self, flashcard_id: str) -> bool:
        """Delete a flashcard."""
        # Get flashcard to find deck_id
        flashcard = await self.flashcard_repo.get_by_id(flashcard_id)
        if not flashcard:
            return False
        
        deck_id = flashcard.deck_id
        success = await self.flashcard_repo.delete(flashcard_id)
        
        if success:
            # Update deck card count
            await self._update_deck_card_count(deck_id)
        
        return success
    
    async def _update_deck_card_count(self, deck_id: str):
        """Update the card count for a deck."""
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        await self.deck_repo.update(deck_id, {"card_count": len(flashcards)})
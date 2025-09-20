"""
Study service implementing business logic for study sessions and reviews.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
from typing import List, Optional
from datetime import datetime
import uuid
from domain.entities import StudySession, CardReview, ReviewDifficulty
from domain.value_objects import StudyProgress
from repositories.interfaces import (
    IStudySessionRepository, ICardReviewRepository, 
    IFlashcardRepository, IUserStatsRepository
)


class StudyService:
    """Service for managing study session business logic."""
    
    def __init__(self, session_repo: IStudySessionRepository, 
                 review_repo: ICardReviewRepository,
                 flashcard_repo: IFlashcardRepository,
                 stats_repo: IUserStatsRepository):
        self.session_repo = session_repo
        self.review_repo = review_repo
        self.flashcard_repo = flashcard_repo
        self.stats_repo = stats_repo
    
    async def start_study_session(self, deck_id: str) -> StudySession:
        """Start a new study session."""
        session = StudySession(
            id=str(uuid.uuid4()),
            deck_id=deck_id,
            start_time=datetime.now(),
            end_time=None,
            cards_studied=0,
            duration=0
        )
        
        return await self.session_repo.create(session)
    
    async def end_study_session(self, session_id: str) -> Optional[StudySession]:
        """End a study session."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            return None
        
        end_time = datetime.now()
        duration = int((end_time - session.start_time).total_seconds())
        
        update_data = {
            "end_time": end_time,
            "duration": duration
        }
        
        updated_session = await self.session_repo.update(session_id, update_data)
        
        if updated_session:
            # Update user stats
            await self._update_user_stats(updated_session)
        
        return updated_session
    
    async def review_card(self, session_id: str, card_id: str, 
                         difficulty: str) -> CardReview:
        """Record a card review."""
        # Validate difficulty
        try:
            difficulty_enum = ReviewDifficulty(difficulty.lower())
        except ValueError:
            raise ValueError(f"Invalid difficulty level: {difficulty}")
        
        review = CardReview(
            id=str(uuid.uuid4()),
            session_id=session_id,
            card_id=card_id,
            difficulty=difficulty_enum,
            reviewed_at=datetime.now()
        )
        
        created_review = await self.review_repo.create(review)
        
        # Update session cards studied count
        await self._update_session_cards_studied(session_id)
        
        return created_review
    
    async def get_study_progress(self, session_id: str, deck_id: str) -> StudyProgress:
        """Get study progress for a session."""
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise ValueError("Study session not found")
        
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        total_cards = len(flashcards)
        current_card = session.cards_studied
        progress_percentage = (current_card / total_cards * 100) if total_cards > 0 else 0
        
        return StudyProgress(
            current_card=current_card,
            total_cards=total_cards,
            progress_percentage=progress_percentage
        )
    
    async def _update_session_cards_studied(self, session_id: str):
        """Update the cards studied count for a session."""
        session = await self.session_repo.get_by_id(session_id)
        if session:
            # Count reviews for this session
            # Note: In a real implementation, you'd query the review repository
            # For now, we'll increment by 1
            new_count = session.cards_studied + 1
            await self.session_repo.update(session_id, {"cards_studied": new_count})
    
    async def _update_user_stats(self, session: StudySession):
        """Update user statistics after a study session."""
        stats = await self.stats_repo.get()
        
        # Update study time
        new_study_time = stats.study_time + session.duration
        
        # Update cards studied
        new_cards_studied = stats.cards_studied + session.cards_studied
        
        # Update study streak (simplified logic)
        today = datetime.now().date()
        last_study_date = stats.last_study_date.date() if stats.last_study_date else None
        
        if last_study_date == today:
            # Already studied today, no change to streak
            new_streak = stats.study_streak
        elif last_study_date and (today - last_study_date).days == 1:
            # Consecutive day, increment streak
            new_streak = stats.study_streak + 1
        elif last_study_date and (today - last_study_date).days > 1:
            # Streak broken, reset to 1
            new_streak = 1
        else:
            # First study session
            new_streak = 1
        
        await self.stats_repo.update({
            "study_time": new_study_time,
            "cards_studied": new_cards_studied,
            "study_streak": new_streak,
            "last_study_date": today
        })
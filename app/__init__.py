"""
Flask application factory following the Dependency Injection pattern.
"""
import asyncio
from flask import Flask
from repositories.memory_repository import (
    MemoryDeckRepository, MemoryFlashcardRepository, MemoryStudySessionRepository,
    MemoryCardReviewRepository, MemoryTestRepository, MemoryChatMessageRepository,
    MemoryUserStatsRepository
)
from repositories.vector_repository import ChromaVectorRepository
from services.deck_service import DeckService
from services.flashcard_service import FlashcardService
from services.study_service import StudyService
from services.test_service import TestService
from services.ai_service import AIService
from services.initialization_service import InitializationService
from app.routes import register_routes


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Initialize repositories
    deck_repo = MemoryDeckRepository()
    flashcard_repo = MemoryFlashcardRepository()
    session_repo = MemoryStudySessionRepository()
    review_repo = MemoryCardReviewRepository()
    test_repo = MemoryTestRepository()
    chat_repo = MemoryChatMessageRepository()
    stats_repo = MemoryUserStatsRepository()
    vector_repo = ChromaVectorRepository()
    
    # Initialize services
    deck_service = DeckService(deck_repo, flashcard_repo)
    flashcard_service = FlashcardService(flashcard_repo, deck_repo)
    study_service = StudyService(session_repo, review_repo, flashcard_repo, stats_repo)
    test_service = TestService(test_repo, flashcard_repo)
    ai_service = AIService(vector_repo, chat_repo, flashcard_repo)
    init_service = InitializationService(vector_repo)
    
    # Store services in app context for access in routes
    app.config['SERVICES'] = {
        'deck_service': deck_service,
        'flashcard_service': flashcard_service,
        'study_service': study_service,
        'test_service': test_service,
        'ai_service': ai_service,
        'init_service': init_service
    }
    
    # Register routes
    register_routes(app)
    
    # Initialize application (data ingestion)
    @app.before_request
    def initialize_app():
        """Initialize the application on first request."""
        if not hasattr(app, 'initialized'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(init_service.initialize_application())
            finally:
                loop.close()
            app.initialized = True
    
    return app
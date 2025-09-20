"""
AI service implementing business logic for chat and quiz generation.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
from typing import List, Optional
import uuid
from datetime import datetime
from domain.entities import ChatMessage, Test, TestType
from domain.value_objects import ChatResponse, QuizQuestion
from repositories.interfaces import IVectorRepository, IChatMessageRepository, IFlashcardRepository


class AIService:
    """Service for AI-powered features like chat and quiz generation."""
    
    def __init__(self, vector_repo: IVectorRepository, 
                 chat_repo: IChatMessageRepository,
                 flashcard_repo: IFlashcardRepository):
        self.vector_repo = vector_repo
        self.chat_repo = chat_repo
        self.flashcard_repo = flashcard_repo
    
    async def answer_question(self, question: str) -> ChatResponse:
        """Answer a question using RAG (Retrieval Augmented Generation)."""
        # Search for relevant content in vector database
        relevant_docs = await self.vector_repo.search_similar(question, limit=5)
        
        # Get all flashcards for additional context
        all_flashcards = await self._get_all_flashcards()
        
        # Find relevant flashcards based on question similarity
        relevant_cards = self._find_relevant_cards(question, all_flashcards)
        
        # Build context from relevant documents and flashcards
        context_parts = []
        
        # Add vector database context
        for doc in relevant_docs:
            context_parts.append(doc["content"])
        
        # Add flashcard context
        for card in relevant_cards:
            context_parts.append(f"Q: {card.question}\nA: {card.answer}")
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using simple pattern matching (in production, use LLM)
        answer = self._generate_answer(question, context)
        
        # Store the chat message
        chat_message = ChatMessage(
            id=str(uuid.uuid4()),
            question=question,
            answer=answer,
            relevant_cards=[card.id for card in relevant_cards],
            created_at=datetime.now()
        )
        await self.chat_repo.create(chat_message)
        
        return ChatResponse(
            answer=answer,
            relevant_cards=[card.id for card in relevant_cards]
        )
    
    async def generate_quiz_question(self, deck_id: str) -> QuizQuestion:
        """Generate a quiz question for a specific deck."""
        flashcards = await self.flashcard_repo.get_by_deck_id(deck_id)
        
        if not flashcards:
            raise ValueError("No flashcards found in deck")
        
        # Simple quiz generation (in production, use LLM)
        import random
        card = random.choice(flashcards)
        
        # Generate multiple choice options
        all_cards = await self._get_all_flashcards()
        other_cards = [c for c in all_cards if c.id != card.id]
        
        # Create options
        options = [card.answer]
        if len(other_cards) >= 3:
            other_answers = [c.answer for c in random.sample(other_cards, 3)]
            options.extend(other_answers)
        else:
            # If not enough other cards, create dummy options
            options.extend([
                "Option A",
                "Option B", 
                "Option C"
            ])
        
        random.shuffle(options)
        correct_index = options.index(card.answer)
        
        return QuizQuestion(
            question=card.question,
            options=options,
            correct_answer=correct_index,
            explanation=f"Based on the flashcard: {card.answer}"
        )
    
    async def get_chat_history(self) -> List[ChatMessage]:
        """Get all chat messages."""
        return await self.chat_repo.get_all()
    
    async def _get_all_flashcards(self) -> List:
        """Get all flashcards from all decks."""
        all_flashcards = []
        # Get all decks first
        from repositories.memory_repository import MemoryDeckRepository
        deck_repo = MemoryDeckRepository()
        decks = await deck_repo.get_all()
        
        # Get flashcards for each deck
        for deck in decks:
            flashcards = await self.flashcard_repo.get_by_deck_id(deck.id)
            all_flashcards.extend(flashcards)
        
        return all_flashcards
    
    def _find_relevant_cards(self, question: str, cards: List) -> List:
        """Find relevant flashcards based on question similarity."""
        # Simple keyword matching (in production, use semantic similarity)
        question_lower = question.lower()
        relevant = []
        
        for card in cards:
            if (question_lower in card.question.lower() or 
                question_lower in card.answer.lower()):
                relevant.append(card)
        
        return relevant[:5]  # Return top 5 relevant cards
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate an answer based on question and context."""
        # Simple template-based answer generation
        # In production, this would use an LLM like OpenAI or Ollama
        
        if not context.strip():
            return "I don't have enough information to answer that question. Please make sure you have some study material loaded."
        
        # Extract key information from context
        context_sentences = context.split('.')[:3]  # Take first 3 sentences
        
        answer = f"Based on your study materials:\n\n"
        for sentence in context_sentences:
            if sentence.strip():
                answer += f"• {sentence.strip()}.\n"
        
        answer += f"\nThis information should help answer your question: '{question}'"
        
        return answer
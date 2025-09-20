"""
Flashcard-specific routes.
"""
from flask import request, jsonify, current_app
from functools import wraps
import asyncio
from app.utils import prepare_response_data


def async_route(f):
    """Decorator to handle async functions in Flask routes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


def get_service(service_name: str):
    """Get a service from the app context."""
    return current_app.config['SERVICES'][service_name]


def register_flashcard_routes(app):
    """Register flashcard routes."""
    
    @app.route('/api/decks/<deck_id>/flashcards', methods=['GET'])
    @async_route
    async def get_flashcards(deck_id):
        try:
            flashcard_service = get_service('flashcard_service')
            flashcards = await flashcard_service.get_flashcards_by_deck(deck_id)
            return jsonify(prepare_response_data(flashcards))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/flashcards', methods=['POST'])
    @async_route
    async def create_flashcard():
        try:
            data = request.get_json()
            flashcard_service = get_service('flashcard_service')
            
            flashcard = await flashcard_service.create_flashcard(
                deck_id=data['deck_id'],
                question=data['question'],
                answer=data['answer']
            )
            return jsonify(prepare_response_data(flashcard)), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/flashcards/<flashcard_id>', methods=['PUT'])
    @async_route
    async def update_flashcard(flashcard_id):
        try:
            data = request.get_json()
            flashcard_service = get_service('flashcard_service')
            
            flashcard = await flashcard_service.update_flashcard(
                flashcard_id,
                question=data.get('question'),
                answer=data.get('answer')
            )
            if not flashcard:
                return jsonify({"error": "Flashcard not found"}), 404
            return jsonify(prepare_response_data(flashcard))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/flashcards/<flashcard_id>', methods=['DELETE'])
    @async_route
    async def delete_flashcard(flashcard_id):
        try:
            flashcard_service = get_service('flashcard_service')
            success = await flashcard_service.delete_flashcard(flashcard_id)
            if not success:
                return jsonify({"error": "Flashcard not found"}), 404
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
"""
AI-powered routes for chat and quiz generation.
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


def register_ai_routes(app):
    """Register AI-powered routes."""
    
    @app.route('/api/chat/messages', methods=['GET'])
    @async_route
    async def get_chat_messages():
        try:
            ai_service = get_service('ai_service')
            messages = await ai_service.get_chat_history()
            return jsonify(prepare_response_data(messages))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/chat/ask', methods=['POST'])
    @async_route
    async def ask_question():
        try:
            data = request.get_json()
            if not data or 'question' not in data:
                return jsonify({"error": "Question is required"}), 400
            
            ai_service = get_service('ai_service')
            response = await ai_service.answer_question(data['question'])
            return jsonify(prepare_response_data(response))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/quiz/generate/<deck_id>', methods=['POST'])
    @async_route
    async def generate_quiz_question(deck_id):
        try:
            ai_service = get_service('ai_service')
            question = await ai_service.generate_quiz_question(deck_id)
            return jsonify(prepare_response_data(question))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
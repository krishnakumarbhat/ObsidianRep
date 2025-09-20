"""
Study session and review routes.
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


def register_study_routes(app):
    """Register study session routes."""
    
    @app.route('/api/study-sessions', methods=['POST'])
    @async_route
    async def create_study_session():
        try:
            data = request.get_json()
            study_service = get_service('study_service')
            
            session = await study_service.start_study_session(data['deck_id'])
            return jsonify(prepare_response_data(session)), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/study-sessions/<session_id>', methods=['PUT'])
    @async_route
    async def end_study_session(session_id):
        try:
            study_service = get_service('study_service')
            session = await study_service.end_study_session(session_id)
            if not session:
                return jsonify({"error": "Study session not found"}), 404
            return jsonify(prepare_response_data(session))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/card-reviews', methods=['POST'])
    @async_route
    async def create_card_review():
        try:
            data = request.get_json()
            study_service = get_service('study_service')
            
            review = await study_service.review_card(
                session_id=data['session_id'],
                card_id=data['card_id'],
                difficulty=data['difficulty']
            )
            return jsonify(prepare_response_data(review)), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/study-sessions/<session_id>/progress', methods=['GET'])
    @async_route
    async def get_study_progress(session_id):
        try:
            data = request.get_json()
            study_service = get_service('study_service')
            
            progress = await study_service.get_study_progress(session_id, data['deck_id'])
            return jsonify(prepare_response_data(progress))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
"""
Flask routes implementing the API endpoints.
Following the Single Responsibility Principle and RESTful design.
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


def register_routes(app):
    """Register all API routes."""
    from app.flashcard_routes import register_flashcard_routes
    from app.study_routes import register_study_routes
    from app.ai_routes import register_ai_routes
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "RecallMind API is running"})
    
    # Deck routes
    @app.route('/api/decks', methods=['GET'])
    @async_route
    async def get_decks():
        try:
            deck_service = get_service('deck_service')
            decks = await deck_service.get_all_decks()
            return jsonify(prepare_response_data(decks))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/decks/<deck_id>', methods=['GET'])
    @async_route
    async def get_deck(deck_id):
        try:
            deck_service = get_service('deck_service')
            deck = await deck_service.get_deck_by_id(deck_id)
            if not deck:
                return jsonify({"error": "Deck not found"}), 404
            return jsonify(prepare_response_data(deck))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/decks', methods=['POST'])
    @async_route
    async def create_deck():
        try:
            data = request.get_json()
            deck_service = get_service('deck_service')
            
            deck = await deck_service.create_deck(
                name=data['name'],
                description=data.get('description'),
                difficulty=data.get('difficulty', 'beginner')
            )
            return jsonify(prepare_response_data(deck)), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/decks/<deck_id>', methods=['PUT'])
    @async_route
    async def update_deck(deck_id):
        try:
            data = request.get_json()
            deck_service = get_service('deck_service')
            
            deck = await deck_service.update_deck(
                deck_id,
                name=data.get('name'),
                description=data.get('description'),
                difficulty=data.get('difficulty')
            )
            if not deck:
                return jsonify({"error": "Deck not found"}), 404
            return jsonify(prepare_response_data(deck))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/decks/<deck_id>', methods=['DELETE'])
    @async_route
    async def delete_deck(deck_id):
        try:
            deck_service = get_service('deck_service')
            success = await deck_service.delete_deck(deck_id)
            if not success:
                return jsonify({"error": "Deck not found"}), 404
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Register additional route modules
    register_flashcard_routes(app)
    register_study_routes(app)
    register_ai_routes(app)
    
    # User stats routes
    @app.route('/api/stats', methods=['GET'])
    @async_route
    async def get_user_stats():
        try:
            stats_repo = current_app.config['SERVICES']['deck_service'].stats_repo
            stats = await stats_repo.get()
            return jsonify(prepare_response_data(stats))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/stats', methods=['PUT'])
    @async_route
    async def update_user_stats():
        try:
            data = request.get_json()
            stats_repo = current_app.config['SERVICES']['deck_service'].stats_repo
            stats = await stats_repo.update(data)
            return jsonify(prepare_response_data(stats))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Data management routes
    @app.route('/api/data/reingest', methods=['POST'])
    @async_route
    async def reingest_data():
        try:
            init_service = get_service('init_service')
            success = await init_service.reingest_data()
            if success:
                return jsonify({"message": "Data re-ingestion completed successfully"})
            else:
                return jsonify({"error": "Data re-ingestion failed"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.core.search_engine import SemanticCodeSearch
from app.config.settings import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for API requests

# Global search engine instance to avoid reloading on each request
search_engine = None

def get_engine():
    """Lazy initialization of the search engine."""
    global search_engine
    if search_engine is None:
        logger.info("Initializing global search engine instance for API server...")
        search_engine = SemanticCodeSearch()
    return search_engine

@app.route('/api/search', methods=['POST'])
def search_code():
    """
    Endpoint for performing semantic search queries.
    Expects a JSON payload with 'query' and optional 'top_k'.
    """
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' parameter in request body."}), 400
    
    query = data['query']
    top_k = data.get('top_k', Config.DEFAULT_TOP_K)
    
    try:
        engine = get_engine()
        # Execute search (uses dynamically loaded snippets from JSON)
        results = engine.search(query, top_k=top_k)
        return jsonify({
            "query": query,
            "results": results
        })
    except Exception as e:
        logger.error(f"Error processing API search request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "model": Config.DEFAULT_MODEL_NAME})

def start_server(host='0.0.0.0', port=5000, debug=False):
    """Starts the Flask development server."""
    logger.info(f"🚀 Starting Code Search API server on http://{host}:{port}/")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    start_server(debug=True)

import argparse
import sys
from typing import List
from app.core.search_engine import SemanticCodeSearch
from app.utils.logger import get_logger
from app.config.settings import Config

logger = get_logger(__name__)

def run_cli():
    """
    Main entry point for the Code Search Engine Command Line Interface.
    Allows users to perform semantic search queries from the terminal.
    """
    
    parser = argparse.ArgumentParser(
        description="🚀 Context-Aware Codebase Search Engine: Find code using natural language queries."
    )
    
    parser.add_argument(
        "query", 
        type=str, 
        help="The search query (e.g., 'how to read a file')"
    )
    
    parser.add_argument(
        "--top-k", 
        type=int, 
        default=Config.DEFAULT_TOP_K, 
        help=f"Number of results to return (default: {Config.DEFAULT_TOP_K})"
    )
    
    parser.add_argument(
        "--model", 
        type=str, 
        default=Config.DEFAULT_MODEL_NAME, 
        help=f"Model name or path to use (default: {Config.DEFAULT_MODEL_NAME})"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize engine
        engine = SemanticCodeSearch(model_name=args.model)
        
        # Execute search (uses dynamically loaded snippets from JSON)
        results = engine.search(args.query, top_k=args.top_k)
        
        # Print results in a clean format
        print(f"\n🔍 Search Results for: '{args.query}'")
        print("="*60)
        
        if not results:
            print("No relevant code snippets found.")
        else:
            for i, res in enumerate(results):
                print(f"Result #{i+1} (Score: {res['score']:.4f})")
                print("-" * 30)
                print(f"Description: {res.get('description', 'No description available')}")
                print(f"Code:\n{res['code']}")
                print("="*60)
            
    except Exception as e:
        logger.error(f"Error during CLI execution: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()

import sys
from app.cli.main import run_cli

if __name__ == "__main__":
    # Ensure dependencies are loaded from current directory
    # Run the CLI entry point
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n👋 Search Engine Stopped. Goodbye!")
        sys.exit(0)

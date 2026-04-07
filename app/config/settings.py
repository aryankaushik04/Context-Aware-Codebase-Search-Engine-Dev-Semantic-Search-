import os

class Config:
    """Base configuration settings for the Code Search Engine."""
    
    # Model configuration
    DEFAULT_MODEL_NAME = "microsoft/codebert-base"
    
    # Search parameters
    DEFAULT_TOP_K = 3
    MAX_SEQUENCE_LENGTH = 512
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Logging
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_LEVEL = "INFO"

    @classmethod
    def setup_dirs(cls):
        """Ensure required directories exist."""
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)

import logging
import os
from datetime import datetime

class TMGELogger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if TMGELogger._initialized:
            return
            
        TMGELogger._initialized = True
        self.setup_logger()

    def setup_logger(self):
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger('TMGE')
        self.logger.setLevel(logging.DEBUG)

        # Create handlers
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # File handler for all logs
        fh = logging.FileHandler(os.path.join(logs_dir, f'tmge_{timestamp}.log'))
        fh.setLevel(logging.DEBUG)

        # Console handler for important logs
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        
        fh.setFormatter(file_formatter)
        ch.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

import logging
import sys
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ensure logs directory exists or create it
    log_dir = Path('logs')
    try:
        log_dir.mkdir(exist_ok=True)
        
        # Create or append to log file
        log_file = log_dir / f'rag_app_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Set file handler to capture all levels including ERROR
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        
        # Log successful initialization
        logger.info(f"Logging initialized. Log file: {log_file}")
        
    except Exception as e:
        logger.error(f"Failed to setup file logging: {str(e)}")
        logger.warning("Continuing with console logging only")

    return logger

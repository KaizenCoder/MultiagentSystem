import sys
import os
from pathlib import Path
import logging
import time

# Add project root to path to allow imports from core
project_root = Path(__file__).resolve().parents[1] # This is PRODUCTION_READY
sys.path.insert(0, str(project_root))

from core import logging_manager, get_logger

LOG_DIR = project_root / 'logs'

def test_logger_initialization():
    """Test that the logger can be initialized."""
    logger = get_logger('test_logger')
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_logger'

def test_log_file_creation():
    """Test that a log file is created using a custom config."""
    test_log_dir = LOG_DIR / "test_logs"
    test_log_dir.mkdir(parents=True, exist_ok=True)
    
    logger_name = f'file_creation_test_{time.time()}'
    log_file = test_log_dir / f"{logger_name}.log"

    custom_config = {
        "logger_name": logger_name,
        "file_enabled": True,
        "log_dir": str(test_log_dir),
        "filename_pattern": f"{logger_name}.log",
        "console_enabled": False # Keep test output clean
    }

    logger = logging_manager.get_logger(custom_config=custom_config)

    log_message = f"Test message for file creation in {logger.name}"
    logger.info(log_message)

    # Shutdown the logger to ensure logs are flushed
    logging_manager.shutdown()

    # Check if the log file was created
    assert log_file.exists(), f"Log file {log_file} was not created."

    # Check if the message is in the log file
    with open(log_file, 'r') as f:
        content = f.read()
        assert log_message in content
    
    # Clean up
    log_file.unlink()
    test_log_dir.rmdir() 
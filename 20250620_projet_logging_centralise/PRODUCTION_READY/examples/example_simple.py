"""
Simple example of how to use the NextGeneration Logging Manager.
"""
import sys
from pathlib import Path
import time
import asyncio

# Add project root to path to allow imports
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

# Import the get_logger function from our core package
from core import get_logger, log_performance

def main():
    """Main function to demonstrate logging."""
    
    print("--- DEMO: NextGeneration Logging ---")

    # 1. Get a default logger
    print("\n1. Getting a default logger...")
    default_logger = get_logger("my_app")
    default_logger.info("This is an informational message from my_app.")
    default_logger.warning("This is a warning message.")

    # 2. Get a specialized logger for an agent
    print("\n2. Getting a specialized agent logger...")
    agent_logger = get_logger("my_agent")
    agent_logger.info(
        "Agent 'data_processor_01' starting its task.",
        extra={
            "agent_id": "data_processor_01",
            "task_id": "dp-12345",
            "input_files": ["file1.csv", "file2.csv"]
        }
    )
    agent_logger.debug("This is a debug message for the agent.")

    # 3. Demonstrate performance logging
    print("\n3. Demonstrating performance logging...")
    with log_performance("long_running_task", logger=default_logger):
        print("   - Simulating a task that takes 0.5 seconds...")
        time.sleep(0.5)
        print("   - Task finished.")

    # 4. Demonstrate logging an error
    print("\n4. Demonstrating error logging with exception info...")
    try:
        result = 1 / 0
    except ZeroDivisionError:
        default_logger.error(
            "An error occurred during a critical calculation.",
            exc_info=True
        )
    
    print("\n--- DEMO FINISHED ---")
    print(f"Check the log files in '{project_root / 'logs'}'")
    
    # In a real async application, you wouldn't need to do this,
    # but for this simple script to exit cleanly, we need to give
    # the async logging thread a moment to process the queue.
    time.sleep(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
⚡ AGENT 108 - PERFORMANCE OPTIMIZER (SPECIALIZED)
Agent Factory Pattern - Sprint 4.5

Mission:
- Analyze code for performance bottlenecks.
- Suggest and (optionally) apply optimizations.
- Profile code execution.
- Validate performance improvements.

This agent is a specialized tool for performance engineering, focusing on
CPU, memory, and I/O optimizations.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import time
import cProfile
import pstats
import asyncio
from datetime import datetime
import signal
from pathlib import Path
import json
import psutil

# --- Configuration Section ---
# Determine project root and add to sys.path
try:
    ROOT_DIR = Path(__file__).resolve().parents[1]
except NameError:
    ROOT_DIR = Path.cwd()

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Directories
LOGS_DIR = ROOT_DIR / "logs" / "agents"
REPORTS_DIR = ROOT_DIR / "reports" / "performance"
DATA_DIR = ROOT_DIR / "data"

# Create directories if they don't exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Agent Class ---
class PerformanceOptimizerAgent:
    """
    A specialized agent for code performance optimization.
    """
    def __init__(self, agent_id="performance_optimizer_108", mode='autonome'):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="general",
                custom_config={
                    "logger_name": f"nextgen.general.108_performance_optimizer.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/general",
                    "metadata": {
                        "agent_type": "108_performance_optimizer",
                        "agent_role": "general",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        self.agent_id = agent_id
        self.agent_name = "Performance Optimizer"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        self.mode = mode
        self.logger = self._setup_logging()
        self.loop = asyncio.get_event_loop()
        self.shutdown_event = asyncio.Event()

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.logger.info(f"🚀 {self.agent_name} ({self.agent_id}) initialized in '{self.mode}' mode.")

    def _setup_logging(self):
        """Sets up a rotating logger for the agent."""
        logger = logging.getLogger(self.agent_id)
        logger.setLevel(logging.INFO)
        log_file = LOGS_DIR / f"{self.agent_id}.log"
        
        # Prevent duplicate handlers
        if not logger.handlers:
            handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger

    def _signal_handler(self, signum, frame):
        """Handles shutdown signals gracefully."""
        self.logger.warning(f"Signal {signum} received. Initiating shutdown...")
        self.shutdown_event.set()

    async def analyze_code(self, file_path: str):
        """
        Analyzes a Python file for potential performance issues.
        This is a simplified static analysis for demonstration.
        """
        self.logger.info(f"Analyzing code in: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            if "for " in content and " in range(" in content:
                issues.append("Potential performance issue: Loop using range() could be slow for large numbers.")
            if "import pandas" in content:
                issues.append("Pandas detected. Ensure efficient DataFrame operations.")
            
            self.logger.info(f"Analysis complete. Found {len(issues)} potential issues.")
            return {
                "file_path": file_path,
                "potential_issues": issues
            }
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred during analysis: {e}")
            return None

    async def profile_code(self, file_path: str, function_name: str, *args, **kwargs):
        """
        Profiles a specific function within a file.
        Note: This is a complex operation simplified for this agent.
        It would typically involve dynamic imports and execution.
        """
        self.logger.info(f"Profiling {function_name} in {file_path}...")
        
        # This is a placeholder for a much more complex dynamic execution logic
        # For security and simplicity, we'll simulate the profiling
        
        profiler = cProfile.Profile()
        profiler.enable()
        
        # --- Simulation of function execution ---
        time.sleep(0.1) # Simulate work
        self.logger.info("Simulated function execution complete.")
        # --- End Simulation ---
        
        profiler.disable()
        
        report_path = REPORTS_DIR / f"profile_{Path(file_path).stem}_{function_name}_{int(time.time())}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            stats = pstats.Stats(profiler, stream=f).sort_stats('cumulative')
            stats.print_stats()
            
        self.logger.info(f"Profiling report saved to: {report_path}")
        return str(report_path)

    async def run(self):
        """The main execution loop for the agent."""
        self.status = "RUNNING"
        self.logger.info(f"Agent {self.agent_name} is now running.")
        
        try:
            while not self.shutdown_event.is_set():
                # In a real scenario, this agent would listen for tasks from a queue
                # or perform scheduled analyses.
                self.logger.info("Heartbeat: Agent is alive. Waiting for tasks...")
                
                # Simulate monitoring system vitals
                cpu_usage = psutil.cpu_percent()
                mem_usage = psutil.virtual_memory().percent
                self.logger.info(f"System vitals: CPU={cpu_usage}%, Memory={mem_usage}%")

                await asyncio.sleep(30)
        
        except asyncio.CancelledError:
            self.logger.info("Main task was cancelled.")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Performs a graceful shutdown of the agent."""
        if self.status == "SHUTTING_DOWN":
            return
            
        self.status = "SHUTTING_DOWN"
        self.logger.info("Agent is shutting down.")
        # Perform cleanup tasks here
        self.logger.info("Cleanup complete. Goodbye!")
        self.status = "SHUTDOWN"

# --- Main Execution ---
async def main():
    """Main function to run the agent."""
    agent = PerformanceOptimizerAgent()
    try:
        await agent.run()
    except Exception as e:
        agent.logger.critical(f"A critical error occurred: {e}", exc_info=True)
        await agent.shutdown()

if __name__ == "__main__":
    # This setup allows the agent to be run as a standalone script
    # and to be shut down gracefully with CTRL+C.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
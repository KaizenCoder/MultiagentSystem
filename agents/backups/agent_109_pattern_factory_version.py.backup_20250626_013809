#!/usr/bin/env python3
"""
AGENT 109 - PATTERN FACTORY VERSION (SPECIALIZED)
Agent Factory Pattern - Sprint 4.5

Mission:
- Enforce the Agent Factory design pattern.
- Validate agent compliance with the pattern.
- Provide templates and tools for creating new agents.
- Manage versioning and compatibility of agents within the factory.

This is a meta-agent, responsible for the integrity of the agent ecosystem.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import asyncio
from datetime import datetime
import signal
from pathlib import Path
import json

# --- Configuration Section ---
try:
    ROOT_DIR = Path(__file__).resolve().parents[1]
except NameError:
    ROOT_DIR = Path.cwd()

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Directories
LOGS_DIR = ROOT_DIR / "logs" / "agents"
REPORTS_DIR = ROOT_DIR / "reports" / "factory_pattern"
TEMPLATES_DIR = ROOT_DIR / "templates" / "agents"

# Create directories if they don't exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# --- Agent Class ---
class PatternFactoryAgent:
    """
    A specialized agent to enforce and manage the Agent Factory Pattern.
    """
    def __init__(self, agent_id="pattern_factory_109"):
        self.agent_id = agent_id
        self.agent_name = "Pattern Factory Version Manager"
        self.version = "2.0.0"
        self.status = "INITIALIZING"
        self.logger = self._setup_logging()
        self.loop = asyncio.get_event_loop()
        self.shutdown_event = asyncio.Event()

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"🚀 {self.agent_name} ({self.agent_id}) initialized.")

    def _setup_logging(self):
        """Sets up a rotating logger for the agent."""
        logger = logging.getLogger(self.agent_id)
        logger.setLevel(logging.INFO)
        log_file = LOGS_DIR / f"{self.agent_id}.log"
        
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

    async def validate_agent_compliance(self, file_path: str):
        """
        Validates if an agent script complies with the basic factory pattern.
        This is a simplified check.
        """
        self.logger.info(f"Validating compliance for: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            findings = {
                "file_path": file_path,
                "compliant": True,
                "issues": []
            }
            
            if "class" not in content:
                findings["compliant"] = False
                findings["issues"].append("No class definition found.")
            if "def __init__" not in content:
                findings["compliant"] = False
                findings["issues"].append("No __init__ method found in class.")
            if "async def run" not in content and "def run" not in content:
                findings["compliant"] = False
                findings["issues"].append("No run method found for agent execution loop.")

            if findings["compliant"]:
                self.logger.info(f"✅ Agent {file_path} is compliant with basic standards.")
            else:
                self.logger.warning(f"❌ Agent {file_path} has compliance issues.")
                
            return findings

        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return {"file_path": file_path, "compliant": False, "issues": ["File not found."]}
        except Exception as e:
            self.logger.error(f"An error occurred during validation: {e}")
            return {"file_path": file_path, "compliant": False, "issues": [str(e)]}

    async def generate_agent_template(self, new_agent_name: str, is_async: bool = True):
        """
        Generates a basic agent template file.
        """
        self.logger.info(f"Generating template for new agent: {new_agent_name}")
        
        template_name = "async_agent_template.py.txt" if is_async else "sync_agent_template.py.txt"
        template_path = TEMPLATES_DIR / template_name
        
        if not template_path.exists():
            self.logger.error(f"Template file not found: {template_path}")
            return None
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        agent_code = template_content.replace("{{AGENT_NAME}}", new_agent_name)
        
        new_agent_filename = f"agent_{new_agent_name.lower().replace(' ', '_')}.py"
        new_agent_path = ROOT_DIR / "agents" / new_agent_filename
        
        with open(new_agent_path, 'w', encoding='utf-8') as f:
            f.write(agent_code)
            
        self.logger.info(f"✅ Template generated at: {new_agent_path}")
        return str(new_agent_path)

    async def run(self):
        """The main execution loop for the agent."""
        self.status = "RUNNING"
        self.logger.info(f"Agent {self.agent_name} is now running.")
        
        try:
            while not self.shutdown_event.is_set():
                self.logger.info("Heartbeat: Pattern Factory is active. Monitoring agent standards...")
                await asyncio.sleep(60)
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
        self.logger.info("Goodbye!")
        self.status = "SHUTDOWN"

# --- Main Execution ---
async def main():
    """Main function to run the agent."""
    agent = PatternFactoryAgent()
    try:
        await agent.run()
    except Exception as e:
        agent.logger.critical(f"A critical error occurred: {e}", exc_info=True)
        await agent.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down gracefully.")
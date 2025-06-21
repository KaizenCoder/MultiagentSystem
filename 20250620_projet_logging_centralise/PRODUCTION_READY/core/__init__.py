from .logging_manager import NextGenLoggingManager, get_logger, get_agent_logger, log_performance

# Singleton instance
logging_manager = NextGenLoggingManager()

__all__ = [
    "NextGenLoggingManager",
    "logging_manager",
    "get_logger",
    "get_agent_logger",
    "log_performance"
] 
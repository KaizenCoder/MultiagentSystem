"""Configuration NextGeneration pour Code Expert"""

import os
from pathlib import Path

# Chemins NextGeneration
NEXTGEN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = NEXTGEN_ROOT / "templates"
AGENTS_DIR = NEXTGEN_ROOT / "agents"
CONFIG_DIR = NEXTGEN_ROOT / "config"

# Configuration performance
CACHE_TTL_SECONDS = 600  # 10 minutes production
MAX_CACHE_SIZE = 1000
THREAD_POOL_SIZE = 8

# Configuration logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuration scurit (Sprint 2)
SECURITY_ENABLED = True
RSA_KEY_SIZE = 2048
HASH_ALGORITHM = "sha256"

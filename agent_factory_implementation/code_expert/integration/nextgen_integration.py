"""Script d'intgration NextGeneration"""

from enhanced_agent_templates import AgentTemplate, TemplateFactory
from optimized_template_manager import TemplateManager
from config.nextgen_config import *

def initialize_nextgen_environment():
    """Initialise environnement NextGeneration avec code expert"""
    template_manager = TemplateManager(
        templates_dir=TEMPLATES_DIR,
        cache_ttl=CACHE_TTL_SECONDS,
        max_cache_size=MAX_CACHE_SIZE
    )
    
    factory = TemplateFactory(template_manager)
    
    return {
        "template_manager": template_manager,
        "factory": factory,
        "status": "[CHECK] ENVIRONNEMENT NEXTGEN INITIALIS"
    }

if __name__ == "__main__":
    result = initialize_nextgen_environment()
    print(f"Integration status: {result['status']}")

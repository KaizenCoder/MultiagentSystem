import sys; sys.path.insert(0, "."); from core.template_manager import TemplateManager; manager = TemplateManager("templates"); print("Templates:", manager.get_available_templates())





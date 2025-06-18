#!/usr/bin/env python3
"""
Agent 3 - Adaptateur de Code (Claude Sonnet 4)
Mission: Adapter les outils sélectionnés pour NextGeneration

Responsabilités:
- Copier les outils sélectionnés vers le répertoire cible
- Adapter le code pour la compatibilité NextGeneration
- Ajouter les en-têtes et configurations nécessaires
- Gérer les dépendances et imports
- Assurer la portabilité des chemins
"""

import os
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class AgentAdaptateurCode:
    """Agent spécialisé dans l'adaptation de code avec Claude Sonnet 4"""
    
    def __init__(self, source_path: str, target_path: str):
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        self.logger = logging.getLogger("Agent3_AdaptateurCode")
        
        # Créer le répertoire cible
        self.target_path.mkdir(parents=True, exist_ok=True)
        
        # Template d'en-tête NextGeneration
        self.nextgen_header = '''#!/usr/bin/env python3
"""
NextGeneration Tool - {tool_name}
Adapté depuis SuperWhisper V6 pour NextGeneration

Configuration NextGeneration:
- Portable: Fonctionne depuis n'importe quel répertoire du projet
- Auto-détection du projet root
- Logging intégré NextGeneration
- Configuration centralisée

Usage:
    python {tool_name}.py [args]
    
Ou depuis n'importe où dans NextGeneration:
    python tools/imported_tools/{category}/{tool_name}.py [args]
"""

import os
import sys
from pathlib import Path

# === Configuration NextGeneration ===
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR

# Auto-détection du projet NextGeneration
while PROJECT_ROOT.parent != PROJECT_ROOT:
    if (PROJECT_ROOT / "orchestrator").exists() or (PROJECT_ROOT / "memory_api").exists():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

# Ajout du projet au Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Configuration logging NextGeneration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NextGen.{tool_name}")

# === Fin Configuration NextGeneration ===

'''
        
    def adapt_selected_tools(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptation complète des outils sélectionnés"""
        self.logger.info("🔧 Démarrage adaptation des outils sélectionnés")
        
        selected_tools = evaluation_data.get("selected_tools", [])
        if not selected_tools:
            self.logger.warning("⚠️ Aucun outil à adapter")
            return {"adapted_tools": [], "adaptation_summary": {}}
            
        adapted_tools = []
        adaptation_errors = []
        
        # Créer la structure de répertoires par catégorie
        self.create_category_structure(selected_tools)
        
        # Adapter chaque outil
        for tool in selected_tools:
            try:
                adapted_tool = self.adapt_single_tool(tool)
                if adapted_tool:
                    adapted_tools.append(adapted_tool)
                    self.logger.info(f"✅ Outil adapté: {tool['name']}")
                else:
                    adaptation_errors.append(f"Échec adaptation: {tool['name']}")
                    
            except Exception as e:
                error_msg = f"Erreur adaptation {tool['name']}: {e}"
                self.logger.error(error_msg)
                adaptation_errors.append(error_msg)
                
        # Générer les fichiers de configuration
        self.generate_configuration_files(adapted_tools)
        
        # Créer le requirements.txt global
        self.generate_requirements_file(adapted_tools)
        
        adaptation_summary = {
            "total_selected": len(selected_tools),
            "successfully_adapted": len(adapted_tools),
            "adaptation_errors": adaptation_errors,
            "categories_created": self.get_created_categories(adapted_tools)
        }
        
        results = {
            "adapted_tools": adapted_tools,
            "adaptation_summary": adaptation_summary
        }
        
        self.logger.info(f"✅ Adaptation terminée: {len(adapted_tools)} outils adaptés")
        return results
        
    def create_category_structure(self, selected_tools: List[Dict[str, Any]]):
        """Création de la structure de répertoires par catégorie"""
        categories = set()
        
        for tool in selected_tools:
            category = tool.get("tool_type", "utility")
            categories.add(category)
            
        for category in categories:
            category_path = self.target_path / category
            category_path.mkdir(exist_ok=True)
            
            # Créer un __init__.py pour chaque catégorie
            init_file = category_path / "__init__.py"
            if not init_file.exists():
                init_content = f'"""NextGeneration Tools - {category.title()} Category"""\n'
                init_file.write_text(init_content, encoding='utf-8')
                
        self.logger.info(f"📁 Structure créée pour {len(categories)} catégories")
        
    def adapt_single_tool(self, tool: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptation d'un outil unique"""
        tool_name = tool["name"]
        tool_category = tool.get("tool_type", "utility")
        source_file_path = self.source_path / tool["path"]
        
        if not source_file_path.exists():
            self.logger.error(f"❌ Fichier source introuvable: {source_file_path}")
            return None
            
        # Chemin de destination
        target_category_path = self.target_path / tool_category
        target_file_path = target_category_path / f"{tool_name}.py"
        
        try:
            # Lire le contenu original
            with open(source_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # Adapter le contenu
            adapted_content = self.adapt_tool_content(original_content, tool)
            
            # Écrire le fichier adapté
            with open(target_file_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
                
            # Copier les fichiers auxiliaires si nécessaires
            self.copy_auxiliary_files(source_file_path, target_category_path, tool)
            
            return {
                "name": tool_name,
                "category": tool_category,
                "source_path": str(source_file_path),
                "target_path": str(target_file_path),
                "size_bytes": target_file_path.stat().st_size,
                "adaptation_applied": True,
                "utility_score": tool.get("utility_score", 0),
                "priority": tool.get("integration_priority", "MEDIUM")
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur adaptation {tool_name}: {e}")
            return None
            
    def adapt_tool_content(self, original_content: str, tool: Dict[str, Any]) -> str:
        """Adaptation du contenu d'un outil"""
        tool_name = tool["name"]
        
        # Retirer l'ancien shebang et imports du début
        lines = original_content.split('\n')
        
        # Trouver où commence le code réel (après les imports initiaux)
        code_start_index = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped and 
                not stripped.startswith('#') and 
                not stripped.startswith('import ') and
                not stripped.startswith('from ') and
                not stripped.startswith('"""') and
                not stripped.startswith("'''")):
                code_start_index = i
                break
                
        # Préserver les docstrings et imports importants
        preserved_imports = []
        in_docstring = False
        docstring_delimiter = None
        
        for i in range(code_start_index):
            line = lines[i].strip()
            
            # Gérer les docstrings
            if line.startswith('"""') or line.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    docstring_delimiter = line[:3]
                elif line.endswith(docstring_delimiter):
                    in_docstring = False
                    
            # Préserver les imports non-standard
            if (line.startswith('import ') or line.startswith('from ')) and not in_docstring:
                # Exclure les imports système standards
                if not any(std in line for std in ['os', 'sys', 'pathlib', 'logging']):
                    preserved_imports.append(lines[i])
                    
        # Construire le contenu adapté
        adapted_content = self.nextgen_header.format(
            tool_name=tool_name,
            category=tool.get("tool_type", "utility")
        )
        
        # Ajouter les imports préservés
        if preserved_imports:
            adapted_content += '\n# Imports spécifiques à l\'outil\n'
            adapted_content += '\n'.join(preserved_imports) + '\n\n'
            
        # Ajouter le code principal adapté
        main_code = '\n'.join(lines[code_start_index:])
        
        # Adaptations spécifiques du code
        main_code = self.apply_code_adaptations(main_code, tool)
        
        adapted_content += main_code
        
        return adapted_content
        
    def apply_code_adaptations(self, code: str, tool: Dict[str, Any]) -> str:
        """Application d'adaptations spécifiques au code"""
        
        # Remplacer les chemins absolus par des chemins relatifs au projet
        code = re.sub(
            r'["\']C:\\[^"\']*["\']',
            'str(PROJECT_ROOT / "relative_path")',
            code
        )
        
        # Adapter les appels de logging
        code = re.sub(
            r'print\(',
            'logger.info(',
            code
        )
        
        # Remplacer les références à __file__ par SCRIPT_DIR
        code = re.sub(
            r'__file__',
            'str(SCRIPT_DIR / Path(__file__).name)',
            code
        )
        
        # Adapter les chemins de configuration
        code = re.sub(
            r'config\.ini',
            'str(PROJECT_ROOT / "config" / "config.ini")',
            code
        )
        
        # Ajouter la gestion d'erreur NextGeneration
        if 'def main(' in code and 'try:' not in code:
            code = code.replace(
                'def main(',
                '''def main('''
            )
            
        return code
        
    def copy_auxiliary_files(self, source_file: Path, target_dir: Path, tool: Dict[str, Any]):
        """Copie des fichiers auxiliaires (config, data, etc.)"""
        source_dir = source_file.parent
        
        # Chercher les fichiers auxiliaires courants
        auxiliary_patterns = [
            f"{tool['name']}.ini",
            f"{tool['name']}.json",
            f"{tool['name']}.yaml",
            f"{tool['name']}.txt",
            "config.*",
            "data.*"
        ]
        
        for pattern in auxiliary_patterns:
            for aux_file in source_dir.glob(pattern):
                if aux_file.is_file() and aux_file != source_file:
                    target_aux_file = target_dir / aux_file.name
                    shutil.copy2(aux_file, target_aux_file)
                    self.logger.info(f"📄 Fichier auxiliaire copié: {aux_file.name}")
                    
    def generate_configuration_files(self, adapted_tools: List[Dict[str, Any]]):
        """Génération des fichiers de configuration"""
        
        # Créer un fichier de configuration global
        config_data = {
            "nextgeneration_tools": {
                "version": "1.0.0",
                "adapted_from": "SuperWhisper_V6",
                "tools": []
            }
        }
        
        for tool in adapted_tools:
            tool_config = {
                "name": tool["name"],
                "category": tool["category"],
                "path": tool["target_path"],
                "priority": tool["priority"],
                "utility_score": tool["utility_score"]
            }
            config_data["nextgeneration_tools"]["tools"].append(tool_config)
            
        # Sauvegarder la configuration
        config_file = self.target_path / "tools_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"⚙️ Configuration générée: {config_file}")
        
        # Créer un script de lancement global
        launcher_script = self.target_path / "run_tool.py"
        launcher_content = '''#!/usr/bin/env python3
"""
NextGeneration Tools Launcher
Script pour exécuter les outils importés depuis n'importe où dans le projet
"""

import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_tool.py <tool_name> [args...]")
        list_available_tools()
        return
        
    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]
    
    # Charger la configuration des outils
    config_file = Path(__file__).parent / "tools_config.json"
    
    if not config_file.exists():
        print("❌ Configuration des outils introuvable")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    # Trouver l'outil
    tool_info = None
    for tool in config["nextgeneration_tools"]["tools"]:
        if tool["name"] == tool_name:
            tool_info = tool
            break
            
    if not tool_info:
        print(f"❌ Outil '{tool_name}' introuvable")
        list_available_tools()
        return
        
    # Exécuter l'outil
    tool_path = Path(tool_info["path"])
    if not tool_path.exists():
        print(f"❌ Fichier outil introuvable: {tool_path}")
        return
        
    import subprocess
    cmd = [sys.executable, str(tool_path)] + tool_args
    subprocess.run(cmd)

def list_available_tools():
    config_file = Path(__file__).parent / "tools_config.json"
    
    if not config_file.exists():
        print("❌ Configuration des outils introuvable")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    print("\\n🔧 Outils disponibles:")
    for tool in config["nextgeneration_tools"]["tools"]:
        print(f"  - {tool['name']} ({tool['category']}) - Priorité: {tool['priority']}")

if __name__ == "__main__":
    main()
'''
        
        with open(launcher_script, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
            
        self.logger.info(f"🚀 Lanceur créé: {launcher_script}")
        
    def generate_requirements_file(self, adapted_tools: List[Dict[str, Any]]):
        """Génération du fichier requirements.txt pour les outils"""
        
        # Collecter toutes les dépendances uniques
        all_dependencies = set()
        
        for tool in adapted_tools:
            tool_name = tool["name"]
            
            # Lire le fichier adapté pour extraire les imports
            try:
                with open(tool["target_path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extraire les imports externes
                import_lines = re.findall(r'^(?:import|from)\s+([^\s.]+)', content, re.MULTILINE)
                
                for imp in import_lines:
                    # Filtrer les modules standards
                    if imp not in ['os', 'sys', 'json', 're', 'time', 'datetime', 'pathlib', 'logging', 'subprocess']:
                        all_dependencies.add(imp)
                        
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur extraction dépendances {tool_name}: {e}")
                
        # Mapping des modules vers les packages PyPI
        package_mapping = {
            'requests': 'requests>=2.25.0',
            'aiohttp': 'aiohttp>=3.8.0',
            'fastapi': 'fastapi>=0.68.0',
            'pydantic': 'pydantic>=1.8.0',
            'sqlalchemy': 'sqlalchemy>=1.4.0',
            'pandas': 'pandas>=1.3.0',
            'numpy': 'numpy>=1.21.0',
            'yaml': 'PyYAML>=6.0',
            'click': 'click>=8.0.0',
            'colorama': 'colorama>=0.4.0',
            'tqdm': 'tqdm>=4.60.0'
        }
        
        requirements = []
        for dep in sorted(all_dependencies):
            if dep in package_mapping:
                requirements.append(package_mapping[dep])
            else:
                requirements.append(dep)
                
        # Écrire le fichier requirements
        if requirements:
            req_file = self.target_path / "requirements.txt"
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write("# NextGeneration Imported Tools Dependencies\n")
                f.write("# Generated automatically by Agent 3 - Adaptateur Code\n\n")
                f.write('\n'.join(requirements))
                
            self.logger.info(f"📋 Requirements générés: {len(requirements)} dépendances")
        else:
            self.logger.info("📋 Aucune dépendance externe détectée")
            
    def get_created_categories(self, adapted_tools: List[Dict[str, Any]]) -> List[str]:
        """Récupération des catégories créées"""
        categories = set()
        for tool in adapted_tools:
            categories.add(tool["category"])
        return sorted(list(categories))

# Test de l'agent si exécuté directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        source_path = sys.argv[1]
        target_path = sys.argv[2]
    else:
        source_path = r"C:\Dev\SuperWhisper_V6\tools"
        target_path = "tools/imported_tools"
        
    # Test avec des données simulées
    test_evaluation_data = {
        "selected_tools": [
            {
                "name": "test_tool",
                "tool_type": "utility",
                "path": "test_tool.py",
                "utility_score": 75.5,
                "integration_priority": "HIGH"
            }
        ]
    }
    
    agent = AgentAdaptateurCode(source_path, target_path)
    results = agent.adapt_selected_tools(test_evaluation_data)
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
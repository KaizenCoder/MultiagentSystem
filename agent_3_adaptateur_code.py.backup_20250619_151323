#!/usr/bin/env python3
"""
Agent 3 - Adaptateur de Code (Claude Sonnet 4)
Mission: Adapter les outils slectionns pour NextGeneration

Responsabilits:
- Copier les outils slectionns vers le rpertoire cible
- Adapter le code pour la compatibilit NextGeneration
- Ajouter les en-ttes et configurations ncessaires
- Grer les dpendances et imports
- Assurer la portabilit des chemins
"""

import os
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class AgentAdaptateurCode:
    """Agent spcialis dans l'adaptation de code avec Claude Sonnet 4"""
    
    def __init__(self, source_path: str, target_path: str):
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)
        self.logger = logging.getLogger("Agent3_AdaptateurCode")
        
        # Crer le rpertoire cible
        self.target_path.mkdir(parents=True, exist_ok=True)
        
        # Template d'en-tte NextGeneration
        self.nextgen_header = '''#!/usr/bin/env python3
"""
NextGeneration Tool - {tool_name}
Adapt depuis SuperWhisper V6 pour NextGeneration

Configuration NextGeneration:
- Portable: Fonctionne depuis n'importe quel rpertoire du projet
- Auto-dtection du projet root
- Logging intgr NextGeneration
- Configuration centralise

Usage:
    python {tool_name}.py [args]
    
Ou depuis n'importe o dans NextGeneration:
    python tools/imported_tools/{category}/{tool_name}.py [args]
"""

import os
import sys
from pathlib import Path

# === Configuration NextGeneration ===
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR

# Auto-dtection du projet NextGeneration
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
        """Adaptation complte des outils slectionns"""
        self.logger.info("[TOOL] Dmarrage adaptation des outils slectionns")
        
        selected_tools = evaluation_data.get("selected_tools", [])
        if not selected_tools:
            self.logger.warning(" Aucun outil  adapter")
            return {"adapted_tools": [], "adaptation_summary": {}}
            
        adapted_tools = []
        adaptation_errors = []
        
        # Crer la structure de rpertoires par catgorie
        self.create_category_structure(selected_tools)
        
        # Adapter chaque outil
        for tool in selected_tools:
            try:
                adapted_tool = self.adapt_single_tool(tool)
                if adapted_tool:
                    adapted_tools.append(adapted_tool)
                    self.logger.info(f"[CHECK] Outil adapt: {tool['name']}")
                else:
                    adaptation_errors.append(f"chec adaptation: {tool['name']}")
                    
            except Exception as e:
                error_msg = f"Erreur adaptation {tool['name']}: {e}"
                self.logger.error(error_msg)
                adaptation_errors.append(error_msg)
                
        # Gnrer les fichiers de configuration
        self.generate_configuration_files(adapted_tools)
        
        # Crer le requirements.txt global
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
        
        self.logger.info(f"[CHECK] Adaptation termine: {len(adapted_tools)} outils adapts")
        return results
        
    def create_category_structure(self, selected_tools: List[Dict[str, Any]]):
        """Cration de la structure de rpertoires par catgorie"""
        categories = set()
        
        for tool in selected_tools:
            category = tool.get("tool_type", "utility")
            categories.add(category)
            
        for category in categories:
            category_path = self.target_path / category
            category_path.mkdir(exist_ok=True)
            
            # Crer un __init__.py pour chaque catgorie
            init_file = category_path / "__init__.py"
            if not init_file.exists():
                init_content = f'"""NextGeneration Tools - {category.title()} Category"""\n'
                init_file.write_text(init_content, encoding='utf-8')
                
        self.logger.info(f"[FOLDER] Structure cre pour {len(categories)} catgories")
        
    def adapt_single_tool(self, tool: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptation d'un outil unique"""
        tool_name = tool["name"]
        tool_category = tool.get("tool_type", "utility")
        source_file_path = self.source_path / tool["path"]
        
        if not source_file_path.exists():
            self.logger.error(f"[CROSS] Fichier source introuvable: {source_file_path}")
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
            
            # crire le fichier adapt
            with open(target_file_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
                
            # Copier les fichiers auxiliaires si ncessaires
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
            self.logger.error(f"[CROSS] Erreur adaptation {tool_name}: {e}")
            return None
            
    def adapt_tool_content(self, original_content: str, tool: Dict[str, Any]) -> str:
        """Adaptation du contenu d'un outil"""
        tool_name = tool["name"]
        
        # Retirer l'ancien shebang et imports du dbut
        lines = original_content.split('\n')
        
        # Trouver o commence le code rel (aprs les imports initiaux)
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
                
        # Prserver les docstrings et imports importants
        preserved_imports = []
        in_docstring = False
        docstring_delimiter = None
        
        for i in range(code_start_index):
            line = lines[i].strip()
            
            # Grer les docstrings
            if line.startswith('"""') or line.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    docstring_delimiter = line[:3]
                elif line.endswith(docstring_delimiter):
                    in_docstring = False
                    
            # Prserver les imports non-standard
            if (line.startswith('import ') or line.startswith('from ')) and not in_docstring:
                # Exclure les imports systme standards
                if not any(std in line for std in ['os', 'sys', 'pathlib', 'logging']):
                    preserved_imports.append(lines[i])
                    
        # Construire le contenu adapt
        adapted_content = self.nextgen_header.format(
            tool_name=tool_name,
            category=tool.get("tool_type", "utility")
        )
        
        # Ajouter les imports prservs
        if preserved_imports:
            adapted_content += '\n# Imports spcifiques  l\'outil\n'
            adapted_content += '\n'.join(preserved_imports) + '\n\n'
            
        # Ajouter le code principal adapt
        main_code = '\n'.join(lines[code_start_index:])
        
        # Adaptations spcifiques du code
        main_code = self.apply_code_adaptations(main_code, tool)
        
        adapted_content += main_code
        
        return adapted_content
        
    def apply_code_adaptations(self, code: str, tool: Dict[str, Any]) -> str:
        """Application d'adaptations spcifiques au code"""
        
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
        
        # Remplacer les rfrences  __file__ par SCRIPT_DIR
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
                    self.logger.info(f"[DOCUMENT] Fichier auxiliaire copi: {aux_file.name}")
                    
    def generate_configuration_files(self, adapted_tools: List[Dict[str, Any]]):
        """Gnration des fichiers de configuration"""
        
        # Crer un fichier de configuration global
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
            
        self.logger.info(f" Configuration gnre: {config_file}")
        
        # Crer un script de lancement global
        launcher_script = self.target_path / "run_tool.py"
        launcher_content = '''#!/usr/bin/env python3
"""
NextGeneration Tools Launcher
Script pour excuter les outils imports depuis n'importe o dans le projet
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
        print("[CROSS] Configuration des outils introuvable")
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
        print(f"[CROSS] Outil '{tool_name}' introuvable")
        list_available_tools()
        return
        
    # Excuter l'outil
    tool_path = Path(tool_info["path"])
    if not tool_path.exists():
        print(f"[CROSS] Fichier outil introuvable: {tool_path}")
        return
        
    import subprocess
    cmd = [sys.executable, str(tool_path)] + tool_args
    subprocess.run(cmd)

def list_available_tools():
    config_file = Path(__file__).parent / "tools_config.json"
    
    if not config_file.exists():
        print("[CROSS] Configuration des outils introuvable")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    print("\\n[TOOL] Outils disponibles:")
    for tool in config["nextgeneration_tools"]["tools"]:
        print(f"  - {tool['name']} ({tool['category']}) - Priorit: {tool['priority']}")

if __name__ == "__main__":
    main()
'''
        
        with open(launcher_script, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
            
        self.logger.info(f"[ROCKET] Lanceur cr: {launcher_script}")
        
    def generate_requirements_file(self, adapted_tools: List[Dict[str, Any]]):
        """Gnration du fichier requirements.txt pour les outils"""
        
        # Collecter toutes les dpendances uniques
        all_dependencies = set()
        
        for tool in adapted_tools:
            tool_name = tool["name"]
            
            # Lire le fichier adapt pour extraire les imports
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
                self.logger.warning(f" Erreur extraction dpendances {tool_name}: {e}")
                
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
                
        # crire le fichier requirements
        if requirements:
            req_file = self.target_path / "requirements.txt"
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write("# NextGeneration Imported Tools Dependencies\n")
                f.write("# Generated automatically by Agent 3 - Adaptateur Code\n\n")
                f.write('\n'.join(requirements))
                
            self.logger.info(f"[CLIPBOARD] Requirements gnrs: {len(requirements)} dpendances")
        else:
            self.logger.info("[CLIPBOARD] Aucune dpendance externe dtecte")
            
    def get_created_categories(self, adapted_tools: List[Dict[str, Any]]) -> List[str]:
        """Rcupration des catgories cres"""
        categories = set()
        for tool in adapted_tools:
            categories.add(tool["category"])
        return sorted(list(categories))
    
    def adapter_outils_apex(self, phase2_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adaptation spcialise des outils Apex_VBA_FRAMEWORK slectionns
        
        Args:
            phase2_data: Donnes de slection de la phase 2
            
        Returns:
            Dict contenant les rsultats d'adaptation
        """
        self.logger.info("[TOOL] Adaptation spcialise outils Apex_VBA_FRAMEWORK")
        
        outils_adaptes = []
        outils_selectionnes = phase2_data.get("outils_selectionnes", [])
        
        # Crer la structure de rpertoires pour Apex
        self._creer_structure_apex()
        
        for outil in outils_selectionnes:
            try:
                if outil["type"] == "python":
                    resultat = self._adapter_outil_python_apex(outil)
                elif outil["type"] == "powershell":
                    resultat = self._adapter_outil_powershell_apex(outil)
                elif outil["type"] == "batch":
                    resultat = self._adapter_outil_batch_apex(outil)
                else:
                    continue
                
                if resultat:
                    outils_adaptes.append(resultat)
                    self.logger.info(f"[CHECK] Outil adapt: {outil['name']}")
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur adaptation {outil['name']}: {e}")
        
        # Gnrer les fichiers de configuration et lanceurs
        self._generer_config_apex(outils_adaptes)
        self._generer_lanceur_apex(outils_adaptes)
        
        resultats = {
            "total_adapted": len(outils_adaptes),
            "outils_adaptes": outils_adaptes,
            "target_directory": str(self.target_path),
            "config_generated": True,
            "launcher_generated": True,
            "adaptation_timestamp": datetime.now().isoformat(),
            "adapter_model": "Claude Sonnet 4"
        }
        
        self.logger.info(f"[CHECK] Adaptation Apex termine: {len(outils_adaptes)} outils adapts")
        return resultats
    
    def _creer_structure_apex(self):
        """Cration de la structure de rpertoires pour Apex"""
        categories = ["python", "powershell", "batch", "config"]
        
        for category in categories:
            category_dir = self.target_path / category
            category_dir.mkdir(parents=True, exist_ok=True)
    
    def _adapter_outil_python_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptation d'un outil Python Apex"""
        try:
            source_path = Path(outil["path"])
            target_path = self.target_path / "python" / f"{outil['name']}.py"
            
            # Lire le contenu source
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Ajouter l'en-tte NextGeneration
            adapted_content = self._generer_entete_nextgeneration_apex(outil, "python")
            adapted_content += "\n\n" + content
            
            # Adapter les chemins pour NextGeneration
            adapted_content = self._adapter_chemins_apex(adapted_content)
            
            # crire le fichier adapt
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
            
            return {
                "name": outil["name"],
                "type": "python",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "apex_subdir": outil.get("apex_subdir", "unknown"),
                "adaptation_success": True
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur adaptation Python {outil['name']}: {e}")
            return None
    
    def _adapter_outil_powershell_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptation d'un outil PowerShell Apex"""
        try:
            source_path = Path(outil["path"])
            target_path = self.target_path / "powershell" / f"{outil['name']}.ps1"
            
            # Lire le contenu source
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Ajouter l'en-tte NextGeneration pour PowerShell
            adapted_content = self._generer_entete_nextgeneration_apex(outil, "powershell")
            adapted_content += "\n\n" + content
            
            # crire le fichier adapt
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
            
            return {
                "name": outil["name"],
                "type": "powershell",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "apex_subdir": outil.get("apex_subdir", "unknown"),
                "adaptation_success": True
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur adaptation PowerShell {outil['name']}: {e}")
            return None
    
    def _adapter_outil_batch_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptation d'un outil Batch Apex"""
        try:
            source_path = Path(outil["path"])
            target_path = self.target_path / "batch" / f"{outil['name']}.bat"
            
            # Lire le contenu source
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Ajouter l'en-tte NextGeneration pour Batch
            adapted_content = self._generer_entete_nextgeneration_apex(outil, "batch")
            adapted_content += "\n\n" + content
            
            # crire le fichier adapt
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
            
            return {
                "name": outil["name"],
                "type": "batch",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "apex_subdir": outil.get("apex_subdir", "unknown"),
                "adaptation_success": True
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur adaptation Batch {outil['name']}: {e}")
            return None
    
    def _generer_entete_nextgeneration_apex(self, outil: Dict[str, Any], type_outil: str) -> str:
        """Gnration de l'en-tte NextGeneration pour outils Apex"""
        if type_outil == "python":
            return f'''#!/usr/bin/env python3
"""
{outil["name"]} - Import depuis Apex_VBA_FRAMEWORK
Partie du systme NextGeneration - Outils intgrs

Source: {outil.get("apex_subdir", "unknown")} | Type: {outil["type"]}
Adaptation automatique par Agent 3 (Claude Sonnet 4)
"""

# === Configuration NextGeneration ===
import os
import sys
from pathlib import Path

# Dtection automatique du projet root
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR
while not (PROJECT_ROOT / ".git").exists() and PROJECT_ROOT.parent != PROJECT_ROOT:
    PROJECT_ROOT = PROJECT_ROOT.parent

# Ajout du projet au PYTHONPATH si ncessaire
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# === Fin Configuration NextGeneration ==='''
        
        elif type_outil == "powershell":
            return f'''# {outil["name"]} - Import depuis Apex_VBA_FRAMEWORK
# Partie du systme NextGeneration - Outils intgrs
#
# Source: {outil.get("apex_subdir", "unknown")} | Type: {outil["type"]}
# Adaptation automatique par Agent 3 (Claude Sonnet 4)

# === Configuration NextGeneration ===
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = $ScriptDir
while (-not (Test-Path (Join-Path $ProjectRoot ".git")) -and $ProjectRoot -ne (Split-Path $ProjectRoot -Parent)) {{
    $ProjectRoot = Split-Path $ProjectRoot -Parent
}}
# === Fin Configuration NextGeneration ==='''
        
        elif type_outil == "batch":
            return f'''@echo off
REM {outil["name"]} - Import depuis Apex_VBA_FRAMEWORK
REM Partie du systme NextGeneration - Outils intgrs
REM
REM Source: {outil.get("apex_subdir", "unknown")} | Type: {outil["type"]}
REM Adaptation automatique par Agent 3 (Claude Sonnet 4)

REM === Configuration NextGeneration ===
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%
:find_git
if exist "%PROJECT_ROOT%\\.git" goto found_git
for %%i in ("%PROJECT_ROOT%\\..") do set PROJECT_ROOT=%%~fi
if "%PROJECT_ROOT%" == "%PROJECT_ROOT:~0,3%" goto found_git
goto find_git
:found_git
REM === Fin Configuration NextGeneration ==='''
        
        return ""
    
    def _adapter_chemins_apex(self, content: str) -> str:
        """Adaptation des chemins dans le contenu pour Apex"""
        # Remplacer les chemins absolus Apex par des chemins relatifs
        content = content.replace("G:\\Dev\\Apex_VBA_FRAMEWORK", str(self.target_path.parent))
        content = content.replace("G:/Dev/Apex_VBA_FRAMEWORK", str(self.target_path.parent))
        
        return content
    
    def _generer_config_apex(self, outils_adaptes: List[Dict[str, Any]]):
        """Gnration du fichier de configuration pour outils Apex"""
        config = {
            "apex_tools_config": {
                "version": "1.0",
                "source": "Apex_VBA_FRAMEWORK",
                "adaptation_date": datetime.now().isoformat(),
                "tools": {}
            }
        }
        
        for outil in outils_adaptes:
            config["apex_tools_config"]["tools"][outil["name"]] = {
                "type": outil["type"],
                "path": outil["target_path"],
                "apex_subdir": outil.get("apex_subdir", "unknown"),
                "adapted": True
            }
        
        config_path = self.target_path / "apex_tools_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _generer_lanceur_apex(self, outils_adaptes: List[Dict[str, Any]]):
        """Gnration du lanceur universel pour outils Apex"""
        lanceur_content = '''#!/usr/bin/env python3
"""
Lanceur universel pour outils Apex_VBA_FRAMEWORK imports
Partie du systme NextGeneration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def load_apex_config():
    """Chargement de la configuration des outils Apex"""
    config_path = Path(__file__).parent / "apex_tools_config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_python_tool(tool_name, tool_path, args):
    """Excution d'un outil Python"""
    cmd = [sys.executable, tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def run_powershell_tool(tool_name, tool_path, args):
    """Excution d'un outil PowerShell"""
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def run_batch_tool(tool_name, tool_path, args):
    """Excution d'un outil Batch"""
    cmd = [tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_apex_tool.py <tool_name> [args...]")
        print("\\nOutils disponibles:")
        
        config = load_apex_config()
        for tool_name, tool_info in config["apex_tools_config"]["tools"].items():
            print(f"  - {tool_name} ({tool_info['type']})")
        return 1
    
    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]
    
    config = load_apex_config()
    tools = config["apex_tools_config"]["tools"]
    
    if tool_name not in tools:
        print(f"Outil '{tool_name}' introuvable")
        return 1
    
    tool_info = tools[tool_name]
    tool_path = tool_info["path"]
    tool_type = tool_info["type"]
    
    if tool_type == "python":
        return run_python_tool(tool_name, tool_path, tool_args).returncode
    elif tool_type == "powershell":
        return run_powershell_tool(tool_name, tool_path, tool_args).returncode
    elif tool_type == "batch":
        return run_batch_tool(tool_name, tool_path, tool_args).returncode
    else:
        print(f"Type d'outil non support: {tool_type}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
        
        lanceur_path = self.target_path / "run_apex_tool.py"
        with open(lanceur_path, 'w', encoding='utf-8') as f:
            f.write(lanceur_content)

# Test de l'agent si excut directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        source_path = sys.argv[1]
        target_path = sys.argv[2]
    else:
        source_path = r"C:\Dev\SuperWhisper_V6\tools"
        target_path = "tools/imported_tools"
        
    # Test avec des donnes simules
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
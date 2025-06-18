#!/usr/bin/env python3
"""
Agent 5 - Documenteur (Gemini 2.0 Flash)
Mission: Gnrer la documentation des outils intgrs dans NextGeneration

Responsabilits:
- Crer la documentation README principale
- Gnrer la documentation individuelle de chaque outil
- Crer les guides d'installation et d'utilisation
- Documenter les catgories d'outils
- Gnrer les exemples d'usage
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re

class AgentDocumenteur:
    """Agent spcialis dans la gnration de documentation avec Gemini 2.0 Flash"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.logger = logging.getLogger("Agent5_Documenteur")
        
    def generate_documentation(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gnration complte de la documentation"""
        self.logger.info(" Dmarrage gnration documentation")
        
        tested_tools = test_data.get("tested_tools", [])
        if not tested_tools:
            self.logger.warning(" Aucun outil test  documenter")
            return {"documentation_files": [], "documentation_summary": {}}
            
        documentation_files = []
        
        # 1. Gnrer le README principal
        main_readme = self.generate_main_readme(tested_tools)
        if main_readme:
            documentation_files.append(main_readme)
            
        # 2. Gnrer la documentation par catgorie
        category_docs = self.generate_category_documentation(tested_tools)
        documentation_files.extend(category_docs)
        
        # 3. Gnrer la documentation individuelle des outils
        tool_docs = self.generate_individual_tool_docs(tested_tools)
        documentation_files.extend(tool_docs)
        
        # 4. Gnrer le guide d'installation
        installation_guide = self.generate_installation_guide(tested_tools)
        if installation_guide:
            documentation_files.append(installation_guide)
            
        # 5. Gnrer le guide d'utilisation
        usage_guide = self.generate_usage_guide(tested_tools)
        if usage_guide:
            documentation_files.append(usage_guide)
            
        # 6. Gnrer le changelog
        changelog = self.generate_changelog(tested_tools)
        if changelog:
            documentation_files.append(changelog)
            
        # Rsum de la documentation
        documentation_summary = self.generate_documentation_summary(documentation_files, tested_tools)
        
        results = {
            "documentation_files": documentation_files,
            "documentation_summary": documentation_summary
        }
        
        self.logger.info(f"[CHECK] Documentation gnre: {len(documentation_files)} fichiers crs")
        return results
        
    def generate_main_readme(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Gnration du README principal"""
        try:
            # Statistiques des outils
            total_tools = len(tested_tools)
            passed_tools = len([t for t in tested_tools if t["overall_status"] == "PASS"])
            categories = {}
            
            for tool in tested_tools:
                category = tool.get("category", "unknown")
                if category not in categories:
                    categories[category] = []
                categories[category].append(tool)
                
            # Gnration du contenu
            content = f"""# NextGeneration Tools - Outils Imports

## Vue d'ensemble

Collection de {total_tools} outils professionnels imports depuis SuperWhisper V6 et adapts pour NextGeneration.

**Statut**: {passed_tools}/{total_tools} outils intgrs avec succs

## Catgories d'Outils

{self.format_categories_list(categories)}

## Installation

```bash
# Installer les dpendances
pip install -r tools/imported_tools/requirements.txt

# Vrifier l'installation
python tools/imported_tools/run_tool.py
```

## Utilisation Rapide

```bash
# Lister les outils disponibles
python tools/imported_tools/run_tool.py

# Excuter un outil
python tools/imported_tools/run_tool.py [nom_outil] [arguments]
```

## Outils Disponibles

{self.format_tools_table(tested_tools)}

## Exemples d'Usage

{self.format_usage_examples(tested_tools[:3])}

## Documentation

- [Guide d'Installation](INSTALLATION.md)
- [Guide d'Utilisation](USAGE.md)
- [Changelog](CHANGELOG.md)
- Documentation par catgorie dans chaque rpertoire

## Support

Les outils sont intgrs avec le systme de logging NextGeneration. Consultez les logs pour le dpannage.
"""
            
            # criture du fichier
            readme_path = self.target_path / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "type": "main_readme",
                "path": str(readme_path),
                "size_bytes": readme_path.stat().st_size,
                "tools_documented": total_tools
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur gnration README principal: {e}")
            return None
            
    def generate_category_documentation(self, tested_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gnration de la documentation par catgorie"""
        category_docs = []
        
        # Grouper par catgorie
        categories = {}
        for tool in tested_tools:
            category = tool.get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(tool)
            
        # Gnrer la doc pour chaque catgorie
        for category, tools in categories.items():
            try:
                content = f"""# {category.title()} - Documentation

## Description

{self.get_category_description(category)}

**Nombre d'outils**: {len(tools)}

## Outils Disponibles

{self.format_category_tools_list(tools)}

## Exemples d'Usage

{self.format_category_usage_examples(tools)}

## Installation

Tous les outils de cette catgorie sont installs automatiquement avec NextGeneration Tools.

## Support

Consultez la documentation individuelle de chaque outil pour plus de dtails.
"""
                
                # Crer le rpertoire de catgorie s'il n'existe pas
                category_path = self.target_path / category
                category_path.mkdir(exist_ok=True)
                
                # crire le fichier README de catgorie
                readme_path = category_path / "README.md"
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                category_docs.append({
                    "type": "category_readme",
                    "category": category,
                    "path": str(readme_path),
                    "size_bytes": readme_path.stat().st_size,
                    "tools_count": len(tools)
                })
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur gnration doc catgorie {category}: {e}")
                
        return category_docs
        
    def generate_individual_tool_docs(self, tested_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gnration de la documentation individuelle des outils"""
        tool_docs = []
        
        for tool in tested_tools:
            try:
                tool_name = tool["name"]
                tool_path = Path(tool["path"])
                
                # Analyser le code de l'outil pour extraire des infos
                tool_analysis = self.analyze_tool_for_documentation(tool_path)
                
                # Gnrer la documentation
                content = f"""# {tool_name} - Documentation

## Description

{tool_analysis.get("description", "Outil import depuis SuperWhisper V6")}

**Catgorie**: {tool.get("category", "unknown")}  
**Statut d'intgration**: {tool.get("overall_status", "UNKNOWN")}  
**Score de qualit**: {tool.get("overall_score", 0)}/100

## Fonctionnalits

{self.format_functions_list(tool_analysis.get("functions", []))}

## Utilisation

{self.format_tool_usage_examples(tool_name, tool_analysis)}

## Configuration

{self.format_tool_configuration(tool_analysis)}

## Dpannage

{self.format_troubleshooting_section(tool)}

---
*Outil adapt depuis SuperWhisper V6 pour NextGeneration*
"""
                
                # crire le fichier de documentation
                doc_path = tool_path.parent / f"{tool_name}_DOC.md"
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                tool_docs.append({
                    "type": "tool_documentation",
                    "tool_name": tool_name,
                    "path": str(doc_path),
                    "size_bytes": doc_path.stat().st_size,
                    "status": tool.get("overall_status", "UNKNOWN")
                })
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur gnration doc outil {tool.get('name', 'unknown')}: {e}")
                
        return tool_docs
        
    def generate_installation_guide(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Gnration du guide d'installation"""
        try:
            # Collecter les dpendances
            all_dependencies = set()
            
            # Lire le fichier requirements.txt s'il existe
            req_file = self.target_path / "requirements.txt"
            if req_file.exists():
                with open(req_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            all_dependencies.add(line)
                            
            content = f"""# Guide d'Installation - NextGeneration Tools

## Prrequis

- Python 3.8+
- NextGeneration project
- Accs en criture au rpertoire tools/

## Installation Automatique

```bash
# Les outils sont dj intgrs dans NextGeneration
# Installer uniquement les dpendances
pip install -r tools/imported_tools/requirements.txt
```

## Dpendances ({len(all_dependencies)})

{self.format_dependencies_list(all_dependencies)}

## Vrification de l'Installation

{self.format_verification_steps(tested_tools[:3])}

## Dpannage

### Problmes courants

1. **Erreur de dpendances**: Rinstaller requirements.txt
2. **Erreur de chemin**: Vrifier la structure NextGeneration
3. **Permissions**: Vrifier les droits d'accs aux fichiers

### Support

Consultez les logs NextGeneration pour plus de dtails sur les erreurs.
"""
            
            # crire le guide d'installation
            install_path = self.target_path / "INSTALLATION.md"
            with open(install_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "type": "installation_guide",
                "path": str(install_path),
                "size_bytes": install_path.stat().st_size,
                "dependencies_count": len(all_dependencies)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur gnration guide installation: {e}")
            return None
            
    def generate_usage_guide(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Gnration du guide d'utilisation"""
        try:
            content = f"""# Guide d'Utilisation - Outils NextGeneration

## Vue d'ensemble

Ce guide vous explique comment utiliser les {len(tested_tools)} outils imports depuis SuperWhisper V6 et adapts pour NextGeneration.

## Mthodes d'Excution

### 1. Excution Directe

```bash
# Depuis le rpertoire de l'outil
cd tools/imported_tools/[category]/
python [tool_name].py [arguments]
```

### 2. Excution via le Lanceur

```bash
# Depuis n'importe o dans NextGeneration
python tools/imported_tools/run_tool.py [tool_name] [arguments]
```

### 3. Excution depuis Python

```python
import sys
sys.path.append('tools/imported_tools')
from [category] import [tool_name]

# Utiliser l'outil...
```

## Outils par Catgorie

{self.format_usage_categories(tested_tools)}

## Exemples d'Usage Courants

{self.format_common_usage_examples(tested_tools)}

## Configuration

Tous les outils sont configurs avec:
- Auto-dtection du projet NextGeneration
- Logging intgr
- Chemins portables
- Configuration centralise

## Dpannage

### Problmes Courants

1. **Import Error**: Vrifiez que les dpendances sont installes
2. **Path Error**: Les outils dtectent automatiquement le projet root
3. **Permission Error**: Vrifiez les permissions d'excution

### Support

Consultez la documentation individuelle de chaque outil ou les logs NextGeneration.
"""
            
            # crire le guide d'utilisation
            usage_path = self.target_path / "USAGE.md"
            with open(usage_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "type": "usage_guide",
                "path": str(usage_path),
                "size_bytes": usage_path.stat().st_size,
                "tools_covered": len(tested_tools)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur gnration guide utilisation: {e}")
            return None
            
    def generate_changelog(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Gnration du changelog"""
        try:
            from datetime import datetime
            
            content = f"""# Changelog - Outils NextGeneration

## Version 1.0.0 - {datetime.now().strftime('%Y-%m-%d')}

### Ajouts
- Intgration de {len(tested_tools)} outils depuis SuperWhisper V6
- Adaptation complte pour NextGeneration
- Configuration portable et auto-dtection projet
- Logging intgr NextGeneration
- Documentation complte

### Outils Intgrs

{self.format_changelog_tools(tested_tools)}

### Amliorations Techniques
- En-ttes NextGeneration standardiss
- Gestion automatique des chemins
- Tests d'intgration complets
- Structure modulaire par catgories

### Configuration
- Fichier de configuration global: `tools_config.json`
- Script de lancement universel: `run_tool.py`
- Requirements automatiques: `requirements.txt`
- Documentation complte par catgorie
"""
            
            # crire le changelog
            changelog_path = self.target_path / "CHANGELOG.md"
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "type": "changelog",
                "path": str(changelog_path),
                "size_bytes": changelog_path.stat().st_size,
                "version": "1.0.0"
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur gnration changelog: {e}")
            return None
            
    def analyze_tool_for_documentation(self, tool_path: Path) -> Dict[str, Any]:
        """Analyse d'un outil pour la documentation"""
        analysis = {
            "description": "",
            "functions": [],
            "classes": [],
            "main_function": None,
            "cli_interface": False,
            "config_files": []
        }
        
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST
            tree = ast.parse(content)
            
            # Extraire la docstring principale
            analysis["description"] = ast.get_docstring(tree) or f"Outil {tool_path.stem}"
            
            # Extraire les fonctions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "args": [arg.arg for arg in node.args.args],
                        "is_main": node.name == "main"
                    }
                    analysis["functions"].append(func_info)
                    
                    if node.name == "main":
                        analysis["main_function"] = func_info
                        
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "methods": []
                    }
                    analysis["classes"].append(class_info)
                    
            # Dtecter interface CLI
            if "argparse" in content or "click" in content or "if __name__ == '__main__':" in content:
                analysis["cli_interface"] = True
                
        except Exception as e:
            self.logger.warning(f" Erreur analyse outil {tool_path}: {e}")
            
        return analysis
        
    def format_categories_list(self, categories: Dict[str, List]) -> str:
        """Formatage de la liste des catgories"""
        lines = []
        for category, tools in categories.items():
            lines.append(f"- **{category.title()}**: {len(tools)} outils")
        return "\n".join(lines)
        
    def format_tools_table(self, tested_tools: List[Dict[str, Any]]) -> str:
        """Formatage du tableau des outils"""
        lines = ["| Outil | Catgorie | Statut | Score |", "|-------|-----------|--------|-------|"]
        
        for tool in tested_tools:
            status_icon = "[CHECK]" if tool.get("overall_status") == "PASS" else ("" if tool.get("overall_status") == "PARTIAL" else "[CROSS]")
            lines.append(f"| {tool['name']} | {tool.get('category', 'unknown')} | {status_icon} {tool.get('overall_status', 'UNKNOWN')} | {tool.get('overall_score', 0)} |")
            
        return "\n".join(lines)
        
    def get_category_description(self, category: str) -> str:
        """Description des catgories"""
        descriptions = {
            "automation": "Outils d'automatisation et de workflows",
            "monitoring": "Outils de surveillance et de monitoring",
            "conversion": "Outils de conversion et transformation de donnes",
            "generation": "Outils de gnration de contenu et de code",
            "utility": "Utilitaires et outils d'aide gnrale",
            "api": "Outils d'API et de communication rseau",
            "data": "Outils de gestion et manipulation de donnes",
            "file": "Outils de gestion de fichiers et rpertoires",
            "network": "Outils rseau et de connectivit",
            "security": "Outils de scurit et cryptographie"
        }
        return descriptions.get(category, f"Outils de catgorie {category}")
        
    def generate_documentation_summary(self, documentation_files: List[Dict[str, Any]], 
                                     tested_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gnration du rsum de documentation"""
        
        # Statistiques par type
        doc_types = {}
        total_size = 0
        
        for doc in documentation_files:
            doc_type = doc.get("type", "unknown")
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            total_size += doc.get("size_bytes", 0)
            
        return {
            "total_files": len(documentation_files),
            "total_size_bytes": total_size,
            "documentation_types": doc_types,
            "tools_documented": len(tested_tools),
            "categories_documented": len(set(tool.get("category") for tool in tested_tools)),
            "documentation_complete": len(documentation_files) >= 4  # README + Installation + Usage + Changelog minimum
        }

    def format_usage_examples(self, tools: List[Dict[str, Any]]) -> str:
        examples = []
        for tool in tools:
            examples.append(f"""### {tool['name']}
```bash
python tools/imported_tools/run_tool.py {tool['name']} --help
```""")
        return "\n\n".join(examples)

    def format_category_tools_list(self, tools: List[Dict[str, Any]]) -> str:
        lines = []
        for tool in tools:
            status_icon = "[CHECK]" if tool.get("overall_status") == "PASS" else ""
            lines.append(f"- **{tool['name']}** {status_icon} - Score: {tool.get('overall_score', 0)}/100")
        return "\n".join(lines)

    def format_category_usage_examples(self, tools: List[Dict[str, Any]]) -> str:
        if not tools:
            return "Aucun exemple disponible."
        
        tool = tools[0]  # Premier outil comme exemple
        return f"""```bash
# Exemple avec {tool['name']}
python tools/imported_tools/run_tool.py {tool['name']} --help
python tools/imported_tools/{tool.get('category', 'utility')}/{tool['name']}.py
```"""

    def format_functions_list(self, functions: List[Dict[str, Any]]) -> str:
        if not functions:
            return "Aucune fonction documente."
        
        lines = []
        for func in functions:
            lines.append(f"- **{func['name']}()**: {func.get('docstring', 'Fonction utilitaire')}")
        return "\n".join(lines)

    def format_tool_usage_examples(self, tool_name: str, analysis: Dict[str, Any]) -> str:
        examples = [f"""```bash
# Excution directe
python tools/imported_tools/*//{tool_name}.py

# Via le lanceur
python tools/imported_tools/run_tool.py {tool_name}
```"""]
        
        if analysis.get("cli_interface"):
            examples.append(f"""```bash
# Aide
python tools/imported_tools/run_tool.py {tool_name} --help
```""")
        
        return "\n\n".join(examples)

    def format_tool_configuration(self, analysis: Dict[str, Any]) -> str:
        return """L'outil est configur automatiquement avec:
- Auto-dtection du projet NextGeneration
- Logging intgr
- Chemins portables
- Configuration centralise"""

    def format_troubleshooting_section(self, tool: Dict[str, Any]) -> str:
        return f"""### Problmes courants

1. **Erreur d'import**: Vrifier les dpendances
2. **Erreur de chemin**: L'outil dtecte automatiquement NextGeneration
3. **Erreur d'excution**: Consulter les logs NextGeneration

**Statut actuel**: {tool.get('overall_status', 'UNKNOWN')}
**Score de qualit**: {tool.get('overall_score', 0)}/100"""

    def format_dependencies_list(self, dependencies: set) -> str:
        if not dependencies:
            return "Aucune dpendance externe requise."
        
        lines = []
        for dep in sorted(dependencies):
            lines.append(f"- {dep}")
        return "\n".join(lines)

    def format_verification_steps(self, tools: List[Dict[str, Any]]) -> str:
        steps = ["```bash", "# Vrifier que les outils sont disponibles"]
        for tool in tools:
            steps.append(f"python tools/imported_tools/run_tool.py {tool['name']} --help")
        steps.append("```")
        return "\n".join(steps)

    def format_usage_categories(self, tested_tools: List[Dict[str, Any]]) -> str:
        categories = {}
        for tool in tested_tools:
            category = tool.get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(tool)
        
        sections = []
        for category, tools in categories.items():
            sections.append(f"""### {category.title()}

{self.format_category_tools_list(tools)}""")
        
        return "\n\n".join(sections)

    def format_common_usage_examples(self, tested_tools: List[Dict[str, Any]]) -> str:
        examples = []
        for i, tool in enumerate(tested_tools[:5]):  # 5 premiers exemples
            examples.append(f"""#### Exemple {i+1}: {tool['name']}
```bash
python tools/imported_tools/run_tool.py {tool['name']}
```""")
        return "\n\n".join(examples)

    def format_changelog_tools(self, tested_tools: List[Dict[str, Any]]) -> str:
        categories = {}
        for tool in tested_tools:
            category = tool.get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(tool['name'])
        
        sections = []
        for category, tools in categories.items():
            sections.append(f"#### {category.title()}")
            for tool in tools:
                sections.append(f"- {tool}")
            sections.append("")
        
        return "\n".join(sections)
    
    def generer_documentation_apex(self, phase4_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gnration de documentation spcialise pour les outils Apex_VBA_FRAMEWORK
        
        Args:
            phase4_data: Donnes des tests de la phase 4
            
        Returns:
            Dict contenant les rsultats de gnration de documentation
        """
        self.logger.info(" Gnration documentation spcialise Apex_VBA_FRAMEWORK")
        
        docs_generees = []
        outils_testes = phase4_data.get("outils_testes", [])
        
        # Gnrer README principal pour Apex
        readme_apex = self._generer_readme_apex(outils_testes)
        docs_generees.append(readme_apex)
        
        # Gnrer documentation pour chaque outil
        for outil in outils_testes:
            if outil.get("test_success", False):
                doc_outil = self._generer_doc_outil_apex(outil)
                if doc_outil:
                    docs_generees.append(doc_outil)
        
        # Gnrer guide d'installation Apex
        guide_install = self._generer_guide_installation_apex(outils_testes)
        docs_generees.append(guide_install)
        
        resultats = {
            "total_docs": len(docs_generees),
            "docs_generees": docs_generees,
            "documentation_timestamp": datetime.now().isoformat(),
            "documenteur_model": "Gemini 2.0 Flash"
        }
        
        self.logger.info(f"[CHECK] Documentation Apex termine: {len(docs_generees)} documents crs")
        return resultats
    
    def _generer_readme_apex(self, outils_testes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gnration du README principal pour outils Apex"""
        readme_content = f'''# Outils Imports depuis Apex_VBA_FRAMEWORK

## [CLIPBOARD] Aperu

Cette collection contient {len(outils_testes)} outils imports et adapts depuis Apex_VBA_FRAMEWORK pour NextGeneration.

## [ROCKET] Outils Disponibles

'''
        
        # Grouper par type
        outils_par_type = {}
        for outil in outils_testes:
            type_outil = outil.get("type", "unknown")
            if type_outil not in outils_par_type:
                outils_par_type[type_outil] = []
            outils_par_type[type_outil].append(outil)
        
        for type_outil, outils in outils_par_type.items():
            readme_content += f"### {type_outil.title()}\n\n"
            for outil in outils:
                status = "[CHECK]" if outil.get("test_success", False) else ""
                readme_content += f"- {status} **{outil['name']}** - {outil.get('test_summary', 'Outil Apex')}\n"
            readme_content += "\n"
        
        readme_content += '''## [TOOL] Utilisation

### Lanceur Universel

```bash
python run_apex_tool.py <nom_outil> [arguments...]
```

### Liste des outils disponibles

```bash
python run_apex_tool.py
```

## [FOLDER] Structure

```
apex_tools/
 python/          # Outils Python adapts
 powershell/      # Scripts PowerShell adapts  
 batch/           # Scripts Batch adapts
 apex_tools_config.json  # Configuration
 run_apex_tool.py # Lanceur universel
```

##  Intgration NextGeneration

Tous les outils ont t adapts pour fonctionner dans l'environnement NextGeneration avec:
- Dtection automatique du projet root
- Configuration portable
- En-ttes NextGeneration standardiss

##  Documentation

Consultez les fichiers de documentation individuels pour chaque outil dans leurs rpertoires respectifs.
'''
        
        readme_path = self.target_path / "README_APEX.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return {
            "type": "readme",
            "name": "README_APEX.md",
            "path": str(readme_path),
            "content_length": len(readme_content)
        }
    
    def _generer_doc_outil_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Gnration de documentation pour un outil Apex spcifique"""
        try:
            nom_outil = outil["name"]
            type_outil = outil["type"]
            
            doc_content = f'''# {nom_outil}

## [CLIPBOARD] Informations

- **Type**: {type_outil}
- **Source**: Apex_VBA_FRAMEWORK
- **Statut**: {"[CHECK] Test avec succs" if outil.get("test_success") else " Tests partiels"}

## [TOOL] Utilisation

### Via le lanceur universel
```bash
python run_apex_tool.py {nom_outil} [arguments...]
```

### Excution directe
```bash
'''
            
            if type_outil == "python":
                doc_content += f"python {type_outil}/{nom_outil}.py [arguments...]\n"
            elif type_outil == "powershell":
                doc_content += f"powershell -ExecutionPolicy Bypass -File {type_outil}/{nom_outil}.ps1 [arguments...]\n"
            elif type_outil == "batch":
                doc_content += f"{type_outil}/{nom_outil}.bat [arguments...]\n"
            
            doc_content += '''```

## [CHART] Tests d'Intgration

'''
            
            test_details = outil.get("test_details", {})
            for test_name, test_result in test_details.items():
                status = "[CHECK]" if test_result else "[CROSS]"
                doc_content += f"- {status} {test_name.replace('_', ' ').title()}\n"
            
            doc_content += f'''

##  Intgration NextGeneration

Cet outil a t adapt pour NextGeneration avec:
- Configuration portable automatique
- Dtection du projet root
- En-tte NextGeneration standardis

##  Notes

- Import depuis: Apex_VBA_FRAMEWORK
- Adaptation: Automatique via Agent 3 (Claude Sonnet 4)
- Tests: Agent 4 (GPT-4 Turbo)
- Documentation: Agent 5 (Gemini 2.0 Flash)
'''
            
            doc_path = self.target_path / type_outil / f"{nom_outil}_README.md"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            
            return {
                "type": "tool_doc",
                "name": f"{nom_outil}_README.md",
                "path": str(doc_path),
                "tool_name": nom_outil,
                "content_length": len(doc_content)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur gnration doc {outil['name']}: {e}")
            return None
    
    def _generer_guide_installation_apex(self, outils_testes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gnration du guide d'installation pour outils Apex"""
        guide_content = '''# Guide d'Installation - Outils Apex_VBA_FRAMEWORK

## [ROCKET] Installation Rapide

1. **Vrifier les prrequis**
   ```bash
   python --version  # Python 3.8+
   ```

2. **Installer les dpendances** (si ncessaire)
   ```bash
   pip install -r requirements.txt
   ```

3. **Tester l'installation**
   ```bash
   python run_apex_tool.py
   ```

## [TOOL] Configuration

### Variables d'Environnement

Les outils Apex utilisent la dtection automatique du projet NextGeneration.
Aucune configuration manuelle n'est requise.

### PowerShell (Windows)

Pour les outils PowerShell, assurez-vous que l'excution de scripts est autorise:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

##  Tests

### Test Global
```bash
python -m pytest tests/  # Si des tests sont disponibles
```

### Test Individuel
```bash
python run_apex_tool.py <nom_outil> --help
```

## [SEARCH] Dpannage

### Erreurs Communes

1. **Outil introuvable**
   - Vrifiez que le nom est correct avec `python run_apex_tool.py`

2. **Erreur d'importation Python**
   - Installez les dpendances: `pip install -r requirements.txt`

3. **Erreur PowerShell**
   - Vrifiez la politique d'excution
   - Utilisez: `powershell -ExecutionPolicy Bypass -File ...`

##  Support

Pour les problmes spcifiques aux outils Apex:
1. Consultez la documentation individuelle de chaque outil
2. Vrifiez les logs dans le rpertoire `logs/`
3. Rfrez-vous  la documentation NextGeneration

##  Ressources

- [Documentation NextGeneration](../docs/)
- [Apex_VBA_FRAMEWORK Original](G:/Dev/Apex_VBA_FRAMEWORK/)
'''
        
        guide_path = self.target_path / "INSTALLATION_GUIDE_APEX.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return {
            "type": "installation_guide",
            "name": "INSTALLATION_GUIDE_APEX.md", 
            "path": str(guide_path),
            "content_length": len(guide_content)
        }

# Test de l'agent si excut directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = "tools/imported_tools"
        
    # Test avec des donnes simules
    test_data = {
        "tested_tools": [
            {
                "name": "test_tool",
                "category": "utility",
                "path": "tools/imported_tools/utility/test_tool.py",
                "overall_status": "PASS",
                "overall_score": 85
            }
        ]
    }
    
    agent = AgentDocumenteur(target_path)
    results = agent.generate_documentation(test_data)
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
#!/usr/bin/env python3
"""
Agent 5 - Documenteur (Gemini 2.0 Flash)
Mission: Générer la documentation des outils intégrés dans NextGeneration

Responsabilités:
- Créer la documentation README principale
- Générer la documentation individuelle de chaque outil
- Créer les guides d'installation et d'utilisation
- Documenter les catégories d'outils
- Générer les exemples d'usage
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re

class AgentDocumenteur:
    """Agent spécialisé dans la génération de documentation avec Gemini 2.0 Flash"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.logger = logging.getLogger("Agent5_Documenteur")
        
    def generate_documentation(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Génération complète de la documentation"""
        self.logger.info("📚 Démarrage génération documentation")
        
        tested_tools = test_data.get("tested_tools", [])
        if not tested_tools:
            self.logger.warning("⚠️ Aucun outil testé à documenter")
            return {"documentation_files": [], "documentation_summary": {}}
            
        documentation_files = []
        
        # 1. Générer le README principal
        main_readme = self.generate_main_readme(tested_tools)
        if main_readme:
            documentation_files.append(main_readme)
            
        # 2. Générer la documentation par catégorie
        category_docs = self.generate_category_documentation(tested_tools)
        documentation_files.extend(category_docs)
        
        # 3. Générer la documentation individuelle des outils
        tool_docs = self.generate_individual_tool_docs(tested_tools)
        documentation_files.extend(tool_docs)
        
        # 4. Générer le guide d'installation
        installation_guide = self.generate_installation_guide(tested_tools)
        if installation_guide:
            documentation_files.append(installation_guide)
            
        # 5. Générer le guide d'utilisation
        usage_guide = self.generate_usage_guide(tested_tools)
        if usage_guide:
            documentation_files.append(usage_guide)
            
        # 6. Générer le changelog
        changelog = self.generate_changelog(tested_tools)
        if changelog:
            documentation_files.append(changelog)
            
        # Résumé de la documentation
        documentation_summary = self.generate_documentation_summary(documentation_files, tested_tools)
        
        results = {
            "documentation_files": documentation_files,
            "documentation_summary": documentation_summary
        }
        
        self.logger.info(f"✅ Documentation générée: {len(documentation_files)} fichiers créés")
        return results
        
    def generate_main_readme(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Génération du README principal"""
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
                
            # Génération du contenu
            content = f"""# NextGeneration Tools - Outils Importés

## Vue d'ensemble

Collection de {total_tools} outils professionnels importés depuis SuperWhisper V6 et adaptés pour NextGeneration.

**Statut**: {passed_tools}/{total_tools} outils intégrés avec succès

## Catégories d'Outils

{self.format_categories_list(categories)}

## Installation

```bash
# Installer les dépendances
pip install -r tools/imported_tools/requirements.txt

# Vérifier l'installation
python tools/imported_tools/run_tool.py
```

## Utilisation Rapide

```bash
# Lister les outils disponibles
python tools/imported_tools/run_tool.py

# Exécuter un outil
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
- Documentation par catégorie dans chaque répertoire

## Support

Les outils sont intégrés avec le système de logging NextGeneration. Consultez les logs pour le dépannage.
"""
            
            # Écriture du fichier
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
            self.logger.error(f"❌ Erreur génération README principal: {e}")
            return None
            
    def generate_category_documentation(self, tested_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Génération de la documentation par catégorie"""
        category_docs = []
        
        # Grouper par catégorie
        categories = {}
        for tool in tested_tools:
            category = tool.get("category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(tool)
            
        # Générer la doc pour chaque catégorie
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

Tous les outils de cette catégorie sont installés automatiquement avec NextGeneration Tools.

## Support

Consultez la documentation individuelle de chaque outil pour plus de détails.
"""
                
                # Créer le répertoire de catégorie s'il n'existe pas
                category_path = self.target_path / category
                category_path.mkdir(exist_ok=True)
                
                # Écrire le fichier README de catégorie
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
                self.logger.error(f"❌ Erreur génération doc catégorie {category}: {e}")
                
        return category_docs
        
    def generate_individual_tool_docs(self, tested_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Génération de la documentation individuelle des outils"""
        tool_docs = []
        
        for tool in tested_tools:
            try:
                tool_name = tool["name"]
                tool_path = Path(tool["path"])
                
                # Analyser le code de l'outil pour extraire des infos
                tool_analysis = self.analyze_tool_for_documentation(tool_path)
                
                # Générer la documentation
                content = f"""# {tool_name} - Documentation

## Description

{tool_analysis.get("description", "Outil importé depuis SuperWhisper V6")}

**Catégorie**: {tool.get("category", "unknown")}  
**Statut d'intégration**: {tool.get("overall_status", "UNKNOWN")}  
**Score de qualité**: {tool.get("overall_score", 0)}/100

## Fonctionnalités

{self.format_functions_list(tool_analysis.get("functions", []))}

## Utilisation

{self.format_tool_usage_examples(tool_name, tool_analysis)}

## Configuration

{self.format_tool_configuration(tool_analysis)}

## Dépannage

{self.format_troubleshooting_section(tool)}

---
*Outil adapté depuis SuperWhisper V6 pour NextGeneration*
"""
                
                # Écrire le fichier de documentation
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
                self.logger.error(f"❌ Erreur génération doc outil {tool.get('name', 'unknown')}: {e}")
                
        return tool_docs
        
    def generate_installation_guide(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Génération du guide d'installation"""
        try:
            # Collecter les dépendances
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

## Prérequis

- Python 3.8+
- NextGeneration project
- Accès en écriture au répertoire tools/

## Installation Automatique

```bash
# Les outils sont déjà intégrés dans NextGeneration
# Installer uniquement les dépendances
pip install -r tools/imported_tools/requirements.txt
```

## Dépendances ({len(all_dependencies)})

{self.format_dependencies_list(all_dependencies)}

## Vérification de l'Installation

{self.format_verification_steps(tested_tools[:3])}

## Dépannage

### Problèmes courants

1. **Erreur de dépendances**: Réinstaller requirements.txt
2. **Erreur de chemin**: Vérifier la structure NextGeneration
3. **Permissions**: Vérifier les droits d'accès aux fichiers

### Support

Consultez les logs NextGeneration pour plus de détails sur les erreurs.
"""
            
            # Écrire le guide d'installation
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
            self.logger.error(f"❌ Erreur génération guide installation: {e}")
            return None
            
    def generate_usage_guide(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Génération du guide d'utilisation"""
        try:
            content = f"""# Guide d'Utilisation - Outils NextGeneration

## Vue d'ensemble

Ce guide vous explique comment utiliser les {len(tested_tools)} outils importés depuis SuperWhisper V6 et adaptés pour NextGeneration.

## Méthodes d'Exécution

### 1. Exécution Directe

```bash
# Depuis le répertoire de l'outil
cd tools/imported_tools/[category]/
python [tool_name].py [arguments]
```

### 2. Exécution via le Lanceur

```bash
# Depuis n'importe où dans NextGeneration
python tools/imported_tools/run_tool.py [tool_name] [arguments]
```

### 3. Exécution depuis Python

```python
import sys
sys.path.append('tools/imported_tools')
from [category] import [tool_name]

# Utiliser l'outil...
```

## Outils par Catégorie

{self.format_usage_categories(tested_tools)}

## Exemples d'Usage Courants

{self.format_common_usage_examples(tested_tools)}

## Configuration

Tous les outils sont configurés avec:
- Auto-détection du projet NextGeneration
- Logging intégré
- Chemins portables
- Configuration centralisée

## Dépannage

### Problèmes Courants

1. **Import Error**: Vérifiez que les dépendances sont installées
2. **Path Error**: Les outils détectent automatiquement le projet root
3. **Permission Error**: Vérifiez les permissions d'exécution

### Support

Consultez la documentation individuelle de chaque outil ou les logs NextGeneration.
"""
            
            # Écrire le guide d'utilisation
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
            self.logger.error(f"❌ Erreur génération guide utilisation: {e}")
            return None
            
    def generate_changelog(self, tested_tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Génération du changelog"""
        try:
            from datetime import datetime
            
            content = f"""# Changelog - Outils NextGeneration

## Version 1.0.0 - {datetime.now().strftime('%Y-%m-%d')}

### Ajouts
- Intégration de {len(tested_tools)} outils depuis SuperWhisper V6
- Adaptation complète pour NextGeneration
- Configuration portable et auto-détection projet
- Logging intégré NextGeneration
- Documentation complète

### Outils Intégrés

{self.format_changelog_tools(tested_tools)}

### Améliorations Techniques
- En-têtes NextGeneration standardisés
- Gestion automatique des chemins
- Tests d'intégration complets
- Structure modulaire par catégories

### Configuration
- Fichier de configuration global: `tools_config.json`
- Script de lancement universel: `run_tool.py`
- Requirements automatiques: `requirements.txt`
- Documentation complète par catégorie
"""
            
            # Écrire le changelog
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
            self.logger.error(f"❌ Erreur génération changelog: {e}")
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
                    
            # Détecter interface CLI
            if "argparse" in content or "click" in content or "if __name__ == '__main__':" in content:
                analysis["cli_interface"] = True
                
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur analyse outil {tool_path}: {e}")
            
        return analysis
        
    def format_categories_list(self, categories: Dict[str, List]) -> str:
        """Formatage de la liste des catégories"""
        lines = []
        for category, tools in categories.items():
            lines.append(f"- **{category.title()}**: {len(tools)} outils")
        return "\n".join(lines)
        
    def format_tools_table(self, tested_tools: List[Dict[str, Any]]) -> str:
        """Formatage du tableau des outils"""
        lines = ["| Outil | Catégorie | Statut | Score |", "|-------|-----------|--------|-------|"]
        
        for tool in tested_tools:
            status_icon = "✅" if tool.get("overall_status") == "PASS" else ("⚠️" if tool.get("overall_status") == "PARTIAL" else "❌")
            lines.append(f"| {tool['name']} | {tool.get('category', 'unknown')} | {status_icon} {tool.get('overall_status', 'UNKNOWN')} | {tool.get('overall_score', 0)} |")
            
        return "\n".join(lines)
        
    def get_category_description(self, category: str) -> str:
        """Description des catégories"""
        descriptions = {
            "automation": "Outils d'automatisation et de workflows",
            "monitoring": "Outils de surveillance et de monitoring",
            "conversion": "Outils de conversion et transformation de données",
            "generation": "Outils de génération de contenu et de code",
            "utility": "Utilitaires et outils d'aide générale",
            "api": "Outils d'API et de communication réseau",
            "data": "Outils de gestion et manipulation de données",
            "file": "Outils de gestion de fichiers et répertoires",
            "network": "Outils réseau et de connectivité",
            "security": "Outils de sécurité et cryptographie"
        }
        return descriptions.get(category, f"Outils de catégorie {category}")
        
    def generate_documentation_summary(self, documentation_files: List[Dict[str, Any]], 
                                     tested_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Génération du résumé de documentation"""
        
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
            status_icon = "✅" if tool.get("overall_status") == "PASS" else "⚠️"
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
            return "Aucune fonction documentée."
        
        lines = []
        for func in functions:
            lines.append(f"- **{func['name']}()**: {func.get('docstring', 'Fonction utilitaire')}")
        return "\n".join(lines)

    def format_tool_usage_examples(self, tool_name: str, analysis: Dict[str, Any]) -> str:
        examples = [f"""```bash
# Exécution directe
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
        return """L'outil est configuré automatiquement avec:
- Auto-détection du projet NextGeneration
- Logging intégré
- Chemins portables
- Configuration centralisée"""

    def format_troubleshooting_section(self, tool: Dict[str, Any]) -> str:
        return f"""### Problèmes courants

1. **Erreur d'import**: Vérifier les dépendances
2. **Erreur de chemin**: L'outil détecte automatiquement NextGeneration
3. **Erreur d'exécution**: Consulter les logs NextGeneration

**Statut actuel**: {tool.get('overall_status', 'UNKNOWN')}
**Score de qualité**: {tool.get('overall_score', 0)}/100"""

    def format_dependencies_list(self, dependencies: set) -> str:
        if not dependencies:
            return "Aucune dépendance externe requise."
        
        lines = []
        for dep in sorted(dependencies):
            lines.append(f"- {dep}")
        return "\n".join(lines)

    def format_verification_steps(self, tools: List[Dict[str, Any]]) -> str:
        steps = ["```bash", "# Vérifier que les outils sont disponibles"]
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

# Test de l'agent si exécuté directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = "tools/imported_tools"
        
    # Test avec des données simulées
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
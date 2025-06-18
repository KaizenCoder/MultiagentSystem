#!/usr/bin/env python3
"""
Agent 1 - Analyseur de Structure (Claude Sonnet 4)
Mission: Analyser la structure des outils dans SuperWhisper_V6/tools

Responsabilits:
- Scanner tous les fichiers Python dans le rpertoire source
- Analyser la structure AST de chaque fichier
- Identifier les types d'outils (automation, monitoring, conversion, etc.)
- Extraire les dpendances et mtadonnes
- Classer les outils par utilit potentielle
"""

import os
import ast
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import importlib.util
import re
from datetime import datetime

class AgentAnalyseurStructure:
    """Agent spcialis dans l'analyse de structure de code Python avec Claude Sonnet 4"""
    
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.logger = logging.getLogger("Agent1_AnalyseurStructure")
        self.analysis_results = {
            "tools": [],
            "categories": {},
            "dependencies": set(),
            "total_files": 0,
            "analyzable_files": 0
        }
        
    def analyze_tools_structure(self) -> Dict[str, Any]:
        """Analyse complte de la structure des outils"""
        self.logger.info(f"[SEARCH] Dmarrage analyse structure: {self.source_path}")
        
        if not self.source_path.exists():
            raise FileNotFoundError(f"Rpertoire source introuvable: {self.source_path}")
            
        # Scanner tous les fichiers Python
        python_files = list(self.source_path.rglob("*.py"))
        self.analysis_results["total_files"] = len(python_files)
        
        self.logger.info(f"[FOLDER] {len(python_files)} fichiers Python trouvs")
        
        # Analyser chaque fichier
        for py_file in python_files:
            try:
                tool_info = self.analyze_single_file(py_file)
                if tool_info:
                    self.analysis_results["tools"].append(tool_info)
                    self.analysis_results["analyzable_files"] += 1
                    
            except Exception as e:
                self.logger.warning(f" Erreur analyse {py_file.name}: {e}")
                
        # Catgoriser les outils
        self.categorize_tools()
        
        # Finaliser l'analyse
        self.analysis_results["dependencies"] = list(self.analysis_results["dependencies"])
        
        self.logger.info(f"[CHECK] Analyse termine: {self.analysis_results['analyzable_files']} outils analyss")
        return self.analysis_results
        
    def analyze_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyse dtaille d'un fichier Python unique"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST
            tree = ast.parse(content)
            
            # Extraction des informations
            tool_info = {
                "name": file_path.stem,
                "path": str(file_path.relative_to(self.source_path)),
                "size_bytes": file_path.stat().st_size,
                "lines_count": len(content.splitlines()),
                "functions": [],
                "classes": [],
                "imports": [],
                "docstring": ast.get_docstring(tree),
                "complexity_score": 0,
                "tool_type": "unknown",
                "utility_indicators": []
            }
            
            # Analyse AST dtaille
            self.extract_ast_elements(tree, tool_info)
            
            # Classification du type d'outil
            tool_info["tool_type"] = self.classify_tool_type(tool_info, content)
            
            # Score de complexit
            tool_info["complexity_score"] = self.calculate_complexity_score(tool_info)
            
            # Indicateurs d'utilit
            tool_info["utility_indicators"] = self.extract_utility_indicators(tool_info, content)
            
            return tool_info
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur analyse fichier {file_path}: {e}")
            return None
            
    def extract_ast_elements(self, tree: ast.AST, tool_info: Dict[str, Any]):
        """Extraction des lments AST (fonctions, classes, imports)"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args_count": len(node.args.args),
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "decorators": [ast.unparse(d) for d in node.decorator_list],
                    "docstring": ast.get_docstring(node)
                }
                tool_info["functions"].append(func_info)
                
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods_count": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "bases": [ast.unparse(base) for base in node.bases],
                    "docstring": ast.get_docstring(node)
                }
                tool_info["classes"].append(class_info)
                
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_name = alias.name
                        tool_info["imports"].append(import_name)
                        self.analysis_results["dependencies"].add(import_name)
                        
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        import_name = f"{module}.{alias.name}" if module else alias.name
                        tool_info["imports"].append(import_name)
                        if module:
                            self.analysis_results["dependencies"].add(module)
                            
    def classify_tool_type(self, tool_info: Dict[str, Any], content: str) -> str:
        """Classification intelligente du type d'outil base sur l'analyse du code"""
        
        # Mots-cls pour chaque catgorie
        categories_keywords = {
            "automation": ["schedule", "cron", "task", "job", "workflow", "pipeline", "automation"],
            "monitoring": ["monitor", "watch", "log", "metric", "alert", "health", "status"],
            "conversion": ["convert", "transform", "parse", "format", "encode", "decode"],
            "generation": ["generate", "create", "build", "make", "produce", "template"],
            "utility": ["util", "helper", "tool", "common", "shared", "base"],
            "api": ["request", "response", "endpoint", "route", "server", "client"],
            "data": ["database", "db", "sql", "query", "data", "storage"],
            "file": ["file", "directory", "path", "folder", "io", "read", "write"],
            "network": ["http", "https", "socket", "network", "connection", "url"],
            "security": ["auth", "token", "encrypt", "decrypt", "hash", "security"]
        }
        
        # Analyse du nom de fichier
        filename_lower = tool_info["name"].lower()
        
        # Analyse du contenu (docstring + code)
        content_lower = content.lower()
        docstring_lower = (tool_info["docstring"] or "").lower()
        
        category_scores = {}
        
        for category, keywords in categories_keywords.items():
            score = 0
            
            # Score bas sur le nom de fichier (poids lev)
            for keyword in keywords:
                if keyword in filename_lower:
                    score += 3
                    
            # Score bas sur la docstring (poids moyen)
            for keyword in keywords:
                if keyword in docstring_lower:
                    score += 2
                    
            # Score bas sur le contenu (poids faible)
            for keyword in keywords:
                score += content_lower.count(keyword) * 0.5
                
            # Score bas sur les imports
            for import_name in tool_info["imports"]:
                for keyword in keywords:
                    if keyword in import_name.lower():
                        score += 1
                        
            category_scores[category] = score
            
        # Retourner la catgorie avec le score le plus lev
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
                
        return "utility"  # Catgorie par dfaut
        
    def calculate_complexity_score(self, tool_info: Dict[str, Any]) -> int:
        """Calcul du score de complexit de l'outil"""
        score = 0
        
        # Complexit base sur le nombre de fonctions
        score += len(tool_info["functions"]) * 2
        
        # Complexit base sur le nombre de classes
        score += len(tool_info["classes"]) * 5
        
        # Complexit base sur les imports
        score += len(tool_info["imports"])
        
        # Complexit base sur la taille
        score += tool_info["lines_count"] // 10
        
        # Bonus pour les fonctions async
        async_functions = sum(1 for f in tool_info["functions"] if f["is_async"])
        score += async_functions * 3
        
        # Bonus pour les dcorateurs
        decorated_functions = sum(1 for f in tool_info["functions"] if f["decorators"])
        score += decorated_functions * 2
        
        return score
        
    def extract_utility_indicators(self, tool_info: Dict[str, Any], content: str) -> List[str]:
        """Extraction des indicateurs d'utilit de l'outil"""
        indicators = []
        
        # Indicateurs bass sur la structure
        if len(tool_info["functions"]) > 5:
            indicators.append("multi_functional")
            
        if len(tool_info["classes"]) > 0:
            indicators.append("object_oriented")
            
        if any(f["is_async"] for f in tool_info["functions"]):
            indicators.append("async_capable")
            
        # Indicateurs bass sur les imports
        important_libs = ["requests", "asyncio", "pathlib", "json", "yaml", "sqlite3", "pandas"]
        for lib in important_libs:
            if any(lib in imp for imp in tool_info["imports"]):
                indicators.append(f"uses_{lib}")
                
        # Indicateurs bass sur le contenu
        if "if __name__ == '__main__':" in content:
            indicators.append("executable_script")
            
        if "argparse" in content or "click" in content:
            indicators.append("cli_interface")
            
        if "logging" in content:
            indicators.append("has_logging")
            
        if "config" in content.lower():
            indicators.append("configurable")
            
        # Indicateurs de qualit
        if tool_info["docstring"]:
            indicators.append("documented")
            
        if any(f["docstring"] for f in tool_info["functions"]):
            indicators.append("functions_documented")
            
        return indicators
        
    def categorize_tools(self):
        """Catgorisation finale des outils analyss"""
        categories = {}
        
        for tool in self.analysis_results["tools"]:
            tool_type = tool["tool_type"]
            if tool_type not in categories:
                categories[tool_type] = []
            categories[tool_type].append(tool["name"])
            
        self.analysis_results["categories"] = categories
        
        # Log des statistiques
        for category, tools in categories.items():
            self.logger.info(f"[CHART] {category}: {len(tools)} outils")
    
    def analyser_structure_apex(self, apex_tools_dir: str) -> Dict[str, Any]:
        """
        Analyse spcialise pour les outils Apex_VBA_FRAMEWORK
        
        Args:
            apex_tools_dir: Rpertoire des outils Apex_VBA_FRAMEWORK
            
        Returns:
            Dict contenant l'analyse complte des outils Apex
        """
        self.logger.info(f"[SEARCH] Analyse spcialise Apex_VBA_FRAMEWORK: {apex_tools_dir}")
        
        apex_path = Path(apex_tools_dir)
        if not apex_path.exists():
            raise FileNotFoundError(f"Rpertoire Apex introuvable: {apex_tools_dir}")
        
        # Analyse des diffrents types d'outils dans Apex
        outils_apex = {
            "python_tools": [],
            "powershell_tools": [],
            "batch_tools": [],
            "vba_tools": [],
            "config_tools": [],
            "directories": []
        }
        
        # Scanner tous les fichiers et rpertoires
        for item in apex_path.rglob("*"):
            if item.is_file():
                if item.suffix == ".py":
                    # Analyser les outils Python
                    analyse = self.analyze_single_file(item)
                    if analyse:
                        analyse["category"] = "python"
                        analyse["apex_subdir"] = item.parent.name
                        outils_apex["python_tools"].append(analyse)
                
                elif item.suffix == ".ps1":
                    # Analyser les scripts PowerShell
                    analyse = self._analyser_fichier_powershell(item)
                    if analyse:
                        analyse["category"] = "powershell"
                        analyse["apex_subdir"] = item.parent.name
                        outils_apex["powershell_tools"].append(analyse)
                
                elif item.suffix in [".bat", ".cmd"]:
                    # Analyser les scripts batch
                    analyse = self._analyser_fichier_batch(item)
                    if analyse:
                        analyse["category"] = "batch"
                        analyse["apex_subdir"] = item.parent.name
                        outils_apex["batch_tools"].append(analyse)
        
        # Statistiques globales
        total_tools = (len(outils_apex["python_tools"]) + 
                      len(outils_apex["powershell_tools"]) + 
                      len(outils_apex["batch_tools"]))
        
        # Classification par sous-rpertoire Apex
        categories_apex = {}
        for tool_type in ["python_tools", "powershell_tools", "batch_tools"]:
            for tool in outils_apex[tool_type]:
                subdir = tool.get("apex_subdir", "root")
                if subdir not in categories_apex:
                    categories_apex[subdir] = 0
                categories_apex[subdir] += 1
        
        resultats = {
            "source_directory": apex_tools_dir,
            "total_tools": total_tools,
            "tools_by_type": {
                "python": len(outils_apex["python_tools"]),
                "powershell": len(outils_apex["powershell_tools"]),
                "batch": len(outils_apex["batch_tools"])
            },
            "apex_directories": outils_apex["directories"],
            "tools_by_apex_category": categories_apex,
            "detailed_analysis": outils_apex,
            "analysis_timestamp": datetime.now().isoformat(),
            "analyzer_model": "Claude Sonnet 4"
        }
        
        self.logger.info(f"[CHECK] Analyse Apex termine: {total_tools} outils trouvs")
        return resultats
    
    def _analyser_fichier_powershell(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Analyse un fichier PowerShell"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Dtection des fonctions PowerShell
            functions = []
            for line in content.split('\n'):
                if line.strip().startswith('function ') or line.strip().startswith('Function '):
                    func_name = line.split()[1].split('(')[0] if len(line.split()) > 1 else "unknown"
                    functions.append(func_name)
            
            return {
                "name": filepath.stem,
                "path": str(filepath),
                "size": filepath.stat().st_size,
                "functions": functions,
                "lines_count": len(content.split('\n')),
                "tool_type": "powershell_script",
                "complexity_score": len(functions) * 2 + len(content.split('\n')) // 10
            }
        except Exception as e:
            self.logger.warning(f" Erreur analyse PowerShell {filepath}: {e}")
            return None
    
    def _analyser_fichier_batch(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Analyse un fichier batch"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Dtection des commandes batch importantes
            commands = []
            for line in content.split('\n'):
                line = line.strip().upper()
                if line and not line.startswith('::') and not line.startswith('REM'):
                    for cmd in ['ECHO', 'SET', 'IF', 'FOR', 'CALL', 'GOTO', 'XCOPY', 'ROBOCOPY']:
                        if line.startswith(cmd):
                            commands.append(cmd)
            
            return {
                "name": filepath.stem,
                "path": str(filepath),
                "size": filepath.stat().st_size,
                "commands": list(set(commands)),
                "lines_count": len(content.split('\n')),
                "tool_type": "batch_script",
                "complexity_score": len(set(commands)) * 3 + len(content.split('\n')) // 5
            }
        except Exception as e:
            self.logger.warning(f" Erreur analyse Batch {filepath}: {e}")
            return None

# Test de l'agent si excut directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        source_path = sys.argv[1]
    else:
        source_path = r"C:\Dev\SuperWhisper_V6\tools"
        
    agent = AgentAnalyseurStructure(source_path)
    results = agent.analyze_tools_structure()
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
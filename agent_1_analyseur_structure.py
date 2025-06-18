#!/usr/bin/env python3
"""
Agent 1 - Analyseur de Structure (Claude Sonnet 4)
Mission: Analyser la structure des outils dans SuperWhisper_V6/tools

Responsabilités:
- Scanner tous les fichiers Python dans le répertoire source
- Analyser la structure AST de chaque fichier
- Identifier les types d'outils (automation, monitoring, conversion, etc.)
- Extraire les dépendances et métadonnées
- Classer les outils par utilité potentielle
"""

import os
import ast
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import importlib.util
import re

class AgentAnalyseurStructure:
    """Agent spécialisé dans l'analyse de structure de code Python avec Claude Sonnet 4"""
    
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
        """Analyse complète de la structure des outils"""
        self.logger.info(f"🔍 Démarrage analyse structure: {self.source_path}")
        
        if not self.source_path.exists():
            raise FileNotFoundError(f"Répertoire source introuvable: {self.source_path}")
            
        # Scanner tous les fichiers Python
        python_files = list(self.source_path.rglob("*.py"))
        self.analysis_results["total_files"] = len(python_files)
        
        self.logger.info(f"📁 {len(python_files)} fichiers Python trouvés")
        
        # Analyser chaque fichier
        for py_file in python_files:
            try:
                tool_info = self.analyze_single_file(py_file)
                if tool_info:
                    self.analysis_results["tools"].append(tool_info)
                    self.analysis_results["analyzable_files"] += 1
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur analyse {py_file.name}: {e}")
                
        # Catégoriser les outils
        self.categorize_tools()
        
        # Finaliser l'analyse
        self.analysis_results["dependencies"] = list(self.analysis_results["dependencies"])
        
        self.logger.info(f"✅ Analyse terminée: {self.analysis_results['analyzable_files']} outils analysés")
        return self.analysis_results
        
    def analyze_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyse détaillée d'un fichier Python unique"""
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
            
            # Analyse AST détaillée
            self.extract_ast_elements(tree, tool_info)
            
            # Classification du type d'outil
            tool_info["tool_type"] = self.classify_tool_type(tool_info, content)
            
            # Score de complexité
            tool_info["complexity_score"] = self.calculate_complexity_score(tool_info)
            
            # Indicateurs d'utilité
            tool_info["utility_indicators"] = self.extract_utility_indicators(tool_info, content)
            
            return tool_info
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse fichier {file_path}: {e}")
            return None
            
    def extract_ast_elements(self, tree: ast.AST, tool_info: Dict[str, Any]):
        """Extraction des éléments AST (fonctions, classes, imports)"""
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
        """Classification intelligente du type d'outil basée sur l'analyse du code"""
        
        # Mots-clés pour chaque catégorie
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
            
            # Score basé sur le nom de fichier (poids élevé)
            for keyword in keywords:
                if keyword in filename_lower:
                    score += 3
                    
            # Score basé sur la docstring (poids moyen)
            for keyword in keywords:
                if keyword in docstring_lower:
                    score += 2
                    
            # Score basé sur le contenu (poids faible)
            for keyword in keywords:
                score += content_lower.count(keyword) * 0.5
                
            # Score basé sur les imports
            for import_name in tool_info["imports"]:
                for keyword in keywords:
                    if keyword in import_name.lower():
                        score += 1
                        
            category_scores[category] = score
            
        # Retourner la catégorie avec le score le plus élevé
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
                
        return "utility"  # Catégorie par défaut
        
    def calculate_complexity_score(self, tool_info: Dict[str, Any]) -> int:
        """Calcul du score de complexité de l'outil"""
        score = 0
        
        # Complexité basée sur le nombre de fonctions
        score += len(tool_info["functions"]) * 2
        
        # Complexité basée sur le nombre de classes
        score += len(tool_info["classes"]) * 5
        
        # Complexité basée sur les imports
        score += len(tool_info["imports"])
        
        # Complexité basée sur la taille
        score += tool_info["lines_count"] // 10
        
        # Bonus pour les fonctions async
        async_functions = sum(1 for f in tool_info["functions"] if f["is_async"])
        score += async_functions * 3
        
        # Bonus pour les décorateurs
        decorated_functions = sum(1 for f in tool_info["functions"] if f["decorators"])
        score += decorated_functions * 2
        
        return score
        
    def extract_utility_indicators(self, tool_info: Dict[str, Any], content: str) -> List[str]:
        """Extraction des indicateurs d'utilité de l'outil"""
        indicators = []
        
        # Indicateurs basés sur la structure
        if len(tool_info["functions"]) > 5:
            indicators.append("multi_functional")
            
        if len(tool_info["classes"]) > 0:
            indicators.append("object_oriented")
            
        if any(f["is_async"] for f in tool_info["functions"]):
            indicators.append("async_capable")
            
        # Indicateurs basés sur les imports
        important_libs = ["requests", "asyncio", "pathlib", "json", "yaml", "sqlite3", "pandas"]
        for lib in important_libs:
            if any(lib in imp for imp in tool_info["imports"]):
                indicators.append(f"uses_{lib}")
                
        # Indicateurs basés sur le contenu
        if "if __name__ == '__main__':" in content:
            indicators.append("executable_script")
            
        if "argparse" in content or "click" in content:
            indicators.append("cli_interface")
            
        if "logging" in content:
            indicators.append("has_logging")
            
        if "config" in content.lower():
            indicators.append("configurable")
            
        # Indicateurs de qualité
        if tool_info["docstring"]:
            indicators.append("documented")
            
        if any(f["docstring"] for f in tool_info["functions"]):
            indicators.append("functions_documented")
            
        return indicators
        
    def categorize_tools(self):
        """Catégorisation finale des outils analysés"""
        categories = {}
        
        for tool in self.analysis_results["tools"]:
            tool_type = tool["tool_type"]
            if tool_type not in categories:
                categories[tool_type] = []
            categories[tool_type].append(tool["name"])
            
        self.analysis_results["categories"] = categories
        
        # Log des statistiques
        for category, tools in categories.items():
            self.logger.info(f"📊 {category}: {len(tools)} outils")

# Test de l'agent si exécuté directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        source_path = sys.argv[1]
    else:
        source_path = r"C:\Dev\SuperWhisper_V6\tools"
        
    agent = AgentAnalyseurStructure(source_path)
    results = agent.analyze_tools_structure()
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
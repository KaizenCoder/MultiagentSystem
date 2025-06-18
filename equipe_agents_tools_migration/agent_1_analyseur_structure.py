#!/usr/bin/env python3
"""
[SEARCH] Agent 1: Analyseur de Structure - Claude Sonnet 4
Mission: Analyser la structure complte des outils SuperWhisper_V6
Responsabilits:
- Scanner tous les rpertoires et fichiers
- Identifier les types d'outils
- Analyser les dpendances
- valuer la complexit
- Gnrer une cartographie dtaille
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import ast
import re

class Agent1AnalyseurStructure:
    """Agent spcialis dans l'analyse de structure des outils"""
    
    def __init__(self, source_path: Path, workspace_path: Path):
        self.source_path = source_path
        self.workspace_path = workspace_path
        self.agent_name = "Agent 1 - Analyseur Structure"
        self.model_name = "Claude Sonnet 4"
        self.start_time = None
        
        # Rsultats d'analyse
        self.structure_complete = {}
        self.outils_detectes = []
        self.dependances_globales = set()
        self.metriques = {}
        
    async def analyser_structure(self) -> Dict[str, Any]:
        """Analyser la structure complte du rpertoire source"""
        self.start_time = datetime.now()
        print(f"[SEARCH] {self.agent_name} - Dmarrage analyse structure")
        
        try:
            # 1. Scanner la structure des rpertoires
            await self._scanner_repertoires()
            
            # 2. Analyser les fichiers Python
            await self._analyser_fichiers_python()
            
            # 3. Dtecter les outils et scripts
            await self._detecter_outils()
            
            # 4. Analyser les dpendances
            await self._analyser_dependances()
            
            # 5. Calculer les mtriques
            await self._calculer_metriques()
            
            # 6. Gnrer le rapport d'analyse
            resultat = await self._generer_rapport()
            
            duree = (datetime.now() - self.start_time).total_seconds()
            print(f"[CHECK] {self.agent_name} - Termin en {duree:.2f}s")
            
            return resultat
            
        except Exception as e:
            print(f"[CROSS] {self.agent_name} - Erreur: {e}")
            raise
    
    async def _scanner_repertoires(self):
        """Scanner la structure des rpertoires"""
        print("[FOLDER] Scanning structure des rpertoires...")
        
        self.structure_complete = {
            "repertoires": {},
            "fichiers_par_type": {},
            "taille_totale": 0,
            "nombre_fichiers": 0
        }
        
        for root, dirs, files in os.walk(self.source_path):
            root_path = Path(root)
            relative_path = root_path.relative_to(self.source_path)
            
            # Analyser le rpertoire
            rep_info = {
                "path": str(relative_path),
                "nombre_fichiers": len(files),
                "sous_repertoires": dirs.copy(),
                "fichiers": []
            }
            
            # Analyser chaque fichier
            for file in files:
                file_path = root_path / file
                try:
                    stat = file_path.stat()
                    extension = file_path.suffix.lower()
                    
                    fichier_info = {
                        "nom": file,
                        "extension": extension,
                        "taille": stat.st_size,
                        "modifie": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    rep_info["fichiers"].append(fichier_info)
                    
                    # Compteurs globaux
                    self.structure_complete["taille_totale"] += stat.st_size
                    self.structure_complete["nombre_fichiers"] += 1
                    
                    # Compteur par type
                    if extension not in self.structure_complete["fichiers_par_type"]:
                        self.structure_complete["fichiers_par_type"][extension] = 0
                    self.structure_complete["fichiers_par_type"][extension] += 1
                    
                except (OSError, PermissionError):
                    continue
            
            self.structure_complete["repertoires"][str(relative_path)] = rep_info
    
    async def _analyser_fichiers_python(self):
        """Analyser spcifiquement les fichiers Python"""
        print(" Analyse des fichiers Python...")
        
        self.fichiers_python = []
        
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    try:
                        # Lire le contenu
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            contenu = f.read()
                        
                        # Analyser avec AST
                        try:
                            tree = ast.parse(contenu)
                            
                            # Extraire les informations
                            imports = self._extraire_imports(tree)
                            fonctions = self._extraire_fonctions(tree)
                            classes = self._extraire_classes(tree)
                            
                        except SyntaxError:
                            imports, fonctions, classes = [], [], []
                        
                        # Analyser le contenu textuel
                        lignes = contenu.split('\n')
                        
                        fichier_info = {
                            "path": str(file_path.relative_to(self.source_path)),
                            "nom": file,
                            "taille": len(contenu),
                            "lignes": len(lignes),
                            "imports": imports,
                            "fonctions": fonctions,
                            "classes": classes,
                            "docstring": self._extraire_docstring(tree),
                            "complexite": self._calculer_complexite(contenu),
                            "type_outil": self._detecter_type_outil(contenu, file)
                        }
                        
                        self.fichiers_python.append(fichier_info)
                        
                        # Ajouter aux dpendances globales
                        self.dependances_globales.update(imports)
                        
                    except (OSError, PermissionError, UnicodeDecodeError):
                        continue
    
    def _extraire_imports(self, tree) -> List[str]:
        """Extraire les imports d'un AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
    
    def _extraire_fonctions(self, tree) -> List[str]:
        """Extraire les noms de fonctions d'un AST"""
        fonctions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fonctions.append(node.name)
        
        return fonctions
    
    def _extraire_classes(self, tree) -> List[str]:
        """Extraire les noms de classes d'un AST"""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return classes
    
    def _extraire_docstring(self, tree) -> Optional[str]:
        """Extraire la docstring principale"""
        try:
            if (isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Constant) and
                isinstance(tree.body[0].value.value, str)):
                return tree.body[0].value.value
        except (IndexError, AttributeError):
            pass
        return None
    
    def _calculer_complexite(self, contenu: str) -> Dict[str, int]:
        """Calculer des mtriques de complexit simple"""
        lignes = contenu.split('\n')
        
        return {
            "lignes_totales": len(lignes),
            "lignes_code": len([l for l in lignes if l.strip() and not l.strip().startswith('#')]),
            "lignes_commentaires": len([l for l in lignes if l.strip().startswith('#')]),
            "lignes_vides": len([l for l in lignes if not l.strip()]),
            "indentation_max": max([len(l) - len(l.lstrip()) for l in lignes if l.strip()], default=0)
        }
    
    def _detecter_type_outil(self, contenu: str, nom_fichier: str) -> str:
        """Dtecter le type d'outil bas sur le contenu et le nom"""
        contenu_lower = contenu.lower()
        nom_lower = nom_fichier.lower()
        
        # Patterns de dtection
        if any(word in contenu_lower for word in ['fastapi', 'flask', 'django', 'app.run']):
            return 'web_api'
        elif any(word in contenu_lower for word in ['streamlit', 'gradio', 'dash']):
            return 'interface_web'
        elif any(word in contenu_lower for word in ['argparse', 'click', 'sys.argv']):
            return 'cli_tool'
        elif any(word in contenu_lower for word in ['pytest', 'unittest', 'test_']):
            return 'test_script'
        elif any(word in nom_lower for word in ['install', 'setup', 'config']):
            return 'installation'
        elif any(word in nom_lower for word in ['monitor', 'watch', 'check']):
            return 'monitoring'
        elif any(word in nom_lower for word in ['convert', 'transform', 'process']):
            return 'conversion'
        elif any(word in nom_lower for word in ['download', 'fetch', 'get']):
            return 'download'
        elif any(word in nom_lower for word in ['generate', 'create', 'make']):
            return 'generation'
        elif any(word in contenu_lower for word in ['automation', 'schedule', 'cron']):
            return 'automation'
        else:
            return 'utility'
    
    async def _detecter_outils(self):
        """Dtecter et cataloguer les outils disponibles"""
        print(" Dtection des outils...")
        
        self.outils_detectes = []
        
        # Analyser les fichiers Python comme outils potentiels
        for fichier in self.fichiers_python:
            if (fichier['lignes'] > 10 and  # Minimum de lignes
                len(fichier['fonctions']) > 0):  # Au moins une fonction
                
                outil = {
                    "nom": fichier['nom'],
                    "path": fichier['path'],
                    "type": fichier['type_outil'],
                    "description": fichier['docstring'] or f"Outil {fichier['type_outil']}",
                    "complexite": fichier['complexite']['lignes_code'],
                    "dependances": fichier['imports'],
                    "fonctions_principales": fichier['fonctions'][:5],  # Top 5
                    "score_utilite": self._calculer_score_utilite(fichier)
                }
                
                self.outils_detectes.append(outil)
        
        # Trier par score d'utilit
        self.outils_detectes.sort(key=lambda x: x['score_utilite'], reverse=True)
    
    def _calculer_score_utilite(self, fichier: Dict) -> int:
        """Calculer un score d'utilit pour un fichier"""
        score = 0
        
        # Points pour la taille (ni trop petit ni trop gros)
        lignes = fichier['complexite']['lignes_code']
        if 20 <= lignes <= 500:
            score += 10
        elif lignes > 500:
            score += 5
        
        # Points pour le type d'outil
        type_scores = {
            'cli_tool': 15,
            'utility': 10,
            'conversion': 12,
            'monitoring': 8,
            'automation': 12,
            'generation': 10,
            'download': 8,
            'web_api': 6,  # Moins prioritaire
            'interface_web': 4,  # Moins prioritaire
            'test_script': 3,
            'installation': 5
        }
        score += type_scores.get(fichier['type_outil'], 5)
        
        # Points pour les fonctions
        score += min(len(fichier['fonctions']) * 2, 20)
        
        # Points pour la documentation
        if fichier['docstring']:
            score += 5
        
        return score
    
    async def _analyser_dependances(self):
        """Analyser les dpendances globales"""
        print(" Analyse des dpendances...")
        
        # Sparer les dpendances standard vs externes
        dependances_standard = {
            'os', 'sys', 'json', 'time', 'datetime', 're', 'pathlib', 'subprocess',
            'asyncio', 'logging', 'argparse', 'collections', 'itertools', 'functools',
            'typing', 'dataclasses', 'enum', 'abc', 'contextlib', 'concurrent',
            'threading', 'multiprocessing', 'urllib', 'http', 'socket', 'ssl'
        }
        
        self.dependances_analyse = {
            "total": len(self.dependances_globales),
            "standard": [],
            "externes": [],
            "inconnues": []
        }
        
        for dep in self.dependances_globales:
            base_dep = dep.split('.')[0]  # Prendre le module racine
            
            if base_dep in dependances_standard:
                self.dependances_analyse["standard"].append(dep)
            elif self._est_dependance_connue(base_dep):
                self.dependances_analyse["externes"].append(dep)
            else:
                self.dependances_analyse["inconnues"].append(dep)
    
    def _est_dependance_connue(self, module: str) -> bool:
        """Vrifier si c'est une dpendance externe connue"""
        deps_connues = {
            'requests', 'numpy', 'pandas', 'matplotlib', 'seaborn', 'plotly',
            'fastapi', 'flask', 'django', 'streamlit', 'gradio',
            'openai', 'anthropic', 'google', 'azure',
            'sqlalchemy', 'psycopg2', 'pymongo', 'redis',
            'pytest', 'unittest', 'mock', 'tqdm', 'click', 'rich',
            'pydantic', 'dataclasses', 'attrs', 'marshmallow'
        }
        return module.lower() in deps_connues
    
    async def _calculer_metriques(self):
        """Calculer les mtriques globales"""
        print("[CHART] Calcul des mtriques...")
        
        self.metriques = {
            "structure": {
                "repertoires_total": len(self.structure_complete["repertoires"]),
                "fichiers_total": self.structure_complete["nombre_fichiers"],
                "taille_totale_mb": round(self.structure_complete["taille_totale"] / (1024*1024), 2),
                "types_fichiers": len(self.structure_complete["fichiers_par_type"])
            },
            "python": {
                "fichiers_python": len(self.fichiers_python),
                "lignes_code_total": sum(f['complexite']['lignes_code'] for f in self.fichiers_python),
                "fonctions_total": sum(len(f['fonctions']) for f in self.fichiers_python),
                "classes_total": sum(len(f['classes']) for f in self.fichiers_python)
            },
            "outils": {
                "outils_detectes": len(self.outils_detectes),
                "types_outils": len(set(o['type'] for o in self.outils_detectes)),
                "score_utilite_moyen": round(sum(o['score_utilite'] for o in self.outils_detectes) / len(self.outils_detectes), 2) if self.outils_detectes else 0
            },
            "dependances": self.dependances_analyse
        }
    
    async def _generer_rapport(self) -> Dict[str, Any]:
        """Gnrer le rapport final d'analyse"""
        duree = (datetime.now() - self.start_time).total_seconds()
        
        rapport = {
            "agent": self.agent_name,
            "model": self.model_name,
            "timestamp": self.start_time.isoformat(),
            "duree_secondes": duree,
            "source_path": str(self.source_path),
            "status": "SUCCESS",
            "structure_complete": self.structure_complete,
            "fichiers_python": self.fichiers_python,
            "outils_detectes": self.outils_detectes,
            "metriques": self.metriques,
            "tools_count": len(self.outils_detectes),
            "recommendations": [
                f"Trouv {len(self.outils_detectes)} outils potentiels",
                f"Types d'outils les plus frquents: {self._get_top_tool_types()}",
                f"Dpendances externes  vrifier: {len(self.dependances_analyse['externes'])}",
                "Prioriser les outils avec score_utilite > 15"
            ]
        }
        
        # Sauvegarder le rapport
        rapport_path = self.workspace_path / "reports" / f"agent_1_analyse_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {rapport_path}")
        return rapport
    
    def _get_top_tool_types(self) -> str:
        """Obtenir les types d'outils les plus frquents"""
        types_count = {}
        for outil in self.outils_detectes:
            type_outil = outil['type']
            types_count[type_outil] = types_count.get(type_outil, 0) + 1
        
        top_types = sorted(types_count.items(), key=lambda x: x[1], reverse=True)[:3]
        return ", ".join([f"{t}({c})" for t, c in top_types])

# Test autonome
if __name__ == "__main__":
    async def test():
        agent = Agent1AnalyseurStructure(
            source_path=Path("C:/Dev/SuperWhisper_V6/tools"),
            workspace_path=Path(__file__).parent
        )
        result = await agent.analyser_structure()
        print(f"[CHECK] Test termin: {result['tools_count']} outils dtects")
    
    asyncio.run(test()) 
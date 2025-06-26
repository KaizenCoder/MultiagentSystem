#!/usr/bin/env python3
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

🎖️ AGENT 10 - DOCUMENTALISTE EXPERT
📚 Documentation complète et parfaite (Sprint 1)

MISSION SPRINT 1:
- Documentation technique complète code expert Claude
- Guides utilisateur Agent Factory Pattern
- Documentation API endpoints (/health, /metrics)
- Standards documentation pour équipe
- Coordination avec Agent 13 (spécialiste documentation)

RESPONSABILITÉS:
- Documentation technique complète
- Guides utilisateur
- Runbook opérateur
- Documentation API
- Coordination avec spécialiste documentation

LIVRABLES:
- Documentation parfaite
- Guides complets
- API documentée
- Standards documentation

UTILISATION OBLIGATOIRE CODE EXPERT CLAUDE:
- enhanced_agent_templates.py : Validation JSON Schema, héritage, hooks
- optimized_template_manager.py : Cache LRU, hot-reload, métriques

Author: Agent Factory Team - Sprint 1
Version: 1.0.0 (Sprint 1)
Created: 2024-12-28
Updated: 2024-12-28
"""

import asyncio
import json
import sys
import os
import re
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional

# Pattern Factory imports
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    print("⚠️ Pattern Factory non disponible. Utilisation des classes de fallback.")
    PATTERN_FACTORY_AVAILABLE = False
    # Fallback classes si l'architecture centrale n'est pas disponible
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_id = f"fallback_{agent_type}"
            self.name = f"Fallback {agent_type}"
            self.logger = logging.getLogger(self.agent_id)
        async def startup(self): pass
        async def shutdown(self): pass

    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            # La classe de fallback utilise 'data' pour la compatibilité avec les tests
            self.data = kwargs.get('payload', {})
            self.payload = self.data

    class Result:
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error

# ===== CONFIGURATION LOGGING (Globale pour le script) =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# ===== STRUCTURES DE DONNÉES (Inchangées) =====

@dataclass
class DocumentationSection:
    """Section documentation structurée"""
    title: str
    content: str
    level: int
    type: str
    tags: List[str]
    author: str = "Agent110DocumentalisteExpert"
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_markdown(self) -> str:
        header = "#" * self.level
        return f"{header} {self.title}\n\n{self.content}\n\n"

@dataclass
class APIDocumentation:
    """Documentation API structurée"""
    endpoint: str
    method: str
    description: str
    parameters: Dict[str, Any]
    responses: Dict[str, Any]
    examples: Dict[str, str]

# ===== GÉNÉRATEURS DE DOCUMENTATION (Inchangés) =====

class CodeDocumentationGenerator:
    """Générateur documentation à partir du code source."""
    def __init__(self, source_path: Path, logger: logging.Logger):
        self.source_path = source_path
        self.logger = logger
        
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyse un seul fichier de code."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            classes = re.findall(r'class\s+(\w+).*?:', content)
            functions = re.findall(r'def\s+(\w+)\(.*?\):', content)
            return {"file": file_path.name, "classes": classes, "functions": functions, "lines": len(content.splitlines())}
        except Exception as e:
            self.logger.error(f"Erreur d'analyse sur {file_path}: {e}")
            return {}
    
    def generate(self) -> str:
        """Génère la documentation complète pour le répertoire source."""
        doc = f"# 🔧 Documentation Technique : {self.source_path.name}\n\n"
        if not self.source_path.is_dir():
            raise FileNotFoundError(f"Le répertoire source n'existe pas : {self.source_path}")
        
        for py_file in sorted(self.source_path.rglob("*.py")):
            analysis = self._analyze_file(py_file)
            if not analysis:
                continue
            
            relative_path = py_file.relative_to(self.source_path)
            doc += f"## 📄 Fichier : `{relative_path}`\n"
            doc += f"- **Lignes de code:** {analysis.get('lines', 0)}\n"
            if analysis.get('classes'):
                doc += f"- **Classes:** {', '.join(analysis.get('classes', []))}\n"
            doc += "\n"
        return doc

class UserGuideGenerator:
    """Générateur de guides utilisateur."""
    def generate_quick_start(self) -> str:
        return """# 🚀 Guide de Démarrage Rapide
## Introduction
Ce guide vous aide à démarrer avec le système.
## Installation
1. Clonez le dépôt.
2. Installez les dépendances : `pip install -r requirements.txt`.
3. Lancez l'application.
"""

# ===== AGENT PRINCIPAL (Nouvelle Implémentation) =====

class Agent110DocumentalisteExpert(Agent):
    """
    🎖️ AGENT 110 - DOCUMENTALISTE EXPERT
    Orchestre les générateurs pour produire une documentation de haute qualité.
    """
    def __init__(self, **config):
        # Pré-initialisation pour satisfaire les dépendances de la classe de base
        self.agent_type = "agent_110_documentaliste_expert"
        self.agent_id = config.get("agent_id", f"{self.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.name = "Agent 110 Documentaliste Expert"
        self.logger = logging.getLogger(self.agent_id)

        # L'appel à super() se fait APRÈS la création des attributs dont il dépend.
        super().__init__(self.agent_type, **config)
        self.logger.info(f"Agent {self.name} initialisé.")

        # Créer le répertoire des rapports pour cet agent s'il n'existe pas
        self.reports_path = Path(config.get("reports_dir", "reports")) / self.agent_id
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Répertoire des rapports configuré : {self.reports_path}")
        
    async def startup(self):
        self.logger.info(f"🚀 Agent {self.agent_id} démarré.")
        await super().startup()

    async def shutdown(self):
        self.logger.info(f"🛑 Agent {self.agent_id} arrêté.")
        await super().shutdown()

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": "2.0.0",
            "description": "Génère de la documentation technique et des guides utilisateur.",
            "tasks": [
                {"name": "generer_doc_code", "description": "Génère la documentation technique pour un répertoire source.", "parameters": {"path": "str"}},
                {"name": "generer_guide_demarrage", "description": "Génère un guide de démarrage rapide standard."},
            ]
        }

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"Exécution de la tâche : {task.task_id}")
        task_params = task.data if hasattr(task, 'data') else (task.payload if hasattr(task, 'payload') else {})
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file_path = None

            if task.task_id == "generer_doc_code" or task.description == "generer_doc_code":
                source_path_str = task_params.get("path")
                if not source_path_str:
                    return Result(success=False, error="Le chemin ('path') du code source est manquant.")
                
                source_name = Path(source_path_str).name
                generator = CodeDocumentationGenerator(Path(source_path_str), self.logger)
                doc_content = generator.generate()
                
                report_filename = f"rapport_doc_code_{source_name}_{timestamp}.md"
                report_file_path = self.reports_path / report_filename
                
                with open(report_file_path, "w", encoding="utf-8") as f:
                    f.write(doc_content)
                self.logger.info(f"Rapport de documentation du code sauvegardé : {report_file_path}")
                return Result(success=True, data={"format": "markdown", "content_file_path": str(report_file_path), "message": f"Documentation du code générée et sauvegardée dans {report_file_path}"})
                    
            elif task.task_id == "generer_guide_demarrage" or task.description == "generer_guide_demarrage":
                generator = UserGuideGenerator()
                guide_content = generator.generate_quick_start()

                report_filename = f"rapport_guide_demarrage_{timestamp}.md"
                report_file_path = self.reports_path / report_filename

                with open(report_file_path, "w", encoding="utf-8") as f:
                    f.write(guide_content)
                self.logger.info(f"Rapport du guide de démarrage sauvegardé : {report_file_path}")
                return Result(success=True, data={"format": "markdown", "content_file_path": str(report_file_path), "message": f"Guide de démarrage généré et sauvegardé dans {report_file_path}"})
            
            else:
                return Result(success=False, error=f"Tâche inconnue: {task.task_id}")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche '{task.task_id}': {e}", exc_info=True)
            return Result(success=False, error=str(e))

# ===== POINT D'ENTRÉE POUR TEST =====

async def main():
    """Point d'entrée pour tester l'agent 110."""
    print("--- DÉMARRAGE DU TEST DE L'AGENT 110 ---")
    agent = None
    # Définir un répertoire de rapports spécifique pour les tests
    test_reports_dir = Path("reports_test_agent110") 
    try:
        # Instanciation directe de l'agent avec le répertoire de test
        agent = Agent110DocumentalisteExpert(reports_dir=str(test_reports_dir))
        await agent.startup()

        print("\n🔬 Test 1: Génération du guide de démarrage...")
        task1 = Task(task_id="generer_guide_demarrage", description="generer_guide_demarrage")
        result1 = await agent.execute_task(task1)
        if result1.success:
            print(f"[✅ SUCCÈS] Guide généré. Chemin: {result1.data.get('content_file_path')}")
        else:
            print(f"[❌ ERREUR] {result1.error}")

        print("\n🔬 Test 2: Génération de la documentation pour le répertoire './core'...")
        task2 = Task(task_id="generer_doc_code", description="generer_doc_code", payload={"path": "./core"})
        result2 = await agent.execute_task(task2)
        if result2.success:
            print(f"[✅ SUCCÈS] Documentation du code générée. Chemin: {result2.data.get('content_file_path')}")
        else:
            print(f"[❌ ERREUR] {result2.error}")

    except Exception as e:
        print(f"[❌ ERREUR] Une exception non gérée s'est produite: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if agent:
            await agent.shutdown()
        # Optionnel: Nettoyer le répertoire de rapports de test si nécessaire
        # import shutil
        # if test_reports_dir.exists():
        # shutil.rmtree(test_reports_dir)
        # print(f"Répertoire de test {test_reports_dir} supprimé.")
        print("\n--- FIN DU TEST DE L'AGENT 110 ---")

if __name__ == "__main__":
    asyncio.run(main())
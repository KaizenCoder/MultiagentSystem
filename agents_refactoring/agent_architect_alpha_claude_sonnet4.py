#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[CONSTRUCTION] AGENT ARCHITECT ALPHA - CLAUDE SONNET 4
Phase 2: Architecture Modulaire avec Principes SRP

Mission: Concevoir architecture modulaire pour les 4 fichiers god mode
- main.py (1,990 lignes  ~100 lignes)
- advanced_coordination.py (779 lignes  ~150 lignes) 
- redis_cluster_manager.py (738 lignes  ~150 lignes)
- monitoring.py (709 lignes  ~150 lignes)

Spcialisation: Architecture Enterprise avec Patterns Avancs
"""

import os
import json
import datetime
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import anthropic
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ArchitecturalPlan:
    """Plan architectural pour un fichier"""
    file_path: str
    current_lines: int
    target_lines: int
    modules_to_extract: List[Dict[str, Any]]
    dependencies: List[str]
    patterns_applied: List[str]
    migration_strategy: str
    risk_level: str
    estimated_effort_hours: int

@dataclass
class ModuleExtraction:
    """Extraction d'un module spcifique"""
    name: str
    new_path: str
    responsibilities: List[str]
    interfaces: List[Dict[str, Any]]
    dependencies: List[str]
    tests_required: bool
    priority: int

class AgentArchitectAlphaClaude:
    """
    [CONSTRUCTION] Agent Architect Alpha - Claude Sonnet 4
    
    Expertise:
    - Single Responsibility Principle (SRP)
    - Dependency Injection Patterns
    - Clean Architecture Layers
    - Interface Segregation
    - Factory & Builder Patterns
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-3-5-sonnet-20241022"
        self.workspace_path = Path(__file__).parent.parent
        self.results_path = self.workspace_path / "refactoring_workspace" / "results" / "alpha_claude"
        self.results_path.mkdir(parents=True, exist_ok=True)
        
        # Configuration architecture
        self.architectural_principles = [
            "Single Responsibility Principle",
            "Dependency Inversion Principle", 
            "Interface Segregation Principle",
            "Composition over Inheritance",
            "Fail Fast Design",
            "Immutable Data Structures",
            "Pure Functions Pattern",
            "Factory Pattern",
            "Repository Pattern",
            "Service Layer Pattern"
        ]
        
        self.patterns_library = {
            "routes": "FastAPI Router Pattern avec Dependency Injection",
            "services": "Service Layer avec Business Logic pure",
            "repositories": "Repository Pattern pour accs donnes",
            "models": "Domain Models avec Pydantic",
            "middleware": "Middleware Chain Pattern",
            "config": "Configuration Factory Pattern",
            "errors": "Exception Hierarchy centralise",
            "events": "Event-Driven Architecture",
            "cache": "Cache Abstraction Layer",
            "monitoring": "Observability Pattern"
        }

    async def analyze_god_mode_file(self, file_path: str) -> ArchitecturalPlan:
        """
        [SEARCH] Analyser un fichier god mode et crer plan architectural
        """
        try:
            # Lire le fichier
            full_path = self.workspace_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Prparer prompt Claude
            prompt = self._create_architecture_prompt(file_path, content)
            
            # Analyser avec Claude
            response = await self._call_claude_async(prompt)
            
            # Parser rponse et crer plan
            plan = self._parse_architectural_response(file_path, response)
            
            # Sauvegarder plan
            await self._save_architectural_plan(plan)
            
            return plan
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse {file_path}: {e}")
            return None

    def _create_architecture_prompt(self, file_path: str, content: str) -> str:
        """
        [TARGET] Crer prompt architectural spcialis
        """
        lines_count = len(content.split('\n'))
        
        prompt = f"""
Tu es un ARCHITECTE LOGICIEL EXPERT specialis dans le refactoring enterprise.

MISSION: Crer plan architectural modulaire pour {file_path} ({lines_count} lignes)

OBJECTIFS:
- Rduire drastiquement taille fichier (objectif: ~100-150 lignes max)
- Appliquer Single Responsibility Principle (SRP)
- Extraire modules spcialiss avec interfaces claires
- Maintenir compatibilit backward totale

ANALYSE REQUISE:
1. RESPONSABILITS identifies dans le code
2. MODULES  extraire avec leurs interfaces
3. PATTERNS architecturaux recommands
4. STRATGIE de migration tape par tape
5. DPENDANCES et ordre d'extraction
6. TESTS ncessaires pour chaque module

PATTERNS DISPONIBLES:
{json.dumps(self.patterns_library, indent=2)}

PRINCIPES  RESPECTER:
{chr(10).join(f"- {p}" for p in self.architectural_principles)}

CONTRAINTES:
- Migration Blue-Green (zro downtime)
- Tests de rgression automatiss
- Backward compatibility absolue
- Performance maintenue/amliore

CODE  ANALYSER:
```python
{content[:10000]}  # Premier tronon pour analyse
```

RPONSE ATTENDUE (JSON):
{{
  "responsabilits_identifies": ["resp1", "resp2", ...],
  "modules_extraction": [
    {{
      "nom": "nom_module",
      "nouveau_chemin": "path/to/module.py",
      "responsabilits": ["resp1"],
      "interfaces": [{{"name": "interface", "methods": ["method1"]}}],
      "dpendances": ["module1"],
      "priorit": 1
    }}
  ],
  "patterns_recommands": ["pattern1", "pattern2"],
  "stratgie_migration": "description tapes",
  "niveau_risque": "FAIBLE|MOYEN|LEV",
  "effort_estim_heures": 8
}}
"""
        return prompt

    async def _call_claude_async(self, prompt: str) -> str:
        """
        [ROBOT] Appel asynchrone  Claude Sonnet 4
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        except Exception as e:
            print(f"[CROSS] Erreur appel Claude: {e}")
            return ""

    def _parse_architectural_response(self, file_path: str, response: str) -> ArchitecturalPlan:
        """
         Parser rponse Claude en plan architectural
        """
        try:
            # Extraire JSON de la rponse
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_content = response[json_start:json_end]
                data = json.loads(json_content)
                
                # Crer objets ModuleExtraction
                modules = []
                for module_data in data.get('modules_extraction', []):
                    module = ModuleExtraction(
                        name=module_data.get('nom', ''),
                        new_path=module_data.get('nouveau_chemin', ''),
                        responsibilities=module_data.get('responsabilits', []),
                        interfaces=module_data.get('interfaces', []),
                        dependencies=module_data.get('dpendances', []),
                        tests_required=True,
                        priority=module_data.get('priorit', 5)
                    )
                    modules.append(module)
                
                # Estimer lignes actuelles
                full_path = self.workspace_path / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    current_lines = len(f.readlines())
                
                # Calculer lignes cibles
                target_lines = 100 if 'main.py' in file_path else 150
                
                return ArchitecturalPlan(
                    file_path=file_path,
                    current_lines=current_lines,
                    target_lines=target_lines,
                    modules_to_extract=[asdict(m) for m in modules],
                    dependencies=data.get('dpendances', []),
                    patterns_applied=data.get('patterns_recommands', []),
                    migration_strategy=data.get('stratgie_migration', ''),
                    risk_level=data.get('niveau_risque', 'MOYEN'),
                    estimated_effort_hours=data.get('effort_estim_heures', 8)
                )
                
        except Exception as e:
            print(f"[CROSS] Erreur parsing rponse: {e}")
            
        # Fallback plan basique
        return ArchitecturalPlan(
            file_path=file_path,
            current_lines=1000,
            target_lines=150,
            modules_to_extract=[],
            dependencies=[],
            patterns_applied=[],
            migration_strategy="Analyse manuelle requise",
            risk_level="LEV",
            estimated_effort_hours=16
        )

    async def _save_architectural_plan(self, plan: ArchitecturalPlan):
        """
         Sauvegarder plan architectural
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = Path(plan.file_path).stem
        
        # JSON dtaill
        json_path = self.results_path / f"architectural_plan_{file_name}_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(plan), f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown
        md_path = self.results_path / f"architectural_plan_{file_name}_{timestamp}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_architectural_report(plan))
        
        print(f"[CHECK] Plan architectural sauvegard: {json_path}")

    def _generate_architectural_report(self, plan: ArchitecturalPlan) -> str:
        """
        [CLIPBOARD] Gnrer rapport architectural Markdown
        """
        return f"""# [CONSTRUCTION] Plan Architectural - {Path(plan.file_path).name}

## [CHART] Vue d'Ensemble

**Fichier:** `{plan.file_path}`  
**Lignes actuelles:** {plan.current_lines}  
**Objectif lignes:** {plan.target_lines}  
**Rduction:** {((plan.current_lines - plan.target_lines) / plan.current_lines * 100):.1f}%  
**Effort estim:** {plan.estimated_effort_hours}h  
**Niveau risque:** {plan.risk_level}

## [TARGET] Modules  Extraire

{self._format_modules_extraction(plan.modules_to_extract)}

##  Patterns Architecturaux

{chr(10).join(f"- {pattern}" for pattern in plan.patterns_applied)}

## [ROCKET] Stratgie de Migration

{plan.migration_strategy}

## [CLIPBOARD] Dpendances

{chr(10).join(f"- {dep}" for dep in plan.dependencies)}

---
*Gnr par Agent Architect Alpha (Claude Sonnet 4)*
"""

    def _format_modules_extraction(self, modules: List[Dict[str, Any]]) -> str:
        """
         Formater modules pour rapport
        """
        if not modules:
            return "Aucun module identifi"
        
        result = []
        for i, module in enumerate(modules, 1):
            result.append(f"""
### {i}. {module.get('name', 'Module')}

**Chemin:** `{module.get('new_path', '')}`  
**Priorit:** {module.get('priority', 5)}  
**Responsabilits:**
{chr(10).join(f"- {resp}" for resp in module.get('responsibilities', []))}

**Interfaces:**
{chr(10).join(f"- {iface.get('name', '')}" for iface in module.get('interfaces', []))}
""")
        
        return "\n".join(result)

    async def create_complete_architecture(self) -> Dict[str, ArchitecturalPlan]:
        """
        [CONSTRUCTION] Crer architecture complte pour tous les fichiers god mode
        """
        god_mode_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py", 
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py"
        ]
        
        print("[CONSTRUCTION] Dmarrage analyse architecturale complte...")
        plans = {}
        
        for file_path in god_mode_files:
            print(f"[SEARCH] Analyse {file_path}...")
            plan = await self.analyze_god_mode_file(file_path)
            if plan:
                plans[file_path] = plan
                print(f"[CHECK] Plan cr pour {file_path}")
            else:
                print(f"[CROSS] chec analyse {file_path}")
        
        # Gnrer rapport global
        await self._generate_global_report(plans)
        
        return plans

    async def _generate_global_report(self, plans: Dict[str, ArchitecturalPlan]):
        """
        [CHART] Gnrer rapport architectural global
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        total_current = sum(plan.current_lines for plan in plans.values())
        total_target = sum(plan.target_lines for plan in plans.values())
        total_effort = sum(plan.estimated_effort_hours for plan in plans.values())
        
        report = f"""# [CONSTRUCTION] Architecture Plan Global - Phase 2

## [CHART] Rsum Excutif

**Date:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Fichiers analyss:** {len(plans)}  
**Lignes actuelles:** {total_current:,}  
**Lignes cibles:** {total_target:,}  
**Rduction totale:** {((total_current - total_target) / total_current * 100):.1f}%  
**Effort total estim:** {total_effort}h

## [FOLDER] Dtails par Fichier

{self._format_global_summary(plans)}

## [TARGET] Prochaines tapes

1. [CHECK] Plans architecturaux crs
2.  Crer Agent Route Extractor
3.  Crer Agent Services Creator
4.  Dmarrer extraction main.py (priorit)

---
*Gnr par Agent Architect Alpha (Claude Sonnet 4)*
"""
        
        report_path = self.results_path / f"global_architecture_plan_{timestamp}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[CHART] Rapport global sauvegard: {report_path}")

    def _format_global_summary(self, plans: Dict[str, ArchitecturalPlan]) -> str:
        """
        [CLIPBOARD] Formater rsum global
        """
        result = []
        for file_path, plan in plans.items():
            reduction = ((plan.current_lines - plan.target_lines) / plan.current_lines * 100)
            result.append(f"""
### {Path(file_path).name}

**Lignes:** {plan.current_lines:,}  {plan.target_lines:,} (-{reduction:.1f}%)  
**Effort:** {plan.estimated_effort_hours}h  
**Risque:** {plan.risk_level}  
**Modules:** {len(plan.modules_to_extract)}
""")
        
        return "\n".join(result)

# [TARGET] EXECUTION PRINCIPALE
async def main():
    """
    [ROCKET] Point d'entre principal Agent Architect Alpha
    """
    print("[CONSTRUCTION] AGENT ARCHITECT ALPHA - CLAUDE SONNET 4")
    print("=" * 50)
    
    agent = AgentArchitectAlphaClaude()
    
    try:
        # Crer architecture complte
        plans = await agent.create_complete_architecture()
        
        print(f"\n[CHECK] SUCCS: {len(plans)} plans architecturaux crs!")
        print("[TARGET] Prt pour Phase 2 - Implmentation")
        
        return plans
        
    except Exception as e:
        print(f"[CROSS] ERREUR: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # Vrification environnement
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("[CROSS] ANTHROPIC_API_KEY manquante dans .env")
        sys.exit(1)
    
    # Excution asynchrone
    result = asyncio.run(main())
    
    if result:
        print(" Agent Architect Alpha termin avec succs!")
    else:
        print(" chec Agent Architect Alpha")
        sys.exit(1) 




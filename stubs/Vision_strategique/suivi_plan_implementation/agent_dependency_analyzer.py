#!/usr/bin/env python3
"""
Agent Dependency Analyzer - Phase 0 Semaine 1
Outil d'analyse du graphe de dépendances des agents NextGeneration

Objectifs:
- Cartographier les dépendances entre les 65+ agents
- Identifier agents "feuilles" (0 dépendances) vs "piliers" (nombreuses dépendances)
- Générer l'ordre de migration optimal
- Sélectionner 4 agents pilotes pour Phase 1
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class AgentInfo:
    """Information sur un agent"""
    name: str
    file_path: str
    lines_of_code: int
    imports: List[str]
    agent_calls: List[str]
    dependencies: Set[str]
    dependents: Set[str]
    complexity_score: float
    category: str
    
class AgentDependencyAnalyzer:
    """Analyseur de dépendances pour les agents NextGeneration"""
    
    def __init__(self, agents_dir: str = "/mnt/c/Dev/nextgeneration/agents"):
        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, AgentInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Patterns pour détecter les dépendances
        self.agent_import_patterns = [
            r'from\s+agent_(\w+)\s+import',
            r'import\s+agent_(\w+)',
            r'from\s+\.agent_(\w+)\s+import',
        ]
        
        self.agent_call_patterns = [
            r'agent_(\w+)\.(\w+)',
            r'Agent(\w+)\(',
            r'run_agent_(\w+)',
            r'execute_agent_(\w+)',
        ]
    
    def scan_agents(self) -> Dict[str, AgentInfo]:
        """Scan tous les agents et analyse leurs dépendances"""
        
        print(f"🔍 Scanning agents in {self.agents_dir}")
        
        # Trouver tous les fichiers agent_*.py (hors backups)
        agent_files = []
        for file_path in self.agents_dir.glob("agent_*.py"):
            if "backup" not in str(file_path) and file_path.name != "__init__.py":
                agent_files.append(file_path)
        
        print(f"📊 Found {len(agent_files)} agent files to analyze")
        
        # Analyser chaque agent
        for file_path in agent_files:
            try:
                agent_info = self._analyze_agent_file(file_path)
                if agent_info:
                    self.agents[agent_info.name] = agent_info
                    print(f"✅ Analyzed: {agent_info.name} ({agent_info.lines_of_code} LOC)")
            except Exception as e:
                print(f"❌ Error analyzing {file_path}: {e}")
        
        # Construire le graphe de dépendances
        self._build_dependency_graph()
        
        print(f"🎯 Analysis complete: {len(self.agents)} agents analyzed")
        return self.agents
    
    def _analyze_agent_file(self, file_path: Path) -> AgentInfo:
        """Analyse un fichier agent individuel"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Could not read {file_path}: {e}")
            return None
            
        # Informations de base
        agent_name = file_path.stem
        lines = content.split('\n')
        lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        # Analyser les imports
        imports = self._extract_imports(content)
        
        # Analyser les appels d'agents
        agent_calls = self._extract_agent_calls(content)
        
        # Catégoriser l'agent
        category = self._categorize_agent(agent_name, content)
        
        # Calculer score de complexité
        complexity_score = self._calculate_complexity_score(content, lines_of_code)
        
        return AgentInfo(
            name=agent_name,
            file_path=str(file_path),
            lines_of_code=lines_of_code,
            imports=imports,
            agent_calls=agent_calls,
            dependencies=set(),  # Sera rempli par _build_dependency_graph
            dependents=set(),    # Sera rempli par _build_dependency_graph
            complexity_score=complexity_score,
            category=category
        )
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extrait les imports d'autres agents"""
        imports = []
        
        for pattern in self.agent_import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    imports.extend(match)
                else:
                    imports.append(match)
        
        return list(set(imports))  # Supprimer doublons
    
    def _extract_agent_calls(self, content: str) -> List[str]:
        """Extrait les appels directs à d'autres agents"""
        calls = []
        
        for pattern in self.agent_call_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    calls.append(match[0])  # Prendre le premier groupe
                else:
                    calls.append(match)
        
        return list(set(calls))  # Supprimer doublons
    
    def _categorize_agent(self, agent_name: str, content: str) -> str:
        """Catégorise l'agent selon son rôle"""
        
        name_lower = agent_name.lower()
        content_lower = content.lower()
        
        # Catégories basées sur les noms et contenu
        if "maintenance" in name_lower:
            return "MAINTENANCE"
        elif "postgresql" in name_lower or "postgres" in name_lower:
            return "POSTGRESQL"
        elif "audit" in name_lower or "qualite" in name_lower:
            return "AUDIT"
        elif "security" in name_lower or "securite" in name_lower:
            return "SECURITY"
        elif "test" in name_lower or "validation" in name_lower:
            return "TESTING"
        elif "monitor" in name_lower or "performance" in name_lower:
            return "MONITORING"
        elif "architecture" in name_lower or "enterprise" in name_lower:
            return "ARCHITECTURE"
        elif "coordinateur" in name_lower or "orchestr" in name_lower:
            return "COORDINATION"
        elif "documentation" in name_lower or "documenteur" in name_lower:
            return "DOCUMENTATION"
        else:
            return "GENERAL"
    
    def _calculate_complexity_score(self, content: str, loc: int) -> float:
        """Calcule un score de complexité pour l'agent"""
        
        score = 0.0
        
        # Facteur 1: Lignes de code (normalisé)
        score += min(loc / 1000, 1.0) * 0.3
        
        # Facteur 2: Nombre de classes
        class_count = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
        score += min(class_count / 5, 1.0) * 0.2
        
        # Facteur 3: Nombre de fonctions
        func_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
        score += min(func_count / 20, 1.0) * 0.2
        
        # Facteur 4: Imports externes
        import_count = len(re.findall(r'^import\s+|^from\s+\w+\s+import', content, re.MULTILINE))
        score += min(import_count / 30, 1.0) * 0.15
        
        # Facteur 5: Mots-clés de complexité
        complexity_keywords = ['async', 'await', 'thread', 'process', 'queue', 'lock', 'sqlalchemy', 'chromadb']
        keyword_count = sum(content.lower().count(keyword) for keyword in complexity_keywords)
        score += min(keyword_count / 10, 1.0) * 0.15
        
        return round(score, 3)
    
    def _build_dependency_graph(self):
        """Construit le graphe de dépendances entre agents"""
        
        print("🔗 Building dependency graph...")
        
        for agent_name, agent_info in self.agents.items():
            # Analyser les imports et calls pour identifier les dépendances
            all_references = agent_info.imports + agent_info.agent_calls
            
            for ref in all_references:
                # Chercher les agents correspondants
                possible_dependencies = [
                    name for name in self.agents.keys() 
                    if ref in name or name.replace('agent_', '').replace('_', '') in ref
                ]
                
                for dep in possible_dependencies:
                    if dep != agent_name:  # Éviter auto-référence
                        agent_info.dependencies.add(dep)
                        self.dependency_graph[agent_name].add(dep)
                        self.reverse_dependency_graph[dep].add(agent_name)
                        self.agents[dep].dependents.add(agent_name)
        
        print(f"📊 Dependency graph built: {sum(len(deps) for deps in self.dependency_graph.values())} total dependencies")
    
    def get_migration_waves(self) -> List[List[str]]:
        """Génère les vagues de migration optimales"""
        
        print("🌊 Calculating migration waves...")
        
        waves = []
        remaining_agents = set(self.agents.keys())
        
        while remaining_agents:
            # Trouver les agents sans dépendances non migrées
            current_wave = []
            
            for agent in remaining_agents.copy():
                dependencies = self.dependency_graph.get(agent, set())
                # Vérifier si toutes les dépendances ont été migrées
                unmigrated_deps = dependencies & remaining_agents
                
                if not unmigrated_deps:  # Aucune dépendance non migrée
                    current_wave.append(agent)
                    remaining_agents.remove(agent)
            
            if current_wave:
                # Trier par complexité croissante dans chaque vague
                current_wave.sort(key=lambda x: self.agents[x].complexity_score)
                waves.append(current_wave)
                print(f"Wave {len(waves)}: {len(current_wave)} agents")
            else:
                # Circular dependency detected - force migration of lowest complexity
                if remaining_agents:
                    forced_agent = min(remaining_agents, key=lambda x: self.agents[x].complexity_score)
                    waves.append([forced_agent])
                    remaining_agents.remove(forced_agent)
                    print(f"⚠️  Forced migration (circular dep): {forced_agent}")
        
        return waves
    
    def select_pilot_agents(self, count: int = 4) -> List[str]:
        """Sélectionne les agents pilotes optimaux"""
        
        print(f"🎯 Selecting {count} pilot agents...")
        
        # Critères de sélection des pilotes:
        # 1. Agents feuilles (0 dépendances) en priorité
        # 2. Complexité faible à moyenne
        # 3. Représentatifs de différentes catégories
        # 4. Nombre de lignes raisonnable (pas trop petits, pas trop gros)
        
        candidates = []
        
        for agent_name, agent_info in self.agents.items():
            dep_count = len(agent_info.dependencies)
            
            # Score de priorité pour pilote
            pilot_score = 0.0
            
            # Bonus si agent feuille
            if dep_count == 0:
                pilot_score += 100
            elif dep_count <= 2:
                pilot_score += 50
            
            # Bonus pour complexité modérée
            if 0.2 <= agent_info.complexity_score <= 0.6:
                pilot_score += 30
            elif agent_info.complexity_score < 0.2:
                pilot_score += 10  # Trop simple
            
            # Bonus pour taille raisonnable
            if 200 <= agent_info.lines_of_code <= 800:
                pilot_score += 20
            elif 100 <= agent_info.lines_of_code <= 1200:
                pilot_score += 10
            
            # Bonus pour catégories importantes
            priority_categories = ["TESTING", "AUDIT", "POSTGRESQL", "MAINTENANCE"]
            if agent_info.category in priority_categories:
                pilot_score += 15
            
            candidates.append((agent_name, pilot_score, agent_info))
        
        # Trier par score décroissant
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Sélectionner en évitant la duplication de catégories
        selected = []
        used_categories = set()
        
        for agent_name, score, agent_info in candidates:
            if len(selected) >= count:
                break
                
            # Préférer la diversité des catégories
            if agent_info.category not in used_categories or len(selected) < count // 2:
                selected.append(agent_name)
                used_categories.add(agent_info.category)
                print(f"✅ Pilot {len(selected)}: {agent_name} (score: {score:.1f}, category: {agent_info.category})")
        
        return selected
    
    def generate_analysis_report(self) -> Dict:
        """Génère un rapport d'analyse complet"""
        
        waves = self.get_migration_waves()
        pilots = self.select_pilot_agents()
        
        # Statistiques générales
        total_agents = len(self.agents)
        total_dependencies = sum(len(deps) for deps in self.dependency_graph.values())
        
        # Agents par catégorie
        categories = defaultdict(list)
        for agent_name, agent_info in self.agents.items():
            categories[agent_info.category].append(agent_name)
        
        # Agents feuilles vs piliers
        leaf_agents = [name for name, info in self.agents.items() if len(info.dependencies) == 0]
        pillar_agents = [name for name, info in self.agents.items() if len(info.dependents) >= 3]
        
        # Complexité moyenne par catégorie
        complexity_by_category = {}
        for category, agent_names in categories.items():
            avg_complexity = sum(self.agents[name].complexity_score for name in agent_names) / len(agent_names)
            complexity_by_category[category] = round(avg_complexity, 3)
        
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_agents": total_agents,
                "total_dependencies": total_dependencies,
                "migration_waves": len(waves),
                "leaf_agents_count": len(leaf_agents),
                "pillar_agents_count": len(pillar_agents)
            },
            "categories": dict(categories),
            "complexity_by_category": complexity_by_category,
            "migration_waves": waves,
            "pilot_agents": pilots,
            "leaf_agents": leaf_agents,
            "pillar_agents": pillar_agents,
            "agents_detail": {
                name: {
                    "lines_of_code": info.lines_of_code,
                    "complexity_score": info.complexity_score,
                    "category": info.category,
                    "dependencies_count": len(info.dependencies),
                    "dependents_count": len(info.dependents),
                    "dependencies": list(info.dependencies),
                    "dependents": list(info.dependents)
                }
                for name, info in self.agents.items()
            }
        }
        
        return report
    
    def save_analysis(self, output_file: str = None):
        """Sauvegarde l'analyse complète"""
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"/mnt/c/Dev/nextgeneration/stubs/Vision_strategique/suivi_plan_implementation/agent_dependency_analysis_{timestamp}.json"
        
        report = self.generate_analysis_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analysis saved to: {output_file}")
        return output_file

def main():
    """Fonction principale d'analyse"""
    
    print("🚀 Agent Dependency Analyzer - Phase 0 Week 1")
    print("=" * 60)
    
    analyzer = AgentDependencyAnalyzer()
    
    # Scanner tous les agents
    agents = analyzer.scan_agents()
    
    # Générer et sauvegarder l'analyse
    output_file = analyzer.save_analysis()
    
    # Afficher un résumé
    report = analyzer.generate_analysis_report()
    
    print("\n📊 SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Agents Analyzed: {report['summary']['total_agents']}")
    print(f"Total Dependencies: {report['summary']['total_dependencies']}")
    print(f"Migration Waves: {report['summary']['migration_waves']}")
    print(f"Leaf Agents: {report['summary']['leaf_agents_count']}")
    print(f"Pillar Agents: {report['summary']['pillar_agents_count']}")
    
    print(f"\n🎯 PILOT AGENTS SELECTED:")
    for i, pilot in enumerate(report['pilot_agents'], 1):
        agent_info = agents[pilot]
        print(f"{i}. {pilot}")
        print(f"   Category: {agent_info.category}")
        print(f"   LOC: {agent_info.lines_of_code}")
        print(f"   Complexity: {agent_info.complexity_score}")
        print(f"   Dependencies: {len(agent_info.dependencies)}")
    
    print(f"\n🌊 MIGRATION WAVES:")
    for i, wave in enumerate(report['migration_waves'], 1):
        print(f"Wave {i}: {len(wave)} agents")
        if i <= 3:  # Afficher détail des 3 premières vagues
            print(f"  {', '.join(wave[:5])}{'...' if len(wave) > 5 else ''}")
    
    print(f"\n📁 Full analysis saved to:")
    print(f"   {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
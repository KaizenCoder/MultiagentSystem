#!/usr/bin/env python3
"""
🔍 AUDIT ASYNC/SYNC - DÉTECTION FAUX AGENTS
===========================================

🎯 Mission : Identifier les FAUX AGENTS (roleplay/sync) vs VRAIS AGENTS (async/Pattern Factory)
⚠️ Problème critique : Pollution massive de la base de code par des agents fictifs

Author: Équipe Maintenance Enterprise
Version: 1.0.0 - Audit Critique
Created: 2025-06-19 19h10
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class AgentAnalysis:
    """Résultat d'analyse d'un agent"""
    file_path: str
    agent_name: str
    is_authentic: bool
    has_async_methods: bool
    has_pattern_factory: bool
    has_roleplay_indicators: bool
    async_methods: List[str]
    sync_methods: List[str]
    issues: List[str]
    size_kb: float
    line_count: int

class AsyncSyncAuditor:
    """Auditeur spécialisé pour détecter faux agents"""
    
    def __init__(self):
        self.agents_dir = Path(".")
        self.results: List[AgentAnalysis] = []
        
        # 🎯 Critères agents authentiques Pattern Factory
        self.required_async_methods = {
            'startup', 'health_check', 'execute_task', 'shutdown', 'get_capabilities'
        }
        
        # 🚨 Indicateurs faux agents (roleplay)
        self.roleplay_indicators = [
            'def main()', 'def run_', 'print(', 'input(', 
            'if __name__', 'def execute_mission', 'def run_agent_',
            'sprint1', 'sprint2', 'sprint3', 'sprint4'
        ]
        
        # ✅ Indicateurs vrais agents
        self.authentic_indicators = [
            'from core.agent_factory_architecture import',
            'async def startup', 'async def health_check',
            'Pattern Factory', 'Control Plane', 'Data Plane'
        ]
    
    def analyze_file(self, file_path: Path) -> AgentAnalysis:
        """Analyser un fichier agent"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Statistiques fichier
            size_kb = file_path.stat().st_size / 1024
            line_count = len(content.splitlines())
            
            # Analyse syntaxique
            async_methods = self._find_async_methods(content)
            sync_methods = self._find_sync_methods(content)
            
            # Détection indicateurs
            has_pattern_factory = any(indicator in content for indicator in self.authentic_indicators)
            has_roleplay = any(indicator in content for indicator in self.roleplay_indicators)
            
            # Validation méthodes async Pattern Factory
            has_async_methods = len(async_methods) >= 3
            has_required_methods = any(method in async_methods for method in ['startup', 'health_check'])
            
            # Détermination authenticité
            is_authentic = (
                has_pattern_factory and 
                has_async_methods and 
                has_required_methods and
                not has_roleplay and
                size_kb > 5  # Agents trop petits suspects
            )
            
            # Issues détectées
            issues = []
            if not has_async_methods:
                issues.append("❌ Manque méthodes async")
            if has_roleplay:
                issues.append("🎭 Indicateurs roleplay détectés")
            if not has_pattern_factory:
                issues.append("🏗️ Pas d'import Pattern Factory")
            if size_kb < 5:
                issues.append("📏 Fichier trop petit (<5KB)")
            
            return AgentAnalysis(
                file_path=str(file_path),
                agent_name=file_path.stem,
                is_authentic=is_authentic,
                has_async_methods=has_async_methods,
                has_pattern_factory=has_pattern_factory,
                has_roleplay_indicators=has_roleplay,
                async_methods=async_methods,
                sync_methods=sync_methods,
                issues=issues,
                size_kb=size_kb,
                line_count=line_count
            )
            
        except Exception as e:
            return AgentAnalysis(
                file_path=str(file_path),
                agent_name=file_path.stem,
                is_authentic=False,
                has_async_methods=False,
                has_pattern_factory=False,
                has_roleplay_indicators=True,
                async_methods=[],
                sync_methods=[],
                issues=[f"❌ Erreur analyse: {str(e)}"],
                size_kb=0,
                line_count=0
            )
    
    def _find_async_methods(self, content: str) -> List[str]:
        """Trouver toutes les méthodes async"""
        pattern = r'async\s+def\s+(\w+)'
        return re.findall(pattern, content)
    
    def _find_sync_methods(self, content: str) -> List[str]:
        """Trouver les méthodes sync suspectes"""
        patterns = [
            r'def\s+(run_\w+)',
            r'def\s+(execute_\w+)',
            r'def\s+(main)',
        ]
        methods = []
        for pattern in patterns:
            methods.extend(re.findall(pattern, content))
        return methods
    
    def audit_all_agents(self) -> Dict[str, Any]:
        """Auditer tous les agents du dossier"""
        print("🔍 AUDIT ASYNC/SYNC EN COURS...")
        
        agent_files = list(self.agents_dir.glob("agent_*.py"))
        agent_files.sort()
        
        for file_path in agent_files:
            if file_path.name.startswith('test_') or file_path.name.startswith('audit_'):
                continue
                
            analysis = self.analyze_file(file_path)
            self.results.append(analysis)
            
            # Status temps réel
            status = "✅ AUTHENTIQUE" if analysis.is_authentic else "🚨 FAUX AGENT"
            print(f"{status} - {analysis.agent_name} ({analysis.size_kb:.1f}KB)")
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict[str, Any]:
        """Générer rapport d'audit"""
        authentic_agents = [a for a in self.results if a.is_authentic]
        fake_agents = [a for a in self.results if not a.is_authentic]
        
        return {
            'summary': {
                'total_agents': len(self.results),
                'authentic_agents': len(authentic_agents),
                'fake_agents': len(fake_agents),
                'authenticity_rate': len(authentic_agents) / len(self.results) * 100 if self.results else 0
            },
            'authentic_agents': [
                {
                    'name': a.agent_name,
                    'size_kb': a.size_kb,
                    'async_methods': len(a.async_methods),
                    'pattern_factory': a.has_pattern_factory
                }
                for a in authentic_agents
            ],
            'fake_agents': [
                {
                    'name': a.agent_name,
                    'size_kb': a.size_kb,
                    'issues': a.issues,
                    'roleplay': a.has_roleplay_indicators
                }
                for a in fake_agents
            ],
            'detailed_results': self.results
        }
    
    def print_detailed_report(self, report: Dict[str, Any]):
        """Afficher rapport détaillé"""
        print("\n" + "="*60)
        print("🔍 RAPPORT AUDIT ASYNC/SYNC - DÉTECTION FAUX AGENTS")
        print("="*60)
        
        summary = report['summary']
        print(f"\n📊 RÉSUMÉ :")
        print(f"• Total agents analysés : {summary['total_agents']}")
        print(f"• ✅ Agents authentiques : {summary['authentic_agents']} ({summary['authenticity_rate']:.1f}%)")
        print(f"• 🚨 Faux agents : {summary['fake_agents']} ({100-summary['authenticity_rate']:.1f}%)")
        
        if report['authentic_agents']:
            print(f"\n✅ AGENTS AUTHENTIQUES (Pattern Factory) :")
            for agent in report['authentic_agents']:
                print(f"  • {agent['name']} - {agent['size_kb']:.1f}KB - {agent['async_methods']} méthodes async")
        
        if report['fake_agents']:
            print(f"\n🚨 FAUX AGENTS À SUPPRIMER :")
            for agent in report['fake_agents']:
                print(f"  • {agent['name']} - {agent['size_kb']:.1f}KB")
                for issue in agent['issues']:
                    print(f"    {issue}")
        
        print(f"\n🎯 RECOMMANDATIONS :")
        if summary['fake_agents'] > 0:
            print(f"⚠️  URGENT : Supprimer {summary['fake_agents']} faux agents avant déploiement")
            print(f"📁 Action : Déplacer vers dossier /roleplay ou supprimer")
        else:
            print(f"✅ Base de code propre - Prêt pour production")

def main():
    """Point d'entrée du script"""
    auditor = AsyncSyncAuditor()
    report = auditor.audit_all_agents()
    auditor.print_detailed_report(report)
    
    # Recommandations de nettoyage
    fake_agents = report['fake_agents']
    if fake_agents:
        print(f"\n🧹 COMMANDES DE NETTOYAGE :")
        print(f"mkdir -p ../roleplay")
        for agent in fake_agents:
            print(f"mv {agent['name']}.py ../roleplay/")

if __name__ == "__main__":
    main() 




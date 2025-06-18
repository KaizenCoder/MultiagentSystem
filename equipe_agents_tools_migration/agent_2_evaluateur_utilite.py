#!/usr/bin/env python3
"""
[TARGET] Agent 2: valuateur d'Utilit - GPT-4 Turbo
Mission: valuer l'utilit des outils dtects pour le projet NextGeneration
Responsabilits:
- Analyser la pertinence de chaque outil
- valuer la compatibilit avec NextGeneration
- Prioriser les outils par valeur ajoute
- Identifier les conflits potentiels
- Gnrer une liste filtre d'outils utiles
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class Agent2EvaluateurUtilite:
    """Agent spcialis dans l'valuation d'utilit des outils"""
    
    def __init__(self, analyse_structure: Dict[str, Any], workspace_path: Path):
        self.analyse_structure = analyse_structure
        self.workspace_path = workspace_path
        self.agent_name = "Agent 2 - valuateur Utilit"
        self.model_name = "GPT-4 Turbo"
        self.start_time = None
        
        # Contexte NextGeneration
        self.nextgen_context = {
            "architecture": ["FastAPI", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
            "patterns": ["Hexagonal", "CQRS", "DI", "Repository", "Service Layer"],
            "technologies": ["Python", "AsyncIO", "Pydantic", "SQLAlchemy", "Prometheus"],
            "domaines": ["orchestration", "agents", "monitoring", "performance", "security"],
            "outils_existants": ["project_backup_system", "generate_pitch_document"]
        }
        
        # Critres d'valuation
        self.criteres_evaluation = {
            "pertinence_technique": 0.3,
            "compatibilite_architecture": 0.25,
            "valeur_ajoutee": 0.2,
            "facilite_integration": 0.15,
            "maintenance": 0.1
        }
    
    async def evaluer_utilite(self) -> Dict[str, Any]:
        """valuer l'utilit des outils dtects"""
        self.start_time = datetime.now()
        print(f"[TARGET] {self.agent_name} - Dmarrage valuation utilit")
        
        try:
            # 1. Analyser le contexte NextGeneration
            await self._analyser_contexte_nextgen()
            
            # 2. valuer chaque outil individuellement
            await self._evaluer_outils_individuels()
            
            # 3. Dtecter les conflits et doublons
            await self._detecter_conflits()
            
            # 4. Prioriser et filtrer
            await self._prioriser_outils()
            
            # 5. Gnrer les recommandations
            resultat = await self._generer_recommandations()
            
            duree = (datetime.now() - self.start_time).total_seconds()
            print(f"[CHECK] {self.agent_name} - Termin en {duree:.2f}s")
            
            return resultat
            
        except Exception as e:
            print(f"[CROSS] {self.agent_name} - Erreur: {e}")
            raise
    
    async def _analyser_contexte_nextgen(self):
        """Analyser le contexte du projet NextGeneration"""
        print("[SEARCH] Analyse du contexte NextGeneration...")
        
        # Analyser les outils existants
        tools_path = self.workspace_path.parent / "tools"
        self.outils_existants_detailles = []
        
        if tools_path.exists():
            for item in tools_path.iterdir():
                if item.is_dir():
                    self.outils_existants_detailles.append({
                        "nom": item.name,
                        "type": "repertoire",
                        "description": f"Outil existant: {item.name}"
                    })
        
        # Dfinir les besoins identifis
        self.besoins_nextgen = {
            "automation": ["scripts de dploiement", "automatisation CI/CD"],
            "monitoring": ["surveillance systme", "mtriques custom"],
            "development": ["outils de dveloppement", "templates"],
            "testing": ["outils de test", "validation"],
            "documentation": ["gnration docs", "diagrammes"],
            "conversion": ["transformation de donnes", "migration"],
            "portability": ["outils multi-plateforme", "conteneurisation"],
            "security": ["audit scurit", "validation"]
        }
    
    async def _evaluer_outils_individuels(self):
        """valuer chaque outil individuellement"""
        print("[CHART] valuation individuelle des outils...")
        
        self.evaluations_detaillees = []
        outils_detectes = self.analyse_structure.get('outils_detectes', [])
        
        for outil in outils_detectes:
            evaluation = await self._evaluer_outil_unique(outil)
            self.evaluations_detaillees.append(evaluation)
    
    async def _evaluer_outil_unique(self, outil: Dict[str, Any]) -> Dict[str, Any]:
        """valuer un outil unique selon nos critres"""
        
        # 1. Pertinence technique
        score_pertinence = self._calculer_pertinence_technique(outil)
        
        # 2. Compatibilit architecture
        score_compatibilite = self._calculer_compatibilite_architecture(outil)
        
        # 3. Valeur ajoute
        score_valeur = self._calculer_valeur_ajoutee(outil)
        
        # 4. Facilit d'intgration
        score_integration = self._calculer_facilite_integration(outil)
        
        # 5. Maintenance
        score_maintenance = self._calculer_score_maintenance(outil)
        
        # Score final pondr
        score_final = (
            score_pertinence * self.criteres_evaluation["pertinence_technique"] +
            score_compatibilite * self.criteres_evaluation["compatibilite_architecture"] +
            score_valeur * self.criteres_evaluation["valeur_ajoutee"] +
            score_integration * self.criteres_evaluation["facilite_integration"] +
            score_maintenance * self.criteres_evaluation["maintenance"]
        )
        
        return {
            "outil": outil,
            "scores": {
                "pertinence_technique": score_pertinence,
                "compatibilite_architecture": score_compatibilite,
                "valeur_ajoutee": score_valeur,
                "facilite_integration": score_integration,
                "maintenance": score_maintenance,
                "score_final": round(score_final, 2)
            },
            "recommandation": self._generer_recommandation_outil(score_final, outil),
            "justification": self._generer_justification(score_final, outil),
            "adaptations_necessaires": self._identifier_adaptations(outil)
        }
    
    def _calculer_pertinence_technique(self, outil: Dict[str, Any]) -> float:
        """Calculer la pertinence technique (0-10)"""
        score = 5.0  # Base
        
        type_outil = outil.get('type', '')
        
        # Bonus par type d'outil
        bonus_types = {
            'automation': 2.0,
            'monitoring': 1.8,
            'cli_tool': 1.5,
            'conversion': 1.3,
            'generation': 1.2,
            'utility': 1.0,
            'download': 0.8,
            'installation': 0.6,
            'test_script': 0.5,
            'web_api': 0.3,
            'interface_web': 0.2
        }
        
        score += bonus_types.get(type_outil, 0)
        
        # Bonus pour les dpendances compatibles
        dependances = outil.get('dependances', [])
        deps_compatibles = ['asyncio', 'pathlib', 'json', 'subprocess', 'logging']
        score += len([d for d in dependances if d in deps_compatibles]) * 0.2
        
        # Malus pour dpendances problmatiques
        deps_problematiques = ['tkinter', 'pygame', 'kivy', 'wx']
        score -= len([d for d in dependances if d in deps_problematiques]) * 0.5
        
        return min(max(score, 0), 10)
    
    def _calculer_compatibilite_architecture(self, outil: Dict[str, Any]) -> float:
        """Calculer la compatibilit avec l'architecture NextGeneration (0-10)"""
        score = 5.0
        
        dependances = outil.get('dependances', [])
        
        # Bonus pour technologies NextGeneration
        tech_nextgen = ['fastapi', 'pydantic', 'sqlalchemy', 'redis', 'prometheus']
        score += len([d for d in dependances if any(t in d.lower() for t in tech_nextgen)]) * 1.0
        
        # Bonus pour patterns async
        if 'asyncio' in dependances:
            score += 1.5
        
        # Malus pour technologies conflictuelles
        tech_conflictuelles = ['flask', 'django', 'tornado', 'bottle']
        score -= len([d for d in dependances if any(t in d.lower() for t in tech_conflictuelles)]) * 1.0
        
        # Bonus pour structure modulaire (beaucoup de fonctions)
        nb_fonctions = len(outil.get('fonctions_principales', []))
        if nb_fonctions >= 3:
            score += 1.0
        elif nb_fonctions >= 5:
            score += 1.5
        
        return min(max(score, 0), 10)
    
    def _calculer_valeur_ajoutee(self, outil: Dict[str, Any]) -> float:
        """Calculer la valeur ajoute pour NextGeneration (0-10)"""
        score = 3.0
        
        nom = outil.get('nom', '').lower()
        description = outil.get('description', '').lower()
        type_outil = outil.get('type', '')
        
        # Vrifier si l'outil rpond  un besoin identifi
        for domaine, besoins in self.besoins_nextgen.items():
            for besoin in besoins:
                if any(mot in nom or mot in description for mot in besoin.split()):
                    score += 2.0
                    break
        
        # Bonus pour nouveaux domaines fonctionnels
        if type_outil in ['conversion', 'portability', 'promotion']:
            score += 1.5
        
        # Malus si doublon avec existant
        for existant in self.outils_existants_detailles:
            if existant['nom'].lower() in nom:
                score -= 2.0
        
        # Bonus pour complexit optimale
        complexite = outil.get('complexite', 0)
        if 50 <= complexite <= 300:
            score += 1.0
        
        return min(max(score, 0), 10)
    
    def _calculer_facilite_integration(self, outil: Dict[str, Any]) -> float:
        """Calculer la facilit d'intgration (0-10)"""
        score = 5.0
        
        dependances = outil.get('dependances', [])
        
        # Bonus pour dpendances standard Python
        deps_standard = ['os', 'sys', 'json', 'pathlib', 'subprocess', 'logging']
        ratio_standard = len([d for d in dependances if d in deps_standard]) / max(len(dependances), 1)
        score += ratio_standard * 2.0
        
        # Malus pour dpendances externes nombreuses
        deps_externes = [d for d in dependances if d not in deps_standard]
        if len(deps_externes) > 5:
            score -= 1.5
        elif len(deps_externes) > 10:
            score -= 3.0
        
        # Bonus pour structure simple
        complexite = outil.get('complexite', 0)
        if complexite < 200:
            score += 1.0
        
        # Bonus si documentation prsente
        if outil.get('description') and len(outil.get('description', '')) > 50:
            score += 1.0
        
        return min(max(score, 0), 10)
    
    def _calculer_score_maintenance(self, outil: Dict[str, Any]) -> float:
        """Calculer le score de maintenance (0-10)"""
        score = 6.0
        
        # Bonus pour documentation
        if outil.get('description'):
            score += 1.0
        
        # Bonus pour structure claire (fonctions bien nommes)
        fonctions = outil.get('fonctions_principales', [])
        fonctions_claires = [f for f in fonctions if not f.startswith('_') and len(f) > 3]
        score += min(len(fonctions_claires) * 0.3, 2.0)
        
        # Malus pour complexit excessive
        complexite = outil.get('complexite', 0)
        if complexite > 500:
            score -= 2.0
        elif complexite > 1000:
            score -= 4.0
        
        return min(max(score, 0), 10)
    
    def _generer_recommandation_outil(self, score: float, outil: Dict[str, Any]) -> str:
        """Gnrer une recommandation pour l'outil"""
        if score >= 7.5:
            return "RECOMMAND"
        elif score >= 6.0:
            return "UTILE"
        elif score >= 4.0:
            return "CONDITIONNEL"
        else:
            return "NON_RECOMMAND"
    
    def _generer_justification(self, score: float, outil: Dict[str, Any]) -> str:
        """Gnrer une justification pour la recommandation"""
        type_outil = outil.get('type', 'unknown')
        nom = outil.get('nom', 'unknown')
        
        if score >= 7.5:
            return f"Outil {type_outil} '{nom}' trs pertinent pour NextGeneration, intgration recommande"
        elif score >= 6.0:
            return f"Outil {type_outil} '{nom}' utile avec quelques adaptations ncessaires"
        elif score >= 4.0:
            return f"Outil {type_outil} '{nom}' potentiellement utile mais ncessite valuation approfondie"
        else:
            return f"Outil {type_outil} '{nom}' non recommand - faible valeur ajoute ou trop complexe"
    
    def _identifier_adaptations(self, outil: Dict[str, Any]) -> List[str]:
        """Identifier les adaptations ncessaires"""
        adaptations = []
        
        # Adaptations pour les chemins
        adaptations.append("Adapter les chemins pour fonctionner depuis n'importe quel rpertoire")
        
        # Adaptations pour les dpendances
        dependances = outil.get('dependances', [])
        deps_externes = [d for d in dependances if d not in ['os', 'sys', 'json', 'pathlib', 'subprocess', 'logging']]
        if deps_externes:
            adaptations.append(f"Vrifier/installer les dpendances: {', '.join(deps_externes[:3])}")
        
        # Adaptations pour l'intgration NextGeneration
        adaptations.append("Adapter la configuration pour l'environnement NextGeneration")
        adaptations.append("Ajouter la documentation et les tests")
        
        return adaptations
    
    async def _detecter_conflits(self):
        """Dtecter les conflits et doublons"""
        print(" Dtection des conflits...")
        
        self.conflits_detectes = []
        
        # Grouper par type d'outil
        outils_par_type = {}
        for eval_outil in self.evaluations_detaillees:
            type_outil = eval_outil['outil']['type']
            if type_outil not in outils_par_type:
                outils_par_type[type_outil] = []
            outils_par_type[type_outil].append(eval_outil)
        
        # Dtecter les doublons
        for type_outil, outils in outils_par_type.items():
            if len(outils) > 1:
                # Trier par score pour garder le meilleur
                outils_tries = sorted(outils, key=lambda x: x['scores']['score_final'], reverse=True)
                meilleur = outils_tries[0]
                doublons = outils_tries[1:]
                
                self.conflits_detectes.append({
                    "type": "doublon",
                    "domaine": type_outil,
                    "meilleur_outil": meilleur['outil']['nom'],
                    "doublons": [d['outil']['nom'] for d in doublons],
                    "recommandation": f"Garder '{meilleur['outil']['nom']}' (score: {meilleur['scores']['score_final']})"
                })
    
    async def _prioriser_outils(self):
        """Prioriser et filtrer les outils"""
        print("[TARGET] Priorisation des outils...")
        
        # Filtrer les outils recommands et utiles
        outils_retenus = []
        outils_rejetes = []
        
        for evaluation in self.evaluations_detaillees:
            recommandation = evaluation['recommandation']
            score = evaluation['scores']['score_final']
            
            if recommandation in ['RECOMMAND', 'UTILE'] and score >= 5.0:
                # Vrifier qu'il n'est pas en doublon
                est_doublon = any(
                    conflit['type'] == 'doublon' and 
                    evaluation['outil']['nom'] in conflit['doublons']
                    for conflit in self.conflits_detectes
                )
                
                if not est_doublon:
                    outils_retenus.append(evaluation)
                else:
                    outils_rejetes.append({
                        **evaluation,
                        "raison_rejet": "Doublon avec un outil mieux not"
                    })
            else:
                outils_rejetes.append({
                    **evaluation,
                    "raison_rejet": f"Score trop faible ({score}) ou non recommand"
                })
        
        # Trier par score final
        self.outils_retenus = sorted(outils_retenus, key=lambda x: x['scores']['score_final'], reverse=True)
        self.outils_rejetes = outils_rejetes
    
    async def _generer_recommandations(self) -> Dict[str, Any]:
        """Gnrer le rapport final avec recommandations"""
        duree = (datetime.now() - self.start_time).total_seconds()
        
        # Statistiques
        nb_total = len(self.evaluations_detaillees)
        nb_retenus = len(self.outils_retenus)
        nb_rejetes = len(self.outils_rejetes)
        
        # Top 10 des outils retenus
        top_outils = self.outils_retenus[:10]
        
        rapport = {
            "agent": self.agent_name,
            "model": self.model_name,
            "timestamp": self.start_time.isoformat(),
            "duree_secondes": duree,
            "status": "SUCCESS",
            "statistiques": {
                "outils_evalues": nb_total,
                "outils_retenus": nb_retenus,
                "outils_rejetes": nb_rejetes,
                "taux_retention": round(nb_retenus / nb_total * 100, 1) if nb_total > 0 else 0
            },
            "outils_utiles": [eval_outil['outil'] for eval_outil in self.outils_retenus],
            "evaluations_detaillees": self.evaluations_detaillees,
            "conflits_detectes": self.conflits_detectes,
            "top_recommandations": top_outils,
            "criteres_evaluation": self.criteres_evaluation,
            "recommendations_globales": [
                f"Retenir {nb_retenus} outils sur {nb_total} analyss",
                f"Prioriser les {min(5, nb_retenus)} premiers outils (scores > 7.0)",
                f"Traiter {len(self.conflits_detectes)} conflits dtects",
                "Adapter tous les outils pour l'environnement NextGeneration"
            ]
        }
        
        # Sauvegarder le rapport
        rapport_path = self.workspace_path / "reports" / f"agent_2_evaluation_utilite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {rapport_path}")
        print(f"[CHART] Rsultat: {nb_retenus}/{nb_total} outils retenus ({round(nb_retenus/nb_total*100, 1)}%)")
        
        return rapport

# Test autonome
if __name__ == "__main__":
    async def test():
        # Simulation d'analyse de structure
        analyse_mock = {
            "outils_detectes": [
                {
                    "nom": "test_tool.py",
                    "type": "cli_tool",
                    "description": "Outil de test CLI",
                    "complexite": 150,
                    "dependances": ["argparse", "json", "pathlib"],
                    "fonctions_principales": ["main", "process_data", "save_results"]
                }
            ]
        }
        
        agent = Agent2EvaluateurUtilite(
            analyse_structure=analyse_mock,
            workspace_path=Path(__file__).parent
        )
        result = await agent.evaluer_utilite()
        print(f"[CHECK] Test termin: {len(result['outils_utiles'])} outils utiles")
    
    asyncio.run(test()) 
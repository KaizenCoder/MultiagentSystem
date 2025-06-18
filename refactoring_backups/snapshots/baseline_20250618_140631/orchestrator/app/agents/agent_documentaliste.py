"""
Agent Documentaliste - Spécialisé dans l'analyse de structure de projet
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

class AgentDocumentaliste:
    """
    Agent spécialisé dans l'analyse de la structure des projets
    et la proposition de classements pertinents
    """
    
    def __init__(self, project_root: str = "/c/Dev"):
        self.project_root = Path(project_root)
        self.agent_id = "agent-documentaliste"
        self.specialization = "Analyse de structure et organisation documentaire"
        
    async def analyser_structure_projet(self) -> Dict[str, Any]:
        """Analyse complète de la structure du projet"""
        
        rapport = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "specialization": self.specialization,
            "analyse": {
                "structure_actuelle": {},
                "problemes_identifies": [],
                "propositions_amelioration": [],
                "plan_reorganisation": {}
            }
        }
        
        # Analyse de la structure actuelle
        rapport["analyse"]["structure_actuelle"] = await self._analyser_structure_actuelle()
        
        # Identification des problèmes
        rapport["analyse"]["problemes_identifies"] = await self._identifier_problemes()
        
        # Propositions d'amélioration
        rapport["analyse"]["propositions_amelioration"] = await self._proposer_ameliorations()
        
        # Plan de réorganisation
        rapport["analyse"]["plan_reorganisation"] = await self._creer_plan_reorganisation()
        
        return rapport
    
    async def _analyser_structure_actuelle(self) -> Dict[str, Any]:
        """Analyse la structure actuelle du projet"""
        
        structure = {
            "projets_identifies": [],
            "types_fichiers": {},
            "doublons_potentiels": [],
            "hierarchie_complexite": {},
            "patterns_organisation": []
        }
        
        # Projets identifiés dans le workspace
        projets = [
            "nextgeneration", "SuperWhisper_V6", "Superwhisper2", "Projet_N8N",
            "lux", "MCP", "pipedream", "improve_cursor", "fail2"
        ]
        
        for projet in projets:
            projet_path = self.project_root / projet
            if projet_path.exists():
                info_projet = {
                    "nom": projet,
                    "taille_approximative": self._estimer_taille_projet(projet_path),
                    "types_contenus": self._analyser_types_contenus(projet_path),
                    "niveau_organisation": self._evaluer_organisation(projet_path),
                    "documentation_presente": self._verifier_documentation(projet_path)
                }
                structure["projets_identifies"].append(info_projet)
        
        # Analyse des types de fichiers
        structure["types_fichiers"] = {
            "code": ["*.py", "*.js", "*.ts", "*.cpp", "*.c"],
            "documentation": ["*.md", "*.txt", "*.rst", "*.doc"],
            "configuration": ["*.json", "*.yaml", "*.yml", "*.ini", "*.cfg"],
            "scripts": ["*.sh", "*.bat", "*.ps1"],
            "données": ["*.csv", "*.xlsx", "*.db", "*.sqlite"],
            "media": ["*.mp3", "*.wav", "*.mp4", "*.avi", "*.jpg", "*.png"]
        }
        
        # Doublons potentiels identifiés
        structure["doublons_potentiels"] = [
            {"type": "SuperWhisper", "versions": ["SuperWhisper", "SuperWhisper_V6", "Superwhisper2"]},
            {"type": "Solutions backup", "versions": ["solution ok 20250604_ok", "Projet_N8N_backup_*"]},
            {"type": "Peer reviews", "versions": ["peer_review", "peer_review next génération"]}
        ]
        
        return structure
    
    async def _identifier_problemes(self) -> List[Dict[str, Any]]:
        """Identifie les problèmes dans l'organisation actuelle"""
        
        problemes = [
            {
                "categorie": "Structure",
                "severite": "Élevée",
                "description": "Multiples versions du même projet (SuperWhisper)",
                "impact": "Confusion, maintenance difficile, espace disque gaspillé"
            },
            {
                "categorie": "Nomenclature",
                "severite": "Moyenne",
                "description": "Conventions de nommage incohérentes",
                "exemples": ["nextgeneration vs NextGeneration", "Superwhisper vs SuperWhisper_V6"]
            },
            {
                "categorie": "Organisation",
                "severite": "Élevée",
                "description": "Fichiers temporaires et backups mélangés avec projets actifs",
                "exemples": ["tmp/", "fail2/", "*_backup_*"]
            },
            {
                "categorie": "Documentation",
                "severite": "Moyenne",
                "description": "Documentation dispersée et incohérente",
                "impact": "Difficile de comprendre l'architecture globale"
            },
            {
                "categorie": "Dépendances",
                "severite": "Moyenne",
                "description": "Projets interdépendants non clairement organisés",
                "impact": "Difficile de comprendre les relations entre projets"
            }
        ]
        
        return problemes
    
    async def _proposer_ameliorations(self) -> List[Dict[str, Any]]:
        """Propose des améliorations pour l'organisation"""
        
        ameliorations = [
            {
                "priorite": "Critique",
                "titre": "Consolidation des versions SuperWhisper",
                "description": "Créer un dossier SuperWhisper unifié avec sous-dossiers par version",
                "structure_proposee": {
                    "SuperWhisper/": {
                        "v1_legacy/": "Archive de la première version",
                        "v2_current/": "Version actuellement développée",
                        "v6_experimental/": "Version expérimentale",
                        "shared/": "Code commun entre versions",
                        "docs/": "Documentation globale"
                    }
                }
            },
            {
                "priorite": "Élevée",
                "titre": "Séparation projets actifs/archives",
                "description": "Créer une hiérarchie claire entre développement actif et archives",
                "structure_proposee": {
                    "active_projects/": "Projets en développement actif",
                    "archived_projects/": "Projets terminés ou abandonnés",
                    "experimental/": "Projets expérimentaux et POCs",
                    "utilities/": "Scripts et outils utilitaires",
                    "documentation/": "Documentation transversale"
                }
            },
            {
                "priorite": "Moyenne",
                "titre": "Standardisation de la documentation",
                "description": "Adopter une structure de documentation standardisée",
                "template_propose": {
                    "README.md": "Description principale du projet",
                    "docs/": {
                        "architecture.md": "Documentation architecture",
                        "api.md": "Documentation API",
                        "deployment.md": "Guide de déploiement",
                        "troubleshooting.md": "Guide de dépannage"
                    }
                }
            }
        ]
        
        return ameliorations
    
    async def _creer_plan_reorganisation(self) -> Dict[str, Any]:
        """Crée un plan détaillé de réorganisation"""
        
        plan = {
            "phase_1_preparation": {
                "duree_estimee": "2-3 heures",
                "actions": [
                    "Backup complet du workspace actuel",
                    "Analyse des dépendances entre projets",
                    "Identification des projets vraiment actifs",
                    "Création de la nouvelle structure de dossiers"
                ]
            },
            "phase_2_migration": {
                "duree_estimee": "4-6 heures",
                "actions": [
                    "Migration des projets actifs vers active_projects/",
                    "Archivage des projets obsolètes",
                    "Consolidation des versions SuperWhisper",
                    "Nettoyage des fichiers temporaires"
                ]
            },
            "phase_3_optimisation": {
                "duree_estimee": "2-3 heures",
                "actions": [
                    "Standardisation de la documentation",
                    "Création d'un index global des projets",
                    "Mise en place de conventions de nommage",
                    "Vérification des liens et dépendances"
                ]
            },
            "structure_cible": {
                "Dev/": {
                    "active_projects/": {
                        "nextgeneration/": "Projet principal multi-agents",
                        "SuperWhisper/": "Suite complète audio/vocal",
                        "MCP/": "Infrastructure MCP",
                        "Orchestrator/": "Système d'orchestration"
                    },
                    "experimental/": {
                        "POCs/": "Preuves de concept",
                        "research/": "Projets de recherche"
                    },
                    "archived/": {
                        "deprecated_versions/": "Versions obsolètes",
                        "completed_projects/": "Projets terminés"
                    },
                    "utilities/": {
                        "scripts/": "Scripts utilitaires",
                        "tools/": "Outils de développement"
                    },
                    "docs/": {
                        "global/": "Documentation transversale",
                        "architecture/": "Documentation architecture globale"
                    }
                }
            },
            "benefices_attendus": [
                "Réduction de 40-50% de l'espace disque par élimination des doublons",
                "Amélioration de la navigabilité et compréhension",
                "Facilitation de la maintenance et des mises à jour",
                "Meilleure collaboration en équipe",
                "Réduction du temps de recherche de fichiers"
            ]
        }
        
        return plan
    
    def _estimer_taille_projet(self, path: Path) -> str:
        """Estime la taille d'un projet"""
        try:
            total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            if total_size > 1024**3:  # > 1GB
                return f"{total_size / (1024**3):.1f} GB"
            elif total_size > 1024**2:  # > 1MB
                return f"{total_size / (1024**2):.1f} MB"
            else:
                return f"{total_size / 1024:.1f} KB"
        except:
            return "Taille inconnue"
    
    def _analyser_types_contenus(self, path: Path) -> List[str]:
        """Analyse les types de contenus d'un projet"""
        extensions = set()
        try:
            for file in path.rglob('*'):
                if file.is_file() and file.suffix:
                    extensions.add(file.suffix.lower())
        except:
            pass
        return list(extensions)[:10]  # Top 10 extensions
    
    def _evaluer_organisation(self, path: Path) -> str:
        """Évalue le niveau d'organisation d'un projet"""
        score = 0
        
        # Présence de README
        if (path / "README.md").exists() or (path / "readme.md").exists():
            score += 2
            
        # Structure de dossiers
        common_dirs = ["src", "docs", "tests", "config", "scripts"]
        for dir_name in common_dirs:
            if (path / dir_name).exists():
                score += 1
                
        # Fichiers de configuration
        config_files = ["package.json", "requirements.txt", "Dockerfile", ".gitignore"]
        for config_file in config_files:
            if (path / config_file).exists():
                score += 1
        
        if score >= 8:
            return "Excellente"
        elif score >= 5:
            return "Bonne"
        elif score >= 3:
            return "Moyenne"
        else:
            return "À améliorer"
    
    def _verifier_documentation(self, path: Path) -> Dict[str, bool]:
        """Vérifie la présence de documentation"""
        return {
            "readme": any((path / name).exists() for name in ["README.md", "readme.md", "README.txt"]),
            "docs_folder": (path / "docs").exists(),
            "api_docs": any((path / "docs" / name).exists() for name in ["api.md", "API.md"] if (path / "docs").exists()),
            "changelog": any((path / name).exists() for name in ["CHANGELOG.md", "HISTORY.md"])
        }

# Instance globale de l'agent
agent_documentaliste = AgentDocumentaliste() 
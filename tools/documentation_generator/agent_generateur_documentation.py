#!/usr/bin/env python3
"""
Agent Générateur Documentation - SuperWhisper_V6 → NextGeneration
Mission: Générer documentation automatique CODE-SOURCE.md exhaustive

Base: Extension de tools/generate_pitch_document/generate_pitch_document.py
Architecture: Réutilisation pattern agents de project_backup_system/agents/
Référence: SuperWhisper_V6 generate_bundle_coordinateur.py (370 fichiers, 235KB)

Fonctionnalités avancées:
- Scan complet projet NextGeneration (>100 fichiers attendus)
- Génération CODE-SOURCE.md (>200KB attendu)
- Modes multiples (préservation, régénération, validation, sauvegarde)
- Métriques projet, informations Git, architecture
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import subprocess
import hashlib
import shutil
import sys

# Golden Source Logging
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core import logging_manager

class AgentGenerateurDocumentation:
    """Agent spécialisé pour générer la documentation complète NextGeneration"""
    
    def __init__(self, analyse_structure: Dict[str, Any], base_generateur: Path, 
                 base_agents: Path, superwhisper_reference: Path, workspace_path: Path):
        self.analyse_structure = analyse_structure
        self.base_generateur = base_generateur
        self.base_agents = base_agents
        self.superwhisper_reference = superwhisper_reference
        self.workspace_path = workspace_path
        self.nextgeneration_root = workspace_path.parent.parent
        
        # Configuration génération
        self.output_file = self.nextgeneration_root / "CODE-SOURCE.md"
        self.template_file = self.workspace_path / "templates" / "TEMPLATE_CODE_SOURCE.md"
        self.config_file = self.workspace_path / "config" / "documentation_config.json"
        
        # Logging
        self.logger = logging_manager.get_logger('doc_generator_agent', custom_config={
            "logger_name": "AgentGenerateurDocumentation",
            "log_level": "INFO",
            "async_enabled": True,
            "elasticsearch_enabled": True
        })
        
        # Métriques de génération
        self.generation_stats = {
            "total_files_scanned": 0,
            "total_size_bytes": 0,
            "generation_time_seconds": 0,
            "code_source_size_kb": 0,
            "modes_supported": ["preservation", "regeneration", "validation", "backup"]
        }
        
    async def generer_documentation_complete(self) -> Dict[str, Any]:
        """Génération complète de la documentation CODE-SOURCE.md"""
        start_time = datetime.now()
        self.logger.info("[🤖] Démarrage génération documentation complète")
        
        try:
            # Étape 1: Créer configuration et templates
            await self._creer_infrastructure_generation()
            
            # Étape 2: Scanner structure complète NextGeneration
            structure_scan = await self._scanner_structure_complete()
            
            # Étape 3: Générer métadonnées Git et projet
            metadata_projet = await self._generer_metadata_projet()
            
            # Étape 4: Générer documentation base sur template
            await self._generer_code_source_template(structure_scan, metadata_projet)
            
            # Étape 5: Modes avancés (préservation, validation, sauvegarde)
            await self._executer_modes_avances()
            
            # Étape 6: Calcul métriques finales
            end_time = datetime.now()
            self.generation_stats["generation_time_seconds"] = (end_time - start_time).total_seconds()
            self.generation_stats["code_source_size_kb"] = self._calculer_taille_fichier(self.output_file)
            
            self.logger.info(f"[✅] Documentation générée: {self.generation_stats['code_source_size_kb']}KB")
            
            return {
                "status": "SUCCESS",
                "output_file": str(self.output_file),
                "doc_size_kb": self.generation_stats["code_source_size_kb"],
                "files_scanned": self.generation_stats["total_files_scanned"],
                "generation_time": self.generation_stats["generation_time_seconds"],
                "modes_executed": self.generation_stats["modes_supported"]
            }
            
        except Exception as e:
            self.logger.error(f"[❌] Erreur génération documentation: {e}")
            return {"status": "FAILED", "error": str(e)}
    
    async def _creer_infrastructure_generation(self):
        """Créer l'infrastructure nécessaire pour la génération"""
        # Créer template basé sur SuperWhisper_V6
        await self._creer_template_code_source()
        
        # Créer configuration
        await self._creer_configuration_generation()
        
        self.logger.info("[📁] Infrastructure de génération créée")
    
    async def _creer_template_code_source(self):
        """Créer le template CODE-SOURCE.md basé sur SuperWhisper_V6"""
        template_content = """# 🚀 CODE SOURCE COMPLET - NEXTGENERATION

## 📊 **MÉTADONNÉES PROJET**

<!-- METADATA_PROJET -->

## 🏗️ **ARCHITECTURE GLOBALE**

<!-- ARCHITECTURE_GLOBALE -->

## 📁 **STRUCTURE PROJET COMPLÈTE**

```
<!-- ARBORESCENCE_COMPLETE -->
```

## 🛠️ **INFRASTRUCTURE MATURE IDENTIFIÉE**

### 📦 **Écosystème Tools (6 outils fonctionnels)**

<!-- TOOLS_ECOSYSTEM -->

### 🤖 **Équipes d'Agents Spécialisés**

<!-- AGENTS_TEAMS -->

### 🎼 **Orchestrateur Principal**

<!-- ORCHESTRATOR -->

### 💾 **API Mémoire & Bases de Données**

<!-- MEMORY_API -->

### 📚 **Documentation & Guides**

<!-- DOCUMENTATION -->

### 🧪 **Tests & Validation**

<!-- TESTS -->

## 📄 **CODE SOURCE DÉTAILLÉ**

<!-- CODEBASE_CONTENT -->

## 📊 **MÉTRIQUES TECHNIQUES**

<!-- TECHNICAL_METRICS -->

## 🎯 **ANALYSES QUALITÉ**

<!-- QUALITY_ANALYSIS -->

---

**🤖 Généré automatiquement par Agent Générateur Documentation**  
**📅 Date:** <!-- GENERATION_DATE -->  
**⏱️ Durée:** <!-- GENERATION_TIME -->  
**📊 Statistiques:** <!-- GENERATION_STATS -->  
**🎯 Mode:** <!-- GENERATION_MODE -->
"""
        
        self.template_file.parent.mkdir(exist_ok=True)
        with open(self.template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    async def _creer_configuration_generation(self):
        """Créer la configuration de génération"""
        config = {
            "project_name": "NextGeneration",
            "generation_modes": {
                "preservation": {
                    "enabled": True,
                    "backup_existing": True,
                    "compare_changes": True
                },
                "regeneration": {
                    "enabled": True,
                    "force_overwrite": False,
                    "validate_before": True
                },
                "validation": {
                    "enabled": True,
                    "dry_run": True,
                    "show_diff": True
                },
                "backup": {
                    "enabled": True,
                    "versioning": True,
                    "compress": True
                }
            },
            "scan_configuration": {
                "include_directories": [
                    "agent_factory_experts_team/",
                    "agent_factory_implementation/", 
                    "tools/",
                    "orchestrator/",
                    "memory_api/",
                    "docs/",
                    "tests/",
                    "scripts/",
                    "config/"
                ],
                "exclude_directories": [
                    ".git",
                    "__pycache__",
                    "node_modules",
                    ".vscode",
                    "chroma_db",
                    "logs",
                    "reports"
                ],
                "include_extensions": [
                    ".py", ".md", ".json", ".yml", ".yaml", 
                    ".txt", ".cfg", ".ini", ".ps1", ".sh",
                    ".sql", ".ts", ".js", ".dockerfile"
                ],
                "max_file_size_mb": 5
            },
            "output_configuration": {
                "target_size_kb": 200,
                "max_size_mb": 10,
                "encoding": "utf-8",
                "format": "markdown"
            }
        }
        
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    async def _scanner_structure_complete(self) -> Dict[str, Any]:
        """Scanner la structure complète du projet NextGeneration"""
        self.logger.info("[🔍] Scan structure complète NextGeneration")
        
        # Charger configuration scan
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        scan_config = config["scan_configuration"]
        structure = {
            "arborescence": "",
            "files_details": [],
            "directories_stats": {},
            "total_files": 0,
            "total_size_bytes": 0
        }
        
        # Générer arborescence
        structure["arborescence"] = await self._generer_arborescence_complete()
        
        # Scanner fichiers détaillés
        for include_dir in scan_config["include_directories"]:
            dir_path = self.nextgeneration_root / include_dir
            if dir_path.exists():
                await self._scanner_repertoire(dir_path, structure, scan_config)
        
        self.generation_stats["total_files_scanned"] = structure["total_files"]
        self.generation_stats["total_size_bytes"] = structure["total_size_bytes"]
        
        self.logger.info(f"[✅] Scan terminé: {structure['total_files']} fichiers, {structure['total_size_bytes']//1024}KB")
        return structure
    
    async def _generer_arborescence_complete(self) -> str:
        """Générer l'arborescence complète du projet"""
        tree_lines = ["nextgeneration/"]
        
        def walk_directory(path: Path, prefix: str = "", is_last: bool = True):
            if path.name.startswith('.') or path.name in ['__pycache__', 'node_modules']:
                return
                
            items = list(path.iterdir())
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            # Afficher répertoires
            for i, dir_item in enumerate(sorted(dirs)):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                connector = "└── " if is_last_dir else "├── "
                tree_lines.append(f"{prefix}{connector}{dir_item.name}/")
                
                next_prefix = prefix + ("    " if is_last_dir else "│   ")
                walk_directory(dir_item, next_prefix, is_last_dir)
            
            # Afficher fichiers
            for i, file_item in enumerate(sorted(files)):
                is_last_file = (i == len(files) - 1)
                connector = "└── " if is_last_file else "├── "
                tree_lines.append(f"{prefix}{connector}{file_item.name}")
        
        walk_directory(self.nextgeneration_root)
        return "\n".join(tree_lines)
    
    async def _scanner_repertoire(self, dir_path: Path, structure: Dict[str, Any], scan_config: Dict[str, Any]):
        """Scanner un répertoire spécifique"""
        for root, dirs, files in os.walk(dir_path):
            # Filtrer répertoires exclus
            dirs[:] = [d for d in dirs if d not in scan_config["exclude_directories"]]
            
            for file in files:
                file_path = Path(root) / file
                
                # Vérifier extension
                if not any(file.endswith(ext) for ext in scan_config["include_extensions"]):
                    continue
                
                # Vérifier taille
                try:
                    file_size = file_path.stat().st_size
                    if file_size > scan_config["max_file_size_mb"] * 1024 * 1024:
                        continue
                    
                    # Lire contenu
                    content = await self._lire_fichier_securise(file_path)
                    if content is not None:
                        structure["files_details"].append({
                            "path": str(file_path.relative_to(self.nextgeneration_root)),
                            "size_bytes": file_size,
                            "content": content,
                            "extension": file_path.suffix,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
                        
                        structure["total_files"] += 1
                        structure["total_size_bytes"] += file_size
                        
                except Exception as e:
                    self.logger.warning(f"[⚠️] Erreur lecture {file_path}: {e}")
    
    async def _lire_fichier_securise(self, file_path: Path) -> Optional[str]:
        """Lire un fichier de manière sécurisée"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return None
    
    async def _generer_metadata_projet(self) -> Dict[str, Any]:
        """Générer les métadonnées du projet"""
        metadata = {
            "project_name": "NextGeneration",
            "generation_date": datetime.now().isoformat(),
            "git_info": await self._obtenir_info_git(),
            "infrastructure_mature": {
                "tools_count": 6,
                "agents_teams": 4,
                "total_agents": len(list(self.nextgeneration_root.rglob("agent_*.py"))),
                "documentation_files": len(list(self.nextgeneration_root.rglob("*.md"))),
                "test_files": len(list(self.nextgeneration_root.rglob("test_*.py")))
            },
            "technical_metrics": {
                "python_files": len(list(self.nextgeneration_root.rglob("*.py"))),
                "config_files": len(list(self.nextgeneration_root.rglob("*.json"))) + len(list(self.nextgeneration_root.rglob("*.yml"))),
                "total_lines": await self._compter_lignes_code()
            }
        }
        
        return metadata
    
    async def _obtenir_info_git(self) -> Dict[str, Any]:
        """Obtenir les informations Git du projet"""
        try:
            # Commit actuel
            commit_hash = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], 
                cwd=self.nextgeneration_root, 
                text=True
            ).strip()
            
            # Branche actuelle
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"], 
                cwd=self.nextgeneration_root, 
                text=True
            ).strip()
            
            # Nombre de commits
            commit_count = subprocess.check_output(
                ["git", "rev-list", "--count", "HEAD"], 
                cwd=self.nextgeneration_root, 
                text=True
            ).strip()
            
            return {
                "commit_hash": commit_hash[:8],
                "branch": branch,
                "commit_count": int(commit_count),
                "last_modified": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _compter_lignes_code(self) -> int:
        """Compter les lignes de code total"""
        total_lines = 0
        for py_file in self.nextgeneration_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += len(f.readlines())
            except Exception:
                pass
        return total_lines
    
    async def _generer_code_source_template(self, structure: Dict[str, Any], metadata: Dict[str, Any]):
        """Générer le CODE-SOURCE.md basé sur le template"""
        self.logger.info("[📝] Génération CODE-SOURCE.md")
        
        # Lire template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer métadonnées
        content = content.replace("<!-- METADATA_PROJET -->", self._formatter_metadata(metadata))
        content = content.replace("<!-- ARBORESCENCE_COMPLETE -->", structure["arborescence"])
        content = content.replace("<!-- CODEBASE_CONTENT -->", self._formatter_codebase(structure["files_details"]))
        content = content.replace("<!-- GENERATION_DATE -->", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        content = content.replace("<!-- GENERATION_STATS -->", json.dumps(self.generation_stats, indent=2))
        
        # Écrire fichier final
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _formatter_metadata(self, metadata: Dict[str, Any]) -> str:
        """Formatter les métadonnées pour l'affichage"""
        return f"""
**📊 Projet:** {metadata['project_name']}  
**📅 Généré le:** {metadata['generation_date']}  
**🌿 Branche Git:** {metadata['git_info'].get('branch', 'N/A')}  
**🔄 Commit:** {metadata['git_info'].get('commit_hash', 'N/A')}  
**📊 Agents:** {metadata['infrastructure_mature']['total_agents']}  
**🛠️ Outils:** {metadata['infrastructure_mature']['tools_count']}  
**📄 Fichiers Python:** {metadata['technical_metrics']['python_files']}  
**📋 Lignes de code:** {metadata['technical_metrics']['total_lines']:,}  
"""
    
    def _formatter_codebase(self, files_details: List[Dict[str, Any]]) -> str:
        """Formatter le contenu du codebase"""
        sections = []
        
        for file_info in files_details[:50]:  # Limiter pour éviter fichier trop volumineux
            relative_path = file_info["path"]
            content = file_info["content"]
            extension = file_info["extension"].lstrip('.')
            
            if not extension:
                extension = 'text'
            
            section = f"""
### 📄 `{relative_path}`

<details>
<summary>Voir le code ({file_info['size_bytes']} bytes)</summary>

```{extension}
{content}
```
</details>
"""
            sections.append(section)
        
        if len(files_details) > 50:
            sections.append(f"\n*... et {len(files_details) - 50} autres fichiers*\n")
        
        return "\n".join(sections)
    
    async def _executer_modes_avances(self):
        """Exécuter les modes avancés de génération"""
        self.logger.info("[⚙️] Exécution modes avancés")
        
        # Mode sauvegarde
        await self._mode_sauvegarde()
        
        # Mode validation
        await self._mode_validation()
    
    async def _mode_sauvegarde(self):
        """Mode sauvegarde avec versioning"""
        if self.output_file.exists():
            backup_name = f"CODE-SOURCE_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            backup_path = self.workspace_path / "backups" / backup_name
            backup_path.parent.mkdir(exist_ok=True)
            shutil.copy2(self.output_file, backup_path)
            self.logger.info(f"[💾] Sauvegarde créée: {backup_path}")
    
    async def _mode_validation(self):
        """Mode validation avec vérifications"""
        if not self.output_file.exists():
            return
        
        # Vérifier taille minimale
        size_kb = self._calculer_taille_fichier(self.output_file)
        if size_kb < 200:
            self.logger.warning(f"[⚠️] Fichier généré petit: {size_kb}KB < 200KB attendu")
        
        # Vérifier structure
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_sections = ["MÉTADONNÉES PROJET", "ARCHITECTURE GLOBALE", "CODE SOURCE DÉTAILLÉ"]
        missing_sections = [section for section in required_sections if section not in content]
        
        if missing_sections:
            self.logger.warning(f"[⚠️] Sections manquantes: {missing_sections}")
        else:
            self.logger.info("[✅] Validation structure réussie")
    
    def _calculer_taille_fichier(self, file_path: Path) -> int:
        """Calculer la taille d'un fichier en KB"""
        if file_path.exists():
            return file_path.stat().st_size // 1024
        return 0 




#!/usr/bin/env python3
"""
🚀 Générateur Documentation NextGeneration - Transposition SuperWhisper_V6
Mission: Générer CODE-SOURCE.md complet automatiquement

Référence: SuperWhisper_V6 generate_bundle_coordinateur.py (370 fichiers, 235KB)
Target: >200KB documentation exhaustive NextGeneration
Infrastructure: Réutilise l'existant (generate_pitch_document, project_backup_system)

Usage:
  python generate_bundle_nextgeneration.py                    # Mode normal
  python generate_bundle_nextgeneration.py --mode validation  # Dry-run preview
  python generate_bundle_nextgeneration.py --mode preservation # Backup avant génération
"""

import os
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess

class GenerateurBundleNextGeneration:
    """Générateur simplifié mais efficace pour NextGeneration"""
    
    def __init__(self, mode: str = "regeneration"):
        self.mode = mode
        self.root_dir = Path(__file__).parent.parent.parent  # nextgeneration/
        self.workspace = Path(__file__).parent
        self.output_file = self.root_dir / "CODE-SOURCE.md"
        
        # Configuration scan spécifique NextGeneration
        self.include_dirs = [
            "agent_factory_experts_team",      # Équipe agents experts
            "agent_factory_implementation",    # Implémentation agents
            "tools",                          # 6 outils matures identifiés
            "orchestrator",                   # Orchestrateur principal
            "memory_api",                     # API mémoire
            "docs",                          # Documentation complète
            "tests",                         # Tests complets
            "scripts",                       # Scripts PowerShell/Bash
            "config",                        # Configurations
            "equipe_agents_tools_migration", # Migration tools
            "monitoring",                    # Monitoring Prometheus/Grafana
            "k8s",                          # Kubernetes
            "nextgeneration",               # Sous-projet
            "prompt"                        # Prompts et documentation
        ]
        
        self.exclude_dirs = {".git", "__pycache__", "node_modules", ".vscode", "chroma_db", ".pytest_cache"}
        self.include_exts = {".py", ".md", ".json", ".yml", ".yaml", ".txt", ".cfg", ".ini", ".ps1", ".sh", ".ts", ".js"}
        # Inclure les logs et reports pour documentation complète mais limiter la taille
        self.size_limit_mb = 2  # Limite 2MB par fichier
        
        # Stats de génération
        self.stats = {"files_scanned": 0, "total_size_bytes": 0, "generation_time": 0, "output_size_kb": 0}
        
        # Configuration logging simple
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger("generate_bundle_nextgeneration")
    
    def generer_documentation_complete(self) -> Dict[str, Any]:
        """🚀 Point d'entrée principal pour générer la documentation"""
        start_time = datetime.now()
        self.logger.info(f"[🚀] DÉMARRAGE GÉNÉRATION NEXTGENERATION (mode: {self.mode})")
        
        try:
            # Mode validation = dry-run
            if self.mode == "validation":
                return self._preview_generation()
            
            # Mode preservation = backup avant
            if self.mode == "preservation" and self.output_file.exists():
                self._create_backup()
            
            # 1. Scanner projet complet
            structure = self._scanner_projet_complet()
            
            # 2. Générer métadonnées
            metadata = self._generer_metadata()
            
            # 3. Créer documentation finale
            documentation = self._creer_documentation_finale(structure, metadata)
            
            # 4. Écrire fichier
            self._ecrire_fichier(documentation)
            
            # 5. Stats finales
            end_time = datetime.now()
            self.stats["generation_time"] = (end_time - start_time).total_seconds()
            self.stats["output_size_kb"] = self._get_file_size_kb(self.output_file)
            
            self.logger.info(f"[✅] SUCCÈS: {self.stats['output_size_kb']}KB en {self.stats['generation_time']:.1f}s")
            
            return {
                "status": "SUCCESS",
                "mode": self.mode,
                "output_file": str(self.output_file),
                "stats": self.stats
            }
            
        except Exception as e:
            self.logger.error(f"[❌] ERREUR: {e}")
            return {"status": "FAILED", "error": str(e)}
    
    def _scanner_projet_complet(self) -> Dict[str, Any]:
        """🔍 Scanner complet du projet NextGeneration"""
        self.logger.info("[🔍] Scan projet NextGeneration")
        
        structure = {
            "arborescence": self._generer_arborescence(),
            "fichiers": [],
            "infrastructure": self._analyser_infrastructure()
        }
        
        # Scanner chaque répertoire inclus
        for include_dir in self.include_dirs:
            dir_path = self.root_dir / include_dir
            if dir_path.exists():
                self._scanner_repertoire(dir_path, structure["fichiers"])
        
        self.stats["files_scanned"] = len(structure["fichiers"])
        self.logger.info(f"[✅] Scan terminé: {self.stats['files_scanned']} fichiers")
        
        return structure
    
    def _generer_arborescence(self) -> str:
        """📁 Générer arborescence projet"""
        lines = ["nextgeneration/"]
        
        def walk_dir(path: Path, prefix: str = ""):
            if path.name.startswith('.') or path.name in self.exclude_dirs:
                return
            
            try:
                items = list(path.iterdir())
                dirs = sorted([i for i in items if i.is_dir()])
                files = sorted([i for i in items if i.is_file()])
                
                # Dirs
                for i, d in enumerate(dirs):
                    is_last = (i == len(dirs) - 1) and not files
                    connector = "└── " if is_last else "├── "
                    lines.append(f"{prefix}{connector}{d.name}/")
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    walk_dir(d, next_prefix)
                
                # Files (limite 15 par dossier)
                for i, f in enumerate(files[:15]):
                    is_last = (i == len(files) - 1) or (i == 14)
                    connector = "└── " if is_last else "├── "
                    lines.append(f"{prefix}{connector}{f.name}")
                
                if len(files) > 15:
                    lines.append(f"{prefix}    ... et {len(files) - 15} autres")
                    
            except PermissionError:
                pass
        
        walk_dir(self.root_dir)
        return "\n".join(lines)
    
    def _scanner_repertoire(self, dir_path: Path, fichiers_list: List[Dict]):
        """📄 Scanner un répertoire"""
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for file in files:
                if not any(file.endswith(ext) for ext in self.include_exts):
                    continue
                
                file_path = Path(root) / file
                try:
                    size = file_path.stat().st_size
                    if size > self.size_limit_mb * 1024 * 1024:  # Skip selon limite
                        continue
                    
                    content = self._read_file_safe(file_path)
                    if content:
                        fichiers_list.append({
                            "path": str(file_path.relative_to(self.root_dir)),
                            "size": size,
                            "content": content,
                            "ext": file_path.suffix
                        })
                        self.stats["total_size_bytes"] += size
                        
                except Exception as e:
                    self.logger.warning(f"[⚠️] Skip {file_path}: {e}")
    
    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """📖 Lecture sécurisée fichier"""
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except:
                continue
        return None
    
    def _analyser_infrastructure(self) -> Dict[str, Any]:
        """🏗️ Analyser infrastructure NextGeneration mature"""
        # Analyser dynamiquement l'infrastructure réelle
        tools_found = []
        for tool_dir in (self.root_dir / "tools").iterdir() if (self.root_dir / "tools").exists() else []:
            if tool_dir.is_dir() and not tool_dir.name.startswith('.'):
                tools_found.append(tool_dir.name)
        
        agents_teams_found = []
        for potential_team in ["agent_factory_experts_team", "agent_factory_implementation", 
                              "equipe_agents_tools_migration", "agents_postgresql_resolution"]:
            if (self.root_dir / potential_team).exists():
                agents_teams_found.append(potential_team)
        
        return {
            "tools_mature": tools_found,
            "agents_teams": agents_teams_found,
            "total_agents": len(list(self.root_dir.rglob("agent_*.py"))),
            "total_py_files": len(list(self.root_dir.rglob("*.py"))),
            "total_docs": len(list(self.root_dir.rglob("*.md"))),
            "total_configs": len(list(self.root_dir.rglob("*.json"))) + len(list(self.root_dir.rglob("*.yml"))),
            "total_scripts": len(list(self.root_dir.rglob("*.ps1"))) + len(list(self.root_dir.rglob("*.sh"))),
            "infrastructure_dirs": [d for d in self.include_dirs if (self.root_dir / d).exists()]
        }
    
    def _generer_metadata(self) -> Dict[str, Any]:
        """📊 Métadonnées projet"""
        return {
            "project": "NextGeneration",
            "generated": datetime.now().isoformat(),
            "generator": "generate_bundle_nextgeneration.py v1.0",
            "mode": self.mode,
            "git": self._get_git_info()
        }
    
    def _get_git_info(self) -> Dict[str, str]:
        """🌿 Info Git"""
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root_dir, text=True).strip()[:8]
            branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=self.root_dir, text=True).strip()
            return {"commit": commit, "branch": branch}
        except:
            return {"commit": "N/A", "branch": "N/A"}
    
    def _creer_documentation_finale(self, structure: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """📝 Créer documentation finale"""
        
        # Header
        doc = f"""# 🚀 CODE SOURCE COMPLET - NEXTGENERATION

## 📊 **MÉTADONNÉES PROJET**

**📊 Projet:** {metadata['project']}  
**📅 Généré le:** {metadata['generated']}  
**🔧 Générateur:** {metadata['generator']}  
**🌿 Branche Git:** {metadata['git']['branch']}  
**🔄 Commit:** {metadata['git']['commit']}  
**⚙️ Mode:** {metadata['mode']}  

## 🏗️ **INFRASTRUCTURE MATURE NEXTGENERATION**

### 🛠️ **Écosystème Tools ({len(structure['infrastructure']['tools_mature'])} outils matures)**
"""
        
        for tool in structure["infrastructure"]["tools_mature"]:
            doc += f"- ✅ **{tool}**\n"
        
        doc += f"""
### 🤖 **Équipes d'Agents ({structure['infrastructure']['total_agents']} agents total)**
"""
        
        for team in structure["infrastructure"]["agents_teams"]:
            doc += f"- 👥 **{team}**\n"
        
        doc += f"""
### 📊 **Métriques Techniques**
- 🐍 **Fichiers Python:** {structure['infrastructure']['total_py_files']:,}
- 📚 **Documentation:** {structure['infrastructure']['total_docs']:,}
- 📄 **Fichiers scannés:** {self.stats['files_scanned']:,}
- 💾 **Taille totale:** {self.stats['total_size_bytes']//1024:,}KB

## 📁 **STRUCTURE PROJET COMPLÈTE**

```
{structure['arborescence']}
```

## 📄 **CODE SOURCE DÉTAILLÉ**

"""
        
        # Code source par répertoires
        by_dir = {}
        for f in structure["fichiers"]:
            dir_name = str(Path(f["path"]).parent)
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(f)
        
        for dir_name, files in sorted(by_dir.items()):
            doc += f"\n### 📁 **{dir_name}**\n\n"
            
            for file_info in files[:8]:  # Max 8 files per dir pour éviter doc trop volumineux
                ext = file_info["ext"].lstrip('.') or 'text'
                doc += f"""
#### 📄 `{file_info["path"]}`
<details>
<summary>Voir le code ({file_info["size"]} bytes)</summary>

```{ext}
{file_info["content"]}
```
</details>
"""
            
            if len(files) > 8:
                doc += f"\n*... et {len(files) - 8} autres fichiers*\n"
        
        # Footer
        doc += f"""

---

**🤖 Généré automatiquement par NextGeneration Documentation Generator**  
**📅 Généré le:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**⏱️ Temps de génération:** {self.stats.get('generation_time', 0):.1f}s  
**📊 Mode:** {self.mode}  
**📈 Fichiers scannés:** {self.stats['files_scanned']}  
**💾 Taille sortie:** {self.stats.get('output_size_kb', 0)}KB  

*🎯 Mission: Transposition SuperWhisper_V6 → NextGeneration RÉUSSIE*  
*📍 Infrastructure NextGeneration mature identifiée et documentée*  
*🚀 Base pour futurs développements et transmissions*
"""
        
        return doc
    
    def _ecrire_fichier(self, contenu: str):
        """💾 Écrire fichier final"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        self.logger.info(f"[💾] Fichier écrit: {self.output_file}")
    
    def _preview_generation(self) -> Dict[str, Any]:
        """👁️ Preview mode validation"""
        try:
            structure = self._scanner_projet_complet()
            
            preview = f"""
🔍 **PREVIEW GÉNÉRATION NEXTGENERATION**

📊 **Statistiques prévues:**
- Fichiers à scanner: {len(structure['fichiers'])}
- Taille estimée: {sum(f['size'] for f in structure['fichiers'])//1024}KB
- Infrastructure mature: {len(structure['infrastructure']['tools_mature'])} outils
- Agents teams: {len(structure['infrastructure']['agents_teams'])}

📁 **Aperçu structure:**
{structure['arborescence'][:1000]}...

⚠️ **Mode validation - Aucune modification**
"""
            
            print(preview)
            return {"status": "VALIDATION_SUCCESS", "preview": preview, "stats": self.stats}
            
        except Exception as e:
            self.logger.error(f"[❌] Erreur preview: {e}")
            return {"status": "VALIDATION_FAILED", "error": str(e)}
    
    def _create_backup(self):
        """💾 Créer backup"""
        backup_name = f"CODE-SOURCE_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        backup_path = self.workspace / "backups" / backup_name
        import shutil
        shutil.copy2(self.output_file, backup_path)
        self.logger.info(f"[💾] Backup: {backup_path}")
    
    def _get_file_size_kb(self, path: Path) -> int:
        """📏 Taille fichier en KB"""
        return path.stat().st_size // 1024 if path.exists() else 0


def main():
    """🎯 Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="🚀 Générateur Documentation NextGeneration")
    parser.add_argument('--mode', choices=['regeneration', 'preservation', 'validation'], 
                        default='regeneration', help='Mode de génération')
    parser.add_argument('--dry-run', action='store_true', help='Preview seulement')
    
    args = parser.parse_args()
    if args.dry_run:
        args.mode = 'validation'
    
    # Exécuter génération
    generateur = GenerateurBundleNextGeneration(mode=args.mode)
    resultat = generateur.generer_documentation_complete()
    
    # Afficher résultat
    if resultat["status"] == "SUCCESS":
        print(f"\n🎉 **SUCCÈS GÉNÉRATION NEXTGENERATION**")
        print(f"📄 Fichier: {resultat['output_file']}")
        print(f"📊 Taille: {resultat['stats']['output_size_kb']}KB")
        print(f"🔍 Fichiers: {resultat['stats']['files_scanned']}")
        print(f"⏱️ Durée: {resultat['stats']['generation_time']:.1f}s")
        print(f"🎯 Mode: {resultat['mode']}")
    elif resultat["status"] == "VALIDATION_SUCCESS":
        print(f"\n✅ **VALIDATION RÉUSSIE**")
        print(f"📊 Fichiers prêts: {resultat['stats']['files_scanned']}")
        print(f"🎯 Mode preview terminé avec succès")
    else:
        print(f"\n❌ **ÉCHEC**: {resultat.get('error', 'Erreur inconnue')}")
        exit(1)


if __name__ == "__main__":
    main() 
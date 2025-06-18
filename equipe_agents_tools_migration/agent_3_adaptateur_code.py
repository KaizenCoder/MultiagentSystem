#!/usr/bin/env python3
"""
[TOOL] Agent 3: Adaptateur de Code - Claude Sonnet 4
Mission: Adapter le code des outils slectionns pour NextGeneration
"""

import asyncio
import json
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class Agent3AdaptateurCode:
    """Agent spcialis dans l'adaptation de code"""
    
    def __init__(self, outils_selectionnes: List[Dict], source_path: Path, target_path: Path, workspace_path: Path):
        self.outils_selectionnes = outils_selectionnes
        self.source_path = source_path
        self.target_path = target_path
        self.workspace_path = workspace_path
        self.agent_name = "Agent 3 - Adaptateur Code"
        self.model_name = "Claude Sonnet 4"
        self.start_time = None
        
        self.outils_adaptes = []
        self.erreurs_adaptation = []
        self.fichiers_crees = []
    
    async def adapter_outils(self) -> Dict[str, Any]:
        """Adapter tous les outils slectionns"""
        self.start_time = datetime.now()
        print(f"[TOOL] {self.agent_name} - Dmarrage adaptation code")
        
        try:
            await self._preparer_environnement()
            
            for outil in self.outils_selectionnes:
                await self._adapter_outil_unique(outil)
            
            await self._generer_configurations()
            resultat = await self._generer_rapport()
            
            duree = (datetime.now() - self.start_time).total_seconds()
            print(f"[CHECK] {self.agent_name} - Termin en {duree:.2f}s")
            
            return resultat
            
        except Exception as e:
            print(f"[CROSS] {self.agent_name} - Erreur: {e}")
            raise
    
    async def _preparer_environnement(self):
        """Prparer l'environnement cible"""
        print("[FOLDER] Prparation de l'environnement cible...")
        
        repertoires = [
            "imported_tools", "imported_tools/automation", "imported_tools/monitoring", 
            "imported_tools/conversion", "imported_tools/generation", "imported_tools/utilities",
            "imported_tools/configs", "imported_tools/docs"
        ]
        
        for rep in repertoires:
            rep_path = self.target_path / rep
            rep_path.mkdir(parents=True, exist_ok=True)
    
    async def _adapter_outil_unique(self, outil: Dict[str, Any]):
        """Adapter un outil unique"""
        nom_outil = outil['nom']
        print(f"[TOOL] Adaptation de {nom_outil}...")
        
        try:
            source_file = self.source_path / outil['path']
            
            # Dterminer le rpertoire cible
            type_outil = outil.get('type', 'utilities')
            target_dir = self.target_path / "imported_tools" / type_outil
            target_file = target_dir / nom_outil
            
            # Lire et adapter le contenu
            with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
                contenu_original = f.read()
            
            contenu_adapte = await self._adapter_contenu(contenu_original, outil)
            
            # crire le fichier adapt
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(contenu_adapte)
            
            adaptation_info = {
                "outil": outil,
                "source_path": str(source_file),
                "target_path": str(target_file),
                "status": "SUCCESS"
            }
            
            self.outils_adaptes.append(adaptation_info)
            self.fichiers_crees.append(str(target_file))
            
            print(f"[CHECK] {nom_outil} adapt avec succs")
            
        except Exception as e:
            print(f"[CROSS] Erreur adaptation {nom_outil}: {e}")
            self.erreurs_adaptation.append({
                "outil": nom_outil,
                "erreur": str(e)
            })
    
    async def _adapter_contenu(self, contenu: str, outil: Dict[str, Any]) -> str:
        """Adapter le contenu d'un fichier"""
        header = f'''#!/usr/bin/env python3
"""
 OUTIL ADAPT POUR NEXTGENERATION
Outil: {outil['nom']} - Type: {outil.get('type', 'utility')}
Adapt le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import os
import sys
from pathlib import Path

# Configuration NextGeneration
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
NEXTGEN_CONFIG = {{
    "project_root": PROJECT_ROOT,
    "tools_dir": PROJECT_ROOT / "tools",
    "logs_dir": PROJECT_ROOT / "logs",
    "data_dir": PROJECT_ROOT / "data"
}}

# Crer les rpertoires ncessaires
for dir_path in NEXTGEN_CONFIG.values():
    if isinstance(dir_path, Path):
        dir_path.mkdir(parents=True, exist_ok=True)

'''
        
        # Adaptations simples
        contenu_adapte = contenu
        contenu_adapte = re.sub(r'["\']([A-Za-z]:\\[^"\']+)["\']', r'str(NEXTGEN_CONFIG["data_dir"])', contenu_adapte)
        contenu_adapte = re.sub(r'os\.environ\[["\']([^"\']+)["\']\]', r'os.environ.get("\1", str(NEXTGEN_CONFIG["project_root"]))', contenu_adapte)
        
        return header + "\n\n" + contenu_adapte
    
    async def _generer_configurations(self):
        """Gnrer les fichiers de configuration"""
        print(" Gnration des configurations...")
        
        # Requirements.txt
        dependances = set()
        for outil in self.outils_selectionnes:
            deps = outil.get('dependances', [])
            for dep in deps:
                if dep not in ['os', 'sys', 'json', 'pathlib', 'subprocess', 'logging']:
                    dependances.add(dep)
        
        requirements_content = "# Dpendances pour les outils imports\n"
        for dep in sorted(dependances):
            requirements_content += f"{dep}\n"
        
        requirements_path = self.target_path / "imported_tools" / "requirements.txt"
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        self.fichiers_crees.append(str(requirements_path))
        
        # Configuration JSON
        config = {
            "imported_tools": {
                "version": "1.0.0",
                "source": "SuperWhisper_V6",
                "total_tools": len(self.outils_adaptes),
                "adaptation_date": datetime.now().isoformat()
            }
        }
        
        config_path = self.target_path / "imported_tools" / "configs" / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        self.fichiers_crees.append(str(config_path))
    
    async def _generer_rapport(self) -> Dict[str, Any]:
        """Gnrer le rapport final"""
        duree = (datetime.now() - self.start_time).total_seconds()
        
        rapport = {
            "agent": self.agent_name,
            "model": self.model_name,
            "timestamp": self.start_time.isoformat(),
            "duree_secondes": duree,
            "status": "SUCCESS" if len(self.outils_adaptes) > 0 else "PARTIAL",
            "statistiques": {
                "outils_selectionnes": len(self.outils_selectionnes),
                "outils_adaptes": len(self.outils_adaptes),
                "erreurs_adaptation": len(self.erreurs_adaptation),
                "fichiers_crees": len(self.fichiers_crees),
                "taux_succes": round(len(self.outils_adaptes) / len(self.outils_selectionnes) * 100, 1) if self.outils_selectionnes else 0
            },
            "outils_adaptes": self.outils_adaptes,
            "erreurs_adaptation": self.erreurs_adaptation,
            "tools_copied": len(self.outils_adaptes),
            "tools_adapted": len(self.outils_adaptes)
        }
        
        # Sauvegarder le rapport
        rapport_path = self.workspace_path / "reports" / f"agent_3_adaptation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {rapport_path}")
        return rapport 
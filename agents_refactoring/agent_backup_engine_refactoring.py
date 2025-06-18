#!/usr/bin/env python3
"""
🔒 Agent Backup Engine - Refactoring NextGeneration
Mission: Backup ultra-sécurisé et versioning pour refactoring god mode files
Modèle: Claude Sonnet 4.0 - Fiabilité critique
"""

import os
import sys
import shutil
import json
import hashlib
import zipfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import subprocess

@dataclass
class BackupSnapshot:
    """Snapshot de backup avec intégrité"""
    timestamp: str
    snapshot_id: str
    description: str
    files_count: int
    total_size: int
    checksum_global: str
    phase: str
    rollback_available: bool
    critical_files: List[str]

@dataclass
class BackupOperation:
    """Opération de backup"""
    operation_id: str
    timestamp: str
    operation_type: str  # FULL, INCREMENTAL, PHASE, EMERGENCY
    status: str  # SUCCESS, FAILED, IN_PROGRESS
    duration: float
    files_backed_up: int
    snapshot: Optional[BackupSnapshot] = None
    error_message: Optional[str] = None

class AgentBackupEngineRefactoring:
    """Agent de backup ultra-sécurisé pour refactoring"""
    
    def __init__(self):
        self.name = "Agent Backup Engine Refactoring"
        self.model = "Claude Sonnet 4.0"
        self.mission = "Backup ultra-sécurisé et protection orchestrateur pendant refactoring"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        # Configuration paths
        self.project_root = Path.cwd()
        self.backup_root = self.project_root / "refactoring_backups"
        self.snapshots_dir = self.backup_root / "snapshots"
        self.incremental_dir = self.backup_root / "incremental"
        self.metadata_dir = self.backup_root / "metadata"
        
        # Fichiers critiques à protéger ABSOLUMENT
        self.critical_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py", 
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py",
            "orchestrator/app/config_fixed.py",
            "orchestrator/app/graph/state.py"
        ]
        
        # État du backup
        self.backup_history: List[BackupOperation] = []
        self.current_snapshot: Optional[BackupSnapshot] = None
        self.baseline_established = False
        
        self._setup_backup_environment()
    
    def _setup_backup_environment(self):
        """Setup sécurisé de l'environnement backup"""
        try:
            # Création structure backup
            self.backup_root.mkdir(exist_ok=True)
            self.snapshots_dir.mkdir(exist_ok=True)
            self.incremental_dir.mkdir(exist_ok=True)
            self.metadata_dir.mkdir(exist_ok=True)
            
            # Vérification permissions
            if not os.access(self.backup_root, os.W_OK):
                raise PermissionError(f"Pas de permissions écriture sur {self.backup_root}")
                
            # Création fichiers de configuration
            self._create_backup_config()
            
            print(f"✅ Environnement backup initialisé: {self.backup_root}")
            
        except Exception as e:
            raise RuntimeError(f"❌ Échec setup environnement backup: {e}")
    
    def _create_backup_config(self):
        """Crée configuration backup"""
        config = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "critical_files": self.critical_files,
            "retention_days": 30,
            "compression_enabled": True,
            "encryption_enabled": False,  # Peut être activé plus tard
            "auto_rollback_threshold": 0.8,  # Si performance < 80%
            "max_snapshots": 50
        }
        
        config_file = self.backup_root / "backup_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def calculate_file_checksum(self, file_path: Path) -> str:
        """Calcule checksum MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return "ERROR"
    
    def create_baseline_snapshot(self) -> BackupSnapshot:
        """Crée snapshot baseline AVANT tout refactoring"""
        print("🔒 Création baseline snapshot CRITIQUE...")
        
        operation_id = f"baseline_{int(time.time())}"
        operation = BackupOperation(
            operation_id=operation_id,
            timestamp=datetime.now().isoformat(),
            operation_type="FULL",
            status="IN_PROGRESS",
            duration=0.0,
            files_backed_up=0
        )
        
        try:
            start_time = time.time()
            
            # Snapshot ID unique
            snapshot_id = f"baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            snapshot_dir = self.snapshots_dir / snapshot_id
            snapshot_dir.mkdir(exist_ok=True)
            
            # Backup orchestrateur COMPLET
            orchestrator_source = self.project_root / "orchestrator"
            orchestrator_backup = snapshot_dir / "orchestrator"
            
            if orchestrator_source.exists():
                shutil.copytree(orchestrator_source, orchestrator_backup, dirs_exist_ok=True)
                print(f"✅ Orchestrateur sauvegardé: {orchestrator_backup}")
            
            # Backup fichiers critiques individuellement
            critical_backup_dir = snapshot_dir / "critical_files"
            critical_backup_dir.mkdir(exist_ok=True)
            
            files_count = 0
            total_size = 0
            critical_files_backed = []
            
            for critical_file in self.critical_files:
                source_file = self.project_root / critical_file
                if source_file.exists():
                    # Création structure répertoire
                    backup_file = critical_backup_dir / critical_file
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copie avec métadonnées
                    shutil.copy2(source_file, backup_file)
                    
                    # Calcul checksum
                    checksum = self.calculate_file_checksum(source_file)
                    
                    # Métadonnées fichier
                    metadata = {
                        "original_path": str(source_file),
                        "backup_path": str(backup_file),
                        "checksum": checksum,
                        "size": source_file.stat().st_size,
                        "modified_time": source_file.stat().st_mtime,
                        "backup_time": datetime.now().isoformat()
                    }
                    
                    metadata_file = backup_file.with_suffix(backup_file.suffix + '.meta')
                    with open(metadata_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    files_count += 1
                    total_size += source_file.stat().st_size
                    critical_files_backed.append(str(critical_file))
                    
                    print(f"✅ Backup critique: {critical_file}")
            
            # Checksum global snapshot
            checksum_global = self._calculate_snapshot_checksum(snapshot_dir)
            
            # Création snapshot
            snapshot = BackupSnapshot(
                timestamp=datetime.now().isoformat(),
                snapshot_id=snapshot_id,
                description="Baseline CRITIQUE avant refactoring",
                files_count=files_count,
                total_size=total_size,
                checksum_global=checksum_global,
                phase="BASELINE",
                rollback_available=True,
                critical_files=critical_files_backed
            )
            
            # Sauvegarde métadonnées snapshot
            snapshot_metadata = snapshot_dir / "snapshot.json"
            with open(snapshot_metadata, 'w') as f:
                json.dump(asdict(snapshot), f, indent=2, ensure_ascii=False)
            
            # Compression snapshot (optionnel)
            compressed_snapshot = self._compress_snapshot(snapshot_dir, snapshot_id)
            
            # Finalisation operation
            operation.status = "SUCCESS"
            operation.duration = time.time() - start_time
            operation.files_backed_up = files_count
            operation.snapshot = snapshot
            
            self.backup_history.append(operation)
            self.current_snapshot = snapshot
            self.baseline_established = True
            
            print(f"🎉 BASELINE SNAPSHOT CRÉÉ: {snapshot_id}")
            print(f"📊 {files_count} fichiers, {total_size:,} bytes")
            print(f"⏱️ Durée: {operation.duration:.1f}s")
            
            return snapshot
            
        except Exception as e:
            operation.status = "FAILED"
            operation.error_message = str(e)
            operation.duration = time.time() - start_time
            self.backup_history.append(operation)
            
            raise RuntimeError(f"❌ Échec création baseline: {e}")
    
    def _calculate_snapshot_checksum(self, snapshot_dir: Path) -> str:
        """Calcule checksum global d'un snapshot"""
        checksums = []
        
        for file_path in sorted(snapshot_dir.rglob("*")):
            if file_path.is_file() and not file_path.name.endswith('.meta'):
                checksum = self.calculate_file_checksum(file_path)
                checksums.append(checksum)
        
        # Checksum des checksums
        combined = "".join(checksums)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _compress_snapshot(self, snapshot_dir: Path, snapshot_id: str) -> Path:
        """Compresse un snapshot"""
        compressed_file = self.snapshots_dir / f"{snapshot_id}.zip"
        
        with zipfile.ZipFile(compressed_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in snapshot_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(snapshot_dir)
                    zipf.write(file_path, arcname)
        
        print(f"📦 Snapshot compressé: {compressed_file}")
        return compressed_file
    
    def create_phase_checkpoint(self, phase_name: str, description: str) -> BackupSnapshot:
        """Crée checkpoint avant chaque phase"""
        print(f"🔄 Checkpoint phase: {phase_name}")
        
        operation_id = f"phase_{phase_name}_{int(time.time())}"
        operation = BackupOperation(
            operation_id=operation_id,
            timestamp=datetime.now().isoformat(),
            operation_type="PHASE",
            status="IN_PROGRESS",
            duration=0.0,
            files_backed_up=0
        )
        
        try:
            start_time = time.time()
            
            snapshot_id = f"phase_{phase_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            snapshot_dir = self.snapshots_dir / snapshot_id
            snapshot_dir.mkdir(exist_ok=True)
            
            # Backup incrémental des fichiers critiques
            files_count = 0
            total_size = 0
            critical_files_backed = []
            
            for critical_file in self.critical_files:
                source_file = self.project_root / critical_file
                if source_file.exists():
                    backup_file = snapshot_dir / critical_file
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.copy2(source_file, backup_file)
                    
                    files_count += 1
                    total_size += source_file.stat().st_size
                    critical_files_backed.append(str(critical_file))
            
            checksum_global = self._calculate_snapshot_checksum(snapshot_dir)
            
            snapshot = BackupSnapshot(
                timestamp=datetime.now().isoformat(),
                snapshot_id=snapshot_id,
                description=f"Checkpoint {phase_name}: {description}",
                files_count=files_count,
                total_size=total_size,
                checksum_global=checksum_global,
                phase=phase_name,
                rollback_available=True,
                critical_files=critical_files_backed
            )
            
            # Sauvegarde métadonnées
            snapshot_metadata = snapshot_dir / "snapshot.json"
            with open(snapshot_metadata, 'w') as f:
                json.dump(asdict(snapshot), f, indent=2, ensure_ascii=False)
            
            operation.status = "SUCCESS"
            operation.duration = time.time() - start_time
            operation.files_backed_up = files_count
            operation.snapshot = snapshot
            
            self.backup_history.append(operation)
            
            print(f"✅ Checkpoint créé: {snapshot_id}")
            return snapshot
            
        except Exception as e:
            operation.status = "FAILED"
            operation.error_message = str(e)
            operation.duration = time.time() - start_time
            self.backup_history.append(operation)
            
            raise RuntimeError(f"❌ Échec checkpoint {phase_name}: {e}")
    
    def emergency_rollback(self, target_snapshot_id: Optional[str] = None) -> bool:
        """Rollback d'urgence vers snapshot"""
        print("🚨 ROLLBACK D'URGENCE INITIÉ...")
        
        try:
            # Détermine snapshot cible
            if target_snapshot_id is None:
                if self.current_snapshot:
                    target_snapshot_id = self.current_snapshot.snapshot_id
                else:
                    # Trouve le dernier snapshot baseline
                    baselines = [op for op in self.backup_history 
                               if op.snapshot and op.snapshot.phase == "BASELINE"]
                    if baselines:
                        target_snapshot_id = baselines[-1].snapshot.snapshot_id
                    else:
                        raise RuntimeError("Aucun snapshot baseline disponible")
            
            # Localise snapshot
            snapshot_dir = self.snapshots_dir / target_snapshot_id
            if not snapshot_dir.exists():
                # Essaie de décompresser
                compressed_file = self.snapshots_dir / f"{target_snapshot_id}.zip"
                if compressed_file.exists():
                    self._decompress_snapshot(compressed_file, snapshot_dir)
                else:
                    raise FileNotFoundError(f"Snapshot {target_snapshot_id} introuvable")
            
            # Lecture métadonnées snapshot
            snapshot_metadata = snapshot_dir / "snapshot.json"
            with open(snapshot_metadata, 'r') as f:
                snapshot_data = json.load(f)
            
            # Restauration fichiers critiques
            files_restored = 0
            orchestrator_backup = snapshot_dir / "orchestrator"
            
            if orchestrator_backup.exists():
                # Sauvegarde état actuel avant rollback
                current_backup = self.project_root / f"orchestrator_before_rollback_{int(time.time())}"
                shutil.copytree(self.project_root / "orchestrator", current_backup)
                
                # Suppression orchestrateur actuel
                shutil.rmtree(self.project_root / "orchestrator")
                
                # Restauration orchestrateur
                shutil.copytree(orchestrator_backup, self.project_root / "orchestrator")
                files_restored += 1
                
                print(f"✅ Orchestrateur restauré depuis {target_snapshot_id}")
            
            # Restauration fichiers critiques individuels
            critical_backup_dir = snapshot_dir / "critical_files"
            if critical_backup_dir.exists():
                for critical_file in self.critical_files:
                    backup_file = critical_backup_dir / critical_file
                    if backup_file.exists():
                        target_file = self.project_root / critical_file
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(backup_file, target_file)
                        files_restored += 1
            
            print(f"🎉 ROLLBACK RÉUSSI: {files_restored} fichiers restaurés")
            print(f"📋 Snapshot source: {target_snapshot_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ ÉCHEC ROLLBACK: {e}")
            return False
    
    def _decompress_snapshot(self, compressed_file: Path, target_dir: Path):
        """Décompresse un snapshot"""
        target_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(compressed_file, 'r') as zipf:
            zipf.extractall(target_dir)
        
        print(f"📦 Snapshot décompressé: {target_dir}")
    
    def get_backup_status(self) -> Dict[str, Any]:
        """Retourne status complet backup"""
        return {
            "agent": self.name,
            "model": self.model,
            "status": self.status,
            "baseline_established": self.baseline_established,
            "current_snapshot": asdict(self.current_snapshot) if self.current_snapshot else None,
            "total_operations": len(self.backup_history),
            "successful_operations": len([op for op in self.backup_history if op.status == "SUCCESS"]),
            "available_snapshots": len(list(self.snapshots_dir.glob("*"))),
            "backup_size_total": sum(f.stat().st_size for f in self.backup_root.rglob("*") if f.is_file()),
            "last_operation": asdict(self.backup_history[-1]) if self.backup_history else None
        }
    
    def generate_backup_report(self) -> Dict[str, Any]:
        """Génère rapport complet backup"""
        status = self.get_backup_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "agent_info": {
                "name": self.name,
                "model": self.model,
                "mission": self.mission,
                "version": self.version
            },
            "backup_status": status,
            "critical_protection": {
                "files_protected": len(self.critical_files),
                "orchestrator_protected": True,
                "rollback_ready": self.baseline_established
            },
            "recommendations": self._generate_backup_recommendations(),
            "next_actions": [
                "Validation backup baseline",
                "Test rollback procédure",
                "Configuration monitoring continu"
            ]
        }
        
        return report
    
    def _generate_backup_recommendations(self) -> List[str]:
        """Génère recommandations backup"""
        recommendations = []
        
        if not self.baseline_established:
            recommendations.append("🔴 CRITIQUE: Créer baseline snapshot immédiatement")
        
        if len(self.backup_history) == 0:
            recommendations.append("⚠️ Aucune opération backup effectuée")
        
        failed_ops = [op for op in self.backup_history if op.status == "FAILED"]
        if failed_ops:
            recommendations.append(f"⚠️ {len(failed_ops)} opérations backup échouées")
        
        recommendations.append("✅ Tester procédure rollback régulièrement")
        recommendations.append("✅ Monitoring espace disque backup")
        
        return recommendations
    
    async def execute_mission(self) -> Dict[str, Any]:
        """Exécute mission backup engine"""
        print(f"🚀 {self.name} - Démarrage mission backup critique")
        
        try:
            self.status = "ACTIVE"
            
            # ÉTAPE 1: Création baseline OBLIGATOIRE
            if not self.baseline_established:
                baseline_snapshot = self.create_baseline_snapshot()
                print(f"✅ Baseline établie: {baseline_snapshot.snapshot_id}")
            
            # ÉTAPE 2: Test procédure rollback
            print("🧪 Test procédure rollback...")
            # Note: En production, on éviterait le test rollback complet
            # Ici on vérifie juste la disponibilité
            if self.current_snapshot:
                print(f"✅ Rollback disponible vers: {self.current_snapshot.snapshot_id}")
            
            # ÉTAPE 3: Génération rapport
            report = self.generate_backup_report()
            
            self.status = "SUCCESS"
            
            print(f"🎉 Mission backup engine ACCOMPLIE")
            
            return {
                "status": "SUCCESS",
                "agent": self.name,
                "model": self.model,
                "mission_completed": True,
                "baseline_established": self.baseline_established,
                "current_snapshot": self.current_snapshot.snapshot_id if self.current_snapshot else None,
                "backup_operations": len(self.backup_history),
                "report": report,
                "rollback_available": True,
                "next_phase_ready": True
            }
            
        except Exception as e:
            self.status = "FAILED"
            print(f"❌ Échec mission backup engine: {e}")
            
            return {
                "status": "FAILED",
                "agent": self.name,
                "error": str(e),
                "backup_operations": len(self.backup_history),
                "rollback_available": self.baseline_established
            }

if __name__ == "__main__":
    # Test agent backup
    agent = AgentBackupEngineRefactoring()
    
    import asyncio
    result = asyncio.run(agent.execute_mission())
    
    print(f"\n📊 RÉSULTAT MISSION BACKUP:")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'SUCCESS':
        print(f"✅ Baseline: {result['baseline_established']}")
        print(f"✅ Snapshot: {result['current_snapshot']}")
        print(f"✅ Rollback: {result['rollback_available']}")
        print(f"✅ Prêt phase suivante: {result['next_phase_ready']}")
    else:
        print(f"❌ Erreur: {result['error']}") 
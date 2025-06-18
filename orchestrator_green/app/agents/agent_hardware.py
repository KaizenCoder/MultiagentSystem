"""
Agent Hardware - Spécialisé dans le diagnostic physique et l'analyse de l'environnement machine
"""

import os
import json
import platform
import psutil
import subprocess
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

class AgentHardware:
    """
    Agent spécialisé dans le diagnostic physique de l'environnement machine
    et l'analyse des performances hardware
    """
    
    def __init__(self):
        self.agent_id = "agent-hardware"
        self.specialization = "Diagnostic physique et analyse de l'environnement machine"
        
    async def diagnostic_complet(self) -> Dict[str, Any]:
        """Effectue un diagnostic physique complet de la machine"""
        
        rapport = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "specialization": self.specialization,
            "diagnostic": {
                "systeme": {},
                "processeur": {},
                "memoire": {},
                "stockage": {},
                "gpu": {},
                "reseau": {},
                "processus": {},
                "performance": {},
                "recommandations": []
            }
        }
        
        # Diagnostic système
        rapport["diagnostic"]["systeme"] = await self._analyser_systeme()
        
        # Diagnostic processeur
        rapport["diagnostic"]["processeur"] = await self._analyser_processeur()
        
        # Diagnostic mémoire
        rapport["diagnostic"]["memoire"] = await self._analyser_memoire()
        
        # Diagnostic stockage
        rapport["diagnostic"]["stockage"] = await self._analyser_stockage()
        
        # Diagnostic GPU
        rapport["diagnostic"]["gpu"] = await self._analyser_gpu()
        
        # Diagnostic réseau
        rapport["diagnostic"]["reseau"] = await self._analyser_reseau()
        
        # Analyse des processus
        rapport["diagnostic"]["processus"] = await self._analyser_processus()
        
        # Analyse des performances
        rapport["diagnostic"]["performance"] = await self._analyser_performance()
        
        # Recommandations
        rapport["diagnostic"]["recommandations"] = await self._generer_recommandations(rapport["diagnostic"])
        
        return rapport
    
    async def _analyser_systeme(self) -> Dict[str, Any]:
        """Analyse les informations système de base"""
        
        systeme = {
            "os": {
                "nom": platform.system(),
                "version": platform.version(),
                "release": platform.release(),
                "architecture": platform.machine(),
                "plateforme": platform.platform()
            },
            "python": {
                "version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "architecture": platform.architecture()
            },
            "machine": {
                "hostname": platform.node(),
                "processeur": platform.processor(),
                "uptime": self._get_uptime()
            },
            "environnement": {
                "utilisateur": os.getenv('USERNAME', os.getenv('USER', 'Unknown')),
                "repertoire_travail": os.getcwd(),
                "variables_importantes": self._get_important_env_vars()
            }
        }
        
        return systeme
    
    async def _analyser_processeur(self) -> Dict[str, Any]:
        """Analyse détaillée du processeur"""
        
        cpu_freq = psutil.cpu_freq()
        cpu_times = psutil.cpu_times()
        
        processeur = {
            "caracteristiques": {
                "coeurs_physiques": psutil.cpu_count(logical=False),
                "coeurs_logiques": psutil.cpu_count(logical=True),
                "frequence_actuelle": f"{cpu_freq.current:.2f} MHz" if cpu_freq else "Non disponible",
                "frequence_min": f"{cpu_freq.min:.2f} MHz" if cpu_freq and cpu_freq.min else "Non disponible",
                "frequence_max": f"{cpu_freq.max:.2f} MHz" if cpu_freq and cpu_freq.max else "Non disponible"
            },
            "utilisation": {
                "utilisation_globale": f"{psutil.cpu_percent(interval=1):.1f}%",
                "utilisation_par_coeur": [f"{usage:.1f}%" for usage in psutil.cpu_percent(interval=1, percpu=True)],
                "temps_cpu": {
                    "utilisateur": cpu_times.user,
                    "systeme": cpu_times.system,
                    "inactif": cpu_times.idle
                }
            },
            "temperature": self._get_cpu_temperature(),
            "charge_moyenne": self._get_load_average()
        }
        
        return processeur
    
    async def _analyser_memoire(self) -> Dict[str, Any]:
        """Analyse détaillée de la mémoire"""
        
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        memoire = {
            "memoire_physique": {
                "totale": self._bytes_to_gb(memory.total),
                "disponible": self._bytes_to_gb(memory.available),
                "utilisee": self._bytes_to_gb(memory.used),
                "libre": self._bytes_to_gb(memory.free),
                "pourcentage_utilise": f"{memory.percent:.1f}%",
                "en_cache": self._bytes_to_gb(getattr(memory, 'cached', 0)),
                "buffers": self._bytes_to_gb(getattr(memory, 'buffers', 0))
            },
            "memoire_swap": {
                "totale": self._bytes_to_gb(swap.total),
                "utilisee": self._bytes_to_gb(swap.used),
                "libre": self._bytes_to_gb(swap.free),
                "pourcentage_utilise": f"{swap.percent:.1f}%"
            },
            "analyse": {
                "statut": self._evaluer_memoire(memory.percent),
                "pression_memoire": "Élevée" if memory.percent > 85 else "Normale",
                "swap_actif": "Oui" if swap.used > 0 else "Non"
            }
        }
        
        return memoire
    
    async def _analyser_stockage(self) -> Dict[str, Any]:
        """Analyse détaillée du stockage"""
        
        stockage = {
            "disques": [],
            "io_stats": {},
            "analyse_globale": {}
        }
        
        # Analyse des partitions
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "taille_totale": self._bytes_to_gb(usage.total),
                    "utilise": self._bytes_to_gb(usage.used),
                    "libre": self._bytes_to_gb(usage.free),
                    "pourcentage_utilise": f"{(usage.used / usage.total * 100):.1f}%",
                    "statut": self._evaluer_disque(usage.used / usage.total * 100)
                }
                stockage["disques"].append(disk_info)
            except PermissionError:
                continue
        
        # Statistiques I/O
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io:
                stockage["io_stats"] = {
                    "lectures": disk_io.read_count,
                    "ecritures": disk_io.write_count,
                    "bytes_lus": self._bytes_to_gb(disk_io.read_bytes),
                    "bytes_ecrits": self._bytes_to_gb(disk_io.write_bytes),
                    "temps_lecture": f"{disk_io.read_time}ms",
                    "temps_ecriture": f"{disk_io.write_time}ms"
                }
        except:
            stockage["io_stats"] = {"status": "Non disponible"}
        
        return stockage
    
    async def _analyser_gpu(self) -> Dict[str, Any]:
        """Analyse du GPU (si disponible)"""
        
        gpu = {
            "detection": "En cours...",
            "cartes_graphiques": [],
            "support_cuda": False,
            "support_opencl": False
        }
        
        # Tentative de détection GPU via nvidia-smi
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'], 
                                   capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split(', ')
                    if len(parts) >= 5:
                        carte = {
                            "nom": parts[0],
                            "memoire_totale": f"{parts[1]} MB",
                            "memoire_utilisee": f"{parts[2]} MB",
                            "temperature": f"{parts[3]}°C",
                            "utilisation": f"{parts[4]}%",
                            "type": "NVIDIA CUDA"
                        }
                        gpu["cartes_graphiques"].append(carte)
                        gpu["support_cuda"] = True
        except:
            pass
        
        # Détection générale via wmic (Windows)
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and 'Name' not in line]
                    for line in lines:
                        if line:
                            gpu["cartes_graphiques"].append({
                                "nom": line,
                                "type": "Générique",
                                "details": "Informations limitées disponibles"
                            })
            except:
                pass
        
        if not gpu["cartes_graphiques"]:
            gpu["detection"] = "Aucun GPU détecté ou informations non accessibles"
        else:
            gpu["detection"] = f"{len(gpu['cartes_graphiques'])} carte(s) graphique(s) détectée(s)"
        
        return gpu
    
    async def _analyser_reseau(self) -> Dict[str, Any]:
        """Analyse des interfaces réseau"""
        
        reseau = {
            "interfaces": [],
            "statistiques_io": {},
            "connectivite": {}
        }
        
        # Interfaces réseau
        for interface, addrs in psutil.net_if_addrs().items():
            interface_info = {
                "nom": interface,
                "adresses": []
            }
            
            for addr in addrs:
                addr_info = {
                    "famille": str(addr.family),
                    "adresse": addr.address,
                    "masque": addr.netmask,
                    "broadcast": addr.broadcast
                }
                interface_info["adresses"].append(addr_info)
            
            # Statistiques de l'interface
            try:
                stats = psutil.net_if_stats()[interface]
                interface_info["statistiques"] = {
                    "active": stats.isup,
                    "vitesse": f"{stats.speed} Mbps" if stats.speed != -1 else "Inconnue",
                    "mtu": stats.mtu
                }
            except:
                interface_info["statistiques"] = {"status": "Non disponible"}
            
            reseau["interfaces"].append(interface_info)
        
        # Statistiques I/O réseau
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                reseau["statistiques_io"] = {
                    "bytes_envoyes": self._bytes_to_mb(net_io.bytes_sent),
                    "bytes_recus": self._bytes_to_mb(net_io.bytes_recv),
                    "paquets_envoyes": net_io.packets_sent,
                    "paquets_recus": net_io.packets_recv,
                    "erreurs_envoi": net_io.errout,
                    "erreurs_reception": net_io.errin
                }
        except:
            reseau["statistiques_io"] = {"status": "Non disponible"}
        
        # Test de connectivité basique
        reseau["connectivite"] = self._tester_connectivite()
        
        return reseau
    
    async def _analyser_processus(self) -> Dict[str, Any]:
        """Analyse des processus en cours"""
        
        processus = {
            "nombre_total": len(psutil.pids()),
            "top_cpu": [],
            "top_memoire": [],
            "processus_suspects": [],
            "analyse": {}
        }
        
        # Collecter les informations des processus
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Top CPU
        processes_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)
        processus["top_cpu"] = [
            {
                "pid": p['pid'],
                "nom": p['name'],
                "cpu": f"{p['cpu_percent'] or 0:.1f}%"
            }
            for p in processes_by_cpu[:10]
        ]
        
        # Top mémoire
        processes_by_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)
        processus["top_memoire"] = [
            {
                "pid": p['pid'],
                "nom": p['name'],
                "memoire": f"{p['memory_percent'] or 0:.1f}%",
                "rss": self._bytes_to_mb(p['memory_info'].rss if p['memory_info'] else 0)
            }
            for p in processes_by_memory[:10]
        ]
        
        # Processus suspects (utilisation élevée)
        for p in processes:
            if (p['cpu_percent'] or 0) > 50 or (p['memory_percent'] or 0) > 10:
                processus["processus_suspects"].append({
                    "pid": p['pid'],
                    "nom": p['name'],
                    "cpu": f"{p['cpu_percent'] or 0:.1f}%",
                    "memoire": f"{p['memory_percent'] or 0:.1f}%",
                    "raison": "Utilisation élevée des ressources"
                })
        
        return processus
    
    async def _analyser_performance(self) -> Dict[str, Any]:
        """Analyse globale des performances"""
        
        performance = {
            "score_global": 0,
            "goulets_etranglement": [],
            "recommandations_performance": [],
            "capacites_ai": {}
        }
        
        # Calcul du score global (sur 100)
        cpu_score = max(0, 100 - psutil.cpu_percent(interval=1))
        memory_score = max(0, 100 - psutil.virtual_memory().percent)
        
        # Score disque (moyenne des disques)
        disk_scores = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_score = max(0, 100 - (usage.used / usage.total * 100))
                disk_scores.append(disk_score)
            except:
                continue
        
        disk_score = sum(disk_scores) / len(disk_scores) if disk_scores else 50
        
        performance["score_global"] = int((cpu_score + memory_score + disk_score) / 3)
        
        # Identification des goulets d'étranglement
        if psutil.cpu_percent(interval=1) > 80:
            performance["goulets_etranglement"].append("CPU surchargé")
        
        if psutil.virtual_memory().percent > 85:
            performance["goulets_etranglement"].append("Mémoire saturée")
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if (usage.used / usage.total * 100) > 90:
                    performance["goulets_etranglement"].append(f"Disque {partition.device} presque plein")
            except:
                continue
        
        # Capacités pour l'IA
        memory_gb = psutil.virtual_memory().total / (1024**3)
        cpu_cores = psutil.cpu_count(logical=True)
        
        performance["capacites_ai"] = {
            "adapte_pour_ia": memory_gb >= 16 and cpu_cores >= 8,
            "memoire_disponible": f"{memory_gb:.1f} GB",
            "coeurs_logiques": cpu_cores,
            "recommandation": self._evaluer_capacites_ia(memory_gb, cpu_cores)
        }
        
        return performance
    
    async def _generer_recommandations(self, diagnostic: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur le diagnostic"""
        
        recommandations = []
        
        # Recommandations mémoire
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 85:
            recommandations.append({
                "categorie": "Mémoire",
                "priorite": "Critique",
                "probleme": f"Utilisation mémoire élevée ({memory_percent:.1f}%)",
                "solution": "Fermer les applications non essentielles, ajouter de la RAM",
                "impact": "Performance dégradée, risque de swap excessif"
            })
        
        # Recommandations CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            recommandations.append({
                "categorie": "Processeur",
                "priorite": "Élevée",
                "probleme": f"Utilisation CPU élevée ({cpu_percent:.1f}%)",
                "solution": "Identifier et optimiser les processus gourmands",
                "impact": "Ralentissements, réactivité réduite"
            })
        
        # Recommandations stockage
        for disque in diagnostic.get("stockage", {}).get("disques", []):
            utilisation = float(disque["pourcentage_utilise"].replace('%', ''))
            if utilisation > 90:
                recommandations.append({
                    "categorie": "Stockage",
                    "priorite": "Critique",
                    "probleme": f"Disque {disque['device']} presque plein ({utilisation:.1f}%)",
                    "solution": "Nettoyer les fichiers inutiles, archiver les données anciennes",
                    "impact": "Risque de panne système, performances dégradées"
                })
        
        # Recommandations IA/ML
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb < 16:
            recommandations.append({
                "categorie": "IA/ML",
                "priorite": "Moyenne",
                "probleme": f"Mémoire limitée pour l'IA ({memory_gb:.1f} GB)",
                "solution": "Upgrade vers 32GB+ pour le ML/AI optimal",
                "impact": "Limitation des modèles utilisables, performance IA réduite"
            })
        
        return recommandations
    
    # Méthodes utilitaires
    def _bytes_to_gb(self, bytes_value: int) -> str:
        """Convertit les bytes en GB"""
        return f"{bytes_value / (1024**3):.2f} GB"
    
    def _bytes_to_mb(self, bytes_value: int) -> str:
        """Convertit les bytes en MB"""
        return f"{bytes_value / (1024**2):.2f} MB"
    
    def _get_uptime(self) -> str:
        """Récupère l'uptime du système"""
        try:
            uptime_seconds = psutil.boot_time()
            uptime = datetime.now().timestamp() - uptime_seconds
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            minutes = int((uptime % 3600) // 60)
            return f"{days}j {hours}h {minutes}m"
        except:
            return "Non disponible"
    
    def _get_important_env_vars(self) -> Dict[str, str]:
        """Récupère les variables d'environnement importantes"""
        important_vars = ['PATH', 'PYTHONPATH', 'CUDA_VISIBLE_DEVICES', 'NVIDIA_VISIBLE_DEVICES']
        return {var: os.getenv(var, 'Non définie') for var in important_vars}
    
    def _get_cpu_temperature(self) -> str:
        """Tente de récupérer la température CPU"""
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            return f"{entries[0].current}°C"
            return "Non disponible"
        except:
            return "Non disponible"
    
    def _get_load_average(self) -> str:
        """Récupère la charge moyenne (Unix/Linux)"""
        try:
            if hasattr(os, 'getloadavg'):
                load1, load5, load15 = os.getloadavg()
                return f"1min: {load1:.2f}, 5min: {load5:.2f}, 15min: {load15:.2f}"
            return "Non disponible (Windows)"
        except:
            return "Non disponible"
    
    def _evaluer_memoire(self, percent: float) -> str:
        """Évalue le statut de la mémoire"""
        if percent < 60:
            return "Optimal"
        elif percent < 80:
            return "Correct"
        elif percent < 90:
            return "Attention"
        else:
            return "Critique"
    
    def _evaluer_disque(self, percent: float) -> str:
        """Évalue le statut du disque"""
        if percent < 70:
            return "Optimal"
        elif percent < 85:
            return "Correct"
        elif percent < 95:
            return "Attention"
        else:
            return "Critique"
    
    def _tester_connectivite(self) -> Dict[str, str]:
        """Teste la connectivité réseau basique"""
        connectivite = {}
        
        # Test ping vers Google DNS
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                       capture_output=True, timeout=5)
            else:
                result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                       capture_output=True, timeout=5)
            
            connectivite["internet"] = "Disponible" if result.returncode == 0 else "Problème"
        except:
            connectivite["internet"] = "Test échoué"
        
        return connectivite
    
    def _evaluer_capacites_ia(self, memory_gb: float, cpu_cores: int) -> str:
        """Évalue les capacités pour l'IA"""
        if memory_gb >= 32 and cpu_cores >= 16:
            return "Excellent pour l'IA/ML lourde"
        elif memory_gb >= 16 and cpu_cores >= 8:
            return "Adapté pour l'IA/ML modérée"
        elif memory_gb >= 8 and cpu_cores >= 4:
            return "Basique pour l'IA légère"
        else:
            return "Insuffisant pour l'IA"

# Instance globale de l'agent
agent_hardware = AgentHardware() 
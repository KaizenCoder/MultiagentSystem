#!/usr/bin/env python3
"""
GESTIONNAIRE DE LOGGING DÉTAILLÉ
===============================

Module de logging avancé pour le suivi détaillé des tests
avec support multi-formats et agrégation des métriques.
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import threading
from queue import Queue
import atexit

class DetailedLogger:
    """Gestionnaire de logging détaillé avec support multi-formats"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuration du logger principal
        self.logger = logging.getLogger("detailed_logger")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler pour le fichier de log détaillé
        detailed_handler = logging.FileHandler(
            self.log_dir / f"detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        detailed_handler.setLevel(logging.DEBUG)
        detailed_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        )
        detailed_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(detailed_handler)
        
        # Handler pour la console (moins détaillé)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Métriques et statistiques
        self.metrics: Dict[str, Any] = {
            "start_time": datetime.now().isoformat(),
            "total_tests": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "warnings": 0,
            "errors": 0,
            "agent_metrics": {}
        }
        
        # File d'attente pour logging asynchrone
        self.log_queue: Queue = Queue()
        self.async_thread = threading.Thread(target=self._process_log_queue, daemon=True)
        self.async_thread.start()
        
        # Enregistrement de la fonction de nettoyage
        atexit.register(self.cleanup)
    
    def log_test_start(self, agent_id: str, test_type: str, params: Dict[str, Any]) -> None:
        """Log le démarrage d'un test"""
        self.metrics["total_tests"] += 1
        if agent_id not in self.metrics["agent_metrics"]:
            self.metrics["agent_metrics"][agent_id] = {
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "warnings": 0,
                "errors": 0,
                "test_durations": []
            }
        self.metrics["agent_metrics"][agent_id]["total_tests"] += 1
        
        message = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "event": "test_start",
            "agent_id": agent_id,
            "test_type": test_type,
            "params": params
        }
        self.log_queue.put(message)
    
    def log_test_result(
        self,
        agent_id: str,
        test_type: str,
        success: bool,
        duration: float,
        metrics: Dict[str, Any],
        errors: Optional[List[str]] = None
    ) -> None:
        """Log le résultat d'un test"""
        if success:
            self.metrics["successful_tests"] += 1
            self.metrics["agent_metrics"][agent_id]["successful_tests"] += 1
        else:
            self.metrics["failed_tests"] += 1
            self.metrics["agent_metrics"][agent_id]["failed_tests"] += 1
        
        self.metrics["agent_metrics"][agent_id]["test_durations"].append(duration)
        
        message = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO" if success else "ERROR",
            "event": "test_result",
            "agent_id": agent_id,
            "test_type": test_type,
            "success": success,
            "duration": duration,
            "metrics": metrics
        }
        if errors:
            message["errors"] = errors
            for error in errors:
                self.metrics["errors"] += 1
                self.metrics["agent_metrics"][agent_id]["errors"] += 1
        
        self.log_queue.put(message)
    
    def log_warning(self, agent_id: str, message: str) -> None:
        """Log un avertissement"""
        self.metrics["warnings"] += 1
        self.metrics["agent_metrics"][agent_id]["warnings"] += 1
        
        warning_message = {
            "timestamp": datetime.now().isoformat(),
            "level": "WARNING",
            "event": "warning",
            "agent_id": agent_id,
            "message": message
        }
        self.log_queue.put(warning_message)
    
    def log_error(self, agent_id: str, error: str, stack_trace: Optional[str] = None) -> None:
        """Log une erreur"""
        self.metrics["errors"] += 1
        self.metrics["agent_metrics"][agent_id]["errors"] += 1
        
        error_message = {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "event": "error",
            "agent_id": agent_id,
            "error": error
        }
        if stack_trace:
            error_message["stack_trace"] = stack_trace
        
        self.log_queue.put(error_message)
    
    def log_metric(self, agent_id: str, metric_name: str, value: Any) -> None:
        """Log une métrique spécifique"""
        metric_message = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "event": "metric",
            "agent_id": agent_id,
            "metric_name": metric_name,
            "value": value
        }
        self.log_queue.put(metric_message)
    
    def get_agent_summary(self, agent_id: str) -> Dict[str, Any]:
        """Retourne un résumé des métriques pour un agent"""
        metrics = self.metrics["agent_metrics"].get(agent_id, {})
        if not metrics:
            return {}
        
        total_tests = metrics["total_tests"]
        success_rate = (metrics["successful_tests"] / total_tests * 100) if total_tests > 0 else 0
        avg_duration = (sum(metrics["test_durations"]) / len(metrics["test_durations"])) if metrics["test_durations"] else 0
        
        return {
            "total_tests": total_tests,
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "warnings": metrics["warnings"],
            "errors": metrics["errors"]
        }
    
    def get_global_summary(self) -> Dict[str, Any]:
        """Retourne un résumé global des métriques"""
        total_tests = self.metrics["total_tests"]
        success_rate = (self.metrics["successful_tests"] / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "start_time": self.metrics["start_time"],
            "end_time": datetime.now().isoformat(),
            "total_tests": total_tests,
            "success_rate": success_rate,
            "total_warnings": self.metrics["warnings"],
            "total_errors": self.metrics["errors"],
            "agent_summaries": {
                agent_id: self.get_agent_summary(agent_id)
                for agent_id in self.metrics["agent_metrics"]
            }
        }
    
    def save_metrics(self) -> None:
        """Sauvegarde les métriques dans un fichier JSON"""
        metrics_file = self.log_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metrics_file, "w") as f:
            json.dump(self.get_global_summary(), f, indent=2)
    
    def _process_log_queue(self) -> None:
        """Traite la file d'attente des logs de manière asynchrone"""
        while True:
            try:
                message = self.log_queue.get()
                if message is None:  # Signal d'arrêt
                    break
                
                # Formatage du message
                log_message = (
                    f"[{message['event']}] "
                    f"Agent: {message['agent_id']} "
                    f"Level: {message['level']}"
                )
                
                if "test_type" in message:
                    log_message += f" Type: {message['test_type']}"
                if "success" in message:
                    log_message += f" Success: {message['success']}"
                if "duration" in message:
                    log_message += f" Duration: {message['duration']:.3f}s"
                if "error" in message:
                    log_message += f" Error: {message['error']}"
                if "message" in message:
                    log_message += f" Message: {message['message']}"
                
                # Logging selon le niveau
                if message["level"] == "ERROR":
                    self.logger.error(log_message)
                elif message["level"] == "WARNING":
                    self.logger.warning(log_message)
                else:
                    self.logger.info(log_message)
                
            except Exception as e:
                self.logger.error(f"Erreur traitement message log: {e}")
    
    def cleanup(self) -> None:
        """Nettoyage à la fermeture"""
        self.log_queue.put(None)  # Signal d'arrêt
        self.async_thread.join()
        self.save_metrics()

# Instance globale du logger
detailed_logger = DetailedLogger()

def get_logger() -> DetailedLogger:
    """Retourne l'instance globale du logger"""
    return detailed_logger 
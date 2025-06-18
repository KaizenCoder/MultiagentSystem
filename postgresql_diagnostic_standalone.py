#!/usr/bin/env python3
"""
Agent de diagnostic PostgreSQL autonome - Version simplifiée
Fonctionne sans dépendances de l'orchestrateur NextGeneration
"""

import asyncio
import json
import sys
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class SimplePostgreSQLDiagnostic:
    """Agent de diagnostic PostgreSQL simplifié."""
    
    def __init__(self):
        self.diagnostic_results = {}
        self.recommendations = []
    
    async def run_diagnostic(self) -> Dict[str, Any]:
        """Lance un diagnostic complet de PostgreSQL."""
        print("🔍 Démarrage du diagnostic PostgreSQL...")
        
        # Tests de diagnostic
        diagnostic_tests = [
            ("Vérification de la disponibilité PostgreSQL", self.check_postgresql_availability),
            ("Vérification des connexions actives", self.check_active_connections),
            ("Vérification de l'espace disque", self.check_disk_space),
            ("Vérification des logs d'erreur", self.check_error_logs),
            ("Vérification de la configuration", self.check_configuration),
            ("Vérification des performances", self.check_performance_metrics),
        ]
        
        for test_name, test_func in diagnostic_tests:
            print(f"📋 {test_name}...")
            try:
                result = await test_func()
                self.diagnostic_results[test_name] = result
                print(f"✅ {test_name} - Terminé")
            except Exception as e:
                error_msg = f"❌ Erreur lors du test '{test_name}': {str(e)}"
                print(error_msg)
                self.diagnostic_results[test_name] = {"error": str(e)}
        
        # Génération des recommandations
        self.generate_recommendations()
        
        # Génération du rapport final
        return self.generate_report()
    
    async def execute_command(self, command: str) -> str:
        """Exécute une commande shell de manière sécurisée."""
        try:
            # Validation basique de sécurité
            allowed_commands = ["pg_isready", "docker", "psql"]
            cmd_parts = command.strip().split()
            if not cmd_parts or cmd_parts[0] not in allowed_commands:
                return f"Error: Command not allowed for security reasons. Command: {command}"
            
            # Exécution de la commande
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
            
            result = ""
            if stdout:
                result += f"STDOUT:\n{stdout.decode(errors='ignore')}"
            if stderr:
                result += f"STDERR:\n{stderr.decode(errors='ignore')}"
            
            if process.returncode != 0:
                return f"Command failed with exit code {process.returncode}:\n{result}"
            
            return f"Command executed successfully:\n{result}"
            
        except asyncio.TimeoutError:
            return "Error: Command execution timed out."
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    async def check_postgresql_availability(self) -> Dict[str, Any]:
        """Vérifie si PostgreSQL est disponible et répond."""
        # Test avec pg_isready
        pg_ready_result = await self.execute_command("pg_isready -h localhost -p 5432")
        
        # Test de connexion Docker si PostgreSQL est en conteneur
        docker_ps_result = await self.execute_command("docker ps --filter name=postgres --format 'table {{.Names}}\\t{{.Status}}'")
        
        return {
            "pg_isready": pg_ready_result,
            "docker_containers": docker_ps_result,
            "status": "available" if "accepting connections" in pg_ready_result else "unavailable"
        }
    
    async def check_active_connections(self) -> Dict[str, Any]:
        """Vérifie le nombre de connexions actives."""
        # Commande pour vérifier les connexions via Docker
        docker_exec_cmd = "docker exec postgres psql -U postgres -c \"SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';\""
        connections_result = await self.execute_command(docker_exec_cmd)
        
        # Vérification des connexions par base de données
        db_connections_cmd = "docker exec postgres psql -U postgres -c \"SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;\""
        db_connections_result = await self.execute_command(db_connections_cmd)
        
        return {
            "active_connections": connections_result,
            "connections_by_database": db_connections_result
        }
    
    async def check_disk_space(self) -> Dict[str, Any]:
        """Vérifie l'espace disque disponible."""
        # Vérification de l'espace disque du système
        disk_space_result = await self.execute_command("docker exec postgres df -h /var/lib/postgresql/data")
        
        # Taille des bases de données
        db_sizes_cmd = "docker exec postgres psql -U postgres -c \"SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database;\""
        db_sizes_result = await self.execute_command(db_sizes_cmd)
        
        return {
            "disk_space": disk_space_result,
            "database_sizes": db_sizes_result
        }
    
    async def check_error_logs(self) -> Dict[str, Any]:
        """Vérifie les logs d'erreur récents."""
        # Logs Docker du conteneur PostgreSQL
        docker_logs_result = await self.execute_command("docker logs postgres --tail 50")
        
        return {
            "recent_logs": docker_logs_result,
            "log_analysis": self.analyze_logs(docker_logs_result)
        }
    
    async def check_configuration(self) -> Dict[str, Any]:
        """Vérifie la configuration PostgreSQL."""
        # Paramètres de configuration importants
        config_cmd = "docker exec postgres psql -U postgres -c \"SELECT name, setting, unit FROM pg_settings WHERE name IN ('max_connections', 'shared_buffers', 'effective_cache_size', 'maintenance_work_mem', 'checkpoint_completion_target', 'wal_buffers', 'default_statistics_target');\""
        config_result = await self.execute_command(config_cmd)
        
        return {
            "configuration": config_result
        }
    
    async def check_performance_metrics(self) -> Dict[str, Any]:
        """Vérifie les métriques de performance."""
        # Statistiques des requêtes lentes
        slow_queries_cmd = "docker exec postgres psql -U postgres -c \"SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;\" 2>/dev/null || echo 'pg_stat_statements extension not available'"
        slow_queries_result = await self.execute_command(slow_queries_cmd)
        
        # Statistiques des tables
        table_stats_cmd = "docker exec postgres psql -U postgres -c \"SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_user_tables ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC LIMIT 10;\""
        table_stats_result = await self.execute_command(table_stats_cmd)
        
        return {
            "slow_queries": slow_queries_result,
            "table_statistics": table_stats_result
        }
    
    def analyze_logs(self, logs: str) -> List[str]:
        """Analyse les logs pour identifier les problèmes courants."""
        issues = []
        
        if "FATAL" in logs:
            issues.append("❌ Erreurs fatales détectées dans les logs")
        if "ERROR" in logs:
            issues.append("⚠️ Erreurs détectées dans les logs")
        if "connection limit exceeded" in logs.lower():
            issues.append("🔴 Limite de connexions dépassée")
        if "out of memory" in logs.lower():
            issues.append("🔴 Problème de mémoire insuffisante")
        if "disk full" in logs.lower():
            issues.append("🔴 Espace disque insuffisant")
        if "checkpoint" in logs.lower() and "slow" in logs.lower():
            issues.append("⚠️ Checkpoints lents détectés")
        
        if not issues:
            issues.append("✅ Aucun problème majeur détecté dans les logs")
        
        return issues
    
    def generate_recommendations(self) -> None:
        """Génère des recommandations basées sur les résultats du diagnostic."""
        print("💡 Génération des recommandations...")
        
        # Analyse des résultats pour générer des recommandations
        for test_name, result in self.diagnostic_results.items():
            if "disponibilité" in test_name and isinstance(result, dict):
                if result.get("status") == "unavailable":
                    self.recommendations.append({
                        "category": "Disponibilité",
                        "issue": "PostgreSQL indisponible",
                        "solution": "Redémarrer le service PostgreSQL avec: docker restart postgres"
                    })
            
            elif "connexions" in test_name:
                if "error" in str(result).lower():
                    self.recommendations.append({
                        "category": "Connexions",
                        "issue": "Problème de connexions",
                        "solution": "Vérifier la configuration max_connections et surveiller les connexions actives"
                    })
            
            elif "espace disque" in test_name:
                if "100%" in str(result) or "No space" in str(result):
                    self.recommendations.append({
                        "category": "Stockage",
                        "issue": "Espace disque insuffisant",
                        "solution": "Nettoyer les logs anciens et effectuer un VACUUM des tables"
                    })
            
            elif "logs d'erreur" in test_name:
                if isinstance(result, dict) and result.get("log_analysis"):
                    for issue in result["log_analysis"]:
                        if "❌" in issue or "🔴" in issue:
                            self.recommendations.append({
                                "category": "Logs",
                                "issue": issue,
                                "solution": "Analyser et corriger l'erreur identifiée"
                            })
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère le rapport final de diagnostic."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "diagnostic_summary": self.create_summary(),
            "detailed_results": self.diagnostic_results,
            "recommendations": self.recommendations,
            "action_items": self.generate_action_items()
        }
        
        return report
    
    def create_summary(self) -> Dict[str, Any]:
        """Crée un résumé du diagnostic."""
        summary = {
            "total_tests": len(self.diagnostic_results),
            "successful_tests": 0,
            "failed_tests": 0,
            "critical_issues": [],
            "warnings": []
        }
        
        for test_name, result in self.diagnostic_results.items():
            if isinstance(result, dict) and "error" in result:
                summary["failed_tests"] += 1
                summary["critical_issues"].append(f"❌ {test_name}: {result['error']}")
            else:
                summary["successful_tests"] += 1
                
                # Analyse des résultats pour identifier les problèmes
                if "unavailable" in str(result).lower():
                    summary["critical_issues"].append(f"🔴 {test_name}: Service indisponible")
                elif "error" in str(result).lower():
                    summary["warnings"].append(f"⚠️ {test_name}: Problème détecté")
        
        return summary
    
    def generate_action_items(self) -> List[str]:
        """Génère une liste d'actions recommandées."""
        actions = []
        
        # Analyse des résultats pour générer des recommandations
        for test_name, result in self.diagnostic_results.items():
            if "Vérification de la disponibilité" in test_name:
                if isinstance(result, dict) and result.get("status") == "unavailable":
                    actions.append("🔧 Redémarrer le service PostgreSQL")
                    actions.append("🔧 Vérifier la configuration réseau")
            
            elif "connexions actives" in test_name:
                if "active_connections" in str(result):
                    actions.append("📊 Surveiller le nombre de connexions actives")
            
            elif "espace disque" in test_name:
                if "100%" in str(result) or "No space" in str(result):
                    actions.append("💾 Nettoyer l'espace disque")
                    actions.append("💾 Archiver les anciens logs")
            
            elif "logs d'erreur" in test_name:
                if isinstance(result, dict) and result.get("log_analysis"):
                    for issue in result["log_analysis"]:
                        if "❌" in issue or "🔴" in issue:
                            actions.append(f"🔧 Résoudre: {issue}")
        
        if not actions:
            actions.append("✅ Aucune action immédiate requise")
        
        return actions
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """Affiche le rapport de diagnostic."""
        print("\n" + "="*60)
        print("📊 RAPPORT DE DIAGNOSTIC POSTGRESQL")
        print("="*60)
        
        summary = report["diagnostic_summary"]
        print(f"\n📋 RÉSUMÉ:")
        print(f"   Tests exécutés: {summary['total_tests']}")
        print(f"   Tests réussis: {summary['successful_tests']}")
        print(f"   Tests échoués: {summary['failed_tests']}")
        
        if summary["critical_issues"]:
            print(f"\n🚨 PROBLÈMES CRITIQUES:")
            for issue in summary["critical_issues"]:
                print(f"   {issue}")
        
        if summary["warnings"]:
            print(f"\n⚠️ AVERTISSEMENTS:")
            for warning in summary["warnings"]:
                print(f"   {warning}")
        
        print(f"\n🔧 ACTIONS RECOMMANDÉES:")
        for action in report["action_items"]:
            print(f"   {action}")
        
        if report["recommendations"]:
            print(f"\n💡 RECOMMANDATIONS:")
            for rec in report["recommendations"]:
                print(f"   📖 {rec['category']}: {rec['issue']}")
                print(f"      → {rec['solution']}")
        
        print("\n" + "="*60)

async def main():
    """Fonction principale pour exécuter le diagnostic."""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        output_json = True
    else:
        output_json = False
    
    agent = SimplePostgreSQLDiagnostic()
    
    try:
        report = await agent.run_diagnostic()
        
        if output_json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            agent.print_report(report)
            
            # Sauvegarder le rapport
            filename = f"postgresql_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Rapport sauvegardé dans {filename}")
    
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 
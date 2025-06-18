#!/usr/bin/env python3
"""
Agent de diagnostic PostgreSQL autonome utilisant l'orchestrateur NextGeneration.
Cet agent utilise les outils sécurisés pour diagnostiquer les problèmes PostgreSQL courants.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Import des outils de l'orchestrateur
from orchestrator.app.agents.tools import execute_shell_command, rag_code_search_tool
from orchestrator.app.security.logging import security_logger, setup_secure_logging


class PostgreSQLDiagnosticAgent:
    """Agent spécialisé dans le diagnostic des problèmes PostgreSQL."""
    
    def __init__(self):
        self.diagnostic_results = {}
        self.recommendations = []
        setup_secure_logging()
    
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
                security_logger.log_error(f"Diagnostic test failed: {test_name}", e)
        
        # Recherche de solutions dans la base de connaissances
        await self.search_solutions()
        
        # Génération du rapport final
        return self.generate_report()
    
    async def check_postgresql_availability(self) -> Dict[str, Any]:
        """Vérifie si PostgreSQL est disponible et répond."""
        # Test avec pg_isready
        pg_ready_result = await execute_shell_command("pg_isready -h localhost -p 5432")
        
        # Test de connexion Docker si PostgreSQL est en conteneur
        docker_ps_result = await execute_shell_command("docker ps --filter name=postgres --format 'table {{.Names}}\\t{{.Status}}'")
        
        return {
            "pg_isready": pg_ready_result,
            "docker_containers": docker_ps_result,
            "status": "available" if "accepting connections" in pg_ready_result else "unavailable"
        }
    
    async def check_active_connections(self) -> Dict[str, Any]:
        """Vérifie le nombre de connexions actives."""
        # Commande pour vérifier les connexions via Docker
        docker_exec_cmd = "docker exec postgres psql -U postgres -c \"SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';\""
        connections_result = await execute_shell_command(docker_exec_cmd)
        
        # Vérification des connexions par base de données
        db_connections_cmd = "docker exec postgres psql -U postgres -c \"SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;\""
        db_connections_result = await execute_shell_command(db_connections_cmd)
        
        return {
            "active_connections": connections_result,
            "connections_by_database": db_connections_result
        }
    
    async def check_disk_space(self) -> Dict[str, Any]:
        """Vérifie l'espace disque disponible."""
        # Vérification de l'espace disque du système
        disk_space_result = await execute_shell_command("docker exec postgres df -h /var/lib/postgresql/data")
        
        # Taille des bases de données
        db_sizes_cmd = "docker exec postgres psql -U postgres -c \"SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database;\""
        db_sizes_result = await execute_shell_command(db_sizes_cmd)
        
        return {
            "disk_space": disk_space_result,
            "database_sizes": db_sizes_result
        }
    
    async def check_error_logs(self) -> Dict[str, Any]:
        """Vérifie les logs d'erreur récents."""
        # Logs Docker du conteneur PostgreSQL
        docker_logs_result = await execute_shell_command("docker logs postgres --tail 50")
        
        return {
            "recent_logs": docker_logs_result,
            "log_analysis": self.analyze_logs(docker_logs_result)
        }
    
    async def check_configuration(self) -> Dict[str, Any]:
        """Vérifie la configuration PostgreSQL."""
        # Paramètres de configuration importants
        config_cmd = "docker exec postgres psql -U postgres -c \"SELECT name, setting, unit FROM pg_settings WHERE name IN ('max_connections', 'shared_buffers', 'effective_cache_size', 'maintenance_work_mem', 'checkpoint_completion_target', 'wal_buffers', 'default_statistics_target');\""
        config_result = await execute_shell_command(config_cmd)
        
        return {
            "configuration": config_result
        }
    
    async def check_performance_metrics(self) -> Dict[str, Any]:
        """Vérifie les métriques de performance."""
        # Statistiques des requêtes lentes
        slow_queries_cmd = "docker exec postgres psql -U postgres -c \"SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;\" 2>/dev/null || echo 'pg_stat_statements extension not available'"
        slow_queries_result = await execute_shell_command(slow_queries_cmd)
        
        # Statistiques des tables
        table_stats_cmd = "docker exec postgres psql -U postgres -c \"SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_user_tables ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC LIMIT 10;\""
        table_stats_result = await execute_shell_command(table_stats_cmd)
        
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
    
    async def search_solutions(self) -> None:
        """Recherche des solutions dans la base de connaissances."""
        print("🔍 Recherche de solutions dans la base de connaissances...")
        
        # Recherche de solutions pour les problèmes identifiés
        search_queries = [
            "PostgreSQL connection problems solutions",
            "PostgreSQL performance optimization",
            "PostgreSQL disk space issues",
            "PostgreSQL memory configuration",
            "PostgreSQL slow queries optimization"
        ]
        
        for query in search_queries:
            try:
                result = await rag_code_search_tool(query)
                if "Found relevant snippets" in result:
                    self.recommendations.append({
                        "query": query,
                        "solutions": result
                    })
            except Exception as e:
                security_logger.log_error(f"Knowledge base search failed for query: {query}", e)
    
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
                # Analyser le nombre de connexions
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
            print(f"\n💡 SOLUTIONS TROUVÉES:")
            for rec in report["recommendations"]:
                print(f"   📖 {rec['query']}")
        
        print("\n" + "="*60)


async def main():
    """Fonction principale pour exécuter le diagnostic."""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        output_json = True
    else:
        output_json = False
    
    agent = PostgreSQLDiagnosticAgent()
    
    try:
        report = await agent.run_diagnostic()
        
        if output_json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            agent.print_report(report)
            
            # Sauvegarder le rapport
            with open(f"postgresql_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Rapport sauvegardé dans postgresql_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {str(e)}")
        security_logger.log_error("Diagnostic agent failed", e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 
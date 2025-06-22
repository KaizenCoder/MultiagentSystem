"""
Script pour lancer l'équipe de maintenance sur le répertoire des agents
"""
from agent_MAINTENANCE_00_chef_equipe_coordinateur import AgentMaintenance00
from agent_MAINTENANCE_01_analyseur_structure import AgentMaintenance01
from agent_MAINTENANCE_02_evaluateur_utilite import AgentMaintenance02
from agent_MAINTENANCE_03_adaptateur_code import AgentMaintenance03
from agent_MAINTENANCE_04_testeur_anti_faux_agents import AgentMaintenance04
from agent_MAINTENANCE_05_documenteur_peer_reviewer import AgentMaintenance05
from agent_MAINTENANCE_06_validateur_final import AgentMaintenance06

class MaintenanceTeamRunner:
    def __init__(self):
    self.team = [
        AgentMaintenance00(),  # Chef d'équipe
        AgentMaintenance01(),  # Analyseur structure
        AgentMaintenance02(),  # Évaluateur utilité
        AgentMaintenance03(),  # Adaptateur code
        AgentMaintenance04(),  # Testeur anti-faux agents
        AgentMaintenance05(),  # Documenteur peer reviewer
        AgentMaintenance06()   # Validateur final
    ]
    
    def run_analysis(self, target_path):
    print("⚙️ Lancement de l'équipe de maintenance...")
    for agent in self.team:
        try:
            print(f"🔧 Exécution de {agent.__class__.__name__}...")
            agent.run_analysis(target_path)
            print(f"✅ {agent.__class__.__name__} terminé avec succès")
        except Exception as e:
            print(f"❌ Erreur dans {agent.__class__.__name__}: {str(e)}")
    print("🏁 Analyse de maintenance terminée")

if __name__ == "__main__":
    runner = MaintenanceTeamRunner()
    runner.run_analysis("./") 

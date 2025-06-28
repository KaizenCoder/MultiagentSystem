import pytest
import asyncio
from pathlib import Path
import sys
import os

# --- Configuration Robuste du Chemin d'Importation ---
try:
    # Ajustement pour pointer vers la racine du projet (nextgeneration/)
    project_root = Path(__file__).resolve().parents[0]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# --- Imports Post-Path-Correction ---
from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise

# Définir les agents cibles pour ce test spécifique
AGENTS_CIBLES = [
    "agents/agent_01_coordinateur_principal.py",
    "agents/agent_02_architecte_code_expert.py",
    "agents/agent_03_specialiste_configuration.py",
    "agents/agent_04_expert_securite_crypto.py",
]

@pytest.mark.asyncio
async def test_maintenance_workflow_on_core_agents():
    """
    Teste le workflow de maintenance complet sur un sous-ensemble d'agents principaux.
    Ce test suit les étapes suivantes :
    1. Instancie le chef d'équipe de maintenance.
    2. Lance une tâche de maintenance en spécifiant les agents cibles.
    3. Vérifie que le workflow se termine avec un statut de SUCCÈS.
    4. S'assure qu'un rapport a bien été généré.
    """
    print("--- Démarrage du test de maintenance sur les agents principaux ---")
    
    # 1. Instanciation du chef d'équipe
    chef_equipe = ChefEquipeCoordinateurEnterprise(
        # NOUVEAU: Fournir les arguments obligatoires
        target_path="agents",
        workspace_path="."
    )
    
    # NOUVEAU: Appeler startup() pour charger la configuration de l'équipe
    await chef_equipe.startup()

    # S'assurer que les agents cibles existent
    for agent_path in AGENTS_CIBLES:
        assert os.path.exists(agent_path), f"L'agent cible {agent_path} n'a pas été trouvé."
    
    # 2. Lancement du workflow de maintenance
    # La méthode 'lancer_workflow_maintenance' doit retourner un rapport ou un statut
    rapport_final = await chef_equipe.workflow_maintenance_complete(mission_config={"target_files": AGENTS_CIBLES})
    
    # NOUVEAU: Appeler shutdown() pour un nettoyage propre
    await chef_equipe.shutdown()

    # 3. Validation du résultat
    print("\n--- Validation du rapport final ---")
    assert rapport_final is not None, "Le workflow n'a retourné aucun rapport."
    print(f"Statut final du workflow : {rapport_final.get('statut_mission')}")
    
    assert rapport_final.get('statut_mission') == "SUCCÈS", \
        f"Le workflow de maintenance a échoué avec le statut : {rapport_final.get('statut_mission')}"

    # 4. Vérification de la génération du rapport
    assert 'rapport_path' in rapport_final, "Le chemin du rapport est manquant dans le résultat final."
    rapport_path = rapport_final['rapport_path']
    print(f"Chemin du rapport généré : {rapport_path}")
    assert os.path.exists(rapport_path), f"Le fichier de rapport {rapport_path} n'a pas été généré."
    
    print("--- Test de maintenance sur les agents principaux terminé avec SUCCÈS ---")

if __name__ == "__main__":
    asyncio.run(test_maintenance_workflow_on_core_agents()) 
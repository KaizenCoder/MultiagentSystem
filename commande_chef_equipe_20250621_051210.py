
# COMMANDE DIRECTE POUR LE CHEF D'ÉQUIPE
# Exécuter dans le répertoire: C:\Dev\nextgeneration\20250620_transformation_equipe_maintenance\agent_equipe_maintenance

import sys
sys.path.append(r"C:\Dev\nextgeneration\20250620_transformation_equipe_maintenance\agent_equipe_maintenance")

from agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateur

# Configuration pour agents experts
config = {
    "target_path": r"C:\Dev\nextgeneration\agent_factory_experts_team",
    "workspace_path": r"C:\Dev\nextgeneration",
    "safe_mode": True,
    "rapport_detaille": True
}

# Lancement
chef = ChefEquipeCoordinateur(**config)
resultats = chef.execute_task()
print("Maintenance terminée:", resultats)





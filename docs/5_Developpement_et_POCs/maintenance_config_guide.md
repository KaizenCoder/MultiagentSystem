
# Guide d'Intégration de la Configuration de Maintenance

Document généré par l'Agent 03 - Spécialiste Configuration le 2025-06-22 14:21:20.

## 1. Vue d'ensemble

La configuration de l'équipe de maintenance est désormais gérée de manière centralisée et statique pour améliorer la robustesse et éviter les dépendances circulaires au démarrage.

- **Schéma de configuration** : La structure est définie dans `core/config_models_agent/config_models_maintenance.py`.
- **Fichier de valeurs** : Les valeurs de configuration sont stockées dans `maintenance_config.json`, situé dans le répertoire `config/`.

## 2. Comment Accéder à la Configuration

Pour charger la configuration dans n'importe quel agent ou service, utilisez la fonction utilitaire `get_maintenance_config()`.

### Exemple d'utilisation

```python
from core.config_models_agent.config_models_maintenance import get_maintenance_config
from pydantic import ValidationError

try:
    config = get_maintenance_config()
    analyseur_config = config.agents.get("analyseur")
    if analyseur_config:
        print(f"Classe de l'analyseur : {analyseur_config.classe_agent}")
except FileNotFoundError as e:
    print(f"ERREUR : Le fichier de configuration est manquant. {e}")
except ValidationError as e:
    print(f"ERREUR : Le fichier de configuration est invalide. {e}")
```

## 3. Mise à jour de la Configuration

Pour modifier la composition de l'équipe, ré-exécutez la mission de l'Agent 03.

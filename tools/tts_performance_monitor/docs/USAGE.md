# Guide d'Utilisation - Monitor Phase3

## Configuration

### Fichier de configuration

Le fichier `config/config.json` contient tous les paramètres configurables.

### Variables d'environnement

- `NG_MONITOR_PHASE3_DEBUG`: Active le mode debug
- `NG_MONITOR_PHASE3_LOG_LEVEL`: Niveau de logging

## Utilisation en ligne de commande

```bash
# Utilisation de base
python tools/monitor_phase3/monitor_phase3.py

# Avec options
python tools/monitor_phase3/monitor_phase3.py --option valeur

# Mode debug
python tools/monitor_phase3/monitor_phase3.py --debug
```

## Utilisation programmatique

```python
from tools.monitor_phase3 import MonitorPhase3

# Instance de base
tool = MonitorPhase3()

# Configuration personnalisée
tool = MonitorPhase3(config_file="custom_config.json")

# Exécution
result = tool.execute()
```

## Exemples

### Exemple 1: Utilisation basique

```python
# Code d'exemple à adapter selon l'outil
```

### Exemple 2: Configuration avancée

```python
# Code d'exemple avancé à adapter
```

## Dépannage

### Problèmes courants

1. **Erreur de configuration**: Vérifier le fichier `config/config.json`
2. **Permissions**: Vérifier les droits d'accès aux fichiers
3. **Dépendances**: Vérifier l'installation avec `pip list`

### Logs

Les logs sont disponibles dans le système de logging NextGeneration.

```bash
# Consultation des logs
tail -f logs/monitor_phase3.log
```

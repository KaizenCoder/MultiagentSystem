# Guide d'Utilisation - Install Phase3 Dependencies

## Configuration

### Fichier de configuration

Le fichier `config/config.json` contient tous les paramètres configurables.

### Variables d'environnement

- `NG_INSTALL_PHASE3_DEPENDENCIES_DEBUG`: Active le mode debug
- `NG_INSTALL_PHASE3_DEPENDENCIES_LOG_LEVEL`: Niveau de logging

## Utilisation en ligne de commande

```bash
# Utilisation de base
python tools/install_phase3_dependencies/install_phase3_dependencies.py

# Avec options
python tools/install_phase3_dependencies/install_phase3_dependencies.py --option valeur

# Mode debug
python tools/install_phase3_dependencies/install_phase3_dependencies.py --debug
```

## Utilisation programmatique

```python
from tools.install_phase3_dependencies import InstallPhase3Dependencies

# Instance de base
tool = InstallPhase3Dependencies()

# Configuration personnalisée
tool = InstallPhase3Dependencies(config_file="custom_config.json")

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
tail -f logs/install_phase3_dependencies.log
```

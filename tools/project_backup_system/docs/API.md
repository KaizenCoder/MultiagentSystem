# API Reference - Zip Backup

## Classes principales

### ZipBackup

Classe principale de l'outil zip_backup.

#### Constructeur
```python
ZipBackup(config_file=None, debug=False)
```

**Paramètres:**
- `config_file` (str, optionnel) : Chemin vers le fichier de configuration
- `debug` (bool, optionnel) : Active le mode debug

#### Méthodes

##### execute()
Exécute l'outil avec la configuration actuelle.

```python
def execute() -> Dict[str, Any]:
    """
    Exécute l'outil
    
    Returns:
        Dict contenant les résultats de l'exécution
    """
```

##### validate_config()
Valide la configuration actuelle.

```python
def validate_config() -> bool:
    """
    Valide la configuration
    
    Returns:
        True si la configuration est valide
    """
```

## Exceptions

### ToolConfigurationError
Levée en cas de problème de configuration.

### ToolExecutionError
Levée en cas d'erreur d'exécution.

## Exemples d'utilisation

```python
from tools.zip_backup import ZipBackup

# Instance basique
tool = ZipBackup()

# Validation configuration
if tool.validate_config():
    result = tool.execute()
    print(result)
```

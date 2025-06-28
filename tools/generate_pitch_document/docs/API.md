# API Reference - Generate Pitch Document

## Classes principales

### GeneratePitchDocument

Classe principale de l'outil generate_pitch_document.

#### Constructeur
```python
GeneratePitchDocument(config_file=None, debug=False)
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
from tools.generate_pitch_document import GeneratePitchDocument

# Instance basique
tool = GeneratePitchDocument()

# Validation configuration
if tool.validate_config():
    result = tool.execute()
    print(result)
```

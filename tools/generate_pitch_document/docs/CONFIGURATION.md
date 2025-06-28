# Configuration - Generate Pitch Document

## Structure de configuration

Le fichier `config/config.json` utilise la structure suivante :

```json
{
  "tool_info": {
    "name": "generate_pitch_document",
    "version": "1.0.0",
    "enabled": true
  },
  "settings": {
    "debug_mode": false,
    "log_level": "INFO",
    "timeout": 30
  },
  "nextgeneration_integration": {
    "use_ng_logging": true,
    "use_ng_monitoring": true
  }
}
```

## Paramètres détaillés

### Section tool_info
- `name` : Nom de l'outil
- `version` : Version de l'outil
- `enabled` : Active/désactive l'outil

### Section settings
- `debug_mode` : Mode debug (true/false)
- `log_level` : Niveau de logging (DEBUG, INFO, WARNING, ERROR)
- `timeout` : Timeout en secondes

### Section nextgeneration_integration
- `use_ng_logging` : Utilise le système de logging NextGeneration
- `use_ng_monitoring` : Active le monitoring NextGeneration

## Variables d'environnement

Les variables d'environnement ont priorité sur la configuration fichier :

- `NG_GENERATE_PITCH_DOCUMENT_DEBUG=true`
- `NG_GENERATE_PITCH_DOCUMENT_LOG_LEVEL=DEBUG`
- `NG_GENERATE_PITCH_DOCUMENT_TIMEOUT=60`

## Configuration par environnement

### Développement
```json
{
  "settings": {
    "debug_mode": true,
    "log_level": "DEBUG",
    "timeout": 60
  }
}
```

### Production
```json
{
  "settings": {
    "debug_mode": false,
    "log_level": "INFO",
    "timeout": 30
  }
}
```

# 🔗 Excel VBA Tools Launcher - NextGeneration

**🎯 FONCTIONNALITÉ : Lanceur universel pour outils Excel/VBA importés d'Apex**

## 🔍 Que fait cet outil ?

**Cet outil lance et gère les outils Excel/VBA importés du framework Apex dans NextGeneration :**

### ✨ Fonctionnalités principales
- 🔧 Outil spécialisé adapté pour NextGeneration
- ⚙️ Configuration flexible et modulaire
- 📊 Intégration complète avec le monitoring NextGeneration
- 🔒 Sécurité et validation intégrées

## 📋 Prérequis

- Python 3.8+
- NextGeneration Core Framework
- Dépendances spécifiques (voir requirements.txt)

## 🚀 Installation

### Installation rapide
```bash
# Depuis le répertoire NextGeneration
cd tools/imported_tools_apex

# Installation des dépendances
pip install -r requirements.txt

# Test de fonctionnement
python imported_tools_apex.py --help
```

### Installation pour développement
```bash
# Installation en mode développement
pip install -e .

# Installation des dépendances de développement
pip install -r requirements-dev.txt
```

## 📖 Utilisation

### Utilisation en ligne de commande

```bash
# Utilisation basique
python tools/imported_tools_apex/imported_tools_apex.py

# Avec configuration personnalisée
python tools/imported_tools_apex/imported_tools_apex.py --config custom_config.json

# Mode debug
python tools/imported_tools_apex/imported_tools_apex.py --debug --verbose
```

### Utilisation programmatique

```python
from tools.imported_tools_apex import ImportedToolsApex

# Instance avec configuration par défaut
tool = ImportedToolsApex()

# Configuration personnalisée
tool = ImportedToolsApex(
    config_file="config/custom.json",
    debug=True
)

# Exécution
result = tool.execute()
print(f"Résultat: {result}")
```

## ⚙️ Configuration

### Fichier de configuration principal

Le fichier `config/config.json` contient tous les paramètres configurables :

```json
{
  "tool_info": {
    "name": "imported_tools_apex",
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

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `NG_IMPORTED_TOOLS_APEX_DEBUG` | Active le mode debug | `false` |
| `NG_IMPORTED_TOOLS_APEX_LOG_LEVEL` | Niveau de logging | `INFO` |
| `NG_IMPORTED_TOOLS_APEX_CONFIG` | Chemin configuration personnalisée | `config/config.json` |

## 🧪 Tests

### Tests unitaires
```bash
# Tests unitaires complets
python -m pytest tests/unit/test_imported_tools_apex.py -v

# Tests avec couverture
python -m pytest tests/unit/test_imported_tools_apex.py --cov=imported_tools_apex
```

### Tests d'intégration
```bash
# Tests d'intégration NextGeneration
python -m pytest tests/integration/test_imported_tools_apex_integration.py -v

# Tests de performance
python -m pytest tests/integration/test_imported_tools_apex_performance.py
```

### Tests manuels
```bash
# Test rapide de fonctionnement
python tools/imported_tools_apex/imported_tools_apex.py --test

# Validation configuration
python tools/imported_tools_apex/imported_tools_apex.py --validate-config
```

## 📊 Monitoring et Observabilité

L'outil est intégré avec le système de monitoring NextGeneration :

- **Logs** : Disponibles dans le système centralisé NextGeneration
- **Métriques** : Collectées automatiquement
- **Alertes** : Configurées selon les seuils NextGeneration

### Consultation des métriques
```bash
# Logs en temps réel
tail -f logs/imported_tools_apex.log

# Métriques de performance
curl http://localhost:9090/metrics | grep imported_tools_apex
```

## 🔧 Dépannage

### Problèmes courants

#### Erreur de configuration
```bash
# Validation de la configuration
python tools/imported_tools_apex/imported_tools_apex.py --validate-config

# Régénération configuration par défaut
python tools/imported_tools_apex/imported_tools_apex.py --reset-config
```

#### Problèmes de permissions
```bash
# Vérification des permissions
ls -la tools/imported_tools_apex/

# Correction des permissions (Linux/Mac)
chmod +x tools/imported_tools_apex/imported_tools_apex.py
```

#### Dépendances manquantes
```bash
# Vérification des dépendances
pip check

# Réinstallation propre
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Logs et diagnostics

```bash
# Logs détaillés
export NG_IMPORTED_TOOLS_APEX_LOG_LEVEL=DEBUG
python tools/imported_tools_apex/imported_tools_apex.py

# Mode diagnostic
python tools/imported_tools_apex/imported_tools_apex.py --diagnostic

# Rapport d'état
python tools/imported_tools_apex/imported_tools_apex.py --status
```

## 📚 Documentation

- [Guide d'utilisation détaillé](docs/USAGE.md)
- [Configuration avancée](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)
- [Guide de développement](docs/DEVELOPMENT.md)
- [FAQ](docs/FAQ.md)

## 🤝 Contribution

### Développement local
```bash
# Clone et setup
git clone <repo>
cd tools/imported_tools_apex

# Environnement de développement
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements-dev.txt
```

### Tests avant contribution
```bash
# Tests complets
make test

# Vérification qualité code
make lint
make format

# Tests de sécurité
make security-check
```

## 📄 Licence

Distribué sous licence NextGeneration. Voir `LICENSE` pour plus d'informations.

## 🔗 Liens utiles

- [Documentation NextGeneration](../docs/)
- [Issues et support](https://github.com/nextgeneration/issues)
- [Roadmap](https://github.com/nextgeneration/projects)

---

**Intégré avec ❤️ dans l'écosystème NextGeneration**

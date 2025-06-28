# Guide de Développement - Imported Tools Apex

## Architecture

L'outil imported_tools_apex suit l'architecture modulaire NextGeneration.

## Structure du code

```
tools/imported_tools_apex/
├── imported_tools_apex.py          # Module principal
├── __init__.py             # Init package
├── config/
│   └── config.json        # Configuration
├── docs/                  # Documentation
├── tests/                 # Tests
└── templates/            # Templates
```

## Standards de développement

### Code Style
- PEP 8 pour Python
- Type hints obligatoires
- Docstrings pour toutes les fonctions publiques

### Tests
- Tests unitaires avec pytest
- Couverture minimale de 80%
- Tests d'intégration obligatoires

### Documentation
- README.md à jour
- Documentation API complète
- Exemples d'utilisation

## Workflow de développement

1. Fork du repository
2. Création d'une branche feature
3. Développement avec tests
4. Pull request avec review
5. Merge après validation

## Debug et profiling

```python
# Mode debug
export NG_IMPORTED_TOOLS_APEX_DEBUG=true
python tools/imported_tools_apex/imported_tools_apex.py

# Profiling
python -m cProfile tools/imported_tools_apex/imported_tools_apex.py
```

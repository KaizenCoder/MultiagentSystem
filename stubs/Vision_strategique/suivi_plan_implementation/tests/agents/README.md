# Tests des Agents

Ce répertoire contient les tests unitaires et d'intégration pour les différents agents du système.

## Structure des Tests

1. **Tests de Base**
   - `test_agent_00_coordination.py` - Tests du coordinateur
   - `test_agent_05_migration_final.py` - Tests de migration
   - `test_agent_109_factory.py` - Tests de la factory
   - `test_agent_111_audit.py` - Tests d'audit
   - `test_agent_MONITORING_25_validation_exhaustive.py` - Tests de monitoring

## Exécution des Tests

Pour exécuter les tests :
```bash
pytest tests/agents/
```

## Conventions de Nommage

- `test_agent_[NUMERO]_[FONCTION].py` pour les tests d'agents spécifiques
- `test_agent_[NOM]_[TYPE]_[DETAILS].py` pour les tests spécialisés 
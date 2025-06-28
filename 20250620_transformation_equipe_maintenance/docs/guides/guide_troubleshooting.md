# 🔍 Guide de Troubleshooting - Agents NextGeneration

## ❌ Erreurs Fréquentes

### 1. ImportError: No module named 'agent_X'
**Cause**: Module non trouvé
**Solution**:
```bash
# Vérifier le répertoire
ls -la agent_*.py

# Vérifier PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Réinstaller
pip install -r requirements.txt
```

### 2. AttributeError: 'Agent' object has no attribute 'startup'
**Cause**: Interface agent incompatible
**Solution**: Vérifier que l'agent implémente les bonnes méthodes

### 3. FileNotFoundError: Target path not found
**Cause**: Chemin cible incorrect
**Solution**:
```bash
# Créer les répertoires
mkdir -p ../agent_factory_implementation/agents
mkdir -p reports
```

## 🔧 Commandes de Diagnostic

### Test des Agents
```bash
# Test complet
python agent_0_chef_equipe_coordinateur.py --test

# Test individuel
python agent_1_analyseur_structure.py --test
```

### Vérification des Chemins
```bash
# Vérifier la configuration
python -c "from pathlib import Path; print(Path('../agent_factory_implementation/agents').exists())"
```

### Logs Détaillés
```bash
# Mode verbose
python agent_0_chef_equipe_coordinateur.py --verbose

# Logs en temps réel
tail -f logs/*.log
```

## 📞 Support

### Informations à Fournir
1. Version Python: `python --version`
2. Système: `uname -a` (Linux/Mac) ou `systeminfo` (Windows)
3. Logs d'erreur complets
4. Commande exacte exécutée

### Contacts
- Documentation: `docs/`
- Issues: Repository GitHub
- Logs: `logs/troubleshooting_*.log`

---
*Créé par Agent 5 Documenteur - 2025-06-20*

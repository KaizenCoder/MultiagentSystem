# 🔧 Guide de Maintenance - Équipe Agents

## 🎯 Maintenance Préventive

### Vérifications Quotidiennes
- [ ] État des agents (health check)
- [ ] Logs d'erreurs
- [ ] Espace disque disponible

### Vérifications Hebdomadaires
- [ ] Performance des agents
- [ ] Mise à jour des dépendances
- [ ] Nettoyage des logs anciens

## 🚨 Résolution de Problèmes

### Problèmes Courants

#### Agent ne démarre pas
```bash
# Vérifier les dépendances
pip check

# Vérifier les permissions
ls -la agent_*.py

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

#### Erreurs d'import
```bash
# Vérifier PYTHONPATH
echo $PYTHONPATH

# Ajouter le répertoire courant
export PYTHONPATH=$PYTHONPATH:.
```

### Logs et Diagnostic
- **Logs**: `./logs/`
- **Rapports**: `./reports/`
- **Debug**: Utiliser `--debug` ou `NEXTGEN_DEBUG=true`

## 🔄 Maintenance Automatisée

### Scripts de Maintenance
```bash
# Maintenance complète
python agent_0_chef_equipe_coordinateur.py --maintenance

# Nettoyage
python maintenance_scripts/cleanup.py

# Sauvegarde
python maintenance_scripts/backup.py
```

---
*Créé par Agent 5 Documenteur - 2025-06-20*

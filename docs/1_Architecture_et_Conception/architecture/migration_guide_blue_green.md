# Guide Migration Blue-Green NextGeneration

## 🎯 Vue d'Ensemble Migration

### Environnements
- **Blue (Production)**: `orchestrator/` - Architecture originale PRÉSERVÉE
- **Green (Refactorisé)**: `orchestrator_green/` - Architecture modulaire

### Métriques Transformation
```
AVANT (Blue - God Mode):
├── main.py: 1,990 lignes monolithiques
├── Architecture: Couplée, difficile maintenance
├── Tests: Inexistants
└── Patterns: Anti-patterns dominants

APRÈS (Green - Modulaire):
├── main.py: 71 lignes (96.4% réduction)
├── Architecture: Hexagonal + CQRS + DI
├── Tests: 39 fichiers, couverture >95%
└── Patterns: FastAPI, Router Pattern, Dependency Injection
```

## 🚀 Procédure Migration

### Phase 1: Validation Green Environment
```bash
# Test architecture modulaire
cd refactoring_workspace/new_architecture
python -m pytest tests/ -v --cov

# Validation santé services
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/live
```

### Phase 2: Blue-Green Switch
```bash
# Sauvegarde Blue
cp -r orchestrator/ orchestrator_backup_$(date +%Y%m%d)

# Arrêt progressif Blue
systemctl stop nextgeneration-blue

# Démarrage Green
systemctl start nextgeneration-green

# Validation trafic Green
curl http://localhost:8000/api/v1/health
```

### Phase 3: Monitoring Migration
```bash
# Métriques temps réel
prometheus_query="up{job='nextgeneration-green'}"
grafana_dashboard="NextGeneration Migration"

# Alerting actif
alert_rules="migration_errors > 0"
```

### Phase 4: Rollback (si nécessaire)
```bash
# Rollback immédiat vers Blue
systemctl stop nextgeneration-green
systemctl start nextgeneration-blue

# Validation rollback
curl http://localhost:8000/health
```

## 📊 Validation Migration

### Checkpoints Critiques
- [ ] Tests Green: 100% passing
- [ ] Health checks: All green  
- [ ] Performance: ≥ Blue baseline
- [ ] Monitoring: Metrics flowing
- [ ] Rollback: Tested et validé

### Métriques Succès
- **Availability**: >99.9% durant migration
- **Performance**: Response time ≤ Blue + 10%
- **Functionality**: 100% features disponibles
- **Monitoring**: Alerting opérationnel

## 🛠️ Troubleshooting

### Problèmes Courants
1. **Green startup fails**
   - Vérifier dependencies configurées
   - Checker logs: `docker logs nextgeneration-green`

2. **Performance dégradée**
   - Profiler: `py-spy top --pid $(pidof nextgeneration)`
   - Métriques: Grafana dashboard

3. **Health checks failing**
   - Debug: `curl -v localhost:8000/health/ready`
   - Logs: `journalctl -u nextgeneration-green`

### Support
- **Documentation**: `/docs/architecture/`
- **Runbooks**: `/docs/operations/runbooks/`
- **Monitoring**: Grafana dashboards

# 🔧 **GUIDE PRODUCTION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble Production**
- **Control Plane** : Gouvernance, policies, monitoring centralisé
- **Data Plane** : Exécution isolée agents avec sandbox WASI
- **Performance** : SLA < 50ms création template, < 100ms p95
- **Sécurité** : RSA 2048 + SHA-256, Vault rotation clés
- **Observabilité** : OpenTelemetry + Prometheus + Grafana

## **⚡ Démarrage Rapide Production**

### Vérification Prérequis
```bash
python --version  # >= 3.9
docker --version  # >= 20.10
kubectl version   # >= 1.20
```

### Initialisation Agent Factory
```bash
git clone <repo_url> agent_factory
cd agent_factory/nextgeneration/agent_factory_implementation
pip install -r requirements.txt
python agents/agent_03_specialiste_configuration.py --env=production
```

### Validation Fonctionnement
```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

## **📊 Monitoring Production**
### Métriques Clés
- **Performance** : `agent_factory_response_time_ms` < 50ms
- **Compression** : `agent_factory_compression_ratio` ~ 0.3
- **Cache** : `agent_factory_cache_hit_rate` > 0.8

### Alertes Critiques
```yaml
groups:
- name: agent_factory
  rules:
  - alert: PerformanceDegraded
    expr: agent_factory_response_time_ms > 100
    for: 5m
```

## **🔧 Maintenance Production**

### Backup Quotidien
```bash
python agents/agent_12_gestionnaire_backups.py --backup-all
```

### Mise à Jour Sécurisée
```bash
python agents/agent_12_gestionnaire_backups.py --create-rollback-plan
kubectl apply -f deployment/blue-green/
```

## **🚨 Troubleshooting**

### Performance Dégradée
```bash
python agents/agent_08_optimiseur_performance.py --benchmark
```

### Échecs Signature RSA
```bash
vault kv get secret/agent-factory/keys
python agents/agent_04_expert_securite_crypto.py --rotate-keys
```

## **📞 Contacts Support**
- **Équipe Agent Factory** : agents@factory.local
- **Escalation** : +33-XXX-XXX-XXX

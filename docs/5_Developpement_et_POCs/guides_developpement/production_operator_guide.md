# 🔧 **GUIDE PRODUCTION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble Production**

### **Architecture Production**
- **Control Plane** : Gouvernance, policies, monitoring centralisé
- **Data Plane** : Exécution isolée agents avec sandbox WASI
- **Performance** : SLA < 50ms création template, < 100ms p95
- **Sécurité** : RSA 2048 + SHA-256, Vault rotation clés
- **Observabilité** : OpenTelemetry + Prometheus + Grafana

### **Agents Production (Sprint 4)**
1. **Agent 08 - Optimiseur Performance** : ThreadPool adaptatif + compression
2. **Agent 09 - Control/Data Plane** : Architecture séparée sécurisée
3. **Agent 12 - Gestionnaire Backups** : Versioning + rollback
4. **Agent 06 - Monitoring Avancé** : Observabilité distribuée

---

## **⚡ Démarrage Rapide Production**

### **1. Vérification Prérequis**
```bash
# Vérifier versions
python --version  # >= 3.9
docker --version  # >= 20.10
kubectl version   # >= 1.20

# Vérifier ressources
free -h           # Mémoire >= 8GB
df -h             # Disque >= 50GB
nproc             # CPU >= 4 cores
```

### **2. Initialisation Agent Factory**
```bash
# Clone repository
git clone <repo_url> agent_factory
cd agent_factory/nextgeneration/agent_factory_implementation

# Installation dépendances
pip install -r requirements.txt

# Initialisation configuration
python agents/agent_03_specialiste_configuration.py --env=production

# Démarrage agents Sprint 4
python agents/agent_08_optimiseur_performance.py
python agents/agent_12_gestionnaire_backups.py
```

### **3. Validation Fonctionnement**
```bash
# Health check
curl http://localhost:8000/health

# Métriques Prometheus
curl http://localhost:8000/metrics

# Création test template
curl -X POST http://localhost:8000/factory/create \
  -H "Content-Type: application/json" \
  -d '{"id":"test","name":"Test Template"}'
```

---

## **📊 Monitoring Production**

### **Métriques Clés**
- **Performance** : `agent_factory_response_time_ms` < 50ms
- **Compression** : `agent_factory_compression_ratio` ~ 0.3
- **Cache** : `agent_factory_cache_hit_rate` > 0.8
- **CPU** : `agent_factory_cpu_usage` < 80%
- **Mémoire** : `agent_factory_memory_usage` < 70%

### **Alertes Critiques**
```yaml
# Prometheus alerts
groups:
- name: agent_factory
  rules:
  - alert: PerformanceDegraded
    expr: agent_factory_response_time_ms > 100
    for: 5m
  - alert: CacheHitRateLow  
    expr: agent_factory_cache_hit_rate < 0.5
    for: 10m
```

### **Dashboard Grafana**
- URL : `http://grafana:3000/d/agent-factory`
- Panels : Performance, Compression, Cache, Resources
- Refresh : 30s auto-refresh

---

## **🔧 Maintenance Production**

### **Backup Quotidien**
```bash
# Backup automatique (Agent 12)
python agents/agent_12_gestionnaire_backups.py --backup-all

# Vérification backups
ls -la backups/production/$(date +%Y%m%d)/
```

### **Mise à Jour Sécurisée**
```bash
# 1. Backup pré-mise à jour
python agents/agent_12_gestionnaire_backups.py --create-rollback-plan

# 2. Déploiement blue-green
kubectl apply -f deployment/blue-green/

# 3. Validation post-déploiement
./scripts/validate_deployment.sh
```

### **Nettoyage Périodique**
```bash
# Nettoyage logs (> 30 jours)
find logs/ -name "*.log" -mtime +30 -delete

# Nettoyage backups anciens
python agents/agent_12_gestionnaire_backups.py --cleanup

# Nettoyage cache templates
python agents/agent_08_optimiseur_performance.py --cache-cleanup
```

---

## **🚨 Troubleshooting**

### **Problèmes Courants**

#### **Performance Dégradée**
```bash
# Diagnostic performance
python agents/agent_08_optimiseur_performance.py --benchmark

# Optimisation ThreadPool
# Ajuster CPU multiplier dans configuration

# Vérification compression
# Analyser ratio compression templates
```

#### **Échecs Signature RSA**
```bash
# Vérification clés Vault
vault kv get secret/agent-factory/keys

# Rotation manuelle clés
python agents/agent_04_expert_securite_crypto.py --rotate-keys

# Validation signature
python agents/agent_04_expert_securite_crypto.py --validate-all
```

#### **Control/Data Plane Issues**
```bash
# Status planes
python agents/agent_09_specialiste_planes.py --status

# Diagnostic sandbox WASI
python agents/agent_09_specialiste_planes.py --sandbox-test

# Vérification isolation
ps aux | grep wasi
```

### **Logs Importants**
- **Performance** : `logs/agent_08_performance_optimizer.log`
- **Sécurité** : `logs/agent_04_security_crypto.log`
- **Backup** : `logs/agent_12_backup_manager.log`
- **Monitoring** : `logs/agent_06_monitoring.log`

---

## **📞 Contacts Support**

### **Équipe Agent Factory**
- **Agent 01 (Coordinateur)** : Orchestration générale
- **Agent 16 (Reviewer Senior)** : Validation architecture  
- **Agent 17 (Reviewer Technique)** : Validation implémentation

### **Escalation Procédure**
1. **Niveau 1** : Logs + diagnostics automatiques
2. **Niveau 2** : Rollback plan Agent 12
3. **Niveau 3** : Contact équipe développement
4. **Niveau 4** : Incident critique - réveil équipe

---

## **📋 Checklist Maintenance**

### **Quotidien**
- [ ] Vérifier métriques performance
- [ ] Contrôler logs erreurs
- [ ] Valider backups automatiques
- [ ] Monitoring dashboard

### **Hebdomadaire**  
- [ ] Nettoyage logs anciens
- [ ] Test procédures rollback
- [ ] Mise à jour dépendances
- [ ] Audit sécurité

### **Mensuel**
- [ ] Review configuration production
- [ ] Optimisation performance
- [ ] Test disaster recovery
- [ ] Formation équipe ops

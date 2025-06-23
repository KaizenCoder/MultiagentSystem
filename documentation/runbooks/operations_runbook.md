# 📖 **RUNBOOK OPÉRATIONS - AGENT FACTORY PATTERN**

## **🚨 Procédures d'Urgence**

### **Incident Performance Critique**
**Symptômes :** Response time > 500ms, SLA violations
**Impact :** Service dégradé utilisateurs

**Actions Immédiates :**
1. **Diagnostic rapide**
   ```bash
   # Vérifier métriques actuelles
   curl -s http://localhost:8000/metrics | grep response_time
   
   # Status agents critiques
   python agents/agent_08_optimiseur_performance.py --status
   python agents/agent_09_specialiste_planes.py --status
   ```

2. **Auto-scaling ThreadPool**
   ```bash
   # Forcer scale-up ThreadPool
   python agents/agent_08_optimiseur_performance.py --scale-up --workers=16
   ```

3. **Cache flush si nécessaire**
   ```bash
   # Reset cache templates
   python agents/agent_08_optimiseur_performance.py --cache-flush
   ```

4. **Rollback si échec**
   ```bash
   # Rollback dernière version stable
   python agents/agent_12_gestionnaire_backups.py --rollback --version=stable
   ```

**Escalation :** Si performance non rétablie en 10 minutes

---

### **Échec Sécurité Critique**
**Symptômes :** Signature RSA failures, Vault inaccessible
**Impact :** Templates non signés, sécurité compromise

**Actions Immédiates :**
1. **Isolation sécurité**
   ```bash
   # Activer mode sécurisé
   python agents/agent_04_expert_securite_crypto.py --secure-mode
   ```

2. **Diagnostic Vault**
   ```bash
   # Status Vault
   vault status
   
   # Test rotation clés
   python agents/agent_04_expert_securite_crypto.py --test-rotation
   ```

3. **Backup clés critiques**
   ```bash
   # Backup clés urgence
   python agents/agent_12_gestionnaire_backups.py --backup-security
   ```

**Escalation :** Immédiate équipe sécurité

---

### **Panne Control/Data Plane**
**Symptômes :** Sandbox WASI offline, isolation compromise
**Impact :** Exécution agents non sécurisée

**Actions Immédiates :**
1. **Status planes**
   ```bash
   # Diagnostic complet planes
   python agents/agent_09_specialiste_planes.py --diagnostic-full
   ```

2. **Restart sandbox WASI**
   ```bash
   # Redémarrage sandbox
   python agents/agent_09_specialiste_planes.py --restart-sandbox
   ```

3. **Validation isolation**
   ```bash
   # Test isolation
   python agents/agent_09_specialiste_planes.py --test-isolation
   ```

---

## **⚙️ Procédures Maintenance**

### **Mise à Jour Production**
**Fenêtre :** Dimanche 02:00-04:00 UTC  
**Durée estimée :** 30 minutes

**Pré-requis :**
- [ ] Backup complet validé
- [ ] Plan rollback préparé  
- [ ] Équipe on-call disponible
- [ ] Tests staging validés

**Procédure :**
1. **Préparation**
   ```bash
   # Backup pré-maintenance
   python agents/agent_12_gestionnaire_backups.py --backup-all --type=pre-maintenance
   
   # Plan rollback
   python agents/agent_12_gestionnaire_backups.py --create-rollback-plan --version=current
   ```

2. **Arrêt contrôlé**
   ```bash
   # Drain traffic
   kubectl patch deployment agent-factory -p '{"spec":{"replicas":0}}'
   
   # Attendre drain complet (2 minutes max)
   kubectl wait --for=condition=available=false deployment/agent-factory --timeout=120s
   ```

3. **Déploiement**
   ```bash
   # Blue-green deployment
   kubectl apply -f deployment/blue-green/green/
   
   # Validation green environment
   ./scripts/validate_green_deployment.sh
   ```

4. **Validation**
   ```bash
   # Switch traffic vers green
   kubectl patch service agent-factory -p '{"spec":{"selector":{"version":"green"}}}'
   
   # Validation fonctionnelle
   ./scripts/post_deployment_tests.sh
   ```

5. **Cleanup**
   ```bash
   # Suppression blue si succès
   kubectl delete -f deployment/blue-green/blue/
   ```

**Rollback si échec :**
```bash
# Rollback immédiat
python agents/agent_12_gestionnaire_backups.py --execute-rollback --plan=latest
```

---

### **Rotation Certificats**
**Fréquence :** Mensuelle automatique  
**Validation :** Hebdomadaire

**Procédure automatique :**
```bash
# Rotation automatique Vault
python agents/agent_04_expert_securite_crypto.py --auto-rotate

# Validation rotation
python agents/agent_04_expert_securite_crypto.py --validate-rotation
```

**Procédure manuelle si échec :**
```bash
# Génération nouveaux certificats
python agents/agent_04_expert_securite_crypto.py --generate-certificates

# Déploiement certificats
python agents/agent_04_expert_securite_crypto.py --deploy-certificates

# Test signature
python agents/agent_04_expert_securite_crypto.py --test-signature
```

---

### **Nettoyage Mensuel**
**Fréquence :** Premier dimanche du mois  
**Durée :** 1 heure

**Checklist :**
- [ ] Cleanup logs > 30 jours
- [ ] Cleanup backups selon rétention
- [ ] Cleanup cache templates
- [ ] Cleanup métriques anciennes
- [ ] Validation espace disque

**Commandes :**
```bash
# Logs cleanup
find logs/ -name "*.log" -mtime +30 -delete

# Backups cleanup
python agents/agent_12_gestionnaire_backups.py --cleanup

# Cache cleanup  
python agents/agent_08_optimiseur_performance.py --cache-cleanup

# Métriques cleanup
curl -X DELETE http://prometheus:9090/api/v1/admin/tsdb/delete_series?match[]={__name__=~"agent_factory.*",job="agent-factory"}
```

---

## **📊 Monitoring & Alertes**

### **Métriques Critiques**
| Métrique | Seuil Warning | Seuil Critical | Action |
|----------|---------------|----------------|--------|
| Response Time | > 100ms | > 200ms | Scale ThreadPool |
| Cache Hit Rate | < 70% | < 50% | Cache rebuild |
| CPU Usage | > 80% | > 90% | Scale horizontalement |
| Memory Usage | > 80% | > 90% | Restart + investigation |
| Backup Success | < 95% | < 90% | Vérification système backup |

### **Dashboards Grafana**
- **Overview** : `http://grafana:3000/d/agent-factory-overview`
- **Performance** : `http://grafana:3000/d/agent-factory-performance`  
- **Security** : `http://grafana:3000/d/agent-factory-security`
- **Infrastructure** : `http://grafana:3000/d/agent-factory-infra`

### **Alertes Slack**
- Canal : `#agent-factory-alerts`
- Critical : Mention @here
- Warning : Notification normale

---

## **🔍 Troubleshooting Guide**

### **FAQ Opérations**

**Q: Comment vérifier si le système est healthy ?**
```bash
# Health check complet
curl http://localhost:8000/health

# Status détaillé agents
python agents/agent_01_coordinateur_principal.py --status-all
```

**Q: Performance dégradée, que faire ?**
1. Vérifier métriques Grafana
2. Analyser logs agents performance
3. Tester benchmark : `python agents/agent_08_optimiseur_performance.py --benchmark`
4. Scale ThreadPool si nécessaire

**Q: Comment créer un backup d'urgence ?**
```bash
# Backup complet immédiat
python agents/agent_12_gestionnaire_backups.py --emergency-backup

# Validation backup
python agents/agent_12_gestionnaire_backups.py --validate-backup --backup-id=<id>
```

**Q: Comment effectuer un rollback ?**
```bash
# Lister plans rollback disponibles
python agents/agent_12_gestionnaire_backups.py --list-rollback-plans

# Exécuter rollback
python agents/agent_12_gestionnaire_backups.py --execute-rollback --plan=<plan_id>
```

---

## **📞 Contacts & Escalation**

### **Niveaux Support**
1. **L1 - Opérateur** : Procédures runbook, monitoring
2. **L2 - Technique** : Diagnostic avancé, configuration
3. **L3 - Développement** : Code, architecture, bugs
4. **L4 - Architecte** : Décisions critiques, refactoring

### **Contacts d'Urgence**
- **On-call primary** : +33-XXX-XXX-XXX
- **On-call secondary** : +33-XXX-XXX-XXX  
- **Manager technique** : +33-XXX-XXX-XXX
- **Architecte système** : +33-XXX-XXX-XXX

### **Canaux Communication**
- **Slack urgent** : `#agent-factory-incidents`
- **Email escalation** : `agent-factory-oncall@company.com`
- **PagerDuty** : Service "Agent Factory Production"

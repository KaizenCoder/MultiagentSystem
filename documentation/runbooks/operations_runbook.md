# 📖 **RUNBOOK OPÉRATIONS - AGENT FACTORY PATTERN**

## **🚨 Procédures d'Urgence**

### Incident Performance Critique
   ```bash
   curl -s http://localhost:8000/metrics | grep response_time
   python agents/agent_08_optimiseur_performance.py --scale-up --workers=16
   python agents/agent_12_gestionnaire_backups.py --rollback --version=stable
   ```

### Échec Sécurité Critique
   ```bash
   python agents/agent_04_expert_securite_crypto.py --secure-mode
   vault status
   python agents/agent_12_gestionnaire_backups.py --backup-security
   ```

## **⚙️ Procédures Maintenance**

### Mise à Jour Production
   ```bash
   python agents/agent_12_gestionnaire_backups.py --backup-all --type=pre-maintenance
   kubectl apply -f deployment/blue-green/green/
   ./scripts/validate_green_deployment.sh
   ```

### Rotation Certificats
   ```bash
python agents/agent_04_expert_securite_crypto.py --auto-rotate
python agents/agent_04_expert_securite_crypto.py --validate-rotation
```

## **📊 Monitoring & Alertes**

| Métrique | Seuil Warning | Seuil Critical | Action |
|----------|---------------|----------------|--------|
| Response Time | > 100ms | > 200ms | Scale ThreadPool |
| Cache Hit Rate | < 70% | < 50% | Cache rebuild |
| CPU Usage | > 80% | > 90% | Scale horizontalement |

## **🔍 Troubleshooting Guide**

### FAQ Opérations
**Q: Comment vérifier si le système est healthy ?**
```bash
curl http://localhost:8000/health
python agents/agent_01_coordinateur_principal.py --status-all
```

**Q: Comment créer un backup d'urgence ?**
```bash
python agents/agent_12_gestionnaire_backups.py --emergency-backup
```

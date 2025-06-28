# Runbook Incidents NextGeneration

## 🚨 Procédures d'Urgence

### Application Down
1. **Diagnostic**
   ```bash
   kubectl get pods -n nextgeneration
   kubectl describe pod nextgeneration-xxx
   kubectl logs nextgeneration-xxx --tail=100
   ```

2. **Actions**
   - Vérifier health checks: `/health/live`
   - Consulter métriques Grafana
   - Redémarrer si nécessaire: `kubectl rollout restart deployment/nextgeneration`

### Performance Dégradée
1. **Métriques clés**
   - Response time P95 > 500ms
   - Error rate > 5%
   - Memory usage > 80%

2. **Actions**
   - Profiling: `kubectl exec -it pod -- py-spy top`
   - Scaling: `kubectl scale deployment nextgeneration --replicas=5`
   - Investigation logs

### Base de Données
1. **Connexions saturées**
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   SELECT * FROM pg_stat_activity WHERE state = 'active';
   ```

2. **Actions**
   - Redémarrer pgBouncer
   - Analyser requêtes lentes
   - Optimiser index si nécessaire

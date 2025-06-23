# Guide Déploiement NextGeneration

## 🚀 Déploiement Production

### 1. Prérequis
- Docker 20.10+
- Kubernetes 1.21+
- Helm 3.0+

### 2. Configuration
```bash
# Variables environnement
export NEXTGEN_ENV=production
export DB_HOST=postgres.internal
export REDIS_HOST=redis.internal

# Secrets
kubectl create secret generic nextgen-secrets --from-env-file=.env.prod
```

### 3. Déploiement
```bash
# Helm chart
helm upgrade --install nextgeneration ./k8s/helm/orchestrator \
  --namespace nextgeneration \
  --values values.prod.yaml

# Validation
kubectl get pods -n nextgeneration
kubectl logs -f deployment/nextgeneration-orchestrator
```

## 🏥 Health Checks

### Endpoints
- `/health/live` - Liveness probe
- `/health/ready` - Readiness probe  
- `/health/startup` - Startup probe

### Monitoring
- Prometheus: `:9090/targets`
- Grafana: `:3000/dashboards`
- AlertManager: `:9093/alerts`

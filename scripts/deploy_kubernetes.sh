#!/bin/bash

# Kubernetes Deployment Script - NextGeneration Orchestrator
# IA-2 Architecture & Production - Sprint 1.3
# 
# This script deploys the orchestrator to Kubernetes with advanced features:
# - Helm chart deployment
# - Auto-scaling configuration  
# - Monitoring stack
# - Security hardening
# - Health checks validation

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HELM_CHART_PATH="$PROJECT_ROOT/k8s/helm/orchestrator"

# Default values
ENVIRONMENT="${ENVIRONMENT:-production}"
NAMESPACE="${NAMESPACE:-orchestrator-$ENVIRONMENT}"
RELEASE_NAME="${RELEASE_NAME:-orchestrator}"
DOMAIN="${DOMAIN:-orchestrator.nextgeneration.com}"
TIMEOUT="${TIMEOUT:-600s}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Error handler
error_exit() {
    log_error "$1"
    exit 1
}

# Help function
show_help() {
    cat << EOF
Kubernetes Deployment Script for NextGeneration Orchestrator

Usage: $0 [OPTIONS]

OPTIONS:
    -e, --environment    Environment (production, staging, development) [default: production]
    -n, --namespace      Kubernetes namespace [default: orchestrator-ENVIRONMENT]
    -r, --release        Helm release name [default: orchestrator]
    -d, --domain         Application domain [default: orchestrator.nextgeneration.com]
    -t, --timeout        Deployment timeout [default: 600s]
    --dry-run           Show what would be deployed without executing
    --upgrade           Upgrade existing deployment
    --rollback          Rollback to previous version
    --uninstall         Uninstall the deployment
    -h, --help          Show this help message

EXAMPLES:
    # Deploy to production
    $0 --environment production

    # Deploy to staging with custom domain
    $0 --environment staging --domain staging.orchestrator.com
    
    # Upgrade existing deployment
    $0 --upgrade
    
    # Dry run deployment
    $0 --dry-run

EOF
}

# Parse command line arguments
DRY_RUN=false
UPGRADE=false
ROLLBACK=false
UNINSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -r|--release)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -d|--domain)
            DOMAIN="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --upgrade)
            UPGRADE=true
            shift
            ;;
        --rollback)
            ROLLBACK=true
            shift
            ;;
        --uninstall)
            UNINSTALL=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            error_exit "Unknown option: $1"
            ;;
    esac
done

# Validate environment
case $ENVIRONMENT in
    production|staging|development)
        ;;
    *)
        error_exit "Invalid environment: $ENVIRONMENT. Must be one of: production, staging, development"
        ;;
esac

# Update namespace based on environment if not explicitly set
if [[ "$NAMESPACE" == "orchestrator-production" && "$ENVIRONMENT" != "production" ]]; then
    NAMESPACE="orchestrator-$ENVIRONMENT"
fi

log_info "Starting Kubernetes deployment for NextGeneration Orchestrator"
log_info "Environment: $ENVIRONMENT"
log_info "Namespace: $NAMESPACE"
log_info "Release: $RELEASE_NAME"
log_info "Domain: $DOMAIN"

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if kubectl is installed and configured
    if ! command -v kubectl &> /dev/null; then
        error_exit "kubectl is not installed or not in PATH"
    fi
    
    # Check kubectl connectivity
    if ! kubectl cluster-info &> /dev/null; then
        error_exit "kubectl cannot connect to Kubernetes cluster"
    fi
    
    # Check if helm is installed
    if ! command -v helm &> /dev/null; then
        error_exit "Helm is not installed or not in PATH"
    fi
    
    # Check Helm chart exists
    if [[ ! -f "$HELM_CHART_PATH/Chart.yaml" ]]; then
        error_exit "Helm chart not found at $HELM_CHART_PATH"
    fi
    
    # Check current context
    CURRENT_CONTEXT=$(kubectl config current-context)
    log_info "Current Kubernetes context: $CURRENT_CONTEXT"
    
    # Validate for production
    if [[ "$ENVIRONMENT" == "production" ]]; then
        log_warning "Deploying to PRODUCTION environment!"
        if [[ ! "$CURRENT_CONTEXT" =~ production ]]; then
            log_warning "Current context doesn't appear to be production: $CURRENT_CONTEXT"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                error_exit "Deployment cancelled"
            fi
        fi
    fi
    
    log_success "Prerequisites check passed"
}

# Create namespace if it doesn't exist
create_namespace() {
    log_info "Ensuring namespace $NAMESPACE exists..."
    
    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log_info "Namespace $NAMESPACE already exists"
    else
        log_info "Creating namespace $NAMESPACE..."
        kubectl create namespace "$NAMESPACE"
        
        # Add labels
        kubectl label namespace "$NAMESPACE" \
            environment="$ENVIRONMENT" \
            app.kubernetes.io/name=orchestrator \
            app.kubernetes.io/managed-by=helm
        
        log_success "Namespace $NAMESPACE created"
    fi
}

# Setup secrets
setup_secrets() {
    log_info "Setting up secrets..."
    
    # Check if external secrets operator is available
    if kubectl get crd secretstores.external-secrets.io &> /dev/null; then
        log_info "External Secrets Operator detected, configuring SecretStore..."
        
        # Create SecretStore for the environment
        cat <<EOF | kubectl apply -f -
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: azure-keyvault
  namespace: $NAMESPACE
spec:
  provider:
    azurekv:
      authType: ManagedIdentity
      vaultUrl: "\${AZURE_KEYVAULT_URL}"
      identityId: "\${AZURE_IDENTITY_CLIENT_ID}"
EOF
        
        log_success "SecretStore configured"
    else
        log_warning "External Secrets Operator not found, manual secret management required"
        
        # Create basic secrets if they don't exist
        if ! kubectl get secret orchestrator-secrets -n "$NAMESPACE" &> /dev/null; then
            log_info "Creating placeholder secrets (update with real values)..."
            kubectl create secret generic orchestrator-secrets \
                --namespace="$NAMESPACE" \
                --from-literal=database_url="postgresql://user:pass@postgres:5432/orchestrator" \
                --from-literal=redis_url="redis://redis:6379/0" \
                --from-literal=openai_api_key="your-openai-key" \
                --from-literal=azure_openai_key="your-azure-key"
        fi
    fi
}

# Install monitoring dependencies
install_monitoring() {
    log_info "Setting up monitoring infrastructure..."
    
    # Add Helm repositories
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    
    # Install Prometheus if not exists
    if ! helm list -n "$NAMESPACE" | grep -q prometheus; then
        log_info "Installing Prometheus..."
        helm install prometheus prometheus-community/kube-prometheus-stack \
            --namespace "$NAMESPACE" \
            --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
            --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=gp3 \
            --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
            --timeout "$TIMEOUT"
    fi
    
    # Install Jaeger if not exists  
    if ! helm list -n "$NAMESPACE" | grep -q jaeger; then
        log_info "Installing Jaeger..."
        helm install jaeger jaegertracing/jaeger \
            --namespace "$NAMESPACE" \
            --set provisionDataStore.cassandra=false \
            --set provisionDataStore.elasticsearch=true \
            --set elasticsearch.minimumMasterNodes=1 \
            --timeout "$TIMEOUT"
    fi
    
    log_success "Monitoring infrastructure ready"
}

# Deploy application
deploy_application() {
    log_info "Deploying NextGeneration Orchestrator..."
    
    # Prepare Helm values for environment
    VALUES_FILE="/tmp/orchestrator-values-$ENVIRONMENT.yaml"
    
    cat > "$VALUES_FILE" <<EOF
# Auto-generated values for $ENVIRONMENT
global:
  environment: $ENVIRONMENT

image:
  tag: "1.3.0"

ingress:
  enabled: true
  hosts:
    - host: $DOMAIN
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: orchestrator-tls
      hosts:
        - $DOMAIN

autoscaling:
  enabled: true
  minReplicas: $([ "$ENVIRONMENT" = "production" ] && echo "3" || echo "2")
  maxReplicas: $([ "$ENVIRONMENT" = "production" ] && echo "20" || echo "10")

postgresql:
  enabled: true
  auth:
    database: orchestrator_$ENVIRONMENT

redis:
  enabled: true
  architecture: $([ "$ENVIRONMENT" = "production" ] && echo "cluster" || echo "standalone")

monitoring:
  prometheus:
    enabled: true
  grafana:
    enabled: true
  jaeger:
    enabled: true

resources:
  limits:
    cpu: $([ "$ENVIRONMENT" = "production" ] && echo "1000m" || echo "500m")
    memory: $([ "$ENVIRONMENT" = "production" ] && echo "1Gi" || echo "512Mi")
  requests:
    cpu: $([ "$ENVIRONMENT" = "production" ] && echo "500m" || echo "250m")
    memory: $([ "$ENVIRONMENT" = "production" ] && echo "512Mi" || echo "256Mi")
EOF

    # Helm command construction
    HELM_CMD="helm"
    
    if [[ "$UPGRADE" == "true" ]]; then
        HELM_CMD="$HELM_CMD upgrade"
    else
        HELM_CMD="$HELM_CMD install"
    fi
    
    HELM_CMD="$HELM_CMD $RELEASE_NAME $HELM_CHART_PATH"
    HELM_CMD="$HELM_CMD --namespace $NAMESPACE"
    HELM_CMD="$HELM_CMD --values $VALUES_FILE"
    HELM_CMD="$HELM_CMD --timeout $TIMEOUT"
    HELM_CMD="$HELM_CMD --wait"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        HELM_CMD="$HELM_CMD --dry-run"
    fi
    
    # Execute deployment
    log_info "Executing: $HELM_CMD"
    eval "$HELM_CMD"
    
    # Cleanup
    rm -f "$VALUES_FILE"
    
    if [[ "$DRY_RUN" == "false" ]]; then
        log_success "Application deployed successfully"
    else
        log_success "Dry run completed successfully"
    fi
}

# Rollback deployment
rollback_deployment() {
    log_info "Rolling back deployment..."
    
    # Get rollback revision
    read -p "Enter revision number to rollback to (leave empty for previous): " REVISION
    
    ROLLBACK_CMD="helm rollback $RELEASE_NAME"
    if [[ -n "$REVISION" ]]; then
        ROLLBACK_CMD="$ROLLBACK_CMD $REVISION"
    fi
    ROLLBACK_CMD="$ROLLBACK_CMD --namespace $NAMESPACE"
    
    eval "$ROLLBACK_CMD"
    log_success "Rollback completed"
}

# Uninstall deployment
uninstall_deployment() {
    log_warning "This will completely remove the deployment!"
    read -p "Are you sure you want to uninstall $RELEASE_NAME? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Uninstalling $RELEASE_NAME..."
        helm uninstall "$RELEASE_NAME" --namespace "$NAMESPACE"
        log_success "Deployment uninstalled"
    else
        log_info "Uninstall cancelled"
    fi
}

# Validate deployment
validate_deployment() {
    log_info "Validating deployment..."
    
    # Check pod status
    log_info "Checking pod status..."
    kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=orchestrator
    
    # Wait for pods to be ready
    log_info "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod \
        -l app.kubernetes.io/name=orchestrator \
        -n "$NAMESPACE" \
        --timeout="$TIMEOUT"
    
    # Check service status
    log_info "Checking service status..."
    kubectl get services -n "$NAMESPACE"
    
    # Check ingress status
    if kubectl get ingress -n "$NAMESPACE" &> /dev/null; then
        log_info "Checking ingress status..."
        kubectl get ingress -n "$NAMESPACE"
    fi
    
    # Test health endpoint
    log_info "Testing health endpoint..."
    POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=orchestrator -o jsonpath='{.items[0].metadata.name}')
    
    if kubectl exec -n "$NAMESPACE" "$POD_NAME" -- curl -s http://localhost:8002/health > /dev/null; then
        log_success "Health endpoint responding"
    else
        log_warning "Health endpoint not responding yet"
    fi
    
    log_success "Deployment validation completed"
}

# Display deployment info
show_deployment_info() {
    log_info "Deployment Information:"
    echo "======================"
    echo "Environment: $ENVIRONMENT"
    echo "Namespace: $NAMESPACE"
    echo "Release: $RELEASE_NAME"
    echo "Domain: $DOMAIN"
    echo
    
    # Show Helm release info
    helm list -n "$NAMESPACE"
    echo
    
    # Show access information
    log_info "Access Information:"
    echo "=================="
    echo "Application URL: https://$DOMAIN"
    echo "Health Check: https://$DOMAIN/health"
    echo "Metrics: https://$DOMAIN/metrics"
    echo "API Documentation: https://$DOMAIN/docs"
    echo
    
    # Show monitoring URLs
    if kubectl get service prometheus-grafana -n "$NAMESPACE" &> /dev/null; then
        echo "Grafana: kubectl port-forward svc/prometheus-grafana 3000:80 -n $NAMESPACE"
    fi
    
    if kubectl get service jaeger-query -n "$NAMESPACE" &> /dev/null; then
        echo "Jaeger: kubectl port-forward svc/jaeger-query 16686:16686 -n $NAMESPACE"
    fi
}

# Main execution
main() {
    # Handle special actions first
    if [[ "$ROLLBACK" == "true" ]]; then
        check_prerequisites
        rollback_deployment
        exit 0
    fi
    
    if [[ "$UNINSTALL" == "true" ]]; then
        check_prerequisites
        uninstall_deployment
        exit 0
    fi
    
    # Normal deployment flow
    check_prerequisites
    create_namespace
    setup_secrets
    
    if [[ "$ENVIRONMENT" == "production" ]]; then
        install_monitoring
    fi
    
    deploy_application
    
    if [[ "$DRY_RUN" == "false" ]]; then
        validate_deployment
        show_deployment_info
    fi
    
    log_success "Kubernetes deployment completed successfully!"
}

# Run main function
main "$@"

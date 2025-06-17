#!/bin/bash
# Blue/Green Enterprise Deployment - Sprint 3.1
# Zero-downtime deployment with comprehensive validation
# IA-2 Architecture & Production

set -euo pipefail

ENVIRONMENT=${1:-production}
STAGE=${2:-full-deployment}
NAMESPACE=${3:-orchestrator}
TIMEOUT=${4:-600}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Validate prerequisites
validate_prerequisites() {
    log "🔍 Validating deployment prerequisites..."
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    # Check helm
    if ! command -v helm &> /dev/null; then
        error "helm is not installed or not in PATH"
        exit 1
    fi
    
    # Check cluster connectivity
    if ! kubectl cluster-info &> /dev/null; then
        error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    # Check namespace exists
    if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log "Creating namespace $NAMESPACE"
        kubectl create namespace "$NAMESPACE"
    fi
    
    # Validate secrets availability
    if ! kubectl get secret orchestrator-secrets -n "$NAMESPACE" &> /dev/null; then
        warning "Orchestrator secrets not found - deployment may fail"
    fi
    
    # Check database connectivity
    info "Validating database migrations..."
    if ! ./scripts/validate-database-migrations.sh "$ENVIRONMENT"; then
        error "Database migration validation failed"
        exit 1
    fi
    
    log "✅ Prerequisites validation completed"
}

# Deploy GREEN environment
deploy_green() {
    log "🟢 Deploying GREEN environment..."
    
    local image_tag=${IMAGE_TAG:-latest}
    local helm_chart="./k8s/helm/orchestrator"
    local values_file="./k8s/helm/orchestrator/values-${ENVIRONMENT}.yaml"
    
    # Check if values file exists
    if [[ ! -f "$values_file" ]]; then
        error "Values file not found: $values_file"
        exit 1
    fi
    
    # Deploy GREEN version
    helm upgrade --install "orchestrator-green" "$helm_chart" \
        --namespace "$NAMESPACE" \
        --values "$values_file" \
        --set image.tag="$image_tag" \
        --set deployment.version="green" \
        --set service.selector.version="green" \
        --set autoscaling.enabled=true \
        --set autoscaling.minReplicas=3 \
        --set autoscaling.maxReplicas=20 \
        --timeout "${TIMEOUT}s" \
        --wait
    
    # Wait for deployment to be ready
    log "⏳ Waiting for GREEN deployment to be ready..."
    kubectl wait --for=condition=available deployment/orchestrator-green \
        -n "$NAMESPACE" \
        --timeout="${TIMEOUT}s"
    
    # Verify all pods are running
    local ready_pods=$(kubectl get pods -l app=orchestrator,version=green -n "$NAMESPACE" -o jsonpath='{.items[*].status.containerStatuses[0].ready}' | grep -o true | wc -l)
    local total_pods=$(kubectl get pods -l app=orchestrator,version=green -n "$NAMESPACE" --no-headers | wc -l)
    
    if [[ "$ready_pods" -eq "$total_pods" ]] && [[ "$total_pods" -gt 0 ]]; then
        log "✅ GREEN deployment ready - $ready_pods/$total_pods pods running"
    else
        error "GREEN deployment not ready - $ready_pods/$total_pods pods running"
        exit 1
    fi
}

# Comprehensive health validation
health_validation() {
    log "🏥 Comprehensive health validation..."
    
    local green_service_url
    green_service_url=$(kubectl get service orchestrator-green-service -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    
    if [[ -z "$green_service_url" ]]; then
        # Use port-forward for testing
        log "Using port-forward for health checks..."
        kubectl port-forward service/orchestrator-green-service 8080:8002 -n "$NAMESPACE" &
        local port_forward_pid=$!
        sleep 5
        green_service_url="localhost:8080"
    fi
    
    # Health check endpoint
    local health_url="http://${green_service_url}/health"
    local max_attempts=30
    local attempt=1
    
    log "🔍 Testing health endpoint: $health_url"
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s -f "$health_url" > /dev/null; then
            log "✅ Health check passed (attempt $attempt)"
            break
        else
            warning "Health check failed (attempt $attempt/$max_attempts)"
            sleep 10
            ((attempt++))
        fi
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        error "Health check failed after $max_attempts attempts"
        [[ -n "${port_forward_pid:-}" ]] && kill "$port_forward_pid" 2>/dev/null || true
        exit 1
    fi
    
    # Performance validation
    log "⚡ Performance validation..."
    if ! ./scripts/performance-validation.sh --environment=green --url="$health_url"; then
        error "Performance validation failed"
        [[ -n "${port_forward_pid:-}" ]] && kill "$port_forward_pid" 2>/dev/null || true
        exit 1
    fi
    
    # Business logic validation
    log "💼 Business logic validation..."
    if ! ./scripts/business-logic-validation.sh --environment=green --url="$health_url"; then
        error "Business logic validation failed"
        [[ -n "${port_forward_pid:-}" ]] && kill "$port_forward_pid" 2>/dev/null || true
        exit 1
    fi
    
    # Cleanup port-forward if used
    [[ -n "${port_forward_pid:-}" ]] && kill "$port_forward_pid" 2>/dev/null || true
    
    log "✅ Comprehensive health validation completed"
}

# Switch traffic to GREEN
switch_traffic() {
    log "🔄 Switching traffic to GREEN..."
    
    # Get current BLUE service selector
    local current_version
    current_version=$(kubectl get service orchestrator-service -n "$NAMESPACE" -o jsonpath='{.spec.selector.version}' 2>/dev/null || echo "blue")
    
    log "Current traffic routing to: $current_version"
    
    # Update service selector to point to GREEN
    kubectl patch service orchestrator-service -n "$NAMESPACE" \
        -p '{"spec":{"selector":{"version":"green"}}}'
    
    # Wait for service to update
    sleep 10
    
    # Verify traffic switch
    local new_version
    new_version=$(kubectl get service orchestrator-service -n "$NAMESPACE" -o jsonpath='{.spec.selector.version}')
    
    if [[ "$new_version" == "green" ]]; then
        log "✅ Traffic successfully switched to GREEN"
    else
        error "Traffic switch failed - current version: $new_version"
        exit 1
    fi
    
    # Monitor traffic for initial period
    log "📊 Monitoring traffic switch..."
    sleep 30
    
    # Check for any immediate errors
    local error_rate
    error_rate=$(kubectl exec -n "$NAMESPACE" deployment/orchestrator-green -- \
        curl -s "http://localhost:8002/metrics" | \
        grep "http_requests_total.*5.." | \
        awk '{sum+=$NF} END {print sum+0}' || echo "0")
    
    if [[ "$error_rate" -gt 5 ]]; then
        warning "High error rate detected: $error_rate errors"
        log "Consider monitoring closely or rolling back"
    else
        log "✅ Traffic switch monitoring completed - error rate: $error_rate"
    fi
}

# Monitor traffic switch
monitor_traffic_switch() {
    log "📈 Advanced traffic switch monitoring..."
    
    local monitoring_duration=${MONITORING_DURATION:-300}  # 5 minutes
    local check_interval=30
    local checks=$((monitoring_duration / check_interval))
    
    for ((i=1; i<=checks; i++)); do
        log "Monitoring check $i/$checks..."
        
        # Check service health
        local healthy_pods=$(kubectl get pods -l app=orchestrator,version=green -n "$NAMESPACE" -o jsonpath='{.items[*].status.containerStatuses[0].ready}' | grep -o true | wc -l)
        
        # Check error rate
        local current_errors=$(kubectl exec -n "$NAMESPACE" deployment/orchestrator-green -- \
            curl -s "http://localhost:8002/metrics" | \
            grep "http_requests_total.*5.." | \
            awk '{sum+=$NF} END {print sum+0}' || echo "0")
        
        # Check response time
        local avg_response_time=$(kubectl exec -n "$NAMESPACE" deployment/orchestrator-green -- \
            curl -s "http://localhost:8002/metrics" | \
            grep "http_request_duration_seconds" | \
            head -1 | \
            awk '{print $NF}' || echo "0")
        
        info "Monitoring metrics - Healthy pods: $healthy_pods, Errors: $current_errors, Avg response: ${avg_response_time}s"
        
        # Alert thresholds
        if [[ "$current_errors" -gt 10 ]]; then
            error "High error rate detected during monitoring: $current_errors"
            return 1
        fi
        
        if [[ $(echo "$avg_response_time > 2.0" | bc -l 2>/dev/null || echo "0") -eq 1 ]]; then
            warning "High response time detected: ${avg_response_time}s"
        fi
        
        sleep $check_interval
    done
    
    log "✅ Traffic switch monitoring completed successfully"
}

# Cleanup BLUE environment
cleanup_blue() {
    log "🔵 Cleaning up BLUE environment..."
    
    # Check if BLUE deployment exists
    if kubectl get deployment orchestrator-blue -n "$NAMESPACE" &>/dev/null; then
        # Scale down BLUE deployment gradually
        log "Scaling down BLUE deployment..."
        kubectl scale deployment orchestrator-blue --replicas=0 -n "$NAMESPACE"
        
        # Wait for pods to terminate
        kubectl wait --for=delete pod -l app=orchestrator,version=blue -n "$NAMESPACE" --timeout=300s
        
        # Delete BLUE resources
        helm uninstall orchestrator-blue -n "$NAMESPACE" || true
        
        # Clean up any remaining resources
        kubectl delete configmap -l app=orchestrator,version=blue -n "$NAMESPACE" --ignore-not-found=true
        kubectl delete secret -l app=orchestrator,version=blue -n "$NAMESPACE" --ignore-not-found=true
        
        log "✅ BLUE environment cleaned up"
    else
        info "No BLUE environment found to cleanup"
    fi
}

# Rollback to BLUE
rollback_blue() {
    log "🔄 Rolling back to BLUE environment..."
    
    # Check if BLUE deployment exists
    if ! kubectl get deployment orchestrator-blue -n "$NAMESPACE" &>/dev/null; then
        error "BLUE deployment not found - cannot rollback"
        exit 1
    fi
    
    # Scale up BLUE deployment
    kubectl scale deployment orchestrator-blue --replicas=3 -n "$NAMESPACE"
    
    # Wait for BLUE to be ready
    kubectl wait --for=condition=available deployment/orchestrator-blue -n "$NAMESPACE" --timeout=300s
    
    # Switch traffic back to BLUE
    kubectl patch service orchestrator-service -n "$NAMESPACE" \
        -p '{"spec":{"selector":{"version":"blue"}}}'
    
    # Verify rollback
    local current_version
    current_version=$(kubectl get service orchestrator-service -n "$NAMESPACE" -o jsonpath='{.spec.selector.version}')
    
    if [[ "$current_version" == "blue" ]]; then
        log "✅ Successfully rolled back to BLUE environment"
    else
        error "Rollback failed - current version: $current_version"
        exit 1
    fi
    
    # Clean up failed GREEN deployment
    helm uninstall orchestrator-green -n "$NAMESPACE" || true
}

# Main execution
main() {
    log "🚀 Starting Blue/Green Enterprise Deployment"
    log "Environment: $ENVIRONMENT, Stage: $STAGE, Namespace: $NAMESPACE"
    
    case $STAGE in
        "validate-prerequisites")
            validate_prerequisites
            ;;
        "deploy-green")
            validate_prerequisites
            deploy_green
            ;;
        "health-validation")
            health_validation
            ;;
        "switch-traffic")
            switch_traffic
            monitor_traffic_switch
            ;;
        "cleanup-blue")
            cleanup_blue
            ;;
        "rollback")
            rollback_blue
            ;;
        "full-deployment")
            validate_prerequisites
            deploy_green
            health_validation
            switch_traffic
            monitor_traffic_switch
            cleanup_blue
            log "🎉 Blue/Green deployment completed successfully!"
            ;;
        *)
            error "Unknown stage: $STAGE"
            echo "Usage: $0 <environment> <stage> [namespace] [timeout]"
            echo "Stages: validate-prerequisites, deploy-green, health-validation, switch-traffic, cleanup-blue, rollback, full-deployment"
            exit 1
            ;;
    esac
}

# Trap for cleanup on script exit
cleanup_on_exit() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        error "Deployment failed with exit code $exit_code"
        if [[ "$STAGE" == "full-deployment" ]]; then
            warning "Consider running rollback: $0 $ENVIRONMENT rollback"
        fi
    fi
}

trap cleanup_on_exit EXIT

# Execute main function
main "$@"

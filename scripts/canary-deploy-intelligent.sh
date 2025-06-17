#!/bin/bash
# Canary Release with Intelligent Monitoring - Sprint 3.1
# Progressive rollout with automated decision making
# IA-2 Architecture & Production

set -euo pipefail

CANARY_PERCENTAGE=${1:-5}
MONITORING_DURATION=${2:-300}  # 5 minutes per stage
NAMESPACE=${3:-orchestrator}
ENVIRONMENT=${4:-production}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Deploy canary at specific percentage
deploy_canary_percentage() {
    local percentage=$1
    log "🕊️ Deploying canary at ${percentage}% traffic..."
    
    # Calculate replica counts
    local total_replicas=10
    local canary_replicas=$(( (percentage * total_replicas) / 100 ))
    local stable_replicas=$(( total_replicas - canary_replicas ))
    
    # Ensure minimum replicas
    if [[ $canary_replicas -eq 0 && $percentage -gt 0 ]]; then
        canary_replicas=1
        stable_replicas=$((total_replicas - 1))
    fi
    
    info "Canary replicas: $canary_replicas, Stable replicas: $stable_replicas"
    
    # Deploy canary version if not exists
    if ! kubectl get deployment orchestrator-canary -n "$NAMESPACE" &>/dev/null; then
        log "Creating canary deployment..."
        
        helm upgrade --install orchestrator-canary ./k8s/helm/orchestrator \
            --namespace "$NAMESPACE" \
            --values ./k8s/helm/orchestrator/values-canary.yaml \
            --set image.tag="${IMAGE_TAG:-latest}" \
            --set deployment.version="canary" \
            --set replicaCount="$canary_replicas" \
            --wait --timeout=300s
    else
        log "Scaling canary deployment to $canary_replicas replicas..."
        kubectl scale deployment orchestrator-canary --replicas="$canary_replicas" -n "$NAMESPACE"
    fi
    
    # Scale stable deployment
    log "Scaling stable deployment to $stable_replicas replicas..."
    kubectl scale deployment orchestrator-stable --replicas="$stable_replicas" -n "$NAMESPACE"
    
    # Wait for deployments to be ready
    kubectl wait --for=condition=available deployment/orchestrator-canary -n "$NAMESPACE" --timeout=300s
    kubectl wait --for=condition=available deployment/orchestrator-stable -n "$NAMESPACE" --timeout=300s
    
    # Update traffic splitting (using Istio VirtualService)
    if kubectl get virtualservice orchestrator-vs -n "$NAMESPACE" &>/dev/null; then
        log "Updating traffic split to ${percentage}% canary..."
        
        cat << EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orchestrator-vs
  namespace: $NAMESPACE
spec:
  hosts:
  - orchestrator-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: orchestrator-service
        subset: canary
      weight: 100
  - route:
    - destination:
        host: orchestrator-service
        subset: canary
      weight: $percentage
    - destination:
        host: orchestrator-service
        subset: stable
      weight: $((100 - percentage))
EOF
    else
        warning "Istio VirtualService not found - using basic service routing"
        # Basic service routing without traffic splitting
        kubectl patch service orchestrator-service -n "$NAMESPACE" \
            --type='json' \
            -p='[{"op": "replace", "path": "/spec/selector", "value": {"app": "orchestrator"}}]'
    fi
    
    log "✅ Canary deployment at ${percentage}% completed"
}

# Monitor canary metrics
monitor_canary_metrics() {
    local percentage=$1
    local duration=$2
    
    log "📊 Monitoring canary metrics for ${duration} seconds..."
    
    local check_interval=30
    local checks=$((duration / check_interval))
    local success_checks=0
    local total_checks=0
    
    for ((i=1; i<=checks; i++)); do
        info "Monitoring check $i/$checks..."
        
        # Get metrics from both canary and stable
        local canary_metrics=$(get_deployment_metrics "orchestrator-canary")
        local stable_metrics=$(get_deployment_metrics "orchestrator-stable")
        
        # Parse metrics
        local canary_error_rate=$(echo "$canary_metrics" | jq -r '.error_rate // 0')
        local canary_latency_p95=$(echo "$canary_metrics" | jq -r '.latency_p95 // 0')
        local canary_cpu_usage=$(echo "$canary_metrics" | jq -r '.cpu_usage // 0')
        
        local stable_error_rate=$(echo "$stable_metrics" | jq -r '.error_rate // 0')
        local stable_latency_p95=$(echo "$stable_metrics" | jq -r '.latency_p95 // 0')
        local stable_cpu_usage=$(echo "$stable_metrics" | jq -r '.cpu_usage // 0')
        
        info "Canary  - Error rate: ${canary_error_rate}%, P95 latency: ${canary_latency_p95}ms, CPU: ${canary_cpu_usage}%"
        info "Stable  - Error rate: ${stable_error_rate}%, P95 latency: ${stable_latency_p95}ms, CPU: ${stable_cpu_usage}%"
        
        # Evaluate canary health
        local canary_healthy=true
        
        # Error rate threshold: canary should not be significantly worse than stable
        if (( $(echo "$canary_error_rate > $stable_error_rate + 2" | bc -l) )); then
            warning "Canary error rate too high: ${canary_error_rate}% vs stable ${stable_error_rate}%"
            canary_healthy=false
        fi
        
        # Latency threshold: canary should not be significantly slower
        if (( $(echo "$canary_latency_p95 > $stable_latency_p95 * 1.5" | bc -l) )); then
            warning "Canary latency too high: ${canary_latency_p95}ms vs stable ${stable_latency_p95}ms"
            canary_healthy=false
        fi
        
        # Absolute thresholds
        if (( $(echo "$canary_error_rate > 5" | bc -l) )); then
            warning "Canary error rate above absolute threshold: ${canary_error_rate}% > 5%"
            canary_healthy=false
        fi
        
        if (( $(echo "$canary_latency_p95 > 2000" | bc -l) )); then
            warning "Canary latency above absolute threshold: ${canary_latency_p95}ms > 2000ms"
            canary_healthy=false
        fi
        
        # Business metrics validation
        local business_metrics_ok=$(validate_business_metrics)
        if [[ "$business_metrics_ok" != "true" ]]; then
            warning "Business metrics validation failed"
            canary_healthy=false
        fi
        
        if [[ "$canary_healthy" == "true" ]]; then
            ((success_checks++))
        fi
        
        ((total_checks++))
        
        sleep $check_interval
    done
    
    # Calculate success rate
    local success_rate=$(( (success_checks * 100) / total_checks ))
    info "Canary monitoring completed - Success rate: ${success_rate}% (${success_checks}/${total_checks})"
    
    # Decision threshold: 80% of checks must pass
    if [[ $success_rate -ge 80 ]]; then
        log "✅ Canary ${percentage}% monitoring successful"
        return 0
    else
        error "❌ Canary ${percentage}% monitoring failed - success rate ${success_rate}% below threshold (80%)"
        return 1
    fi
}

# Get deployment metrics
get_deployment_metrics() {
    local deployment_name=$1
    
    # Get pod metrics via kubectl top and prometheus if available
    local pods=$(kubectl get pods -l app=orchestrator,version=${deployment_name#orchestrator-} -n "$NAMESPACE" -o jsonpath='{.items[*].metadata.name}')
    
    if [[ -z "$pods" ]]; then
        echo '{"error_rate": 0, "latency_p95": 0, "cpu_usage": 0}'
        return
    fi
    
    # Calculate average metrics across pods
    local total_error_rate=0
    local total_latency=0
    local total_cpu=0
    local pod_count=0
    
    for pod in $pods; do
        # Get metrics from pod's /metrics endpoint
        local pod_metrics=$(kubectl exec "$pod" -n "$NAMESPACE" -- \
            curl -s "http://localhost:8002/metrics" 2>/dev/null || echo "")
        
        if [[ -n "$pod_metrics" ]]; then
            # Parse Prometheus metrics
            local error_count=$(echo "$pod_metrics" | grep "http_requests_total.*5.." | awk '{sum+=$NF} END {print sum+0}')
            local total_requests=$(echo "$pod_metrics" | grep "http_requests_total" | head -1 | awk '{print $NF}')
            local latency_p95=$(echo "$pod_metrics" | grep "http_request_duration_seconds.*0.95" | awk '{print $NF * 1000}' || echo "0")
            
            if [[ "$total_requests" -gt 0 ]]; then
                local error_rate=$(echo "scale=2; $error_count * 100 / $total_requests" | bc -l)
                total_error_rate=$(echo "$total_error_rate + $error_rate" | bc -l)
            fi
            
            total_latency=$(echo "$total_latency + $latency_p95" | bc -l)
            ((pod_count++))
        fi
        
        # Get CPU usage from kubectl top
        local cpu_usage=$(kubectl top pod "$pod" -n "$NAMESPACE" --no-headers 2>/dev/null | awk '{print $2}' | sed 's/m$//' || echo "0")
        total_cpu=$(echo "$total_cpu + $cpu_usage" | bc -l)
    done
    
    # Calculate averages
    if [[ $pod_count -gt 0 ]]; then
        local avg_error_rate=$(echo "scale=2; $total_error_rate / $pod_count" | bc -l)
        local avg_latency=$(echo "scale=2; $total_latency / $pod_count" | bc -l)
        local avg_cpu=$(echo "scale=2; $total_cpu / $pod_count / 10" | bc -l)  # Convert from millicores to percentage
        
        echo "{\"error_rate\": $avg_error_rate, \"latency_p95\": $avg_latency, \"cpu_usage\": $avg_cpu}"
    else
        echo '{"error_rate": 0, "latency_p95": 0, "cpu_usage": 0}'
    fi
}

# Validate business metrics
validate_business_metrics() {
    # Check business KPIs via API
    local api_response=$(curl -s "http://orchestrator-service.$NAMESPACE.svc.cluster.local:8002/business/kpis" 2>/dev/null || echo "{}")
    
    if [[ -n "$api_response" && "$api_response" != "{}" ]]; then
        local user_satisfaction=$(echo "$api_response" | jq -r '.user_satisfaction_score // 8.0')
        local conversion_rate=$(echo "$api_response" | jq -r '.conversion_rate // 10.0')
        
        # Validate thresholds
        if (( $(echo "$user_satisfaction >= 7.5" | bc -l) )) && \
           (( $(echo "$conversion_rate >= 8.0" | bc -l) )); then
            echo "true"
        else
            echo "false"
        fi
    else
        # Default to true if metrics unavailable
        echo "true"
    fi
}

# Rollback canary deployment
rollback_canary() {
    log "🔄 Rolling back canary deployment..."
    
    # Scale canary to 0
    kubectl scale deployment orchestrator-canary --replicas=0 -n "$NAMESPACE"
    
    # Scale stable to full capacity
    kubectl scale deployment orchestrator-stable --replicas=10 -n "$NAMESPACE"
    
    # Update traffic to 100% stable
    if kubectl get virtualservice orchestrator-vs -n "$NAMESPACE" &>/dev/null; then
        cat << EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orchestrator-vs
  namespace: $NAMESPACE
spec:
  hosts:
  - orchestrator-service
  http:
  - route:
    - destination:
        host: orchestrator-service
        subset: stable
      weight: 100
EOF
    fi
    
    log "✅ Canary rollback completed"
}

# Promote canary to stable
promote_canary() {
    log "🎉 Promoting canary to stable..."
    
    # Update stable deployment with canary image
    local canary_image=$(kubectl get deployment orchestrator-canary -n "$NAMESPACE" -o jsonpath='{.spec.template.spec.containers[0].image}')
    kubectl set image deployment/orchestrator-stable orchestrator="$canary_image" -n "$NAMESPACE"
    
    # Scale stable to full capacity
    kubectl scale deployment orchestrator-stable --replicas=10 -n "$NAMESPACE"
    
    # Remove canary deployment
    kubectl scale deployment orchestrator-canary --replicas=0 -n "$NAMESPACE"
    helm uninstall orchestrator-canary -n "$NAMESPACE" || true
    
    # Update traffic to 100% stable
    if kubectl get virtualservice orchestrator-vs -n "$NAMESPACE" &>/dev/null; then
        cat << EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orchestrator-vs
  namespace: $NAMESPACE
spec:
  hosts:
  - orchestrator-service
  http:
  - route:
    - destination:
        host: orchestrator-service
        subset: stable
      weight: 100
EOF
    fi
    
    log "✅ Canary promotion completed"
}

# Validate canary metrics and decide next action
validate_canary_metrics() {
    local percentage=$1
    
    # Run monitoring
    if monitor_canary_metrics "$percentage" "$MONITORING_DURATION"; then
        echo "SUCCESS"
    else
        echo "FAILURE"
    fi
}

# Main canary deployment function
main() {
    log "🚀 Starting Canary Release Intelligent Deployment"
    log "Initial percentage: $CANARY_PERCENTAGE%, Monitoring duration: $MONITORING_DURATION seconds"
    
    # Check if this is a full progressive deployment
    if [[ "$CANARY_PERCENTAGE" == "progressive" ]]; then
        log "🔄 Running progressive canary deployment..."
        
        # Progressive canary deployment stages
        for percentage in 5 10 25 50 100; do
            log "═══ Canary Stage: ${percentage}% ═══"
            
            if [[ $percentage -eq 100 ]]; then
                promote_canary
                log "🎉 Progressive canary deployment completed successfully - 100% traffic on new version"
                break
            else
                deploy_canary_percentage "$percentage"
                
                if ! monitor_canary_metrics "$percentage" "$MONITORING_DURATION"; then
                    error "🚨 Canary deployment failed at ${percentage}% - initiating rollback"
                    rollback_canary
                    exit 1
                fi
                
                log "✅ Canary ${percentage}% stage successful"
                
                if [[ $percentage -lt 50 ]]; then
                    log "⏳ Waiting before next canary stage..."
                    sleep 60
                fi
            fi
        done
    else
        # Single percentage deployment
        deploy_canary_percentage "$CANARY_PERCENTAGE"
        
        local metrics_result=$(validate_canary_metrics "$CANARY_PERCENTAGE")
        
        if [[ $metrics_result == "SUCCESS" ]]; then
            log "✅ Canary ${CANARY_PERCENTAGE}% validation successful"
        else
            error "❌ Canary ${CANARY_PERCENTAGE}% validation failed - initiating rollback"
            rollback_canary
            exit 1
        fi
    fi
}

# Execute main function
main "$@"

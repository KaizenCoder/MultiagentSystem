# Blue/Green Deployment Script for Windows
# Phase 1 Sprint 1.4 - Production-Ready CI/CD
# Date: June 17, 2025

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [string]$Namespace = "orchestrator-prod",
    
    [Parameter(Mandatory=$false)]
    [int]$HealthCheckTimeout = 300
)

# Configuration
$BLUE_SERVICE = "orchestrator-blue"
$GREEN_SERVICE = "orchestrator-green"
$MAIN_SERVICE = "orchestrator"
$IMAGE_TAG = $env:GITHUB_SHA ?? "latest"

Write-Host "🚀 Starting Blue/Green Deployment" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Namespace: $Namespace" -ForegroundColor Yellow
Write-Host "Image Tag: $IMAGE_TAG" -ForegroundColor Yellow

# Function to check service health
function Test-ServiceHealth {
    param([string]$ServiceUrl)
    
    try {
        $response = Invoke-RestMethod -Uri "$ServiceUrl/health" -Method Get -TimeoutSec 10
        return $response.status -eq "healthy"
    }
    catch {
        return $false
    }
}

# Function to get current active service
function Get-ActiveService {
    try {
        $selector = kubectl get service $MAIN_SERVICE -n $Namespace -o jsonpath='{.spec.selector.version}' 2>$null
        return $selector
    }
    catch {
        return "blue"  # Default to blue if no service exists
    }
}

# Determine target service (opposite of current)
$currentActive = Get-ActiveService
$targetService = if ($currentActive -eq "blue") { "green" } else { "blue" }
$targetColor = $targetService

Write-Host "Current active: $currentActive" -ForegroundColor Cyan
Write-Host "Deploying to: $targetColor" -ForegroundColor Cyan

# Step 1: Deploy new version to target environment
Write-Host "📦 Deploying new version to $targetColor environment..." -ForegroundColor Blue

$deploymentYaml = @"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator-$targetColor
  namespace: $Namespace
  labels:
    app: orchestrator
    version: $targetColor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestrator
      version: $targetColor
  template:
    metadata:
      labels:
        app: orchestrator
        version: $targetColor
    spec:
      containers:
      - name: orchestrator
        image: orchestrator:$IMAGE_TAG
        ports:
        - containerPort: 8002
        env:
        - name: ENVIRONMENT
          value: "$Environment"
        - name: VERSION
          value: "$targetColor"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8002
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8002
          initialDelaySeconds: 15
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: orchestrator-$targetColor
  namespace: $Namespace
  labels:
    app: orchestrator
    version: $targetColor
spec:
  selector:
    app: orchestrator
    version: $targetColor
  ports:
  - port: 80
    targetPort: 8002
    protocol: TCP
  type: ClusterIP
"@

$deploymentYaml | kubectl apply -f - -n $Namespace

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Failed to deploy $targetColor environment"
    exit 1
}

# Step 2: Wait for deployment to be ready
Write-Host "⏳ Waiting for $targetColor deployment to be ready..." -ForegroundColor Blue

kubectl wait --for=condition=available --timeout=${HealthCheckTimeout}s deployment/orchestrator-$targetColor -n $Namespace

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Deployment $targetColor failed to become ready"
    exit 1
}

# Step 3: Health check the new deployment
Write-Host "🔍 Performing health checks on $targetColor environment..." -ForegroundColor Blue

$serviceUrl = "http://orchestrator-$targetColor.$Namespace.svc.cluster.local"
$healthCheckAttempts = 0
$maxAttempts = 30

do {
    $healthCheckAttempts++
    Write-Host "Health check attempt $healthCheckAttempts/$maxAttempts" -ForegroundColor Yellow
    
    if (Test-ServiceHealth $serviceUrl) {
        Write-Host "✅ Health check passed" -ForegroundColor Green
        break
    }
    
    if ($healthCheckAttempts -ge $maxAttempts) {
        Write-Error "❌ Health checks failed after $maxAttempts attempts"
        
        # Cleanup failed deployment
        Write-Host "🧹 Cleaning up failed deployment..." -ForegroundColor Red
        kubectl delete deployment orchestrator-$targetColor -n $Namespace
        kubectl delete service orchestrator-$targetColor -n $Namespace
        exit 1
    }
    
    Start-Sleep -Seconds 10
} while ($true)

# Step 4: Switch traffic to new deployment
Write-Host "🔄 Switching traffic to $targetColor environment..." -ForegroundColor Blue

$mainServiceYaml = @"
apiVersion: v1
kind: Service
metadata:
  name: $MAIN_SERVICE
  namespace: $Namespace
  labels:
    app: orchestrator
    service: main
spec:
  selector:
    app: orchestrator
    version: $targetColor
  ports:
  - port: 80
    targetPort: 8002
    protocol: TCP
  type: LoadBalancer
"@

$mainServiceYaml | kubectl apply -f - -n $Namespace

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Failed to switch traffic to $targetColor"
    exit 1
}

# Step 5: Final validation
Write-Host "✅ Performing final validation..." -ForegroundColor Blue
Start-Sleep -Seconds 30

$mainServiceUrl = "http://$MAIN_SERVICE.$Namespace.svc.cluster.local"
if (Test-ServiceHealth $mainServiceUrl) {
    Write-Host "✅ Blue/Green deployment successful!" -ForegroundColor Green
    Write-Host "✅ Traffic switched to $targetColor environment" -ForegroundColor Green
    
    # Cleanup old deployment
    $oldService = if ($targetColor -eq "blue") { "green" } else { "blue" }
    Write-Host "🧹 Cleaning up old $oldService deployment..." -ForegroundColor Yellow
    
    Start-Sleep -Seconds 60  # Grace period
    kubectl delete deployment orchestrator-$oldService -n $Namespace --ignore-not-found=true
    kubectl delete service orchestrator-$oldService -n $Namespace --ignore-not-found=true
    
    Write-Host "🎉 Blue/Green deployment completed successfully!" -ForegroundColor Green
} else {
    Write-Error "❌ Final validation failed, rolling back..."
    
    # Rollback: switch back to previous version
    $rollbackServiceYaml = @"
apiVersion: v1
kind: Service
metadata:
  name: $MAIN_SERVICE
  namespace: $Namespace
spec:
  selector:
    app: orchestrator
    version: $currentActive
  ports:
  - port: 80
    targetPort: 8002
    protocol: TCP
  type: LoadBalancer
"@
    
    $rollbackServiceYaml | kubectl apply -f - -n $Namespace
    
    # Cleanup failed deployment
    kubectl delete deployment orchestrator-$targetColor -n $Namespace
    kubectl delete service orchestrator-$targetColor -n $Namespace
    
    Write-Error "❌ Deployment failed and rolled back to $currentActive"
    exit 1
}

Write-Host "📊 Deployment Summary:" -ForegroundColor Cyan
Write-Host "  Previous active: $currentActive" -ForegroundColor White
Write-Host "  New active: $targetColor" -ForegroundColor White
Write-Host "  Image tag: $IMAGE_TAG" -ForegroundColor White
Write-Host "  Environment: $Environment" -ForegroundColor White
Write-Host "  Namespace: $Namespace" -ForegroundColor White

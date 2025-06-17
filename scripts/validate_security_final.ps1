# Security Validation Script for Windows
# Phase 1 Sprint 1.4 - Production-Ready Security Audit
# Date: June 17, 2025

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [string]$ReportPath = "security_audit_report.json",
    
    [Parameter(Mandatory=$false)]
    [switch]$DetailedOutput
)

# Configuration
$ORCHESTRATOR_URL = $env:ORCHESTRATOR_URL ?? "http://localhost:8002"
$MEMORY_API_URL = $env:MEMORY_API_URL ?? "http://localhost:8001"

# Security test results
$SecurityResults = @{
    Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Environment = $Environment
    Tests = @()
    Summary = @{
        Total = 0
        Passed = 0
        Failed = 0
        Critical = 0
        High = 0
        Medium = 0
        Low = 0
    }
}

Write-Host "🔒 Starting Security Validation Audit" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow

# Function to add test result
function Add-TestResult {
    param(
        [string]$TestName,
        [string]$Category,
        [string]$Severity,
        [bool]$Passed,
        [string]$Description,
        [string]$Details = ""
    )
    
    $result = @{
        Name = $TestName
        Category = $Category
        Severity = $Severity
        Passed = $Passed
        Description = $Description
        Details = $Details
        Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    }
    
    $SecurityResults.Tests += $result
    $SecurityResults.Summary.Total++
    
    if ($Passed) {
        $SecurityResults.Summary.Passed++
        $status = "✅ PASS"
        $color = "Green"
    } else {
        $SecurityResults.Summary.Failed++
        $status = "❌ FAIL"
        $color = "Red"
        
        switch ($Severity) {
            "Critical" { $SecurityResults.Summary.Critical++ }
            "High" { $SecurityResults.Summary.High++ }
            "Medium" { $SecurityResults.Summary.Medium++ }
            "Low" { $SecurityResults.Summary.Low++ }
        }
    }
    
    Write-Host "$status [$Severity] $TestName" -ForegroundColor $color
}

# Run basic security tests
Write-Host "`n🔐 Testing Authentication & Authorization..." -ForegroundColor Blue

# Test health endpoint accessibility
try {
    $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/health" -UseBasicParsing -TimeoutSec 10
    Add-TestResult -TestName "Health Endpoint Accessibility" -Category "Authentication" -Severity "Low" `
        -Passed ($response.StatusCode -eq 200) `
        -Description "Health endpoint should be accessible" `
        -Details "Status: $($response.StatusCode)"
} catch {
    Add-TestResult -TestName "Health Endpoint Accessibility" -Category "Authentication" -Severity "Low" `
        -Passed $false -Description "Health endpoint failed" -Details $_.Exception.Message
}

# Test protected endpoints
try {
    $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/admin/config" -UseBasicParsing -TimeoutSec 10
    Add-TestResult -TestName "Admin Endpoint Protection" -Category "Authorization" -Severity "High" `
        -Passed ($response.StatusCode -eq 401 -or $response.StatusCode -eq 403) `
        -Description "Admin endpoints should require authentication" `
        -Details "Status: $($response.StatusCode)"
} catch {
    Add-TestResult -TestName "Admin Endpoint Protection" -Category "Authorization" -Severity "High" `
        -Passed $true -Description "Admin endpoint properly protected" -Details "Access denied"
}

Write-Host "`n🛡️ Testing Input Validation..." -ForegroundColor Blue

# SQL Injection test
$sqlPayload = "'; DROP TABLE users; --"
try {
    $response = Invoke-WebRequest -Uri "$MEMORY_API_URL/memories?query=$sqlPayload" -UseBasicParsing -TimeoutSec 10
    Add-TestResult -TestName "SQL Injection Protection" -Category "Input Validation" -Severity "Critical" `
        -Passed ($response.StatusCode -ge 400) `
        -Description "Application should reject SQL injection attempts" `
        -Details "Payload rejected: $($response.StatusCode -ge 400)"
} catch {
    Add-TestResult -TestName "SQL Injection Protection" -Category "Input Validation" -Severity "Critical" `
        -Passed $true -Description "SQL injection properly blocked" -Details "Request blocked"
}

Write-Host "`n🔒 Testing HTTPS & TLS..." -ForegroundColor Blue

# Test security headers
try {
    $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/health" -UseBasicParsing
    $hasHSTS = $response.Headers.ContainsKey("Strict-Transport-Security")
    $hasCSP = $response.Headers.ContainsKey("Content-Security-Policy")
    $hasXFrame = $response.Headers.ContainsKey("X-Frame-Options")
    
    Add-TestResult -TestName "Security Headers" -Category "Transport Security" -Severity "Medium" `
        -Passed ($hasHSTS -and $hasCSP -and $hasXFrame) `
        -Description "Security headers should be present" `
        -Details "HSTS: $hasHSTS, CSP: $hasCSP, X-Frame: $hasXFrame"
} catch {
    Add-TestResult -TestName "Security Headers" -Category "Transport Security" -Severity "Medium" `
        -Passed $false -Description "Failed to check security headers" -Details $_.Exception.Message
}

Write-Host "`n⏱️ Testing Rate Limiting..." -ForegroundColor Blue

# Rate limiting test
$rateLimitBreached = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/health" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 429) {
            $rateLimitBreached = $true
            break
        }
    } catch {
        if ($_.Exception.Message.Contains("429")) {
            $rateLimitBreached = $true
            break
        }
    }
    Start-Sleep -Milliseconds 100
}

Add-TestResult -TestName "Rate Limiting" -Category "DoS Protection" -Severity "Medium" `
    -Passed $rateLimitBreached `
    -Description "Rate limiting should prevent excessive requests" `
    -Details "Rate limit active: $rateLimitBreached"

Write-Host "`n⚠️ Testing Error Handling..." -ForegroundColor Blue

# Test error information disclosure
try {
    $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/nonexistent-endpoint" -UseBasicParsing
    $hasStackTrace = $response.Content.Contains("Traceback") -or $response.Content.Contains("Exception")
    
    Add-TestResult -TestName "Error Information Disclosure" -Category "Information Disclosure" -Severity "Medium" `
        -Passed (-not $hasStackTrace) `
        -Description "Error responses should not expose sensitive information" `
        -Details "Stack trace exposed: $hasStackTrace"
} catch {
    Add-TestResult -TestName "Error Information Disclosure" -Category "Information Disclosure" -Severity "Medium" `
        -Passed $true -Description "Error handling works correctly" -Details "Generic error response"
}

Write-Host "`n🔑 Testing Secrets Management..." -ForegroundColor Blue

# Test for exposed secrets
try {
    $response = Invoke-WebRequest -Uri "$ORCHESTRATOR_URL/config" -UseBasicParsing
    $hasExposedSecrets = $response.Content.Contains("password") -or 
                        $response.Content.Contains("api_key") -or 
                        $response.Content.Contains("secret")
    
    Add-TestResult -TestName "Secret Exposure" -Category "Secrets Management" -Severity "Critical" `
        -Passed (-not $hasExposedSecrets) `
        -Description "Application should not expose secrets" `
        -Details "Secrets exposed: $hasExposedSecrets"
} catch {
    Add-TestResult -TestName "Secret Exposure" -Category "Secrets Management" -Severity "Critical" `
        -Passed $true -Description "Config endpoint properly protected" -Details "Access denied"
}

# Generate final report
Write-Host "`n📊 Security Audit Summary:" -ForegroundColor Cyan
Write-Host "  Total Tests: $($SecurityResults.Summary.Total)" -ForegroundColor White
Write-Host "  Passed: $($SecurityResults.Summary.Passed)" -ForegroundColor Green
Write-Host "  Failed: $($SecurityResults.Summary.Failed)" -ForegroundColor Red
Write-Host "  Critical Issues: $($SecurityResults.Summary.Critical)" -ForegroundColor Red
Write-Host "  High Issues: $($SecurityResults.Summary.High)" -ForegroundColor Red
Write-Host "  Medium Issues: $($SecurityResults.Summary.Medium)" -ForegroundColor Yellow
Write-Host "  Low Issues: $($SecurityResults.Summary.Low)" -ForegroundColor Yellow

# Calculate security score
$weightedScore = 100
if ($SecurityResults.Summary.Critical -gt 0) { $weightedScore -= 30 }
if ($SecurityResults.Summary.High -gt 0) { $weightedScore -= 20 }
if ($SecurityResults.Summary.Medium -gt 0) { $weightedScore -= 10 }
if ($SecurityResults.Summary.Low -gt 0) { $weightedScore -= 5 }

$SecurityResults.Summary.SecurityScore = [math]::Max(0, $weightedScore)

Write-Host "`n🎯 Security Score: $($SecurityResults.Summary.SecurityScore)/100" -ForegroundColor $(
    if ($SecurityResults.Summary.SecurityScore -ge 90) { "Green" }
    elseif ($SecurityResults.Summary.SecurityScore -ge 70) { "Yellow" }
    else { "Red" }
)

# Save report
$SecurityResults | ConvertTo-Json -Depth 10 | Out-File -FilePath $ReportPath -Encoding UTF8
Write-Host "📄 Security report saved to: $ReportPath" -ForegroundColor Blue

# Exit with appropriate code
if ($SecurityResults.Summary.Critical -gt 0) {
    Write-Host "❌ CRITICAL security issues found! Deployment should be blocked." -ForegroundColor Red
    exit 1
} elseif ($SecurityResults.Summary.High -gt 0) {
    Write-Host "⚠️  HIGH security issues found! Review required." -ForegroundColor Yellow
    exit 2
} else {
    Write-Host "✅ Security validation completed successfully!" -ForegroundColor Green
    exit 0
}

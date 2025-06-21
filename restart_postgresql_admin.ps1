# Script PowerShell pour redémarrer PostgreSQL avec droits administrateur
# À exécuter en tant qu'administrateur

Write-Host "🔄 Redémarrage du service PostgreSQL..." -ForegroundColor Yellow

try {
    # Arrêt du service
    Write-Host "⏹️ Arrêt du service postgresql-x64-17..." -ForegroundColor Cyan
    Stop-Service -Name "postgresql-x64-17" -Force
    Start-Sleep -Seconds 3
    
    # Démarrage du service  
    Write-Host "▶️ Démarrage du service postgresql-x64-17..." -ForegroundColor Cyan
    Start-Service -Name "postgresql-x64-17"
    Start-Sleep -Seconds 2
    
    # Vérification
    $service = Get-Service -Name "postgresql-x64-17"
    if ($service.Status -eq "Running") {
        Write-Host "✅ Service PostgreSQL redémarré avec succès !" -ForegroundColor Green
        Write-Host "🔧 Configuration lc_messages = 'C' maintenant active" -ForegroundColor Green
    } else {
        Write-Host "❌ Échec du redémarrage du service" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Erreur lors du redémarrage : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Assurez-vous d'exécuter ce script en tant qu'administrateur" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Pour tester la résolution :" -ForegroundColor Cyan  
Write-Host "   python test_postgresql_utf8.py" -ForegroundColor White
Write-Host "" 
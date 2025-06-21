@echo off
REM ====================================================================
REM 🎖️ LANCEMENT TRANSMISSION MISSION - CHEF D'ÉQUIPE DE MAINTENANCE
REM ====================================================================
REM
REM 🎯 Mission : Exécuter la transmission de mission au Chef d'Équipe
REM             pour prise en charge des agents experts
REM
REM 📊 Contexte : TaskMaster NextGeneration - Maintenance Automatisée
REM
REM Author: Assistant IA - Script de lancement
REM Created: 2025-01-21
REM ====================================================================

echo.
echo ===============================================================================
echo 🎖️ TASKMASTER NEXTGENERATION - TRANSMISSION MISSION CHEF D'EQUIPE
echo ===============================================================================
echo.
echo 🎯 Préparation de la transmission de mission au Chef d'Équipe de Maintenance
echo 📂 Répertoire cible: agent_factory_experts_team
echo ⏱️  Début: %date% %time%
echo.

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou accessible
    echo 💡 Veuillez installer Python 3.8+ et l'ajouter au PATH
    pause
    exit /b 1
)

REM Vérification du fichier de transmission
if not exist "transmission_mission_chef_equipe_maintenance.py" (
    echo ❌ ERREUR: Fichier transmission_mission_chef_equipe_maintenance.py introuvable
    echo 💡 Vérifiez que vous êtes dans le bon répertoire
    pause
    exit /b 1
)

REM Vérification de l'équipe de maintenance
if not exist "20250620_transformation_equipe_maintenance\agent_equipe_maintenance" (
    echo ❌ ERREUR: Équipe de maintenance introuvable
    echo 💡 Vérifiez la structure du projet
    pause
    exit /b 1
)

REM Vérification des agents experts
if not exist "agent_factory_experts_team" (
    echo ❌ ERREUR: Répertoire agent_factory_experts_team introuvable
    echo 💡 Vérifiez la structure du projet
    pause
    exit /b 1
)

echo ✅ Vérifications préliminaires réussies
echo.
echo 🚀 LANCEMENT DE LA TRANSMISSION...
echo.

REM Exécution du script de transmission
python "transmission_mission_chef_equipe_maintenance.py"

REM Vérification du résultat
if errorlevel 1 (
    echo.
    echo ❌ ERREUR lors de l'exécution de la transmission
    echo 🔍 Consultez les messages d'erreur ci-dessus
) else (
    echo.
    echo ✅ TRANSMISSION TERMINÉE AVEC SUCCÈS
    echo 📋 Consultez les fichiers de mission et résultats générés
)

echo.
echo ⏱️  Fin: %date% %time%
echo ===============================================================================
echo.

pause

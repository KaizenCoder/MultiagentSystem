@echo off
echo 🎮 Surveillance Continue RTX3090 - NextGeneration
echo Démarrage monitoring automatique...

:loop
echo [%DATE% %TIME%] Lancement monitoring RTX3090
python monitor_rtx3090.py --duration 300 --interval 5
echo [%DATE% %TIME%] Monitoring terminé, pause 30s
timeout /t 30 /nobreak >nul
goto loop

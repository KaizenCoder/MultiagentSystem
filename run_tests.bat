@echo off
setlocal

rem Configuration environnement
set PYTHONPATH=%~dp0
set TEST_ENV=validation
set LOG_LEVEL=INFO

rem Exécution des tests
python -m pytest test_agent_05_migration.py -v 
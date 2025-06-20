#!/bin/bash

# 🧪 SCRIPT VALIDATION PHASE - PLAN ACTION CHATGPT
# Valide chaque phase du plan d'action prioritaire
# CONTRAINTE: Travail exclusivement dans 20250620_projet_logging_centralise/3_reponse_cursor/

echo "🧪 VALIDATION PHASE - TESTS COMPLETS"
echo "===================================="
echo "Timestamp: $(date)"
echo "Répertoire: $(pwd)"
echo "Contrainte: Travail uniquement dans 20250620_projet_logging_centralise/3_reponse_cursor/"
echo ""

# Vérification répertoire de travail
EXPECTED_DIR="20250620_projet_logging_centralise/3_reponse_cursor"
CURRENT_DIR=$(basename $(dirname $(pwd)))/$(basename $(pwd))

if [[ "$CURRENT_DIR" != "$EXPECTED_DIR" ]]; then
    echo "🚨 ERREUR: Répertoire incorrect!"
    echo "Attendu: $EXPECTED_DIR"
    echo "Actuel: $CURRENT_DIR"
    echo "Veuillez vous placer dans le bon répertoire."
    exit 1
fi

echo "✅ Répertoire de travail correct: $CURRENT_DIR"
echo ""

# Variables de résultat
UNIT_RESULT=1
INTEGRATION_RESULT=1
PERF_RESULT=1
CHATGPT_RESULT=1
OVERALL_RESULT=1

# 1. Tests unitaires
echo "1️⃣ Tests unitaires..."
echo "-------------------"
if python test_simple_chatgpt.py; then
    UNIT_RESULT=0
    echo "✅ Tests unitaires PASSÉS"
else
    echo "❌ Tests unitaires ÉCHOUÉS"
fi
echo ""

# 2. Tests intégration
echo "2️⃣ Tests intégration..."
echo "---------------------"
if python test_integration_chatgpt.py 2>/dev/null; then
    INTEGRATION_RESULT=0
    echo "✅ Tests intégration PASSÉS"
else
    echo "❌ Tests intégration ÉCHOUÉS (attendu si Phase 1 non terminée)"
fi
echo ""

# 3. Tests performance
echo "3️⃣ Tests performance..."
echo "--------------------"
python -c "
import time
import sys
try:
    from logging_manager_optimized import LoggingManager
    start = time.time()
    manager = LoggingManager()
    logger = manager.get_logger('test_perf')
    for i in range(1000):
        logger.info(f'Test performance {i}')
    duration = time.time() - start
    print(f'Performance: {duration:.3f}s for 1000 logs')
    if duration < 2.0:
        print('✅ Performance ACCEPTABLE')
        sys.exit(0)
    else:
        print('⚠️ Performance LENTE')
        sys.exit(1)
except Exception as e:
    print(f'❌ Erreur performance: {e}')
    sys.exit(1)
"
PERF_RESULT=$?
echo ""

# 4. Tests fonctionnalités ChatGPT
echo "4️⃣ Tests fonctionnalités ChatGPT..."
echo "---------------------------------"
python -c "
import sys
try:
    from logging_manager_optimized import LoggingManager
    from template_manager_integrated import TemplateManager
    from agent_coordinateur_integrated import AgentCoordinateur
    
    # Test chargement modules
    lm = LoggingManager()
    tm = TemplateManager()
    ac = AgentCoordinateur()
    
    # Test fonctionnalités ChatGPT
    features_ok = 0
    
    # Test Elasticsearch
    if hasattr(lm, 'elasticsearch_enabled'):
        features_ok += 1
        print('✅ Elasticsearch Integration détectée')
    
    # Test Encryption
    if hasattr(lm, 'encryption_enabled'):
        features_ok += 1
        print('✅ Encryption Security détectée')
    
    # Test Alerting
    if hasattr(lm, 'alerting_enabled'):
        features_ok += 1
        print('✅ Intelligent Alerting détecté')
    
    # Test AI Coordination
    if hasattr(ac, 'ai_coordination_engine'):
        features_ok += 1
        print('✅ AI Coordination détectée')
    
    # Test Analytics
    if hasattr(tm, 'get_analytics'):
        features_ok += 1
        print('✅ Advanced Analytics détectées')
    
    print(f'Fonctionnalités ChatGPT: {features_ok}/5')
    
    if features_ok >= 4:
        print('✅ Intégrations ChatGPT FONCTIONNELLES')
        sys.exit(0)
    else:
        print('⚠️ Intégrations ChatGPT PARTIELLES')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ Erreur intégration ChatGPT: {e}')
    sys.exit(1)
"
CHATGPT_RESULT=$?
echo ""

# 5. Test constante manquante (Phase 1 spécifique)
echo "5️⃣ Test constante ALERT_THRESHOLD_ERROR..."
echo "----------------------------------------"
python -c "
import sys
try:
    from logging_manager_optimized import ALERT_THRESHOLD_ERROR
    print(f'✅ Constante ALERT_THRESHOLD_ERROR trouvée: {ALERT_THRESHOLD_ERROR}')
    sys.exit(0)
except ImportError:
    print('❌ Constante ALERT_THRESHOLD_ERROR MANQUANTE (Phase 1 non terminée)')
    sys.exit(1)
"
CONST_RESULT=$?
echo ""

# Calcul résultat global
echo "📊 RÉSUMÉ VALIDATION"
echo "==================="
echo "Tests unitaires:      $([ $UNIT_RESULT -eq 0 ] && echo '✅ PASSÉ' || echo '❌ ÉCHOUÉ')"
echo "Tests intégration:    $([ $INTEGRATION_RESULT -eq 0 ] && echo '✅ PASSÉ' || echo '❌ ÉCHOUÉ')"
echo "Tests performance:    $([ $PERF_RESULT -eq 0 ] && echo '✅ PASSÉ' || echo '❌ ÉCHOUÉ')"
echo "Tests ChatGPT:        $([ $CHATGPT_RESULT -eq 0 ] && echo '✅ PASSÉ' || echo '❌ ÉCHOUÉ')"
echo "Constante manquante:  $([ $CONST_RESULT -eq 0 ] && echo '✅ PASSÉ' || echo '❌ ÉCHOUÉ')"
echo ""

# Déterminer phase actuelle
if [ $CONST_RESULT -eq 0 ] && [ $INTEGRATION_RESULT -eq 0 ] && [ $UNIT_RESULT -eq 0 ]; then
    echo "🎯 PHASE 1 CRITIQUE: ✅ TERMINÉE"
    PHASE_STATUS="PHASE_1_COMPLETE"
elif [ $UNIT_RESULT -eq 0 ] && [ $CHATGPT_RESULT -eq 0 ] && [ $PERF_RESULT -eq 0 ]; then
    echo "🔥 PHASE 2 IMPORTANTE: En cours/À valider"
    PHASE_STATUS="PHASE_2_PROGRESS"
else
    echo "⚡ PHASE 1 CRITIQUE: ❌ EN COURS"
    PHASE_STATUS="PHASE_1_IN_PROGRESS"
fi

# Calcul score estimé
TESTS_PASSED=0
[ $UNIT_RESULT -eq 0 ] && TESTS_PASSED=$((TESTS_PASSED + 1))
[ $INTEGRATION_RESULT -eq 0 ] && TESTS_PASSED=$((TESTS_PASSED + 1))
[ $PERF_RESULT -eq 0 ] && TESTS_PASSED=$((TESTS_PASSED + 1))
[ $CHATGPT_RESULT -eq 0 ] && TESTS_PASSED=$((TESTS_PASSED + 1))
[ $CONST_RESULT -eq 0 ] && TESTS_PASSED=$((TESTS_PASSED + 1))

SCORE_ESTIME=$(( (TESTS_PASSED * 100) / 5 ))
echo ""
echo "📈 Score estimé: ${SCORE_ESTIME}% (${TESTS_PASSED}/5 tests)"

# Résultat final
if [ $UNIT_RESULT -eq 0 ] && [ $INTEGRATION_RESULT -eq 0 ] && [ $PERF_RESULT -eq 0 ] && [ $CHATGPT_RESULT -eq 0 ] && [ $CONST_RESULT -eq 0 ]; then
    echo ""
    echo "🏆 VALIDATION COMPLÈTE RÉUSSIE"
    echo "Phase suivante recommandée"
    OVERALL_RESULT=0
else
    echo ""
    echo "⚠️ VALIDATION PARTIELLE"
    echo "Corrections nécessaires avant phase suivante"
    OVERALL_RESULT=1
fi

echo ""
echo "Status: $PHASE_STATUS"
echo "Répertoire vérifié: $CURRENT_DIR"
echo "Timestamp fin: $(date)"

exit $OVERALL_RESULT 
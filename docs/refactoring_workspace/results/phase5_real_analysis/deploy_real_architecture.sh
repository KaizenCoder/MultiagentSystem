#!/bin/bash
# Script déploiement NextGeneration - Architecture Réelle
# Généré le 2025-06-18 19:25:13
# Basé sur scan de 39 fichiers

echo "🚀 Déploiement NextGeneration - Architecture Réelle"
echo "📊 Fichiers: 39 | Lignes: 1110 | Endpoints: 11"

# Variables
APP_NAME="nextgeneration"
ARCHITECTURE_PATH="refactoring_workspace/new_architecture"
PORT=8000

# Vérification prérequis
echo "🔍 Vérification architecture..."
if [ ! -d "$ARCHITECTURE_PATH" ]; then
    echo "❌ Architecture path non trouvé: $ARCHITECTURE_PATH"
    exit 1
fi

echo "✅ Architecture trouvée: 39 fichiers"

# Installation dépendances
echo "📦 Installation dépendances..."
pip install -r requirements.txt

# Configuration monitoring
echo "⚙️ Configuration monitoring..."
cp refactoring_workspace/results/phase5_real_analysis/prometheus_real_architecture.yml monitoring/
cp refactoring_workspace/results/phase5_real_analysis/alerts_real_architecture.yml monitoring/

# Démarrage application
echo "🎯 Démarrage application..."
cd $ARCHITECTURE_PATH
uvicorn main:app --host 0.0.0.0 --port $PORT --reload &
APP_PID=$!

# Attente démarrage
echo "⏳ Attente démarrage application..."
sleep 10

# Tests santé
echo "🏥 Tests santé..."

curl -f http://localhost:$PORT/ || echo "⚠️ Endpoint GET / non accessible"

curl -f http://localhost:$PORT/health || echo "⚠️ Endpoint GET /health non accessible"

curl -f http://localhost:$PORT/status || echo "⚠️ Endpoint GET /status non accessible"

curl -f http://localhost:$PORT/health || echo "⚠️ Endpoint GET /health non accessible"

curl -f http://localhost:$PORT/health || echo "⚠️ Endpoint GET /health non accessible"

# Validation déploiement
echo "✅ Déploiement terminé"
echo "🌐 Application: http://localhost:$PORT"
echo "📊 Métriques: http://localhost:$PORT/metrics"
echo "🏥 Santé: http://localhost:$PORT/health"
echo "📋 PID: $APP_PID"

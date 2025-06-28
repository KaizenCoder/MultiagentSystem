#!/usr/bin/env bash
# Script de test des APIs de l'orchestrateur

echo "🧪 TESTS DES APIS ORCHESTRATEUR"
echo "================================"

API_BASE="http://localhost:8002"
API_KEY="demo-key-for-testing"

echo "📍 Base URL: $API_BASE"
echo "🔑 API Key: $API_KEY"
echo ""

# Test 1: Health Check
echo "1️⃣ Test Health Check"
curl -X GET "$API_BASE/health" \
  -H "Accept: application/json" \
  | python -m json.tool
echo -e "\n"

# Test 2: Documentation
echo "2️⃣ Test Documentation disponible"
curl -s -o /dev/null -w "%{http_code}" "$API_BASE/docs"
echo " - Documentation Swagger"
echo ""

# Test 3: OpenAPI Schema
echo "3️⃣ Test OpenAPI Schema"
curl -X GET "$API_BASE/openapi.json" \
  -H "Accept: application/json" \
  | python -c "import json, sys; data=json.load(sys.stdin); print(f'📋 Titre: {data.get(\"info\", {}).get(\"title\", \"N/A\")}'); print(f'📋 Version: {data.get(\"info\", {}).get(\"version\", \"N/A\")}'); print(f'📋 Endpoints: {len(data.get(\"paths\", {}))}')"
echo ""

echo "✅ Tests de base terminés!"
echo "💡 Utilisez les scripts Python pour des tests plus avancés"

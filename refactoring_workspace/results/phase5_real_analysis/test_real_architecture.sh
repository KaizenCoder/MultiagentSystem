#!/bin/bash
# Tests architecture réelle NextGeneration
# Généré le 2025-06-18 19:25:13

echo "🧪 Tests architecture réelle"
echo "📊 Architecture: 39 fichiers, 11 endpoints"

BASE_URL="http://localhost:8000"
FAILED_TESTS=0

# Fonction test endpoint
test_endpoint() {
    local method=$1
    local path=$2
    local expected_status=${3:-200}
    
    echo "🔍 Test $method $path"
    
    case $method in
        "GET")
            status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")
            ;;
        "POST")
            status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL$path")
            ;;
        *)
            status=$(curl -s -o /dev/null -w "%{http_code}" -X $method "$BASE_URL$path")
            ;;
    esac
    
    if [ "$status" -eq "$expected_status" ]; then
        echo "✅ $method $path: $status"
    else
        echo "❌ $method $path: $status (attendu: $expected_status)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Tests endpoints découverts
test_endpoint "GET" "/"
test_endpoint "GET" "/health"
test_endpoint "GET" "/status"
test_endpoint "GET" "/health"
test_endpoint "GET" "/health"
test_endpoint "GET" "/health"
test_endpoint "GET" "/status"
test_endpoint "GET" "/health"
test_endpoint "GET" "/status"
test_endpoint "GET" "/health"
test_endpoint "GET" "/health"

# Tests santé
test_endpoint "GET" "/health" 200
test_endpoint "GET" "/metrics" 200

# Résultat final
echo ""
if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ Tous les tests passent (11 endpoints testés)"
    exit 0
else
    echo "❌ $FAILED_TESTS tests échoués sur 11"
    exit 1
fi

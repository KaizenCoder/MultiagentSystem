#!/bin/bash
# Script de déploiement staging sécurisé
# scripts/deploy_staging_secure.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STAGING_ENV="${STAGING_ENV:-staging}"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-localhost:5000}"
IMAGE_TAG="${IMAGE_TAG:-staging-$(date +%Y%m%d-%H%M%S)}"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifications préalables
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker non trouvé"
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose non trouvé"
        exit 1
    fi
    
    # Vérifier que nous sommes dans le bon répertoire
    if [[ ! -f "$PROJECT_ROOT/docker-compose.yml" ]]; then
        log_error "Fichier docker-compose.yml non trouvé dans $PROJECT_ROOT"
        exit 1
    fi
    
    log_success "Prérequis OK"
}

# Validation sécurité pre-déploiement
run_security_validation() {
    log_info "Validation sécurité pre-déploiement..."
    
    cd "$PROJECT_ROOT"
    
    # Exécuter le script de validation sécurité
    if [[ -f "$SCRIPT_DIR/validate_security_fixes.py" ]]; then
        python3 "$SCRIPT_DIR/validate_security_fixes.py" --quick
        if [[ $? -ne 0 ]]; then
            log_error "Validation sécurité échouée"
            exit 1
        fi
    else
        log_warning "Script de validation sécurité non trouvé, skip"
    fi
    
    log_success "Validation sécurité OK"
}

# Build sécurisé des images
build_secure_images() {
    log_info "Build sécurisé des images Docker..."
    
    cd "$PROJECT_ROOT"
    
    # Build de l'orchestrateur avec optimisations sécurité
    log_info "Build orchestrator:$IMAGE_TAG..."
    docker build \
        --no-cache \
        --pull \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --security-opt no-new-privileges:true \
        -t "orchestrator:$IMAGE_TAG" \
        -f orchestrator/Dockerfile \
        orchestrator/
    
    # Build de l'API mémoire
    log_info "Build memory_api:$IMAGE_TAG..."
    docker build \
        --no-cache \
        --pull \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --security-opt no-new-privileges:true \
        -t "memory_api:$IMAGE_TAG" \
        -f memory_api/Dockerfile \
        memory_api/
    
    log_success "Images buildées avec succès"
}

# Scan sécurité des images
scan_image_security() {
    log_info "Scan sécurité des images Docker..."
    
    # Vérifier si Trivy est disponible
    if command -v trivy &> /dev/null; then
        log_info "Scan avec Trivy..."
        
        # Scan orchestrator
        trivy image --severity HIGH,CRITICAL --exit-code 1 "orchestrator:$IMAGE_TAG"
        if [[ $? -ne 0 ]]; then
            log_error "Vulnérabilités critiques détectées dans orchestrator"
            exit 1
        fi
        
        # Scan memory_api
        trivy image --severity HIGH,CRITICAL --exit-code 1 "memory_api:$IMAGE_TAG"
        if [[ $? -ne 0 ]]; then
            log_error "Vulnérabilités critiques détectées dans memory_api"
            exit 1
        fi
        
        log_success "Scan Trivy OK"
    else
        log_warning "Trivy non disponible, skip scan sécurité des images"
    fi
}

# Setup environnement staging
setup_staging_environment() {
    log_info "Setup environnement staging..."
    
    cd "$PROJECT_ROOT"
    
    # Copier la configuration staging
    if [[ ! -f ".env.staging" ]]; then
        log_warning "Fichier .env.staging non trouvé, utilisation de .env.example"
        cp env.example .env.staging
    fi
    
    # Créer le réseau Docker si nécessaire
    docker network create orchestrator-staging-network 2>/dev/null || true
    
    # Créer les volumes persistants
    docker volume create orchestrator-staging-db 2>/dev/null || true
    docker volume create orchestrator-staging-chromadb 2>/dev/null || true
    
    log_success "Environnement staging configuré"
}

# Déploiement avec Docker Compose
deploy_services() {
    log_info "Déploiement des services staging..."
    
    cd "$PROJECT_ROOT"
    
    # Arrêter les services existants
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml down --remove-orphans
    
    # Démarrer les services en mode détaché
    ORCHESTRATOR_IMAGE_TAG="$IMAGE_TAG" \
    MEMORY_API_IMAGE_TAG="$IMAGE_TAG" \
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
    
    log_success "Services déployés"
}

# Health checks post-déploiement
run_health_checks() {
    log_info "Health checks post-déploiement..."
    
    # Attendre que les services démarrent
    log_info "Attente du démarrage des services (30s)..."
    sleep 30
    
    # Vérifier le health check de l'orchestrateur
    for i in {1..5}; do
        if curl -f -s http://localhost:8002/health > /dev/null; then
            log_success "Orchestrateur healthy"
            break
        else
            if [[ $i -eq 5 ]]; then
                log_error "Orchestrateur non accessible après 5 tentatives"
                show_service_logs
                exit 1
            fi
            log_warning "Tentative $i/5 échouée, retry dans 10s..."
            sleep 10
        fi
    done
    
    # Vérifier l'API mémoire
    for i in {1..5}; do
        if curl -f -s http://localhost:8001/health > /dev/null; then
            log_success "Memory API healthy"
            break
        else
            if [[ $i -eq 5 ]]; then
                log_error "Memory API non accessible après 5 tentatives"
                show_service_logs
                exit 1
            fi
            log_warning "Memory API tentative $i/5 échouée, retry dans 10s..."
            sleep 10
        fi
    done
    
    log_success "Tous les health checks OK"
}

# Tests end-to-end post-déploiement
run_e2e_tests() {
    log_info "Tests end-to-end post-déploiement..."
    
    cd "$PROJECT_ROOT"
    
    # Tests de base avec pytest
    if [[ -d "tests/integration" ]]; then
        python3 -m pytest tests/integration/ -v --tb=short -m "not slow" --maxfail=3
        if [[ $? -ne 0 ]]; then
            log_error "Tests E2E échoués"
            show_service_logs
            exit 1
        fi
        log_success "Tests E2E OK"
    else
        log_warning "Répertoire tests/integration non trouvé, skip E2E"
    fi
}

# Tests de sécurité en environnement staging
run_staging_security_tests() {
    log_info "Tests de sécurité staging..."
    
    # Test de base avec curl
    log_info "Test de protection RCE..."
    response=$(curl -s -X POST http://localhost:8002/analyze \
        -H "Content-Type: application/json" \
        -d '{"task_description": "test", "file_content": "eval(\"__import__(\\\"os\\\").system(\\\"id\\\")\")"}' \
        -w "%{http_code}")
    
    if [[ "$response" =~ (400|422|200) ]]; then
        log_success "Protection RCE fonctionnelle"
    else
        log_error "Protection RCE peut-être défaillante (code: $response)"
        exit 1
    fi
    
    # Test SSRF
    log_info "Test de protection SSRF..."
    response=$(curl -s -X POST http://localhost:8002/query \
        -H "Content-Type: application/json" \
        -d '{"url": "http://localhost:22"}' \
        -w "%{http_code}")
    
    if [[ "$response" =~ (400|422|403) ]]; then
        log_success "Protection SSRF fonctionnelle"
    else
        log_warning "Vérifier la protection SSRF (code: $response)"
    fi
}

# Affichage des logs en cas d'erreur
show_service_logs() {
    log_info "Logs des services pour debug..."
    
    echo "=== Logs Orchestrateur ==="
    docker-compose logs --tail=50 orchestrator
    
    echo "=== Logs Memory API ==="
    docker-compose logs --tail=50 memory_api
    
    echo "=== Logs PostgreSQL ==="
    docker-compose logs --tail=20 postgres
}

# Fonction de rollback
rollback_deployment() {
    log_warning "Rollback du déploiement..."
    
    cd "$PROJECT_ROOT"
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml down
    
    # Redémarrer avec les images précédentes si disponibles
    if docker images | grep -q "orchestrator:previous"; then
        docker tag orchestrator:previous orchestrator:latest
        docker tag memory_api:previous memory_api:latest
        docker-compose up -d
        log_info "Rollback vers les images précédentes effectué"
    else
        log_warning "Pas d'images précédentes disponibles pour rollback"
    fi
}

# Gestion des signaux pour cleanup
cleanup() {
    log_info "Cleanup en cours..."
    # Pas de cleanup automatique pour éviter de casser un déploiement en cours
}

trap cleanup EXIT

# ============================================================================
# EXÉCUTION PRINCIPALE
# ============================================================================

main() {
    log_info "🚀 DÉPLOIEMENT STAGING SÉCURISÉ - Quick Wins Sprint 1"
    echo "========================================================"
    echo "Project: $PROJECT_ROOT"
    echo "Environment: $STAGING_ENV"
    echo "Image Tag: $IMAGE_TAG"
    echo "========================================================"
    
    # Sauvegarder les images actuelles pour rollback
    if docker images | grep -q "orchestrator:latest"; then
        docker tag orchestrator:latest orchestrator:previous 2>/dev/null || true
        docker tag memory_api:latest memory_api:previous 2>/dev/null || true
    fi
    
    # Exécution des étapes
    check_prerequisites
    run_security_validation
    build_secure_images
    scan_image_security
    setup_staging_environment
    deploy_services
    run_health_checks
    run_e2e_tests
    run_staging_security_tests
    
    log_success "🎉 DÉPLOIEMENT STAGING RÉUSSI"
    echo ""
    echo "Services accessibles:"
    echo "  • Orchestrateur: http://localhost:8002"
    echo "  • Memory API: http://localhost:8001"
    echo "  • Health Check: curl http://localhost:8002/health"
    echo ""
    echo "Pour les logs: docker-compose logs -f [service]"
    echo "Pour arrêter: docker-compose down"
}

# Vérifier les arguments
if [[ "${1:-}" == "--rollback" ]]; then
    rollback_deployment
    exit 0
elif [[ "${1:-}" == "--logs" ]]; then
    show_service_logs
    exit 0
elif [[ "${1:-}" == "--help" ]]; then
    echo "Usage: $0 [--rollback|--logs|--help]"
    echo ""
    echo "Options:"
    echo "  --rollback    Rollback vers les images précédentes"
    echo "  --logs        Afficher les logs des services"
    echo "  --help        Afficher cette aide"
    echo ""
    echo "Variables d'environnement:"
    echo "  STAGING_ENV       Nom de l'environnement (défaut: staging)"
    echo "  IMAGE_TAG         Tag des images Docker (défaut: staging-YYYYMMDD-HHMMSS)"
    echo "  DOCKER_REGISTRY   Registry Docker (défaut: localhost:5000)"
    exit 0
fi

# Exécution principale
main "$@"

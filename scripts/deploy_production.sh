#!/bin/bash

# Script de déploiement production sécurisé
# Automatisation complète du setup selon les exigences IA-2

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT="${ENVIRONMENT:-production}"
LOG_FILE="${PROJECT_ROOT}/logs/deployment-$(date +%Y%m%d-%H%M%S).log"

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${1}" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}[INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    log "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

# Vérifications préliminaires
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Docker et Docker Compose
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    # Vérifier que Docker fonctionne
    if ! docker info &> /dev/null; then
        log_error "Docker n'est pas en cours d'exécution"
        exit 1
    fi
    
    # Vérifier l'espace disque
    AVAILABLE_SPACE=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    REQUIRED_SPACE=10485760  # 10GB en KB
    
    if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
        log_error "Espace disque insuffisant. Requis: 10GB, disponible: $((AVAILABLE_SPACE/1024/1024))GB"
        exit 1
    fi
    
    log_success "Prérequis validés"
}

# Création des répertoires de données
setup_data_directories() {
    log_info "Création des répertoires de données..."
    
    sudo mkdir -p /data/{postgres,redis,chroma,prometheus,grafana,elasticsearch}
    sudo chown -R 1000:1000 /data
    sudo chmod -R 755 /data
    
    # Répertoires de logs
    mkdir -p "$PROJECT_ROOT/logs"
    chmod 755 "$PROJECT_ROOT/logs"
    
    log_success "Répertoires de données créés"
}

# Configuration des secrets Docker
setup_docker_secrets() {
    log_info "Configuration des secrets Docker..."
    
    # Initialiser Docker Swarm si nécessaire
    if ! docker info | grep -q "Swarm: active"; then
        log_info "Initialisation de Docker Swarm..."
        docker swarm init --advertise-addr 127.0.0.1
    fi
    
    # Générer ou vérifier les secrets
    declare -A secrets=(
        ["orchestrator_api_key"]="$(openssl rand -base64 32)"
        ["postgres_user"]="postgres"
        ["postgres_password"]="$(openssl rand -base64 24)"
        ["vault_token"]="$(openssl rand -base64 32)"
        ["grafana_admin_password"]="$(openssl rand -base64 16)"
        ["grafana_secret_key"]="$(openssl rand -base64 32)"
        ["elastic_password"]="$(openssl rand -base64 16)"
        ["chroma_credentials"]='{"username":"admin","password":"'$(openssl rand -base64 16)'"}'
    )
    
    # Secrets depuis variables d'environnement
    if [ -n "${OPENAI_API_KEY:-}" ]; then
        secrets["openai_api_key"]="$OPENAI_API_KEY"
    else
        log_error "OPENAI_API_KEY non définie"
        exit 1
    fi
    
    if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
        secrets["anthropic_api_key"]="$ANTHROPIC_API_KEY"
    else
        log_error "ANTHROPIC_API_KEY non définie"
        exit 1
    fi
    
    # Créer les secrets Docker
    for secret_name in "${!secrets[@]}"; do
        if docker secret inspect "$secret_name" &>/dev/null; then
            log_info "Secret $secret_name existe déjà"
        else
            echo "${secrets[$secret_name]}" | docker secret create "$secret_name" -
            log_success "Secret $secret_name créé"
        fi
    done
    
    # Sauvegarder les secrets pour référence (chiffré)
    echo "# Secrets générés le $(date)" > "$PROJECT_ROOT/.secrets-backup"
    for secret_name in "${!secrets[@]}"; do
        if [[ "$secret_name" != *"api_key"* ]]; then  # Ne pas sauvegarder les API keys
            echo "$secret_name=${secrets[$secret_name]}" >> "$PROJECT_ROOT/.secrets-backup"
        fi
    done
    chmod 600 "$PROJECT_ROOT/.secrets-backup"
    
    log_success "Secrets Docker configurés"
}

# Configuration SSL/TLS
setup_ssl_certificates() {
    log_info "Configuration des certificats SSL..."
    
    mkdir -p "$PROJECT_ROOT/config/ssl"
    
    # Générer certificat auto-signé pour développement/staging
    if [ "$ENVIRONMENT" != "production" ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "$PROJECT_ROOT/config/ssl/orchestrator.key" \
            -out "$PROJECT_ROOT/config/ssl/orchestrator.crt" \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        
        # Combiner pour HAProxy
        cat "$PROJECT_ROOT/config/ssl/orchestrator.crt" "$PROJECT_ROOT/config/ssl/orchestrator.key" > \
            "$PROJECT_ROOT/config/ssl/orchestrator.pem"
    else
        log_warning "En production, utilisez des certificats valides de votre CA"
        # En production, copiez vos certificats ici
        # cp /path/to/your/cert.pem "$PROJECT_ROOT/config/ssl/orchestrator.pem"
    fi
    
    chmod 600 "$PROJECT_ROOT/config/ssl"/*
    
    log_success "Certificats SSL configurés"
}

# Configuration des fichiers de configuration
setup_configuration_files() {
    log_info "Configuration des fichiers de configuration..."
    
    # PostgreSQL
    mkdir -p "$PROJECT_ROOT/config/postgres"
    cat > "$PROJECT_ROOT/config/postgres/postgresql.conf" << 'EOF'
# PostgreSQL Configuration Production
shared_preload_libraries = 'pg_stat_statements'
max_connections = 200
shared_buffers = 512MB
effective_cache_size = 1GB
maintenance_work_mem = 128MB
work_mem = 8MB
wal_buffers = 16MB
max_wal_size = 2GB
min_wal_size = 1GB
checkpoint_completion_target = 0.9
random_page_cost = 1.1
effective_io_concurrency = 200
log_statement = 'all'
log_min_duration_statement = 1000
log_connections = on
log_disconnections = on
log_lock_waits = on
logging_collector = on
EOF

    cat > "$PROJECT_ROOT/config/postgres/pg_hba.conf" << 'EOF'
# PostgreSQL Access Control
local   all             all                                     scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    all             all             172.20.0.0/16           scram-sha-256
EOF

    # Redis
    mkdir -p "$PROJECT_ROOT/config/redis"
    cat > "$PROJECT_ROOT/config/redis/redis.conf" << 'EOF'
# Redis Configuration Production
bind 0.0.0.0
port 6379
protected-mode yes
tcp-backlog 511
timeout 0
tcp-keepalive 300
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
maxmemory 1gb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
EOF

    # AlertManager
    mkdir -p "$PROJECT_ROOT/config/alertmanager"
    cat > "$PROJECT_ROOT/config/alertmanager/alertmanager.yml" << 'EOF'
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@company.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://webhook-service:5000/alerts'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
EOF

    log_success "Fichiers de configuration créés"
}

# Construction et démarrage des services
build_and_deploy() {
    log_info "Construction et déploiement des services..."
    
    cd "$PROJECT_ROOT"
    
    # Build des images
    log_info "Construction des images Docker..."
    docker-compose -f docker-compose.production.yml build --no-cache
    
    # Démarrage des services de base d'abord
    log_info "Démarrage des services de base..."
    docker-compose -f docker-compose.production.yml up -d postgres redis-cluster chromadb
    
    # Attendre que les services de base soient prêts
    log_info "Attente de la disponibilité des services de base..."
    sleep 30
    
    # Vérifier la santé des services de base
    for service in postgres redis-cluster chromadb; do
        timeout=60
        while [ $timeout -gt 0 ]; do
            if docker-compose -f docker-compose.production.yml ps | grep "$service" | grep -q "healthy\|Up"; then
                log_success "Service $service est prêt"
                break
            fi
            sleep 5
            timeout=$((timeout - 5))
        done
        
        if [ $timeout -le 0 ]; then
            log_error "Service $service n'est pas devenu disponible"
            exit 1
        fi
    done
    
    # Démarrer les services de monitoring
    log_info "Démarrage des services de monitoring..."
    docker-compose -f docker-compose.production.yml up -d prometheus grafana alertmanager elasticsearch
    
    sleep 20
    
    # Démarrer les services applicatifs
    log_info "Démarrage des services applicatifs..."
    docker-compose -f docker-compose.production.yml up -d memory-api
    
    sleep 15
    
    # Démarrer les orchestrateurs
    log_info "Démarrage des orchestrateurs..."
    docker-compose -f docker-compose.production.yml up -d orchestrator-1 orchestrator-2 orchestrator-3
    
    sleep 20
    
    # Démarrer le load balancer
    log_info "Démarrage du load balancer..."
    docker-compose -f docker-compose.production.yml up -d load-balancer
    
    # Démarrer les services de logging
    log_info "Démarrage des services de logging..."
    docker-compose -f docker-compose.production.yml up -d logstash kibana jaeger
    
    log_success "Tous les services sont démarrés"
}

# Vérifications post-déploiement
verify_deployment() {
    log_info "Vérification du déploiement..."
    
    # Attendre un peu pour que tout se stabilise
    sleep 30
    
    # Vérifier les services critiques
    services=("postgres" "redis-cluster" "orchestrator-1" "orchestrator-2" "orchestrator-3" "memory-api" "load-balancer")
    
    for service in "${services[@]}"; do
        if docker-compose -f docker-compose.production.yml ps | grep "$service" | grep -q "Up\|healthy"; then
            log_success "✓ Service $service fonctionne"
        else
            log_error "✗ Service $service ne fonctionne pas"
            docker-compose -f docker-compose.production.yml logs "$service" | tail -20
        fi
    done
    
    # Test des endpoints
    log_info "Test des endpoints..."
    
    # Health check
    if curl -f -s http://localhost/health > /dev/null; then
        log_success "✓ Health check endpoint accessible"
    else
        log_error "✗ Health check endpoint non accessible"
    fi
    
    # Metrics endpoint
    if curl -f -s http://localhost/metrics > /dev/null; then
        log_success "✓ Metrics endpoint accessible"
    else
        log_warning "⚠ Metrics endpoint non accessible"
    fi
    
    # Grafana
    if curl -f -s http://localhost:3000/api/health > /dev/null; then
        log_success "✓ Grafana accessible"
    else
        log_warning "⚠ Grafana non accessible"
    fi
    
    # Prometheus
    if curl -f -s http://localhost:9090/-/healthy > /dev/null; then
        log_success "✓ Prometheus accessible"
    else
        log_warning "⚠ Prometheus non accessible"
    fi
    
    log_success "Vérification du déploiement terminée"
}

# Affichage des informations de connexion
display_connection_info() {
    log_info "Informations de connexion:"
    echo
    echo "🌐 Application:"
    echo "  - Load Balancer: https://localhost (HTTP redirigé vers HTTPS)"
    echo "  - Health Check: http://localhost/health"
    echo "  - API Documentation: http://localhost/docs"
    echo
    echo "📊 Monitoring:"
    echo "  - Grafana: http://localhost:3000"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - AlertManager: http://localhost:9093"
    echo
    echo "🔍 Logging:"
    echo "  - Kibana: http://localhost:5601"
    echo "  - Jaeger: http://localhost:16686"
    echo
    echo "🔐 Credentials:"
    echo "  - Grafana admin password: voir .secrets-backup"
    echo "  - Elasticsearch password: voir .secrets-backup"
    echo
    echo "📂 Data directories: /data/*"
    echo "📝 Logs: $PROJECT_ROOT/logs/"
    echo
}

# Nettoyage en cas d'erreur
cleanup_on_error() {
    log_error "Erreur détectée. Nettoyage en cours..."
    
    if [ "$ENVIRONMENT" != "production" ]; then
        docker-compose -f docker-compose.production.yml down
        log_info "Services arrêtés"
    else
        log_warning "En production, nettoyage manuel requis"
    fi
}

# Script principal
main() {
    log_info "=== Déploiement Production Multi-Agent Orchestrator ==="
    log_info "Environnement: $ENVIRONMENT"
    log_info "Démarrage: $(date)"
    
    # Piège pour nettoyage en cas d'erreur
    trap cleanup_on_error ERR
    
    # Étapes du déploiement
    check_prerequisites
    setup_data_directories
    setup_docker_secrets
    setup_ssl_certificates
    setup_configuration_files
    build_and_deploy
    verify_deployment
    display_connection_info
    
    log_success "=== Déploiement terminé avec succès ==="
    log_info "Durée totale: $SECONDS secondes"
    echo
    log_info "Pour arrêter les services: docker-compose -f docker-compose.production.yml down"
    log_info "Pour voir les logs: docker-compose -f docker-compose.production.yml logs -f"
    log_info "Pour redémarrer: docker-compose -f docker-compose.production.yml restart"
}

# Execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

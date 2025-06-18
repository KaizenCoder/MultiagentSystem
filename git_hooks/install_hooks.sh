#!/bin/bash
# 🚀 INSTALLATION AUTOMATIQUE GIT HOOKS NEXTGENERATION
# Installation et configuration des hooks Git
# Version: 1.0 - Décembre 2024
# Référence: Transposition SuperWhisper_V6 → NextGeneration

set -e

# 🎯 CONFIGURATION
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
HOOKS_DIR="$PROJECT_ROOT/git_hooks"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 📊 FONCTIONS UTILITAIRES
log_info() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] INFO: $1${NC}"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')] SUCCESS: $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] WARNING: $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')] ERROR: $1${NC}"
}

show_banner() {
    echo -e "${BLUE}"
    cat << 'EOF'
🚀 INSTALLATION GIT HOOKS NEXTGENERATION
==========================================
Configuration automatique des hooks Git
pour validation qualité et workflows
==========================================
EOF
    echo -e "${NC}"
}

# 🔍 VALIDATION ENVIRONNEMENT
validate_environment() {
    log_info "🔍 Validation environnement installation"
    
    # Vérifier qu'on est dans un repo Git
    if [ ! -d "$PROJECT_ROOT/.git" ]; then
        log_error "Pas un repository Git: $PROJECT_ROOT"
        log_error "Exécuter depuis la racine du projet NextGeneration"
        exit 1
    fi
    
    # Vérifier existence dossier hooks source
    if [ ! -d "$HOOKS_DIR" ]; then
        log_error "Dossier git_hooks non trouvé: $HOOKS_DIR"
        exit 1
    fi
    
    # Vérifier Python
    if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
        log_warning "Python non détecté, certains hooks pourraient échouer"
    else
        PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
        log_success "Python détecté: $($PYTHON_CMD --version)"
    fi
    
    # Vérifier permissions
    if [ ! -w "$PROJECT_ROOT/.git" ]; then
        log_error "Permissions insuffisantes pour .git/"
        exit 1
    fi
    
    log_success "Environnement validé"
}

# 💾 SAUVEGARDE HOOKS EXISTANTS
backup_existing_hooks() {
    log_info "💾 Sauvegarde hooks existants"
    
    local backup_dir="$HOOKS_DIR/backups/backup_$TIMESTAMP"
    mkdir -p "$backup_dir"
    
    local hooks_backed_up=0
    
    if [ -d "$GIT_HOOKS_DIR" ]; then
        for hook in "$GIT_HOOKS_DIR"/*; do
            if [ -f "$hook" ] && [ ! -f "$hook.sample" ]; then
                local hook_name=$(basename "$hook")
                cp "$hook" "$backup_dir/$hook_name"
                log_info "Sauvegardé: $hook_name"
                ((hooks_backed_up++))
            fi
        done
    fi
    
    if [ $hooks_backed_up -gt 0 ]; then
        log_success "Hooks sauvegardés: $hooks_backed_up dans $backup_dir"
    else
        log_info "Aucun hook existant à sauvegarder"
        rmdir "$backup_dir" 2>/dev/null || true
    fi
}

# 📥 INSTALLATION HOOKS
install_hooks() {
    log_info "📥 Installation hooks NextGeneration"
    
    # Créer dossier hooks Git si nécessaire
    mkdir -p "$GIT_HOOKS_DIR"
    
    local hooks_installed=0
    
    # Installation pre-commit
    if [ -f "$HOOKS_DIR/pre-commit" ]; then
        cp "$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
        chmod +x "$GIT_HOOKS_DIR/pre-commit"
        log_success "Hook installé: pre-commit"
        ((hooks_installed++))
    else
        log_warning "Hook pre-commit non trouvé dans $HOOKS_DIR"
    fi
    
    # Installation autres hooks (futur)
    for hook_file in "$HOOKS_DIR"/pre-push "$HOOKS_DIR"/post-commit; do
        if [ -f "$hook_file" ]; then
            local hook_name=$(basename "$hook_file")
            cp "$hook_file" "$GIT_HOOKS_DIR/$hook_name"
            chmod +x "$GIT_HOOKS_DIR/$hook_name"
            log_success "Hook installé: $hook_name"
            ((hooks_installed++))
        fi
    done
    
    if [ $hooks_installed -eq 0 ]; then
        log_error "Aucun hook installé"
        exit 1
    fi
    
    log_success "Hooks installés: $hooks_installed"
}

# 🔧 CONFIGURATION ENVIRONNEMENT
setup_environment() {
    log_info "🔧 Configuration environnement"
    
    # Créer dossiers nécessaires
    mkdir -p "$PROJECT_ROOT/logs/git_hooks"
    log_success "Dossier logs créé: logs/git_hooks/"
    
    # Configuration Git locale (optionnelle)
    git config --local hooks.nextgeneration.enabled true
    git config --local hooks.nextgeneration.version "1.0"
    git config --local hooks.nextgeneration.installed "$TIMESTAMP"
    
    log_success "Configuration Git locale mise à jour"
    
    # Fichier de configuration par défaut
    local config_file="$HOOKS_DIR/config.json"
    if [ ! -f "$config_file" ]; then
        cat > "$config_file" << 'EOF'
{
    "validation": {
        "python_syntax": true,
        "pep8_standards": true,
        "powershell_syntax": true,
        "markdown_validation": true,
        "gpu_validation": true,
        "documentation_check": true,
        "tools_integrity": true
    },
    "thresholds": {
        "documentation_age_hours": 24,
        "max_validation_time_seconds": 60
    },
    "logging": {
        "level": "INFO",
        "save_detailed_logs": true,
        "log_retention_days": 7
    }
}
EOF
        log_success "Configuration par défaut créée: $config_file"
    else
        log_info "Configuration existante conservée: $config_file"
    fi
}

# 🧪 TEST INSTALLATION
test_installation() {
    log_info "🧪 Test installation hooks"
    
    # Test hook pre-commit
    if [ -x "$GIT_HOOKS_DIR/pre-commit" ]; then
        log_info "Test hook pre-commit..."
        
        # Test avec commit vide pour vérification
        if git status --porcelain | grep -q .; then
            log_info "Modifications détectées, test avec fichiers existants"
        else
            log_info "Aucune modification, test basique"
        fi
        
        # Test exécution hook
        if "$GIT_HOOKS_DIR/pre-commit" 2>/dev/null; then
            log_success "Hook pre-commit fonctionne"
        else
            local exit_code=$?
            if [ $exit_code -eq 1 ]; then
                log_warning "Hook pre-commit s'exécute mais détecte des problèmes"
                log_info "Normal si fichiers non conformes présents"
            else
                log_error "Hook pre-commit défaillant (code: $exit_code)"
            fi
        fi
    else
        log_error "Hook pre-commit non installé ou non exécutable"
    fi
    
    # Vérifier logs
    if [ -d "$PROJECT_ROOT/logs/git_hooks" ]; then
        local log_count=$(find "$PROJECT_ROOT/logs/git_hooks" -name "*.log" | wc -l)
        if [ $log_count -gt 0 ]; then
            log_success "Logs générés: $log_count fichier(s)"
        fi
    fi
}

# 📋 AFFICHAGE STATUS FINAL
show_status() {
    log_info "📋 Status installation hooks NextGeneration"
    
    echo
    echo -e "${GREEN}✅ INSTALLATION TERMINÉE${NC}"
    echo
    
    # Hooks installés
    echo "🔗 Hooks installés:"
    for hook in "$GIT_HOOKS_DIR"/*; do
        if [ -x "$hook" ] && [[ ! "$hook" =~ \.sample$ ]]; then
            local hook_name=$(basename "$hook")
            echo "  ✅ $hook_name"
        fi
    done
    
    echo
    
    # Configuration
    echo "⚙️ Configuration:"
    echo "  📁 Projet: $PROJECT_ROOT"
    echo "  📋 Config: git_hooks/config.json"
    echo "  📝 Logs: logs/git_hooks/"
    
    echo
    
    # Prochaines étapes
    echo -e "${BLUE}🚀 PROCHAINES ÉTAPES:${NC}"
    echo "1. Tester commit: git commit --allow-empty -m 'Test hooks'"
    echo "2. Consulter logs: ls -la logs/git_hooks/"
    echo "3. Configuration: edit git_hooks/config.json"
    echo "4. Documentation: cat git_hooks/README.md"
    
    echo
    
    # Variables d'environnement optionnelles
    echo -e "${YELLOW}💡 CONFIGURATION AVANCÉE:${NC}"
    echo "export NEXTGEN_HOOK_VERBOSE=1      # Mode verbeux"
    echo "export NEXTGEN_HOOK_SKIP_GPU=1     # Ignorer GPU"
    echo "export NEXTGEN_HOOK_SKIP_DOCS=1    # Ignorer docs"
    
    echo
    echo -e "${GREEN}🏆 Hooks NextGeneration installés avec succès!${NC}"
}

# 🚀 FONCTION PRINCIPALE
main() {
    show_banner
    
    log_info "Début installation hooks NextGeneration"
    log_info "Répertoire: $PROJECT_ROOT"
    
    # Validation environnement
    validate_environment
    
    # Sauvegarde hooks existants
    backup_existing_hooks
    
    # Installation hooks
    install_hooks
    
    # Configuration environnement
    setup_environment
    
    # Test installation
    test_installation
    
    # Status final
    show_status
    
    log_success "Installation terminée avec succès"
}

# 📖 AIDE
show_help() {
    cat << 'EOF'
🚀 INSTALLATION GIT HOOKS NEXTGENERATION

USAGE:
    ./install_hooks.sh [OPTIONS]

OPTIONS:
    -h, --help          Afficher cette aide
    --test-only         Seulement tester les hooks existants
    --backup-only       Seulement sauvegarder hooks existants
    --no-test           Installer sans tester

EXEMPLES:
    ./install_hooks.sh                  # Installation complète
    ./install_hooks.sh --test-only      # Test uniquement
    ./install_hooks.sh --no-test        # Installation sans test

DESCRIPTION:
    Installe automatiquement les hooks Git NextGeneration:
    - pre-commit: Validation qualité avant commit
    - Configuration environnement
    - Tests d'intégration
    - Sauvegarde hooks existants

RÉFÉRENCE:
    Transposition SuperWhisper_V6 → NextGeneration
    Standards Git adaptés 2025
EOF
}

# 🎯 POINT D'ENTRÉE
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    --test-only)
        validate_environment
        test_installation
        exit 0
        ;;
    --backup-only)
        validate_environment
        backup_existing_hooks
        exit 0
        ;;
    --no-test)
        show_banner
        validate_environment
        backup_existing_hooks
        install_hooks
        setup_environment
        show_status
        exit 0
        ;;
    *)
        main
        ;;
esac 
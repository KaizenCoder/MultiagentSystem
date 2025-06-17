-- Script de configuration PostgreSQL pour NextGeneration
-- Configuration optimisée par IA-2

-- Création de l'utilisateur nextgen_admin
CREATE USER nextgen_admin WITH ENCRYPTED PASSWORD 'NextGen2025!Secure' CREATEDB;

-- Création de la base de données orchestrator
CREATE DATABASE orchestrator OWNER nextgen_admin;

-- Attribution des privilèges
GRANT ALL PRIVILEGES ON DATABASE orchestrator TO nextgen_admin;

-- Connexion à la base orchestrator
\c orchestrator;

-- Création du schéma pour l'orchestrateur
CREATE SCHEMA IF NOT EXISTS orchestrator AUTHORIZATION nextgen_admin;

-- Attribution des privilèges sur le schéma
GRANT ALL ON SCHEMA orchestrator TO nextgen_admin;
GRANT ALL ON SCHEMA public TO nextgen_admin;

-- Configuration pour l'optimisation (selon IA-2)
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Recharger la configuration
SELECT pg_reload_conf();

-- Afficher les informations de connexion
\echo '✅ Configuration PostgreSQL terminée!'
\echo '🔗 Base de données: orchestrator'
\echo '👤 Utilisateur: nextgen_admin'
\echo '🔒 Authentification: configurée'
\echo '⚙️ Optimisations: appliquées' 
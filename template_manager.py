"""
Template Manager pour le Pattern Factory
Gestionnaire des templates JSON pour la création d'agents
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import os
from datetime import datetime

from base_agent_template import BaseAgent, TemplateBasedAgent, AgentConfig

class TemplateManager:
    """
    Gestionnaire des templates pour la création d'agents
    Remplace l'approche hard-coded par une approche déclarative
    """
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialise le gestionnaire de templates
        
        Args:
            templates_dir: Répertoire contenant les templates JSON
        """
        self.templates_dir = Path(templates_dir)
        self.logger = logging.getLogger("TemplateManager")
        self.loaded_templates = {}
        self.active_agents = {}
        
        # Créer le répertoire s'il n'existe pas
        self.templates_dir.mkdir(exist_ok=True)
        
        self._load_all_templates()
    
    def _load_all_templates(self):
        """Charge tous les templates disponibles"""
        if not self.templates_dir.exists():
            self.logger.warning(f"Répertoire de templates {self.templates_dir} n'existe pas")
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                self._load_template(template_file)
                self.logger.info(f"Template chargé: {template_file.name}")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement de {template_file}: {e}")
    
    def _load_template(self, template_path: Path):
        """Charge un template spécifique"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            template_name = template_data.get('name', template_path.stem)
            self.loaded_templates[template_name] = {
                'path': str(template_path),
                'data': template_data,
                'loaded_at': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement du template {template_path}: {e}")
            raise
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """Liste tous les templates disponibles"""
        templates_info = []
        
        for name, template_info in self.loaded_templates.items():
            data = template_info['data']
            templates_info.append({
                'name': name,
                'version': data.get('version', '1.0.0'),
                'role': data.get('role', 'Unknown'),
                'domain': data.get('domain', 'General'),
                'description': data.get('description', ''),
                'path': template_info['path'],
                'loaded_at': template_info['loaded_at'].isoformat()
            })
        
        return templates_info
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Récupère un template spécifique"""
        if template_name in self.loaded_templates:
            return self.loaded_templates[template_name]['data']
        
        self.logger.warning(f"Template '{template_name}' non trouvé")
        return None
    
    def create_agent(self, template_name: str, agent_id: str = None) -> Optional[TemplateBasedAgent]:
        """
        Crée un agent à partir d'un template
        
        Args:
            template_name: Nom du template à utiliser
            agent_id: ID unique pour l'agent (optionnel)
            
        Returns:
            Instance de l'agent créé ou None si erreur
        """
        try:
            template_data = self.get_template(template_name)
            if not template_data:
                return None
            
            # Créer l'agent
            agent = TemplateBasedAgent(config_data=template_data)
            
            # Générer un ID unique si non fourni
            if not agent_id:
                agent_id = f"{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Stocker l'agent actif
            self.active_agents[agent_id] = {
                'agent': agent,
                'template_name': template_name,
                'created_at': datetime.now()
            }
            
            self.logger.info(f"Agent créé: {agent_id} basé sur {template_name}")
            return agent
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de l'agent {template_name}: {e}")
            return None
    
    def get_agent(self, agent_id: str) -> Optional[TemplateBasedAgent]:
        """Récupère un agent actif par son ID"""
        if agent_id in self.active_agents:
            return self.active_agents[agent_id]['agent']
        return None
    
    def list_active_agents(self) -> List[Dict[str, Any]]:
        """Liste tous les agents actifs"""
        agents_info = []
        
        for agent_id, agent_info in self.active_agents.items():
            agent = agent_info['agent']
            agents_info.append({
                'id': agent_id,
                'name': agent.config.name,
                'role': agent.config.role,
                'status': agent.status,
                'template': agent_info.get('template_name', 'Unknown'),
                'created_at': agent_info['created_at'].isoformat(),
                'uptime': (datetime.now() - agent_info['created_at']).total_seconds()
            })
        
        return agents_info
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du gestionnaire"""
        return {
            'templates_loaded': len(self.loaded_templates),
            'active_agents': len(self.active_agents),
            'templates_dir': str(self.templates_dir),
            'templates': list(self.loaded_templates.keys()),
            'agents': list(self.active_agents.keys())
        } 
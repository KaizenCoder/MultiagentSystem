#!/usr/bin/env python3
"""
Stub amélioré pour pipeline
Fournit les classes et fonctions pipeline
"""

class Pipeline:
    """Classe Pipeline pour traitement de données"""
    
    def __init__(self, steps=None):
        self.steps = steps or []
    
    def add_step(self, step):
        """Ajoute une étape au pipeline"""
        self.steps.append(step)
    
    def execute(self, data):
        """Exécute le pipeline"""
        result = data
        for step in self.steps:
            result = step(result)
        return result

def create_pipeline(steps=None):
    """Crée un nouveau pipeline"""
    return Pipeline(steps)

class DataProcessor:
    """Processeur de données"""
    
    def __init__(self):
        pass
    
    def process(self, data):
        return data

# Variables globales pour compatibilité
pipeline_instance = Pipeline()

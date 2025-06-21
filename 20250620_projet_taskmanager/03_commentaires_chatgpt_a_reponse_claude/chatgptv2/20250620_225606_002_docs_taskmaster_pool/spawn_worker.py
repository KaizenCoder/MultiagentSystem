#!/usr/bin/env python3
"""Spawne plusieurs TaskMasters en parallèle avec multiprocessing"""
import multiprocessing
from template_manager_integrated import AgentTaskMasterNextGeneration

missions = [
    "Génère la documentation",
    "Analyse sécurité",
    "Audit SQL",
    "Nettoyage logs",
    "Test API",
]

def launch_agent(mission):
    agent = AgentTaskMasterNextGeneration()
    agent.create_task_sync(mission)  # méthode synchrone (à adapter si besoin)

if __name__ == "__main__":
    procs = []
    for mission in missions:
        p = multiprocessing.Process(target=launch_agent, args=(mission,))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

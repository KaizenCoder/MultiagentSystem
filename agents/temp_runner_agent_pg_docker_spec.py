#!/usr/bin/env python3
# temp_runner_agent_pg_docker_spec.py

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"INFO: Python sys.path: {sys.path}")

try:
    from agents.agent_POSTGRESQL_docker_specialist import AgentDockerSpecialist, create_agent_docker_specialist
    print("SUCCESS: Agent 'AgentDockerSpecialist' imported correctly.")
    
    try:
        # Test instantiation via factory function
        agent = create_agent_docker_specialist()
        print("SUCCESS: Agent 'AgentDockerSpecialist' instantiated correctly via factory.")
        
        # Test direct instantiation
        agent2 = AgentDockerSpecialist()
        print("SUCCESS: Agent 'AgentDockerSpecialist' instantiated correctly directly.")

    except Exception as e:
        print(f"FAILURE: Could not instantiate Agent 'AgentDockerSpecialist'. Error: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"FAILURE: Could not import Agent 'AgentDockerSpecialist'. Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc() 
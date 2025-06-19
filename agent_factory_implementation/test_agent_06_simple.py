#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 TEST SIMPLE AGENT 06 - DIAGNOSTIC
Diagnostique le problème de variable OPENTELEMETRY_AVAILABLE
"""

import sys
import os
from pathlib import Path

print("🔍 DIAGNOSTIC AGENT 06 SPRINT 4")
print("=" * 50)

# Test import OpenTelemetry
try:
    from opentelemetry import trace, metrics
    OPENTELEMETRY_AVAILABLE = True
    print("✅ OpenTelemetry importé avec succès")
except ImportError as e:
    OPENTELEMETRY_AVAILABLE = False
    print(f"❌ OpenTelemetry import échec: {e}")

print(f"📊 OPENTELEMETRY_AVAILABLE = {OPENTELEMETRY_AVAILABLE}")

# Test import des dépendances
print("\n📦 TEST DÉPENDANCES:")
dependencies = [
    "jsonschema",
    "cryptography",
    "prometheus_client"
]

for dep in dependencies:
    try:
        __import__(dep)
        print(f"✅ {dep}")
    except ImportError as e:
        print(f"❌ {dep}: {e}")

# Test simple import Agent 06
print("\n🤖 TEST IMPORT AGENT 06:")
try:
    # Ajouter le chemin agents
    agents_path = Path(__file__).parent / "agents"
    sys.path.insert(0, str(agents_path))
    
    # Test import minimal
    import agent_06_specialiste_monitoring_sprint4
    print("✅ Agent 06 module importé")
    
    # Test création instance
    from agent_06_specialiste_monitoring_sprint4 import Agent06AdvancedMonitoring
    agent = Agent06AdvancedMonitoring()
    print(f"✅ Agent 06 instancié: {agent.agent_name} v{agent.version}")
    
except Exception as e:
    print(f"❌ Erreur Agent 06: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 DIAGNOSTIC TERMINÉ") 
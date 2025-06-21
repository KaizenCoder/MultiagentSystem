#!/usr/bin/env python3
"""
NextGeneration Tools Launcher
Script pour excuter les outils imports depuis n'importe o dans le projet
"""

import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_tool.py <tool_name> [args...]")
        list_available_tools()
        return
        
    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]
    
    # Charger la configuration des outils
    config_file = Path(__file__).parent / "tools_config.json"
    
    if not config_file.exists():
        print("[CROSS] Configuration des outils introuvable")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    # Trouver l'outil
    tool_info = None
    for tool in config["nextgeneration_tools"]["tools"]:
        if tool["name"] == tool_name:
            tool_info = tool
            break
            
    if not tool_info:
        print(f"[CROSS] Outil '{tool_name}' introuvable")
        list_available_tools()
        return
        
    # Excuter l'outil
    tool_path = Path(tool_info["path"])
    if not tool_path.exists():
        print(f"[CROSS] Fichier outil introuvable: {tool_path}")
        return
        
    import subprocess
    cmd = [sys.executable, str(tool_path)] + tool_args
    subprocess.run(cmd)

def list_available_tools():
    config_file = Path(__file__).parent / "tools_config.json"
    
    if not config_file.exists():
        print("[CROSS] Configuration des outils introuvable")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    print("\n[TOOL] Outils disponibles:")
    for tool in config["nextgeneration_tools"]["tools"]:
        print(f"  - {tool['name']} ({tool['category']}) - Priorit: {tool['priority']}")

if __name__ == "__main__":
    main()





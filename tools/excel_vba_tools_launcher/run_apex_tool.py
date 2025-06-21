#!/usr/bin/env python3
"""
Lanceur universel pour outils Apex_VBA_FRAMEWORK imports
Partie du systme NextGeneration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def load_apex_config():
    """Chargement de la configuration des outils Apex"""
    config_path = Path(__file__).parent / "apex_tools_config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_python_tool(tool_name, tool_path, args):
    """Excution d'un outil Python"""
    cmd = [sys.executable, tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def run_powershell_tool(tool_name, tool_path, args):
    """Excution d'un outil PowerShell"""
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def run_batch_tool(tool_name, tool_path, args):
    """Excution d'un outil Batch"""
    cmd = [tool_path] + args
    return subprocess.run(cmd, capture_output=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_apex_tool.py <tool_name> [args...]")
        print("\nOutils disponibles:")
        
        config = load_apex_config()
        for tool_name, tool_info in config["apex_tools_config"]["tools"].items():
            print(f"  - {tool_name} ({tool_info['type']})")
        return 1
    
    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]
    
    config = load_apex_config()
    tools = config["apex_tools_config"]["tools"]
    
    if tool_name not in tools:
        print(f"Outil '{tool_name}' introuvable")
        return 1
    
    tool_info = tools[tool_name]
    tool_path = tool_info["path"]
    tool_type = tool_info["type"]
    
    if tool_type == "python":
        return run_python_tool(tool_name, tool_path, tool_args).returncode
    elif tool_type == "powershell":
        return run_powershell_tool(tool_name, tool_path, tool_args).returncode
    elif tool_type == "batch":
        return run_batch_tool(tool_name, tool_path, tool_args).returncode
    else:
        print(f"Type d'outil non support: {tool_type}")
        return 1

if __name__ == "__main__":
    sys.exit(main())





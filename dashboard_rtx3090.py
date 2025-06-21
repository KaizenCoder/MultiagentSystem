#!/usr/bin/env python3
"""
Dashboard Monitoring RTX3090 Simple
"""

import time
import json
import os
import subprocess
from datetime import datetime

def get_gpu_info():
    """Rcupre infos GPU RTX3090"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            parts = result.stdout.strip().split(', ')
            return {
                "memory_used_mb": int(parts[0]),
                "memory_total_mb": int(parts[1]), 
                "temperature_c": int(parts[2]),
                "utilization_percent": int(parts[3])
            }
    except:
        return None

def main():
    """Dashboard simple RTX3090"""
    print(" DASHBOARD RTX3090 - NextGeneration")
    print("=" * 50)
    
    while True:
        gpu_info = get_gpu_info()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if gpu_info:
            memory_percent = (gpu_info["memory_used_mb"] / gpu_info["memory_total_mb"]) * 100
            
            print(f"[{timestamp}] VRAM: {gpu_info['memory_used_mb']}/{gpu_info['memory_total_mb']}MB ({memory_percent:.1f}%)")
            print(f"[{timestamp}] Temp: {gpu_info['temperature_c']}C | Usage: {gpu_info['utilization_percent']}%")
            
            # Alertes
            if memory_percent > 90:
                print(" ALERTE: VRAM > 90%")
            if gpu_info["temperature_c"] > 80:
                print(" ALERTE: Temprature > 80C")
        else:
            print(f"[{timestamp}] [CROSS] Impossible de lire GPU")
        
        time.sleep(5)

if __name__ == "__main__":
    main()





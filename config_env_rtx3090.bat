@echo off
echo 🎮 Configuration Ollama RTX3090 - NextGeneration
echo Définition variables d'environnement permanentes...

setx CUDA_VISIBLE_DEVICES "1"
setx CUDA_DEVICE_ORDER "PCI_BUS_ID"
setx OLLAMA_MODELS "D:\modeles_llm"
setx OLLAMA_GPU_DEVICE "1"
setx OLLAMA_BASE_URL "http://localhost:11434"

echo ✅ Variables configurées avec succès
echo ⚠️  Redémarrage nécessaire pour prise en compte
pause

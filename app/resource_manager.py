import re
import os
from dotenv import load_dotenv
from pynvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
)

load_dotenv()

MODEL_VRAM_FACTOR = 0.56

def _detect_vram() -> float:
    override = os.getenv("MODELS_VRAM_MAX")
    if override and override.strip():
        return float(override)
    
    nvmlInit()
    try:
        handle = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetMemoryInfo(handle)
        return info.total / (1024 ** 3)
    finally:
        nvmlShutdown()


def estimate_model_vram(model: str) -> float:
    if model.endswith("-cloud"):
        return 0.0

    match = re.search(r'(\d+(?:\.\d+)?)b', model)

    if match is None:
        raise ValueError(
            f"Não foi possível determinar o tamanho do modelo: '{model}'. "
            "Esperado um sufixo como '7b', '20b' ou '3.8b'."
        )

    raw_model_size = float(match.group(1))

    return raw_model_size * MODEL_VRAM_FACTOR



## MODULE LOADING ###

AVAILABLE_VRAM_GB = _detect_vram()

print(estimate_model_vram('gpt-oss:20b'))
print(estimate_model_vram('llama3.2:3b'))
print(estimate_model_vram('gpt-oss:120b-cloud')) 
print(estimate_model_vram('modelo:latest'))
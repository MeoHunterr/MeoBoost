

from utils import registry, system

def has_intel_gpu():
    
    return system.get_gpu_type() == "intel"

def is_vram_increased():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Intel\GMM", "DedicatedSegmentSize")
    return val == 1024

def toggle_vram():
    
    if is_vram_increased():
        registry.reg_delete(r"HKLM\SOFTWARE\Intel\GMM", "DedicatedSegmentSize")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Intel\GMM", "DedicatedSegmentSize", 1024, "REG_DWORD")
    return True



from utils import registry, system
from config import REG_APP

def is_gpu_tweaks_on():
    
    return registry.value_exists(REG_APP, "GpuTweaks")

def toggle_gpu_tweaks():
    
    if is_gpu_tweaks_on():
        registry.reg_delete(REG_APP, "GpuTweaks")
        
        hw = registry.read_value(r"HKLM\System\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode")
        if hw is not None:
            registry.reg_add(r"HKLM\System\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 1, "REG_DWORD")
        
        registry.reg_delete(r"HKCU\System\GameConfigStore", "GameDVR_Enabled")
        registry.reg_delete(r"HKCU\System\GameConfigStore", "GameDVR_FSEBehaviorMode")
        registry.reg_delete(r"HKCU\System\GameConfigStore", "GameDVR_FSEBehavior")
        registry.reg_delete(r"HKCU\System\GameConfigStore", "GameDVR_HonorUserFSEBehaviorMode")
        registry.reg_delete(r"HKCU\System\GameConfigStore", "GameDVR_DXGIHonorFSEWindowsCompatible")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\GpuEnergyDrv", "Start", 2, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Scheduler", "EnablePreemption", 1, "REG_DWORD")
    else:
        registry.reg_add(REG_APP, "GpuTweaks", 1, "REG_DWORD")
        
        hw = registry.read_value(r"HKLM\System\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode")
        if hw is not None:
            registry.reg_add(r"HKLM\System\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 2, "REG_DWORD")
        
        registry.reg_add(r"HKCU\Software\Microsoft\GameBar", "AllowAutoGameMode", 1, "REG_DWORD")
        registry.reg_add(r"HKCU\Software\Microsoft\GameBar", "AutoGameModeEnabled", 1, "REG_DWORD")
        
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_Enabled", 0, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_FSEBehaviorMode", 2, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_FSEBehavior", 2, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_HonorUserFSEBehaviorMode", 1, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_DXGIHonorFSEWindowsCompatible", 1, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_EFSEFeatureFlags", 0, "REG_DWORD")
        registry.reg_add(r"HKCU\System\GameConfigStore", "GameDVR_DSEBehavior", 2, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\GpuEnergyDrv", "Start", 4, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Scheduler", "EnablePreemption", 0, "REG_DWORD")
    
    return True

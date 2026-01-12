

from utils import registry, system

def has_amd_gpu():
    
    return system.get_gpu_type() == "amd"

def get_amd_path():
    
    code, stdout, _ = system.run_cmd(
        r'reg query "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}" /s /v "DriverDesc"'
    )
    
    if code != 0:
        return None
    
    current_path = ""
    for line in stdout.split('\n'):
        if 'HKEY' in line:
            current_path = line.strip()
        if 'AMD' in line.upper() or 'ATI' in line.upper() or 'RADEON' in line.upper():
            return current_path.replace("HKEY_LOCAL_MACHINE", "HKLM")
    
    return None

def apply_amd_tweaks():
    
    path = get_amd_path()
    if not path:
        return False
    
    registry.reg_add(path, "DisableSAMUPowerGating", 1, "REG_DWORD")
    registry.reg_add(path, "DisableUVDPowerGatingDynamic", 1, "REG_DWORD")
    registry.reg_add(path, "DisableVCEPowerGating", 1, "REG_DWORD")
    registry.reg_add(path, "EnableAspmL0s", 0, "REG_DWORD")
    registry.reg_add(path, "EnableAspmL1", 0, "REG_DWORD")
    registry.reg_add(path, "EnableUlps", 0, "REG_DWORD")
    
    registry.reg_add(path, "KMD_DeLagEnabled", 1, "REG_DWORD")
    registry.reg_add(path, "KMD_FRTEnabled", 0, "REG_DWORD")
    registry.reg_add(path, "DisableDMACopy", 1, "REG_DWORD")
    registry.reg_add(path, "DisableBlockWrite", 0, "REG_DWORD")
    registry.reg_add(path, "StutterMode", 0, "REG_DWORD")
    registry.reg_add(path, "PP_SclkDeepSleepDisable", 1, "REG_DWORD")
    registry.reg_add(path, "PP_ThermalAutoThrottlingEnable", 0, "REG_DWORD")
    registry.reg_add(path, "DisableDrmdmaPowerGating", 1, "REG_DWORD")
    registry.reg_add(path, "KMD_EnableComputePreemption", 0, "REG_DWORD")
    
    umd_path = f"{path}\\UMD"
    registry.reg_add(umd_path, "Main3D_DEF", "1", "REG_SZ")
    
    return True

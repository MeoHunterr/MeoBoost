

import os
from utils import registry, system, files
from config import REG_APP, FILES_DIR

POWER_PLAN_GUID = "88888888-8888-8888-8888-888888888888"

def is_power_plan_on():
    
    active = system.get_active_power_plan()
    return active and "MeoBoost" in active

def toggle_power_plan():
    
    if is_power_plan_on():
        system.run_cmd("powercfg -restoredefaultschemes")
        return True
    else:
        pow_file = files.get_file("meoboost.pow")
        if not pow_file:
            pow_file = files.get_file("MeoBoost.pow")  # Fallback
        
        if not pow_file:
            return False
        
        system.run_cmd(f"powercfg /d {POWER_PLAN_GUID}")
        
        code, _, _ = system.run_cmd(f'powercfg /import "{pow_file}" {POWER_PLAN_GUID}')
        if code != 0:
            return False
        
        system.run_cmd(f'powercfg /changename {POWER_PLAN_GUID} "MeoBoost Ultimate" "Power plan tối ưu cho gaming"')
        
        return system.set_power_plan(POWER_PLAN_GUID)

def is_svchost_on():
    
    ram_kb = system.get_ram_kb()
    target = ram_kb + 1024000
    current = registry.read_value(r"HKLM\SYSTEM\CurrentControlSet\Control", "SvcHostSplitThresholdInKB")
    return current and current >= target

def toggle_svchost():
    
    if is_svchost_on():
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control", "SvcHostSplitThresholdInKB", 3670016, "REG_DWORD")
    else:
        ram_kb = system.get_ram_kb()
        target = ram_kb + 1024000
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control", "SvcHostSplitThresholdInKB", target, "REG_DWORD")
    return True

def is_timer_on():
    
    return system.service_running("STR")

def toggle_timer():
    
    if is_timer_on():
        system.set_service_startup("STR", "disabled")
        system.stop_service("STR")
        system.bcdedit("/deletevalue useplatformclock")
        system.bcdedit("/deletevalue useplatformtick")
        system.bcdedit("/deletevalue disabledynamictick")
    else:
        exe_path = files.get_file("SetTimerResolutionService.exe")
        if not exe_path:
            return False
        
        if not system.service_exists("STR"):
            dotnet = os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"),
                                   r"Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe")
            if os.path.exists(dotnet):
                os.chdir(FILES_DIR)
                system.run_cmd(f'"{dotnet}" /i SetTimerResolutionService.exe')
        
        system.set_service_startup("STR", "auto")
        system.start_service("STR")
        system.bcdedit("/set disabledynamictick yes")
        system.bcdedit("/deletevalue useplatformclock")
        
        if system.get_windows_build() >= 19042:
            system.bcdedit("/deletevalue useplatformtick")
        else:
            system.bcdedit("/set useplatformtick yes")
    
    return True

def is_idle_disabled():
    
    code, stdout, _ = system.run_cmd("powercfg /qh scheme_current sub_processor IDLEDISABLE")
    return "0x00000001" in stdout

def toggle_idle():
    
    if is_idle_disabled():
        system.run_cmd("powercfg /setacvalueindex scheme_current sub_processor IDLEDISABLE 0")
    else:
        system.run_cmd("powercfg /setacvalueindex scheme_current sub_processor IDLEDISABLE 1")
    system.run_cmd("powercfg /setactive scheme_current")
    return True

def is_cstates_off():
    
    val = registry.read_value(
        r"HKLM\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000",
        "AllowDeepCStates"
    )
    return val == 0

def toggle_cstates():
    
    path = r"HKLM\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000"
    if is_cstates_off():
        registry.reg_add(path, "AllowDeepCStates", 1, "REG_DWORD")
    else:
        registry.reg_add(path, "AllowDeepCStates", 0, "REG_DWORD")
    return True

def is_pstates_on():
    
    subkeys = registry.get_subkeys(r"HKLM\System\ControlSet001\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}")
    
    for key in subkeys:
        if key.isdigit():
            path = rf"HKLM\System\ControlSet001\Control\Class\{{4d36e968-e325-11ce-bfc1-08002be10318}}\{key}"
            val = registry.read_value(path, "DisableDynamicPstate")
            if val == 1:
                return True
    return False

def toggle_pstates():
    
    subkeys = registry.get_subkeys(r"HKLM\System\ControlSet001\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}")
    
    for key in subkeys:
        if key.isdigit():
            path = rf"HKLM\System\ControlSet001\Control\Class\{{4d36e968-e325-11ce-bfc1-08002be10318}}\{key}"
            desc = registry.read_value(path, "DriverDesc")
            
            if desc and "NVIDIA" in str(desc).upper():
                if is_pstates_on():
                    registry.reg_delete(path, "DisableDynamicPstate")
                else:
                    registry.reg_add(path, "DisableDynamicPstate", 1, "REG_DWORD")
    
    return True

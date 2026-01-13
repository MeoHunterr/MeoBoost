

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
        pow_file = files.get_file("MeoBoost.pow")
        if not pow_file:
            pow_file = files.get_file("meoboost.pow")  # Fallback
        
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
    """Check if MeoBoost timer resolution service is running."""
    # Check if our scheduled task exists and is enabled
    code, out, _ = system.run_cmd('schtasks /query /tn "MeoBoostTimerRes" 2>nul')
    return code == 0 and "Ready" in out

def toggle_timer():
    """Toggle timer resolution optimization using native PowerShell.
    
    Uses PowerShell with NtSetTimerResolution instead of external .exe files.
    This achieves the same 0.5ms timer resolution without third-party tools.
    """
    task_name = "MeoBoostTimerRes"
    script_dir = os.path.join(os.environ.get("USERPROFILE", ""), ".MeoBoost")
    script_path = os.path.join(script_dir, "timer_service.ps1")
    
    if is_timer_on():
        # Disable: Delete scheduled task and reset bcdedit settings
        system.run_cmd(f'schtasks /delete /tn "{task_name}" /f')
        system.bcdedit("/deletevalue useplatformclock")
        system.bcdedit("/deletevalue useplatformtick")
        system.bcdedit("/deletevalue disabledynamictick")
        
        # Kill any running PowerShell timer process
        system.run_cmd('taskkill /f /im powershell.exe /fi "WINDOWTITLE eq MeoBoostTimer" 2>nul')
    else:
        # Create timer resolution script using native Windows API
        ps_script = '''
# MeoBoost Timer Resolution Service
# Sets Windows timer resolution to 0.5ms for reduced input latency
$Host.UI.RawUI.WindowTitle = "MeoBoostTimer"

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class NtTimer {
    [DllImport("ntdll.dll", SetLastError=true)]
    public static extern int NtSetTimerResolution(int DesiredResolution, bool SetResolution, out int CurrentResolution);
    
    [DllImport("ntdll.dll", SetLastError=true)]
    public static extern int NtQueryTimerResolution(out int MinimumResolution, out int MaximumResolution, out int CurrentResolution);
}
"@

# Query current timer resolution
$min = 0; $max = 0; $cur = 0
[NtTimer]::NtQueryTimerResolution([ref]$min, [ref]$max, [ref]$cur) | Out-Null

# Set to maximum resolution (0.5ms = 5000 * 100ns)
$newRes = 0
[NtTimer]::NtSetTimerResolution(5000, $true, [ref]$newRes) | Out-Null

# Keep running to maintain the resolution
while ($true) {
    Start-Sleep -Seconds 60
    # Refresh timer resolution periodically
    [NtTimer]::NtSetTimerResolution(5000, $true, [ref]$newRes) | Out-Null
}
'''
        # Save script
        os.makedirs(script_dir, exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(ps_script)
        
        # Delete old task if exists
        system.run_cmd(f'schtasks /delete /tn "{task_name}" /f 2>nul')
        
        # Create scheduled task to run at logon
        create_cmd = (
            f'schtasks /create /tn "{task_name}" '
            f'/tr "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File \\"{script_path}\\"" '
            f'/sc onlogon '
            f'/rl highest '
            f'/f'
        )
        system.run_cmd(create_cmd)
        
        # Apply bcdedit settings for timer
        system.bcdedit("/set disabledynamictick yes")
        system.bcdedit("/deletevalue useplatformclock")
        
        if system.get_windows_build() >= 19042:
            system.bcdedit("/deletevalue useplatformtick")
        else:
            system.bcdedit("/set useplatformtick yes")
        
        # Start the task now
        system.run_cmd(f'schtasks /run /tn "{task_name}"')
    
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

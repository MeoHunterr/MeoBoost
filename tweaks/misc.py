"""
MeoBoost Miscellaneous Tools
"""

import os
import shutil
import subprocess
from utils import registry, system, files
from config import FILES_DIR


def clear_memory_native():
    """Clear memory using native PowerShell commands (no external tools)."""
    # Force garbage collection and working set trimming via PowerShell
    ps_script = """
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    Get-Process | ForEach-Object {
        try { $_.MinWorkingSet = 1 } catch {}
    }
    """
    system.run_cmd(f'powershell -NoProfile -Command "{ps_script}"')


def run_cleaner():
    """Clean temporary files and free memory."""
    temp_dir = os.environ.get("TEMP", "")
    windir = os.environ.get("SYSTEMROOT", r"C:\Windows")
    
    # Clear recycle bin
    # Clear recycle bin
    try:
        recycle_bin = os.path.join(os.environ.get("SYSTEMDRIVE", "C:"), "$Recycle.bin")
        if os.path.exists(recycle_bin):
            shutil.rmtree(recycle_bin, ignore_errors=True)
    except Exception:
        pass
    
    # Clear user temp
    if temp_dir and os.path.exists(temp_dir):
        for item in os.listdir(temp_dir):
            try:
                path = os.path.join(temp_dir, item)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except (OSError, PermissionError):
                # Skip files in use or permission denied
                pass
    
    # Clear Windows temp
    win_temp = os.path.join(windir, "Temp")
    if os.path.exists(win_temp):
        for item in os.listdir(win_temp):
            try:
                os.remove(os.path.join(win_temp, item))
            except (OSError, PermissionError):
                # Skip files in use or permission denied
                pass
    
    # Clear prefetch
    prefetch = os.path.join(windir, "Prefetch")
    if os.path.exists(prefetch):
        for item in os.listdir(prefetch):
            try:
                os.remove(os.path.join(prefetch, item))
            except (OSError, PermissionError):
                # Skip files in use or permission denied
                pass
    
    # Clear memory using native PowerShell (replaces EmptyStandbyList.exe)
    clear_memory_native()
    
    return True


def game_boost(exe_path):
    """Optimize Windows for a specific game executable."""
    if not os.path.exists(exe_path):
        return False
    
    exe_name = os.path.basename(exe_path)
    
    # Set GPU preference to high performance
    registry.reg_add(
        r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences",
        exe_path, "GpuPreference=2;", "REG_SZ"
    )
    
    # Disable fullscreen optimizations
    registry.reg_add(
        r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers",
        exe_path, "~ DISABLEDXMAXIMIZEDWINDOWEDMODE", "REG_SZ"
    )
    
    # Set high CPU priority
    path = rf"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}\PerfOptions"
    registry.reg_add(path, "CpuPriorityClass", 3, "REG_DWORD")
    
    return True


def soft_restart():
    """Soft restart Windows components (explorer, network, memory)."""
    # Restart explorer
    system.kill_process("explorer.exe")
    windir = os.environ.get("SYSTEMROOT", r"C:\Windows")
    explorer = os.path.join(windir, "explorer.exe")
    subprocess.Popen([explorer])
    
    # Reset network
    system.run_cmd("netsh advfirewall reset")
    system.run_cmd("ipconfig /release")
    system.run_cmd("ipconfig /renew")
    system.run_cmd("nbtstat -R")
    system.run_cmd("nbtstat -RR")
    system.run_cmd("ipconfig /flushdns")
    system.run_cmd("ipconfig /registerdns")
    
    # Clear memory using native PowerShell
    clear_memory_native()
    
    return True


def is_audio_latency_on():
    """Check if MeoBoost audio latency task is enabled."""
    # Check if scheduled task exists and is enabled
    code, out, _ = system.run_cmd('schtasks /query /tn "MeoBoostAudioLatency" 2>nul')
    return code == 0 and "Ready" in out


def toggle_audio_latency():
    """Toggle audio latency optimization using native Windows timer resolution.
    
    Uses PowerShell to set timer resolution instead of external REAL.exe.
    This achieves similar audio latency improvements without third-party tools.
    """
    task_name = "MeoBoostAudioLatency"
    
    if is_audio_latency_on():
        # Disable: Delete scheduled task
        system.run_cmd(f'schtasks /delete /tn "{task_name}" /f')
    else:
        # Enable: Create scheduled task that sets timer resolution at logon
        # Use native PowerShell to set high-resolution timer
        ps_script = '''
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class TimerRes {
    [DllImport("ntdll.dll", SetLastError=true)]
    public static extern int NtSetTimerResolution(int DesiredResolution, bool SetResolution, out int CurrentResolution);
}
"@
$current = 0
[TimerRes]::NtSetTimerResolution(5000, $true, [ref]$current)
Start-Sleep -Seconds 86400
'''
        # Save script to a temp location
        script_path = os.path.join(os.environ.get("USERPROFILE", ""), ".MeoBoost", "timer_res.ps1")
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(ps_script)
        
        # Delete old task if exists
        system.run_cmd(f'schtasks /delete /tn "{task_name}" /f 2>nul')
        
        # Create new task that runs at logon
        create_cmd = (
            f'schtasks /create /tn "{task_name}" '
            f'/tr "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File \\"{script_path}\\"" '
            f'/sc onlogon '
            f'/rl highest '
            f'/f'
        )
        system.run_cmd(create_cmd)
        
        # Start it now
        system.run_cmd(f'schtasks /run /tn "{task_name}"')
    
    return True


def set_w32_priority(value):
    """Set Win32 priority separation value."""
    return registry.reg_add(
        r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl",
        "Win32PrioritySeparation", value, "REG_DWORD"
    )


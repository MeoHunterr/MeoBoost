

import os
import shutil
from utils import registry, system, files
from config import FILES_DIR

def run_cleaner():
    
    temp_dir = os.environ.get("TEMP", "")
    windir = os.environ.get("SYSTEMROOT", r"C:\Windows")
    
    system.run_cmd("rd /s /q %SYSTEMDRIVE%\\$Recycle.bin", shell=True)
    
    if temp_dir and os.path.exists(temp_dir):
        for item in os.listdir(temp_dir):
            try:
                path = os.path.join(temp_dir, item)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except:
                pass
    
    win_temp = os.path.join(windir, "Temp")
    if os.path.exists(win_temp):
        for item in os.listdir(win_temp):
            try:
                os.remove(os.path.join(win_temp, item))
            except:
                pass
    
    prefetch = os.path.join(windir, "Prefetch")
    if os.path.exists(prefetch):
        for item in os.listdir(prefetch):
            try:
                os.remove(os.path.join(prefetch, item))
            except:
                pass
    
    esl = files.get_file("EmptyStandbyList.exe")
    if esl:
        for mode in ["workingsets", "modifiedpagelist", "standbylist", "priority0standbylist"]:
            system.run_cmd(f'"{esl}" {mode}')
    
    return True

def game_boost(exe_path):
    
    if not os.path.exists(exe_path):
        return False
    
    exe_name = os.path.basename(exe_path)
    
    registry.reg_add(r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences", exe_path, "GpuPreference=2;", "REG_SZ")
    
    registry.reg_add(r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", exe_path, "~ DISABLEDXMAXIMIZEDWINDOWEDMODE", "REG_SZ")
    
    path = rf"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}\PerfOptions"
    registry.reg_add(path, "CpuPriorityClass", 3, "REG_DWORD")
    
    return True

def soft_restart():
    
    system.kill_process("explorer.exe")
    windir = os.environ.get("SYSTEMROOT", r"C:\Windows")
    os.startfile(os.path.join(windir, "explorer.exe"))
    
    system.run_cmd("netsh advfirewall reset")
    system.run_cmd("ipconfig /release")
    system.run_cmd("ipconfig /renew")
    system.run_cmd("nbtstat -R")
    system.run_cmd("nbtstat -RR")
    system.run_cmd("ipconfig /flushdns")
    system.run_cmd("ipconfig /registerdns")
    
    esl = files.get_file("EmptyStandbyList.exe")
    if esl:
        system.run_cmd(f'"{esl}" standbylist')
    
    return True

def is_audio_latency_on():
    
    return system.service_running("MeoAudio")

def toggle_audio_latency():
    
    nssm = files.get_file("nssm.exe")
    real = files.get_file("REAL.exe")
    
    if not nssm or not real:
        return False
    
    if is_audio_latency_on():
        system.run_cmd(f'"{nssm}" set MeoAudio start SERVICE_DISABLED')
        system.run_cmd(f'"{nssm}" stop MeoAudio')
    else:
        if not system.service_exists("MeoAudio"):
            system.run_cmd(f'"{nssm}" install MeoAudio "{real}"')
            system.run_cmd(f'"{nssm}" set MeoAudio DisplayName "MeoBoost Audio Latency Reducer"')
            system.run_cmd(f'"{nssm}" set MeoAudio Description "Reduces Audio Latency"')
            system.run_cmd(f'"{nssm}" set MeoAudio Start SERVICE_AUTO_START')
            system.run_cmd(f'"{nssm}" set MeoAudio AppAffinity 1')
        
        system.run_cmd(f'"{nssm}" set MeoAudio start SERVICE_AUTO_START')
        system.run_cmd(f'"{nssm}" start MeoAudio')
    
    return True

def set_w32_priority(value):
    
    return registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", value, "REG_DWORD")

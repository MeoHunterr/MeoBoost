

import os
from datetime import datetime

from utils import system
from utils import registry
from config import BACKUP_DIR, DATA_DIR

def create_restore_point(description="MeoBoost Backup"):
    
    registry.reg_add(
        r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\SystemRestore",
        "SystemRestorePointCreationFrequency", 0, "REG_DWORD"
    )
    
    system.run_powershell("Enable-ComputerRestore -Drive 'C:\\'")
    
    code, _, _ = system.run_cmd(
        f'wmic.exe /namespace:\\\\root\\default Path SystemRestore Call CreateRestorePoint "{description}", 100, 7'
    )
    return code == 0

def backup_registry():
    
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    backup_path = os.path.join(BACKUP_DIR, date_str)
    
    system.make_dir(backup_path)
    
    hklm_file = os.path.join(backup_path, "HKLM.reg")
    hkcu_file = os.path.join(backup_path, "HKCU.reg")
    
    ok1 = registry.export_key("HKLM", hklm_file)
    ok2 = registry.export_key("HKCU", hkcu_file)
    
    return ok1 and ok2

def full_backup():
    
    system.make_dir(DATA_DIR)
    system.make_dir(BACKUP_DIR)
    
    rp = create_restore_point()
    rb = backup_registry()
    
    return rp or rb

def is_first_run():
    
    marker = os.path.join(DATA_DIR, ".initialized")
    return not os.path.exists(marker)

def mark_initialized():
    
    system.make_dir(DATA_DIR)
    marker = os.path.join(DATA_DIR, ".initialized")
    try:
        with open(marker, "w") as f:
            f.write(datetime.now().isoformat())
        return True
    except:
        return False

def get_backup_list():
    
    if not os.path.exists(BACKUP_DIR):
        return []
    
    backups = []
    for name in os.listdir(BACKUP_DIR):
        path = os.path.join(BACKUP_DIR, name)
        if os.path.isdir(path):
            backups.append(name)
    
    return sorted(backups, reverse=True)

def restore_backup(date_str):
    
    backup_path = os.path.join(BACKUP_DIR, date_str)
    
    hklm_file = os.path.join(backup_path, "HKLM.reg")
    hkcu_file = os.path.join(backup_path, "HKCU.reg")
    
    ok = True
    if os.path.exists(hklm_file):
        ok = ok and registry.import_file(hklm_file)
    if os.path.exists(hkcu_file):
        ok = ok and registry.import_file(hkcu_file)
    
    return ok

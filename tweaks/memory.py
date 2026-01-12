

from utils import registry, system
from config import REG_APP

def is_memory_on():
    
    return registry.value_exists(REG_APP, "MemoryOn")

def toggle_memory():
    
    if is_memory_on():
        registry.reg_delete(REG_APP, "MemoryOn")
        
        registry.reg_delete(r"HKLM\Software\Microsoft\FTH", "Enabled")
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BackgroundAppGlobalToggle", 1, "REG_DWORD")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "LargeSystemCache")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnablePrefetcher", 3, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnableSuperfetch", 3, "REG_DWORD")
        
        registry.reg_add(r"HKCU\Control Panel\Desktop", "WaitToKillAppTimeout", "20000", "REG_SZ")
        registry.reg_add(r"HKLM\System\CurrentControlSet\Control", "WaitToKillServiceTimeout", "20000", "REG_SZ")
        registry.reg_add(r"HKCU\Control Panel\Desktop", "HungAppTimeout", "5000", "REG_SZ")
        
        system.run_cmd("fsutil behavior set memoryusage 1")
        system.run_cmd("fsutil behavior set mftzone 1")
        system.run_cmd("fsutil behavior set disablelastaccess 2")
        system.run_cmd("fsutil behavior set disablecompression 0")
    else:
        registry.reg_add(REG_APP, "MemoryOn", 1, "REG_DWORD")
        
        registry.reg_add(r"HKLM\Software\Microsoft\FTH", "Enabled", 0, "REG_DWORD")
        
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\Software\Policies\Microsoft\Windows\AppPrivacy", "LetAppsRunInBackground", 2, "REG_DWORD")
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BackgroundAppGlobalToggle", 0, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive", 1, "REG_DWORD")
        
        system.run_powershell("Disable-MMAgent -PageCombining -mc")
        registry.reg_add(r"HKLM\System\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePageCombining", 1, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "LargeSystemCache", 1, "REG_DWORD")
        
        registry.reg_add(r"HKLM\System\CurrentControlSet\Control\Session Manager", "HeapDeCommitFreeBlockThreshold", 262144, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnablePrefetcher", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters", "EnableSuperfetch", 0, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power", "HiberbootEnabled", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\Power", "HibernateEnabled", 0, "REG_DWORD")
        
        registry.reg_add(r"HKCU\Control Panel\Desktop", "WaitToKillAppTimeout", "1000", "REG_SZ")
        registry.reg_add(r"HKLM\System\CurrentControlSet\Control", "WaitToKillServiceTimeout", "1000", "REG_SZ")
        registry.reg_add(r"HKCU\Control Panel\Desktop", "HungAppTimeout", "1000", "REG_SZ")
        
        system.run_cmd("fsutil behavior set memoryusage 2")
        system.run_cmd("fsutil behavior set mftzone 2")
        system.run_cmd("fsutil behavior set disablelastaccess 1")
        system.run_cmd("fsutil behavior set disable8dot3 1")
        system.run_cmd("fsutil behavior set disablecompression 1")
        system.run_cmd("fsutil behavior set disabledeletenotify 0")
    
    return True

def is_csrss_high():
    
    val = registry.read_value(
        r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\csrss.exe\PerfOptions",
        "CpuPriorityClass"
    )
    return val == 4

def toggle_csrss():
    
    path = r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\csrss.exe\PerfOptions"
    mm_path = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
    
    if is_csrss_high():
        registry.reg_delete(path, "CpuPriorityClass")
        registry.reg_delete(path, "IoPriority")
        registry.reg_delete(mm_path, "NoLazyMode")
        registry.reg_delete(mm_path, "AlwaysOn")
        registry.reg_delete(mm_path, "NetworkThrottlingIndex")
        registry.reg_delete(mm_path, "SystemResponsiveness")
    else:
        registry.reg_add(path, "CpuPriorityClass", 4, "REG_DWORD")
        registry.reg_add(path, "IoPriority", 3, "REG_DWORD")
        registry.reg_add(mm_path, "NoLazyMode", 1, "REG_DWORD")
        registry.reg_add(mm_path, "AlwaysOn", 1, "REG_DWORD")
        registry.reg_add(mm_path, "NetworkThrottlingIndex", 10, "REG_DWORD")
        registry.reg_add(mm_path, "SystemResponsiveness", 0, "REG_DWORD")
    
    return True

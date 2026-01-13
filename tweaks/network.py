

import os
from utils import registry, system
from config import REG_APP, REG_TCPIP, BACKUP_DIR

def is_tcpip_on():
    
    return registry.value_exists(REG_APP, "TcpipOn")

def toggle_tcpip():
    
    if is_tcpip_on():
        registry.reg_delete(REG_APP, "TcpipOn")
        system.run_powershell("Set-NetTCPSetting -SettingName '*' -InitialCongestionWindow 4 -ErrorAction SilentlyContinue")
        
        for name in ["TcpMaxConnectRetransmissions", "Tcp1323Opts", "TcpTimedWaitDelay",
                     "DelayedAckFrequency", "DelayedAckTicks", "CongestionAlgorithm", "MultihopSets"]:
            registry.reg_delete(REG_TCPIP, name)
        
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "IRPStackSize")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "SizReqBuf")
    else:
        registry.reg_add(REG_APP, "TcpipOn", 1, "REG_DWORD")
        
        system.run_powershell(
            "Enable-NetAdapterQos -Name '*'; "
            "Disable-NetAdapterPowerManagement -Name '*'; "
            "Set-NetTCPSetting -SettingName '*' -MemoryPressureProtection Disabled -InitialCongestionWindow 10 -ErrorAction SilentlyContinue"
        )
        
        registry.reg_add(REG_TCPIP, "TcpMaxConnectRetransmissions", 1, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "Tcp1323Opts", 1, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "TcpTimedWaitDelay", 32, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "DelayedAckFrequency", 1, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "DelayedAckTicks", 1, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "CongestionAlgorithm", 1, "REG_DWORD")
        registry.reg_add(REG_TCPIP, "MultihopSets", 15, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "IRPStackSize", 50, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "SizReqBuf", 17424, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", "Size", 3, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters", "NegativeCacheTime", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters", "NegativeSOACacheTime", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters", "NetFailureCacheTime", 0, "REG_DWORD")
        
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\AFD\Parameters", "DoNotHoldNicBuffers", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\AFD\Parameters", "NonBlockingSendSpecialBuffering", 1, "REG_DWORD")
    
    return True

def is_nic_on():
    
    return os.path.exists(os.path.join(BACKUP_DIR, "nic_backup.txt"))

def toggle_nic():
    
    if is_nic_on():
        marker = os.path.join(BACKUP_DIR, "nic_backup.txt")
        if os.path.exists(marker):
            os.remove(marker)
    else:
        system.make_dir(BACKUP_DIR)
        
        code, stdout, _ = system.run_cmd(
            r'reg query "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}" /s /v "DriverDesc"'
        )
        
        if code == 0:
            current_path = ""
            for line in stdout.split('\n'):
                if 'HKEY' in line:
                    current_path = line.strip().replace("HKEY_LOCAL_MACHINE", "HKLM")
                elif 'DriverDesc' in line and current_path:
                    registry.reg_add(current_path, "MIMOPowerSaveMode", "3", "REG_SZ")
                    registry.reg_add(current_path, "PowerSavingMode", "0", "REG_SZ")
                    registry.reg_add(current_path, "EnableGreenEthernet", "0", "REG_SZ")
                    registry.reg_add(current_path, "*EEE", "0", "REG_SZ")
                    registry.reg_add(current_path, "EnableConnectedPowerGating", 0, "REG_DWORD")
                    registry.reg_add(current_path, "EnableDynamicPowerGating", "0", "REG_SZ")
                    registry.reg_add(current_path, "PnPCapabilities", "24", "REG_SZ")
        
        with open(os.path.join(BACKUP_DIR, "nic_backup.txt"), "w") as f:
            f.write("Applied")
        
        system.run_cmd("ipconfig /release")
        system.run_cmd("ipconfig /renew")
    
    return True

def is_netsh_on():
    
    return registry.value_exists(REG_APP, "NetshOn")

def toggle_netsh():
    
    if is_netsh_on():
        registry.reg_delete(REG_APP, "NetshOn")
        
        system.netsh("int tcp set supplemental Internet congestionprovider=default")
        system.netsh("int tcp set global initialRto=3000")
        system.netsh("int tcp set global rss=default")
        system.netsh("int tcp set global dca=default")
        system.netsh("int tcp set global netdma=default")
        system.netsh("int tcp set global timestamps=default")
    else:
        registry.reg_add(REG_APP, "NetshOn", 1, "REG_DWORD")
        
        system.netsh("int tcp set global dca=enabled")
        system.netsh("int tcp set global netdma=enabled")
        system.netsh("interface isatap set state disabled")
        system.netsh("int tcp set global timestamps=disabled")
        system.netsh("int tcp set global rss=enabled")
        system.netsh("int tcp set global nonsackrttresiliency=disabled")
        system.netsh("int tcp set global initialRto=2000")
        system.netsh("int tcp set supplemental template=custom icw=10")
    
    return True

def is_msi_on():
    
    return registry.value_exists(REG_APP, "MsiOn")

def toggle_msi():
    
    if is_msi_on():
        registry.reg_delete(REG_APP, "MsiOn")
    else:
        registry.reg_add(REG_APP, "MsiOn", 1, "REG_DWORD")
        
        code, stdout, _ = system.run_cmd('wmic path Win32_VideoController GET PNPDeviceID')
        if code == 0:
            for line in stdout.split('\n'):
                line = line.strip()
                if line.startswith("PCI\\VEN_"):
                    path = rf"HKLM\SYSTEM\CurrentControlSet\Enum\{line}\Device Parameters\Interrupt Management\MessageSignaledInterruptProperties"
                    registry.reg_add(path, "MSISupported", 1, "REG_DWORD")
    
    return True

def is_affinity_on():
    
    return registry.value_exists(REG_APP, "AffinityOn")

def toggle_affinity():
    
    cores = system.get_cpu_info()["cores"]
    
    if cores <= 2:
        return False  # Không áp dụng cho CPU 2 core
    
    if is_affinity_on():
        registry.reg_delete(REG_APP, "AffinityOn")
        code, stdout, _ = system.run_cmd(
            r'reg query "HKLM\SYSTEM\CurrentControlSet\Enum" /s /v "MSISupported"'
        )
        if code == 0:
            current_path = ""
            for line in stdout.split('\n'):
                if 'HKEY' in line:
                    current_path = line.strip().replace("HKEY_LOCAL_MACHINE", "HKLM")
                elif 'MSISupported' in line and current_path:
                    affinity_path = current_path.replace("MessageSignaledInterruptProperties", "Affinity Policy")
                    registry.reg_delete(affinity_path, "DevicePolicy")
                    registry.reg_delete(affinity_path, "AssignmentSetOverride")
    else:
        registry.reg_add(REG_APP, "AffinityOn", 1, "REG_DWORD")
        code, stdout, _ = system.run_cmd(
            r'reg query "HKLM\SYSTEM\CurrentControlSet\Enum" /s /v "MSISupported"'
        )
        if code == 0:
            current_path = ""
            for line in stdout.split('\n'):
                if 'HKEY' in line:
                    current_path = line.strip().replace("HKEY_LOCAL_MACHINE", "HKLM")
                elif 'MSISupported' in line and current_path:
                    affinity_path = current_path.replace("MessageSignaledInterruptProperties", "Affinity Policy")
                    registry.reg_add(affinity_path, "DevicePolicy", 4, "REG_DWORD")
    
    return True

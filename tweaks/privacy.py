

from utils import registry, system
from config import REG_APP

def is_telemetry_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry")
    return val == 0

def toggle_telemetry():
    
    if is_telemetry_off():
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry")
        registry.reg_delete(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry")
        system.set_service_startup("DiagTrack", "auto")
        system.start_service("DiagTrack")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", 0, "REG_DWORD")
        system.set_service_startup("DiagTrack", "disabled")
        system.stop_service("DiagTrack")
        system.stop_service("dmwappushservice")
    return True

def is_cortana_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana")
    return val == 0

def toggle_cortana():
    
    if is_cortana_off():
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana")
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "DisableWebSearch")
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "ConnectedSearchUseWeb")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "DisableWebSearch", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "ConnectedSearchUseWeb", 0, "REG_DWORD")
    return True

def is_activity_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "EnableActivityFeed")
    return val == 0

def toggle_activity():
    
    if is_activity_off():
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "EnableActivityFeed")
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "PublishUserActivities")
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "UploadUserActivities")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "EnableActivityFeed", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "PublishUserActivities", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "UploadUserActivities", 0, "REG_DWORD")
    return True

def is_location_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", "Value")
    return val == "Deny"

def toggle_location():
    
    if is_location_off():
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", "Value", "Allow", "REG_SZ")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", "Value", "Deny", "REG_SZ")
    return True

def is_ads_off():
    
    val = registry.read_value(r"HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled")
    return val == 0

def toggle_ads():
    
    if is_ads_off():
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 1, "REG_DWORD")
    else:
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo", "DisabledByGroupPolicy", 1, "REG_DWORD")
    return True

def is_feedback_off():
    
    val = registry.read_value(r"HKCU\Software\Microsoft\Siuf\Rules", "NumberOfSIUFInPeriod")
    return val == 0

def toggle_feedback():
    
    if is_feedback_off():
        registry.reg_delete(r"HKCU\Software\Microsoft\Siuf\Rules", "NumberOfSIUFInPeriod")
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "DoNotShowFeedbackNotifications")
    else:
        registry.reg_add(r"HKCU\Software\Microsoft\Siuf\Rules", "NumberOfSIUFInPeriod", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "DoNotShowFeedbackNotifications", 1, "REG_DWORD")
    return True

def is_camera_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam", "Value")
    return val == "Deny"

def toggle_camera():
    
    if is_camera_off():
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam", "Value", "Allow", "REG_SZ")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam", "Value", "Deny", "REG_SZ")
    return True

def is_microphone_off():
    
    val = registry.read_value(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone", "Value")
    return val == "Deny"

def toggle_microphone():
    
    if is_microphone_off():
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone", "Value", "Allow", "REG_SZ")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone", "Value", "Deny", "REG_SZ")
    return True

def apply_all_privacy():
    
    toggle_telemetry() if not is_telemetry_off() else None
    toggle_cortana() if not is_cortana_off() else None
    toggle_activity() if not is_activity_off() else None
    toggle_ads() if not is_ads_off() else None
    toggle_feedback() if not is_feedback_off() else None
    toggle_copilot() if not is_copilot_off() else None
    toggle_bg_apps() if not is_bg_apps_off() else None
    toggle_bing_search() if not is_bing_search_off() else None
    
    services = [
        "DiagTrack", "dmwappushservice", "diagnosticshub.standardcollector.service",
        "WerSvc", "WMPNetworkSvc", "WSearch"
    ]
    for svc in services:
        system.set_service_startup(svc, "disabled")
        system.stop_service(svc)
    
    tasks = [
        r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
        r"\Microsoft\Windows\Application Experience\ProgramDataUpdater",
        r"\Microsoft\Windows\Autochk\Proxy",
        r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
        r"\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
        r"\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector",
    ]
    for task in tasks:
        system.run_cmd(f'schtasks /change /tn "{task}" /disable')
    
    return True


# === WinUtil Privacy Tweaks ===

def is_copilot_off():
    val = registry.read_value(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot")
    return val == 1


def toggle_copilot():
    if is_copilot_off():
        registry.reg_delete(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot")
        registry.reg_delete(r"HKCU\Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot")
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowCopilotButton", 1, "REG_DWORD")
    else:
        registry.reg_add(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1, "REG_DWORD")
        registry.reg_add(r"HKCU\Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1, "REG_DWORD")
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowCopilotButton", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\Microsoft\Windows\Shell\Copilot", "IsCopilotAvailable", 0, "REG_DWORD")
    return True


def is_bg_apps_off():
    val = registry.read_value(r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled")
    return val == 1


def toggle_bg_apps():
    if is_bg_apps_off():
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 0, "REG_DWORD")
    else:
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 1, "REG_DWORD")
    return True


def is_bing_search_off():
    val = registry.read_value(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled")
    return val == 0


def toggle_bing_search():
    if is_bing_search_off():
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", 1, "REG_DWORD")
    else:
        registry.reg_add(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", 0, "REG_DWORD")
    return True

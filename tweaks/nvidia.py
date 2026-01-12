

import os
from utils import registry, system, files
from config import REG_APP, REG_NVIDIA, FILES_DIR

def get_nvidia_paths():
    
    paths = []
    code, stdout, _ = system.run_cmd(
        r'reg query "HKLM\System\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}" /t REG_SZ /s /e /f "NVIDIA"'
    )
    if code == 0:
        for line in stdout.split('\n'):
            if 'HKEY' in line:
                paths.append(line.strip().replace("HKEY_LOCAL_MACHINE", "HKLM"))
    return paths

def is_hdcp_off():
    
    for path in get_nvidia_paths():
        val = registry.read_value(path, "RMHdcpKeyglobZero")
        if val == 1:
            return True
    return False

def toggle_hdcp():
    
    paths = get_nvidia_paths()
    turning_on = not is_hdcp_off()
    
    for path in paths:
        if turning_on:
            registry.reg_add(path, "RMHdcpKeyglobZero", 1, "REG_DWORD")
        else:
            registry.reg_add(path, "RMHdcpKeyglobZero", 0, "REG_DWORD")
    
    return True

def is_preemption_off():
    
    return registry.read_value(REG_NVIDIA, "DisablePreemption") == 1

def toggle_preemption():
    
    if is_preemption_off():
        registry.reg_delete(REG_NVIDIA, "DisablePreemption")
        registry.reg_delete(REG_NVIDIA, "DisableCudaContextPreemption")
        registry.reg_delete(REG_NVIDIA, "EnableCEPreemption")
        registry.reg_delete(REG_NVIDIA, "DisablePreemptionOnS3S4")
        registry.reg_delete(REG_NVIDIA, "ComputePreemption")
    else:
        registry.reg_add(REG_NVIDIA, "DisablePreemption", 1, "REG_DWORD")
        registry.reg_add(REG_NVIDIA, "DisableCudaContextPreemption", 1, "REG_DWORD")
        registry.reg_add(REG_NVIDIA, "EnableCEPreemption", 0, "REG_DWORD")
        registry.reg_add(REG_NVIDIA, "DisablePreemptionOnS3S4", 1, "REG_DWORD")
        registry.reg_add(REG_NVIDIA, "ComputePreemption", 0, "REG_DWORD")
    return True

def is_npi_applied():
    
    return registry.value_exists(REG_APP, "NpiApplied")

def toggle_npi():
    
    npi_exe = files.get_file("nvidiaProfileInspector.exe")
    if not npi_exe:
        return False
    
    if is_npi_applied():
        profile = files.get_file("Base_Profile.nip")
        if profile:
            os.chdir(FILES_DIR)
            system.run_cmd(f'nvidiaProfileInspector.exe "{profile}"')
        registry.reg_delete(REG_APP, "NpiApplied")
    else:
        profile = files.get_file("meoboost.nip")
        if not profile:
            profile = files.get_file("Base_Profile.nip")
        
        if profile:
            os.chdir(FILES_DIR)
            system.run_cmd(f'nvidiaProfileInspector.exe "{profile}"')
            registry.reg_add(REG_APP, "NpiApplied", 1, "REG_DWORD")
    
    return True

def is_telemetry_off():
    
    return registry.value_exists(REG_APP, "TelemetryOff")

def toggle_telemetry():
    
    if is_telemetry_off():
        registry.reg_delete(REG_APP, "TelemetryOff")
        registry.reg_delete(r"HKLM\SOFTWARE\NVIDIA Corporation\NvControlPanel2\Client", "OptInOrOutPreference")
        registry.reg_delete(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID44231")
        registry.reg_delete(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID64640")
        registry.reg_delete(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID66610")
        
        tasks = [
            "NvTmRep_CrashReport1_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport2_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport3_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport4_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
        ]
        for task in tasks:
            system.run_cmd(f'schtasks /change /enable /tn "{task}"')
    else:
        registry.reg_add(REG_APP, "TelemetryOff", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\NVIDIA Corporation\NvControlPanel2\Client", "OptInOrOutPreference", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID44231", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID64640", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SOFTWARE\NVIDIA Corporation\Global\FTS", "EnableRID66610", 0, "REG_DWORD")
        
        registry.reg_delete(r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "NvBackend")
        
        tasks = [
            "NvTmRep_CrashReport1_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport2_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport3_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
            "NvTmRep_CrashReport4_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}",
        ]
        for task in tasks:
            system.run_cmd(f'schtasks /change /disable /tn "{task}"')
    
    return True

def is_nvidia_tweaks_on():
    
    return registry.value_exists(REG_APP, "NvidiaTweaks")

def toggle_nvidia_tweaks():
    
    if is_nvidia_tweaks_on():
        registry.reg_delete(REG_APP, "NvidiaTweaks")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "PlatformSupportMiracast", 1, "REG_DWORD")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\Global\NVTweak", "DisplayPowerSaving")
    else:
        registry.reg_add(REG_APP, "NvidiaTweaks", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "PlatformSupportMiracast", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\Global\NVTweak", "DisplayPowerSaving", 0, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS", "EnableRID61684", 1, "REG_DWORD")
        
        for path in get_nvidia_paths():
            registry.reg_add(path, "EnableTiledDisplay", 0, "REG_DWORD")
            registry.reg_add(path, "TCCSupported", 0, "REG_DWORD")
    
    return True

def is_wc_off():
    
    return registry.read_value(REG_NVIDIA, "DisableWriteCombining") == 1

def toggle_wc():
    
    if is_wc_off():
        registry.reg_delete(REG_NVIDIA, "DisableWriteCombining")
    else:
        registry.reg_add(REG_NVIDIA, "DisableWriteCombining", 1, "REG_DWORD")
    return True

def is_nvidia_dram_active_on():
    
    return registry.value_exists(REG_APP, "NvidiaDramActive")

def toggle_nvidia_dram_active():
    
    if is_nvidia_dram_active_on():
        registry.reg_delete(REG_APP, "NvidiaDramActive")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableGpuASPMFlags")
            registry.reg_delete(path, "RMEnableHybridNvlink")
    else:
        registry.reg_add(REG_APP, "NvidiaDramActive", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableGpuASPMFlags", 0x1F, "REG_DWORD")
            registry.reg_add(path, "RMEnableHybridNvlink", 1, "REG_DWORD")
    return True

def is_nvidia_acpi_d3_on():
    
    return registry.value_exists(REG_APP, "NvidiaAcpiD3")

def toggle_nvidia_acpi_d3():
    
    if is_nvidia_acpi_d3_on():
        registry.reg_delete(REG_APP, "NvidiaAcpiD3")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMAcpiD3ColdControl")
            registry.reg_delete(path, "RMDeepL1EntryLatencyUsec")
    else:
        registry.reg_add(REG_APP, "NvidiaAcpiD3", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMAcpiD3ColdControl", 0, "REG_DWORD")
            registry.reg_add(path, "RMDeepL1EntryLatencyUsec", 1, "REG_DWORD")
    return True

def is_nvidia_bus_clocks_on():
    
    return registry.value_exists(REG_APP, "NvidiaBusClocks")

def toggle_nvidia_bus_clocks():
    
    if is_nvidia_bus_clocks_on():
        registry.reg_delete(REG_APP, "NvidiaBusClocks")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnableBusClockGating")
            registry.reg_delete(path, "RMPcieSpeedOverride")
    else:
        registry.reg_add(REG_APP, "NvidiaBusClocks", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnableBusClockGating", 0, "REG_DWORD")
            registry.reg_add(path, "RMPcieSpeedOverride", 3, "REG_DWORD")
    return True

def is_nvidia_elpg_on():
    
    return registry.value_exists(REG_APP, "NvidiaElpg")

def toggle_nvidia_elpg():
    
    if is_nvidia_elpg_on():
        registry.reg_delete(REG_APP, "NvidiaElpg")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableELPG")
            registry.reg_delete(path, "RMElpgEnabled")
    else:
        registry.reg_add(REG_APP, "NvidiaElpg", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableELPG", 1, "REG_DWORD")
            registry.reg_add(path, "RMElpgEnabled", 0, "REG_DWORD")
    return True

def is_nvidia_engine_clocks_on():
    
    return registry.value_exists(REG_APP, "NvidiaEngineClocks")

def toggle_nvidia_engine_clocks():
    
    if is_nvidia_engine_clocks_on():
        registry.reg_delete(REG_APP, "NvidiaEngineClocks")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEngineClock")
            registry.reg_delete(path, "RMForcePostGC6ClkSpeed")
    else:
        registry.reg_add(REG_APP, "NvidiaEngineClocks", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEngineClock", 1, "REG_DWORD")
            registry.reg_add(path, "RMForcePostGC6ClkSpeed", 1, "REG_DWORD")
    return True

def is_nvidia_gc6_idle_on():
    
    return registry.value_exists(REG_APP, "NvidiaGc6Idle")

def toggle_nvidia_gc6_idle():
    
    if is_nvidia_gc6_idle_on():
        registry.reg_delete(REG_APP, "NvidiaGc6Idle")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableGC6")
            registry.reg_delete(path, "RMGc6IdleThresholdUsec")
    else:
        registry.reg_add(REG_APP, "NvidiaGc6Idle", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableGC6", 1, "REG_DWORD")
            registry.reg_add(path, "RMGc6IdleThresholdUsec", 0xFFFFFFFF, "REG_DWORD")
    return True

def is_nvidia_interrupts_on():
    
    return registry.value_exists(REG_APP, "NvidiaInterrupts")

def toggle_nvidia_interrupts():
    
    if is_nvidia_interrupts_on():
        registry.reg_delete(REG_APP, "NvidiaInterrupts")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RmGpuInterruptOptimization")
            registry.reg_delete(path, "RMEnableMsiInterrupts")
    else:
        registry.reg_add(REG_APP, "NvidiaInterrupts", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RmGpuInterruptOptimization", 1, "REG_DWORD")
            registry.reg_add(path, "RMEnableMsiInterrupts", 1, "REG_DWORD")
    return True

def is_nvidia_pci_latency_on():
    
    return registry.value_exists(REG_APP, "NvidiaPciLatency")

def toggle_nvidia_pci_latency():
    
    if is_nvidia_pci_latency_on():
        registry.reg_delete(REG_APP, "NvidiaPciLatency")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMPciLatencyTimer")
            registry.reg_delete(path, "RMMaxMpsLimit")
    else:
        registry.reg_add(REG_APP, "NvidiaPciLatency", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMPciLatencyTimer", 0, "REG_DWORD")
            registry.reg_add(path, "RMMaxMpsLimit", 0, "REG_DWORD")
    return True

def is_nvidia_power_features_on():
    
    return registry.value_exists(REG_APP, "NvidiaPowerFeatures")

def toggle_nvidia_power_features():
    
    if is_nvidia_power_features_on():
        registry.reg_delete(REG_APP, "NvidiaPowerFeatures")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm", "DisablePowerManagement")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnablePowerManagement")
    else:
        registry.reg_add(REG_APP, "NvidiaPowerFeatures", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm", "DisablePowerManagement", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnablePowerManagement", 0, "REG_DWORD")
    return True

def is_nvidia_frame_scheduling_on():
    
    return registry.value_exists(REG_APP, "NvidiaFrameScheduling")

def toggle_nvidia_frame_scheduling():
    
    if is_nvidia_frame_scheduling_on():
        registry.reg_delete(REG_APP, "NvidiaFrameScheduling")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnablePreemption")
            registry.reg_delete(path, "RMFlipQueueLimit")
    else:
        registry.reg_add(REG_APP, "NvidiaFrameScheduling", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnablePreemption", 0, "REG_DWORD")
            registry.reg_add(path, "RMFlipQueueLimit", 1, "REG_DWORD")
    return True

def is_nvidia_gfe_on():
    
    return registry.value_exists(REG_APP, "NvidiaGfe")

def toggle_nvidia_gfe():
    
    if is_nvidia_gfe_on():
        registry.reg_delete(REG_APP, "NvidiaGfe")
        services = ["NvContainerLocalSystem", "NvContainerNetworkService", "NVDisplay.ContainerLocalSystem"]
        for svc in services:
            system.run_cmd(f'sc config "{svc}" start= auto')
    else:
        registry.reg_add(REG_APP, "NvidiaGfe", 1, "REG_DWORD")
        services = ["NvContainerLocalSystem", "NvContainerNetworkService", "NVDisplay.ContainerLocalSystem"]
        for svc in services:
            system.run_cmd(f'sc stop "{svc}"')
            system.run_cmd(f'sc config "{svc}" start= disabled')
    return True

def is_nvidia_low_power_on():
    
    return registry.value_exists(REG_APP, "NvidiaLowPower")

def toggle_nvidia_low_power():
    
    if is_nvidia_low_power_on():
        registry.reg_delete(REG_APP, "NvidiaLowPower")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableLPWR")
            registry.reg_delete(path, "RMLpwrEiIdleThresholdUs")
    else:
        registry.reg_add(REG_APP, "NvidiaLowPower", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableLPWR", 1, "REG_DWORD")
            registry.reg_add(path, "RMLpwrEiIdleThresholdUs", 0xFFFFFFFF, "REG_DWORD")
    return True

def is_nvidia_aspm_off():
    
    return registry.value_exists(REG_APP, "NvidiaAspmOff")

def toggle_nvidia_aspm():
    
    if is_nvidia_aspm_off():
        registry.reg_delete(REG_APP, "NvidiaAspmOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableASPM")
            registry.reg_delete(path, "RMPcieAspmL0sLatency")
            registry.reg_delete(path, "RMPcieAspmL1Latency")
    else:
        registry.reg_add(REG_APP, "NvidiaAspmOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableASPM", 1, "REG_DWORD")
            registry.reg_add(path, "RMPcieAspmL0sLatency", 0, "REG_DWORD")
            registry.reg_add(path, "RMPcieAspmL1Latency", 0, "REG_DWORD")
    return True

def is_nvidia_display_power_off():
    
    return registry.value_exists(REG_APP, "NvidiaDisplayPowerOff")

def toggle_nvidia_display_power():
    
    if is_nvidia_display_power_off():
        registry.reg_delete(REG_APP, "NvidiaDisplayPowerOff")
        registry.reg_delete(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\Global\NVTweak", "DisplayPowerSaving")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisplayPowerManagement")
    else:
        registry.reg_add(REG_APP, "NvidiaDisplayPowerOff", 1, "REG_DWORD")
        registry.reg_add(r"HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\Global\NVTweak", "DisplayPowerSaving", 0, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisplayPowerManagement", 0, "REG_DWORD")
    return True

def is_nvidia_ecc_off():
    
    return registry.value_exists(REG_APP, "NvidiaEccOff")

def toggle_nvidia_ecc():
    
    if is_nvidia_ecc_off():
        registry.reg_delete(REG_APP, "NvidiaEccOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnableEcc")
    else:
        registry.reg_add(REG_APP, "NvidiaEccOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnableEcc", 0, "REG_DWORD")
    return True

def is_nvidia_gc5_caching_off():
    
    return registry.value_exists(REG_APP, "NvidiaGc5CachingOff")

def toggle_nvidia_gc5_caching():
    
    if is_nvidia_gc5_caching_off():
        registry.reg_delete(REG_APP, "NvidiaGc5CachingOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableGC5")
            registry.reg_delete(path, "RMGc5CacheSupport")
    else:
        registry.reg_add(REG_APP, "NvidiaGc5CachingOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableGC5", 1, "REG_DWORD")
            registry.reg_add(path, "RMGc5CacheSupport", 0, "REG_DWORD")
    return True

def is_nvidia_misc_power_off():
    
    return registry.value_exists(REG_APP, "NvidiaMiscPowerOff")

def toggle_nvidia_misc_power():
    
    if is_nvidia_misc_power_off():
        registry.reg_delete(REG_APP, "NvidiaMiscPowerOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnableMemoryPowerManagement")
            registry.reg_delete(path, "RMEnableFbMemPowerMgmt")
    else:
        registry.reg_add(REG_APP, "NvidiaMiscPowerOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnableMemoryPowerManagement", 0, "REG_DWORD")
            registry.reg_add(path, "RMEnableFbMemPowerMgmt", 0, "REG_DWORD")
    return True

def is_nvidia_thermal_throttle_off():
    
    return registry.value_exists(REG_APP, "NvidiaThermalThrottleOff")

def toggle_nvidia_thermal_throttle():
    
    if is_nvidia_thermal_throttle_off():
        registry.reg_delete(REG_APP, "NvidiaThermalThrottleOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableThermalThrottling")
            registry.reg_delete(path, "RMEnableThermalPowerManagement")
    else:
        registry.reg_add(REG_APP, "NvidiaThermalThrottleOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableThermalThrottling", 1, "REG_DWORD")
            registry.reg_add(path, "RMEnableThermalPowerManagement", 0, "REG_DWORD")
    return True

def is_nvidia_tcc_off():
    
    return registry.value_exists(REG_APP, "NvidiaTccOff")

def toggle_nvidia_tcc():
    
    if is_nvidia_tcc_off():
        registry.reg_delete(REG_APP, "NvidiaTccOff")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "TCCSupported")
    else:
        registry.reg_add(REG_APP, "NvidiaTccOff", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "TCCSupported", 0, "REG_DWORD")
    return True

def is_nvidia_polling_latency_on():
    
    return registry.value_exists(REG_APP, "NvidiaPollingLatency")

def toggle_nvidia_polling_latency():
    
    if is_nvidia_polling_latency_on():
        registry.reg_delete(REG_APP, "NvidiaPollingLatency")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMPollingInterval")
            registry.reg_delete(path, "RMGpuPollPeriod")
    else:
        registry.reg_add(REG_APP, "NvidiaPollingLatency", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMPollingInterval", 1, "REG_DWORD")
            registry.reg_add(path, "RMGpuPollPeriod", 1, "REG_DWORD")
    return True

def is_nvidia_clock_policy_on():
    
    return registry.value_exists(REG_APP, "NvidiaClockPolicy")

def toggle_nvidia_clock_policy():
    
    if is_nvidia_clock_policy_on():
        registry.reg_delete(REG_APP, "NvidiaClockPolicy")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMEnableAggressivePState")
            registry.reg_delete(path, "RMUnrestrictedPState")
    else:
        registry.reg_add(REG_APP, "NvidiaClockPolicy", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMEnableAggressivePState", 1, "REG_DWORD")
            registry.reg_add(path, "RMUnrestrictedPState", 1, "REG_DWORD")
    return True

def is_nvidia_watchdog_on():
    
    return registry.value_exists(REG_APP, "NvidiaWatchdog")

def toggle_nvidia_watchdog():
    
    if is_nvidia_watchdog_on():
        registry.reg_delete(REG_APP, "NvidiaWatchdog")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisableWatchdog")
            registry.reg_delete(path, "RMWatchdogTimeout")
    else:
        registry.reg_add(REG_APP, "NvidiaWatchdog", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisableWatchdog", 1, "REG_DWORD")
            registry.reg_add(path, "RMWatchdogTimeout", 0, "REG_DWORD")
    return True

def is_nvidia_perf_limits_on():
    
    return registry.value_exists(REG_APP, "NvidiaPerfLimits")

def toggle_nvidia_perf_limits():
    
    if is_nvidia_perf_limits_on():
        registry.reg_delete(REG_APP, "NvidiaPerfLimits")
        for path in get_nvidia_paths():
            registry.reg_delete(path, "RMDisablePerfLimit")
            registry.reg_delete(path, "RMPerfLevelSrc")
            registry.reg_delete(path, "RMUnlockPerformance")
    else:
        registry.reg_add(REG_APP, "NvidiaPerfLimits", 1, "REG_DWORD")
        for path in get_nvidia_paths():
            registry.reg_add(path, "RMDisablePerfLimit", 1, "REG_DWORD")
            registry.reg_add(path, "RMPerfLevelSrc", 0x2222, "REG_DWORD")
            registry.reg_add(path, "RMUnlockPerformance", 1, "REG_DWORD")
    return True


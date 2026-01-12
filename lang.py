

def get_system_language():
    try:
        import ctypes
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return "vi" if lang_id == 1066 else "en"
    except:
        return "en"

TWEAKS = {
    "power_plan": {
        "vi": {"name": "Power Plan", "desc": "Kế hoạch điện tối ưu cho gaming", "risk": "⚡ Tăng điện"},
        "en": {"name": "Power Plan", "desc": "Optimized power plan for gaming", "risk": "⚡ More power"}
    },
    "svchost": {
        "vi": {"name": "SvcHost Split", "desc": "Tách service theo RAM", "risk": "✓ An toàn"},
        "en": {"name": "SvcHost Split", "desc": "Split services by RAM", "risk": "✓ Safe"}
    },
    "csrss": {
        "vi": {"name": "CSRSS Priority", "desc": "Tăng ưu tiên input chuột", "risk": "✓ An toàn"},
        "en": {"name": "CSRSS Priority", "desc": "Mouse input priority", "risk": "✓ Safe"}
    },
    "timer": {
        "vi": {"name": "Timer Resolution", "desc": "Độ chính xác timer 0.5ms", "risk": "⚡ Tăng điện"},
        "en": {"name": "Timer Resolution", "desc": "0.5ms timer accuracy", "risk": "⚡ More power"}
    },
    "msi": {
        "vi": {"name": "MSI Mode", "desc": "MSI cho GPU và NIC", "risk": "✓ An toàn"},
        "en": {"name": "MSI Mode", "desc": "MSI for GPU and NIC", "risk": "✓ Safe"}
    },
    "affinity": {
        "vi": {"name": "CPU Affinity", "desc": "Phân bố thiết bị CPU", "risk": "✓ An toàn"},
        "en": {"name": "CPU Affinity", "desc": "Spread devices across CPU", "risk": "✓ Safe"}
    },
    "memory": {
        "vi": {"name": "Memory Opt", "desc": "Tối ưu RAM, tắt prefetch", "risk": "⚠ Chậm boot"},
        "en": {"name": "Memory Opt", "desc": "RAM optimization, no prefetch", "risk": "⚠ Slow boot"}
    },
    "mouse": {
        "vi": {"name": "Mouse Fix", "desc": "Xóa mouse acceleration", "risk": "✓ An toàn"},
        "en": {"name": "Mouse Fix", "desc": "Remove acceleration", "risk": "✓ Safe"}
    },
    
    "gpu": {
        "vi": {"name": "GPU Tweaks", "desc": "HAGS, FSO, GameMode", "risk": "✓ An toàn"},
        "en": {"name": "GPU Tweaks", "desc": "HAGS, FSO, GameMode", "risk": "✓ Safe"}
    },
    "hdcp": {
        "vi": {"name": "HDCP Off", "desc": "Tắt bảo vệ nội dung HD", "risk": "✓ An toàn"},
        "en": {"name": "HDCP Off", "desc": "Disable HD protection", "risk": "✓ Safe"}
    },
    "preemption": {
        "vi": {"name": "Preemption", "desc": "Tắt GPU preemption", "risk": "⚠ Có thể đơ"},
        "en": {"name": "Preemption", "desc": "Disable GPU preemption", "risk": "⚠ May hang"}
    },
    "telemetry": {
        "vi": {"name": "NV Telemetry", "desc": "Tắt thu thập Nvidia", "risk": "✓ An toàn"},
        "en": {"name": "NV Telemetry", "desc": "Disable Nvidia telemetry", "risk": "✓ Safe"}
    },
    "nvidia_tweaks": {
        "vi": {"name": "NV Tweaks", "desc": "Power saving, services", "risk": "✓ An toàn"},
        "en": {"name": "NV Tweaks", "desc": "Power saving, services", "risk": "✓ Safe"}
    },
    "npi": {
        "vi": {"name": "Profile Inspector", "desc": "Profile Nvidia tối ưu", "risk": "⚠ Reset settings"},
        "en": {"name": "Profile Inspector", "desc": "Optimized Nvidia profile", "risk": "⚠ Reset settings"}
    },
    "write_combining": {
        "vi": {"name": "Write Combining", "desc": "VRAM latency", "risk": "⚠ Có thể giảm FPS"},
        "en": {"name": "Write Combining", "desc": "VRAM latency", "risk": "⚠ May reduce FPS"}
    },
    "amd_tweaks": {
        "vi": {"name": "AMD Tweaks", "desc": "Power gating, DeLag, ULPS", "risk": "🔥 Tăng nhiệt GPU"},
        "en": {"name": "AMD Tweaks", "desc": "Power gating, DeLag, ULPS", "risk": "🔥 Hotter GPU"}
    },
    "intel_vram": {
        "vi": {"name": "Intel VRAM", "desc": "Tăng VRAM lên 1024MB", "risk": "✓ An toàn"},
        "en": {"name": "Intel VRAM", "desc": "Increase VRAM to 1024MB", "risk": "✓ Safe"}
    },
    
    "tcpip": {
        "vi": {"name": "TCP/IP", "desc": "Tối ưu stack mạng", "risk": "⚠ Không dùng Wi-Fi"},
        "en": {"name": "TCP/IP", "desc": "Network stack optimization", "risk": "⚠ No Wi-Fi"}
    },
    "nic": {
        "vi": {"name": "NIC Opt", "desc": "Tắt power saving NIC", "risk": "⚠ Không dùng Wi-Fi"},
        "en": {"name": "NIC Opt", "desc": "Disable NIC power saving", "risk": "⚠ No Wi-Fi"}
    },
    "netsh": {
        "vi": {"name": "Netsh", "desc": "DCA, RSS, timestamps", "risk": "✓ An toàn"},
        "en": {"name": "Netsh", "desc": "DCA, RSS, timestamps", "risk": "✓ Safe"}
    },
    
    "mitigations": {
        "vi": {"name": "Mitigations", "desc": "Tắt Spectre/Meltdown", "risk": "🔓 Giảm bảo mật"},
        "en": {"name": "Mitigations", "desc": "Disable Spectre/Meltdown", "risk": "🔓 Less secure"}
    },
    "bcdedit": {
        "vi": {"name": "BCDEdit", "desc": "Boot config tweaks", "risk": "⚠ Có thể không boot"},
        "en": {"name": "BCDEdit", "desc": "Boot config tweaks", "risk": "⚠ May fail boot"}
    },
    "usb_power": {
        "vi": {"name": "USB Power", "desc": "Tắt USB power saving", "risk": "⚡ Tăng điện"},
        "en": {"name": "USB Power", "desc": "Disable USB power saving", "risk": "⚡ More power"}
    },
    "cstates": {
        "vi": {"name": "C-States", "desc": "Tắt deep C-States", "risk": "🔥 Tăng nhiệt CPU"},
        "en": {"name": "C-States", "desc": "Disable deep C-States", "risk": "🔥 Hotter CPU"}
    },
    "idle": {
        "vi": {"name": "Disable Idle", "desc": "CPU không idle", "risk": "🔥🔥 RẤT NÓNG"},
        "en": {"name": "Disable Idle", "desc": "CPU never idles", "risk": "🔥🔥 VERY HOT"}
    },
    "pstates": {
        "vi": {"name": "P-States 0", "desc": "GPU max clock", "risk": "🔥 Tăng nhiệt GPU"},
        "en": {"name": "P-States 0", "desc": "GPU max clock", "risk": "🔥 Hotter GPU"}
    },
    
    "win_telemetry": {
        "vi": {"name": "Win Telemetry", "desc": "Tắt thu thập Windows", "risk": "✓ An toàn"},
        "en": {"name": "Win Telemetry", "desc": "Disable Windows telemetry", "risk": "✓ Safe"}
    },
    "cortana": {
        "vi": {"name": "Cortana", "desc": "Tắt Cortana", "risk": "✓ An toàn"},
        "en": {"name": "Cortana", "desc": "Disable Cortana", "risk": "✓ Safe"}
    },
    "activity": {
        "vi": {"name": "Activity History", "desc": "Tắt lịch sử hoạt động", "risk": "✓ An toàn"},
        "en": {"name": "Activity History", "desc": "Disable activity history", "risk": "✓ Safe"}
    },
    "location": {
        "vi": {"name": "Location", "desc": "Tắt theo dõi vị trí", "risk": "✓ An toàn"},
        "en": {"name": "Location", "desc": "Disable location tracking", "risk": "✓ Safe"}
    },
    "ads": {
        "vi": {"name": "Ads ID", "desc": "Tắt ID quảng cáo", "risk": "✓ An toàn"},
        "en": {"name": "Ads ID", "desc": "Disable advertising ID", "risk": "✓ Safe"}
    },
    "feedback": {
        "vi": {"name": "Feedback", "desc": "Tắt feedback Windows", "risk": "✓ An toàn"},
        "en": {"name": "Feedback", "desc": "Disable Windows feedback", "risk": "✓ Safe"}
    },
    "all_privacy": {
        "vi": {"name": "All Privacy", "desc": "Áp dụng tất cả privacy", "risk": "✓ An toàn"},
        "en": {"name": "All Privacy", "desc": "Apply all privacy tweaks", "risk": "✓ Safe"}
    },
    
    "visual_fx": {
        "vi": {"name": "Visual FX", "desc": "Tắt animations, transparency", "risk": "✓ An toàn"},
        "en": {"name": "Visual FX", "desc": "Disable animations, transparency", "risk": "✓ Safe"}
    },
    "gamebar": {
        "vi": {"name": "Game Bar", "desc": "Tắt Xbox Game Bar/DVR", "risk": "✓ An toàn"},
        "en": {"name": "Game Bar", "desc": "Disable Xbox Game Bar/DVR", "risk": "✓ Safe"}
    },
    "defender": {
        "vi": {"name": "Defender", "desc": "Giảm tác động, thêm exclusions", "risk": "⚠ Giảm bảo mật"},
        "en": {"name": "Defender", "desc": "Reduce impact, add exclusions", "risk": "⚠ Less secure"}
    },
    "ntfs": {
        "vi": {"name": "NTFS Tweaks", "desc": "Tối ưu file system", "risk": "✓ An toàn"},
        "en": {"name": "NTFS Tweaks", "desc": "File system optimization", "risk": "✓ Safe"}
    },
    "services": {
        "vi": {"name": "Services", "desc": "Tắt SysMain, WSearch, Xbox", "risk": "⚠ Có thể lỗi app"},
        "en": {"name": "Services", "desc": "Disable SysMain, WSearch, Xbox", "risk": "⚠ May break apps"}
    },
    "dx": {
        "vi": {"name": "DirectX", "desc": "TDR level, GPU priority", "risk": "✓ An toàn"},
        "en": {"name": "DirectX", "desc": "TDR level, GPU priority", "risk": "✓ Safe"}
    },
    "startup": {
        "vi": {"name": "Startup", "desc": "Bỏ delay khởi động", "risk": "✓ An toàn"},
        "en": {"name": "Startup", "desc": "Remove startup delay", "risk": "✓ Safe"}
    },
    "priority": {
        "vi": {"name": "Priority", "desc": "Game task scheduling", "risk": "✓ An toàn"},
        "en": {"name": "Priority", "desc": "Game task scheduling", "risk": "✓ Safe"}
    },
    "irq": {
        "vi": {"name": "IRQ Affinity", "desc": "Phân bố IRQ, giảm core 0", "risk": "✓ An toàn"},
        "en": {"name": "IRQ Affinity", "desc": "Distribute IRQ, reduce core 0", "risk": "✓ Safe"}
    },
    "dpc": {
        "vi": {"name": "DPC Latency", "desc": "Giảm DPC latency", "risk": "✓ An toàn"},
        "en": {"name": "DPC Latency", "desc": "Reduce DPC latency", "risk": "✓ Safe"}
    },
    "mmcss": {
        "vi": {"name": "MMCSS", "desc": "Tối ưu multimedia scheduler", "risk": "✓ An toàn"},
        "en": {"name": "MMCSS", "desc": "Optimize multimedia scheduler", "risk": "✓ Safe"}
    },
    "wer": {
        "vi": {"name": "Error Reporting", "desc": "Tắt báo lỗi Windows", "risk": "✓ An toàn"},
        "en": {"name": "Error Reporting", "desc": "Disable Windows error report", "risk": "✓ Safe"}
    },
    "nagle": {
        "vi": {"name": "Nagle Off", "desc": "Tắt Nagle, giảm ping", "risk": "✓ An toàn"},
        "en": {"name": "Nagle Off", "desc": "Disable Nagle, lower ping", "risk": "✓ Safe"}
    },
    "throttle": {
        "vi": {"name": "Throttle Off", "desc": "Tắt power throttling", "risk": "⚡ Tăng điện"},
        "en": {"name": "Throttle Off", "desc": "Disable power throttling", "risk": "⚡ More power"}
    },
    "parking": {
        "vi": {"name": "Core Parking", "desc": "Tắt CPU core parking", "risk": "⚡ Tăng điện"},
        "en": {"name": "Core Parking", "desc": "Disable CPU core parking", "risk": "⚡ More power"}
    },
    "all_fps": {
        "vi": {"name": "All FPS", "desc": "Áp dụng tất cả FPS tweaks", "risk": "⚠ Nhiều thay đổi"},
        "en": {"name": "All FPS", "desc": "Apply all FPS tweaks", "risk": "⚠ Many changes"}
    },
    
    "cleaner": {
        "vi": {"name": "Cleaner", "desc": "Xóa temp, cache", "risk": "✓ An toàn"},
        "en": {"name": "Cleaner", "desc": "Clear temp, cache", "risk": "✓ Safe"}
    },
    "game_boost": {
        "vi": {"name": "Game Boost", "desc": "Tối ưu cho 1 game", "risk": "✓ An toàn"},
        "en": {"name": "Game Boost", "desc": "Optimize one game", "risk": "✓ Safe"}
    },
    "soft_restart": {
        "vi": {"name": "Soft Restart", "desc": "Restart explorer, DNS", "risk": "✓ An toàn"},
        "en": {"name": "Soft Restart", "desc": "Restart explorer, DNS", "risk": "✓ Safe"}
    },
    "audio": {
        "vi": {"name": "Audio Latency", "desc": "Giảm latency âm thanh", "risk": "⚡ Tăng CPU"},
        "en": {"name": "Audio Latency", "desc": "Reduce audio latency", "risk": "⚡ More CPU"}
    },
    "w32": {
        "vi": {"name": "W32 Priority", "desc": "Priority separation", "risk": "✓ An toàn"},
        "en": {"name": "W32 Priority", "desc": "Priority separation", "risk": "✓ Safe"}
    },
    "backup": {
        "vi": {"name": "Backup", "desc": "Backup registry", "risk": "✓ An toàn"},
        "en": {"name": "Backup", "desc": "Backup registry", "risk": "✓ Safe"}
    },
    
    "nvidia_dram_active": {
        "vi": {"name": "NV DRAM Active", "desc": "Giữ bộ nhớ GPU luôn sẵn sàng, giảm delay", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV DRAM Active", "desc": "Keep GPU memory active, reduce delay", "risk": "⚡ More power"}
    },
    "nvidia_acpi_d3": {
        "vi": {"name": "NV ACPI D3", "desc": "Ngăn GPU ngủ sâu, giảm độ trễ wake", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV ACPI D3", "desc": "Prevent deep sleep, reduce wake latency", "risk": "⚡ More power"}
    },
    "nvidia_bus_clocks": {
        "vi": {"name": "NV Bus Clocks", "desc": "Giữ tốc độ PCIe ổn định, giảm micro-stutter", "risk": "✓ An toàn"},
        "en": {"name": "NV Bus Clocks", "desc": "Stable PCIe speed, reduce micro-stutter", "risk": "✓ Safe"}
    },
    "nvidia_elpg": {
        "vi": {"name": "NV ELPG", "desc": "Tối ưu tiết kiệm điện, giảm input lag", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV ELPG", "desc": "Optimize power gating, reduce input lag", "risk": "⚡ More power"}
    },
    "nvidia_engine_clocks": {
        "vi": {"name": "NV Engine Clocks", "desc": "Giữ tốc độ GPU cao, phản hồi nhanh", "risk": "🔥 Tăng nhiệt GPU"},
        "en": {"name": "NV Engine Clocks", "desc": "Keep high GPU clock, fast response", "risk": "🔥 Hotter GPU"}
    },
    "nvidia_gc6_idle": {
        "vi": {"name": "NV GC6 Idle", "desc": "Ngăn GPU giảm hiệu năng quá sâu", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV GC6 Idle", "desc": "Prevent deep idle states", "risk": "⚡ More power"}
    },
    "nvidia_interrupts": {
        "vi": {"name": "NV Interrupts", "desc": "Ưu tiên xử lý GPU, giảm input lag", "risk": "✓ An toàn"},
        "en": {"name": "NV Interrupts", "desc": "Prioritize GPU commands, reduce input lag", "risk": "✓ Safe"}
    },
    "nvidia_pci_latency": {
        "vi": {"name": "NV PCI Latency", "desc": "Tối ưu đường truyền PCIe", "risk": "✓ An toàn"},
        "en": {"name": "NV PCI Latency", "desc": "Optimize PCIe data transfer", "risk": "✓ Safe"}
    },
    "nvidia_power_features": {
        "vi": {"name": "NV Power Features", "desc": "Mở rộng kiểm soát năng lượng", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV Power Features", "desc": "Expand power control for performance", "risk": "⚡ More power"}
    },
    "nvidia_frame_scheduling": {
        "vi": {"name": "NV Frame Sched", "desc": "Xuất khung hình đều đặn hơn", "risk": "✓ An toàn"},
        "en": {"name": "NV Frame Sched", "desc": "Smoother frame pacing", "risk": "✓ Safe"}
    },
    "nvidia_gfe": {
        "vi": {"name": "NV GFE Off", "desc": "Tắt dịch vụ GeForce Experience", "risk": "✓ An toàn"},
        "en": {"name": "NV GFE Off", "desc": "Disable GeForce Experience services", "risk": "✓ Safe"}
    },
    "nvidia_low_power": {
        "vi": {"name": "NV Low Power", "desc": "Giữ vùng xử lý GPU luôn hoạt động", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV Low Power", "desc": "Keep GPU processing zones active", "risk": "⚡ More power"}
    },
    
    "nvidia_aspm": {
        "vi": {"name": "NV ASPM Off", "desc": "Tắt quản lý điện PCIe", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV ASPM Off", "desc": "Disable PCIe power management", "risk": "⚡ More power"}
    },
    "nvidia_display_power": {
        "vi": {"name": "NV Display Power", "desc": "Tắt giảm chất lượng hiển thị", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV Display Power", "desc": "Disable display power saving", "risk": "⚡ More power"}
    },
    "nvidia_ecc": {
        "vi": {"name": "NV ECC Off", "desc": "Tắt kiểm lỗi bộ nhớ, tăng băng thông", "risk": "⚠ Card chuyên dụng"},
        "en": {"name": "NV ECC Off", "desc": "Disable ECC, more bandwidth", "risk": "⚠ Pro cards only"}
    },
    "nvidia_gc5_caching": {
        "vi": {"name": "NV GC5 Off", "desc": "Ngăn GPU nghỉ tạm thời", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV GC5 Off", "desc": "Prevent temporary sleep states", "risk": "⚡ More power"}
    },
    "nvidia_misc_power": {
        "vi": {"name": "NV Misc Power", "desc": "Tắt tiết kiệm điện lặt vặt", "risk": "⚡ Tăng điện"},
        "en": {"name": "NV Misc Power", "desc": "Disable misc power features", "risk": "⚡ More power"}
    },
    "nvidia_thermal_throttle": {
        "vi": {"name": "NV Thermal Off", "desc": "Tắt tự hạ tốc khi nóng", "risk": "🔥🔥 RẤT NÓNG"},
        "en": {"name": "NV Thermal Off", "desc": "Disable thermal throttling", "risk": "🔥🔥 VERY HOT"}
    },
    "nvidia_tcc": {
        "vi": {"name": "NV TCC Off", "desc": "Chế độ Graphics thay vì Compute", "risk": "✓ An toàn"},
        "en": {"name": "NV TCC Off", "desc": "Graphics mode instead of Compute", "risk": "✓ Safe"}
    },
    
    "nvidia_polling_latency": {
        "vi": {"name": "NV Polling", "desc": "Giảm thời gian chờ CPU-GPU", "risk": "✓ An toàn"},
        "en": {"name": "NV Polling", "desc": "Reduce CPU-GPU polling latency", "risk": "✓ Safe"}
    },
    "nvidia_clock_policy": {
        "vi": {"name": "NV Clock Policy", "desc": "Cho phép GPU boost không giới hạn", "risk": "🔥 Tăng nhiệt GPU"},
        "en": {"name": "NV Clock Policy", "desc": "Unrestricted GPU boost", "risk": "🔥 Hotter GPU"}
    },
    "nvidia_watchdog": {
        "vi": {"name": "NV Watchdog", "desc": "Giảm tiến trình kiểm tra lỗi nội bộ", "risk": "⚠ Có thể đơ"},
        "en": {"name": "NV Watchdog", "desc": "Reduce internal error checking", "risk": "⚠ May hang"}
    },
    "nvidia_perf_limits": {
        "vi": {"name": "NV Perf Limits", "desc": "Gỡ bỏ giới hạn hiệu năng driver", "risk": "🔥 Tăng nhiệt GPU"},
        "en": {"name": "NV Perf Limits", "desc": "Unlock driver performance limits", "risk": "🔥 Hotter GPU"}
    },
    
    "com_ports": {
        "vi": {"name": "COM Ports Off", "desc": "Tắt cổng COM1/COM2 không dùng", "risk": "✓ An toàn"},
        "en": {"name": "COM Ports Off", "desc": "Disable unused COM ports", "risk": "✓ Safe"}
    },
    "eisa_pic": {
        "vi": {"name": "EISA PIC Off", "desc": "Tắt bộ điều khiển ngắt cũ", "risk": "⚠ Keyboard cũ"},
        "en": {"name": "EISA PIC Off", "desc": "Disable legacy interrupt controller", "risk": "⚠ Legacy keyboards"}
    },
    "hpet": {
        "vi": {"name": "HPET Off", "desc": "Tắt bộ hẹn giờ HPET, giảm input lag", "risk": "✓ An toàn"},
        "en": {"name": "HPET Off", "desc": "Disable HPET, reduce input lag", "risk": "✓ Safe"}
    },
    "gs_wavetable": {
        "vi": {"name": "GS Wavetable Off", "desc": "Tắt mô phỏng MIDI, giảm độ trễ âm thanh", "risk": "⚠ MIDI apps"},
        "en": {"name": "GS Wavetable Off", "desc": "Disable MIDI synth, reduce audio latency", "risk": "⚠ MIDI apps"}
    },
    "hyperv_driver": {
        "vi": {"name": "Hyper-V Off", "desc": "Tắt driver máy ảo Hyper-V", "risk": "⚠ VMs không chạy"},
        "en": {"name": "Hyper-V Off", "desc": "Disable Hyper-V infrastructure", "risk": "⚠ VMs won't work"}
    },
    "rdp_redirector": {
        "vi": {"name": "RDP Redirector Off", "desc": "Tắt điều khiển từ xa", "risk": "⚠ RDP không dùng"},
        "en": {"name": "RDP Redirector Off", "desc": "Disable remote desktop redirector", "risk": "⚠ No RDP"}
    },
}

UI = {
    "vi": {
        "app_name": "MeoBoost",
        "version": "Phiên bản",
        "subtitle": "Windows Performance Optimizer",
        "menu_optimize": "Tối ưu",
        "menu_deep_optimize": "Tối ưu sâu",
        "menu_privacy": "Quyền riêng tư",
        "menu_tools": "Công cụ",
        "menu_about": "Thông tin",
        "menu_language": "Ngôn ngữ",
        "menu_exit": "Thoát",
        "select": "Chọn",
        "back": "Quay lại",
        "continue": "Tiếp tục",
        "page": "Trang",
        "on": "BẬT",
        "off": "TẮT",
        "na": "N/A",
        "applying": "Đang áp dụng",
        "success": "Thành công",
        "failed": "Thất bại",
        "error": "Lỗi",
        "nvidia_section": "NVIDIA",
        "network_section": "Mạng",
        "amd_section": "AMD",
        "intel_section": "Intel",
        "advanced_warning": "⚠ Cảnh báo: Các tùy chọn nguy hiểm!",
        "disclaimer_title": "Lưu ý",
        "disclaimer_text": "Nếu không hiểu tweak, đừng bật. Khuyên backup trước.",
        "disclaimer_agree": "Nhập 'ok' để tiếp tục",
        "enter_game_path": "Nhập đường dẫn .exe",
        "file_not_found": "File không tồn tại",
        "creating_backup": "Đang backup...",
        "need_admin": "Cần quyền Admin",
        "requesting_admin": "Đang yêu cầu...",
        "about_desc": "Tối ưu Windows cho gaming",
    },
    "en": {
        "app_name": "MeoBoost",
        "version": "Version",
        "subtitle": "Windows Performance Optimizer",
        "menu_optimize": "Optimize",
        "menu_deep_optimize": "Deep Optimize",
        "menu_privacy": "Privacy",
        "menu_tools": "Tools",
        "menu_about": "About",
        "menu_language": "Language",
        "menu_exit": "Exit",
        "select": "Select",
        "back": "Back",
        "continue": "Continue",
        "page": "Page",
        "on": "ON",
        "off": "OFF",
        "na": "N/A",
        "applying": "Applying",
        "success": "Success",
        "failed": "Failed",
        "error": "Error",
        "nvidia_section": "NVIDIA",
        "network_section": "Network",
        "amd_section": "AMD",
        "intel_section": "Intel",
        "advanced_warning": "⚠ Warning: Dangerous options!",
        "disclaimer_title": "Notice",
        "disclaimer_text": "Don't enable what you don't understand. Backup first.",
        "disclaimer_agree": "Type 'ok' to continue",
        "enter_game_path": "Enter .exe path",
        "file_not_found": "File not found",
        "creating_backup": "Creating backup...",
        "need_admin": "Admin required",
        "requesting_admin": "Requesting...",
        "about_desc": "Windows optimizer for gaming",
    }
}

_lang = None

def init_language(lang=None):
    global _lang
    _lang = lang if lang else get_system_language()

def get_lang():
    global _lang
    if not _lang:
        init_language()
    return _lang

def set_lang(lang):
    global _lang
    _lang = lang

def t(key):
    return UI.get(get_lang(), UI["en"]).get(key, key)

def tw(tweak_key, field):
    tweak = TWEAKS.get(tweak_key, {})
    return tweak.get(get_lang(), tweak.get("en", {})).get(field, "")

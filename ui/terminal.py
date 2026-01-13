"""
MeoBoost Terminal UI - Full Mode
"""

import os
import sys
import subprocess

from rich.console import Console
from rich.table import Table
from rich import box

from config import VERSION, APP_NAME, DATA_DIR, GITHUB_URL
from lang import t, tw, get_lang, set_lang, init_language
from utils import system, backup

from tweaks import power, nvidia, amd, intel, gpu_common, network, memory, input, misc
from tweaks import system as sys_tweaks
from tweaks import privacy, fps


console = Console()

C1, C2, C3 = "#00d4ff", "#0096c7", "#ff6b9d"
OK, WARN, ERR, DIM = "#00ff88", "#ffaa00", "#ff4444", "#555555"


def cls():
    # Clear screen using subprocess for security (avoid shell injection)
    if os.name == 'nt':
        subprocess.run(['cmd', '/c', 'cls'], shell=False, check=False)
    else:
        subprocess.run(['clear'], shell=False, check=False)


def badge(on, na=False):
    if na:
        return f"[{DIM}]─[/]"
    return f"[{OK}]●[/]" if on else f"[{ERR}]○[/]"


def item(key, tid, on, na=False):
    name = tw(tid, "name") or tid
    desc = tw(tid, "desc") or ""
    risk = tw(tid, "risk") or ""
    rc = OK if "✓" in risk else (ERR if "🔥" in risk or "🔓" in risk else WARN)
    return f"[{C2}][{key}][/] {name} {badge(on, na)}\n[{DIM}]{desc}[/]\n[{rc}]{risk}[/]"


def logo():
    cls()
    console.print(f"[{C1}]╔{'═'*68}╗[/]", justify="center")
    console.print(f"[{C1}]║                                                                    ║[/]", justify="center")
    console.print(f"[{C1}]║    ▄▀▄▀▄   ▄▀▄▀▄  ▄▀▀▀▄  ▄▀▀▀▄  ▄▀▀▀▄  ▄▀▀▀▄  ▄▀▀▀▀  ▀▀▀█▀▀▀       ║[/]", justify="center")
    console.print(f"[{C2}]║    █ █ █   █▀▀▀   █   █  █   █  █   █  █   █  ▀▀▀▀█    █          ║[/]", justify="center")
    console.print(f"[{C2}]║    █   █   █▄▄▄   ▀▄▄▄▀  ▀▄▄▄▀  ▀▄▄▄▀  ▀▄▄▄▀  ▄▄▄▄▀    █          ║[/]", justify="center")
    console.print(f"[{C1}]║                                                                    ║[/]", justify="center")
    console.print(f"[{C1}]╚{'═'*68}╝[/]", justify="center")
    console.print()


def grid(items, cols=3):
    tbl = Table(show_header=False, box=None, expand=True, padding=(0, 2))
    for _ in range(cols):
        tbl.add_column(ratio=1)
    for i in range(0, len(items), cols):
        row = items[i:i+cols]
        while len(row) < cols:
            row.append("")
        tbl.add_row(*row)
    console.print(tbl)


def footer(pg=None, tot=None):
    console.print()
    nav = f"[{DIM}][B]{t('back')}[/]"
    if pg and tot and tot > 1:
        nav += f" [{C2}][N]{t('page')} {pg}/{tot}[/]"
    nav += f" [{ERR}][X]{t('menu_exit')}[/]"
    console.print(nav, justify="center")


def inp():
    console.print()
    try:
        return console.input(f"[{C3}]▸[/] ").strip()
    except (KeyboardInterrupt, EOFError):
        # Handle Ctrl+C and EOF gracefully - return exit command
        return "x"


# === MAIN ===

_beta = False

def main():
    while True:
        logo()
        items = [
            f"[{C2}][1][/] {t('menu_optimize')}",
            f"[{C2}][2][/] {t('menu_deep_optimize')}",
            f"[{C2}][3][/] {t('menu_privacy')}",
            f"[{C2}][4][/] {t('menu_tools')}",
            f"[{C2}][5][/] {t('menu_language')} [{DIM}]{get_lang().upper()}[/]",
            f"[{ERR}][X][/] {t('menu_exit')}",
        ]
        
        tbl = Table(show_header=False, box=None, expand=True, padding=(1, 3))
        tbl.add_column(ratio=1, justify="center")
        tbl.add_column(ratio=1, justify="center")
        for i in range(0, len(items), 2):
            tbl.add_row(items[i], items[i+1] if i+1 < len(items) else "")
        console.print(tbl)
        
        ch = inp()
        if ch == "1": menu_optimize()
        elif ch == "2": menu_deep_optimize()
        elif ch == "3": menu_privacy()
        elif ch == "4": menu_tools()
        elif ch == "5": menu_lang()
        elif ch.lower() == "x": break


# === OPTIMIZE (Merged with FPS) ===

def menu_optimize(pg=1):
    gpu = system.get_gpu_type()
    laptop = system.is_laptop()
    # Pages: 1=Basic, 2=FPS, 3=FPS2, 4=GPU, 5=Network
    total_pages = 5
    
    while True:
        logo()
        console.print(f"[{C1}]─── {t('menu_optimize')} ───[/] [{DIM}]{t('page')} {pg}/{total_pages}[/]", justify="center")
        console.print()
        
        if pg == 1:
            # Basic system optimizations
            console.print(f"[{C3}]◈[/] [{C1}]Basic[/]", justify="center")
            console.print()
            items = [
                item("1", "power_plan", power.is_power_plan_on(), laptop),
                item("2", "svchost", power.is_svchost_on()),
                item("3", "csrss", memory.is_csrss_high()),
                item("4", "timer", power.is_timer_on()),
                item("5", "msi", network.is_msi_on()),
                item("6", "affinity", network.is_affinity_on()),
                item("7", "memory", memory.is_memory_on()),
                item("8", "mouse", input.is_mouse_fix_on()),
            ]
            acts = {
                "1": power.toggle_power_plan, "2": power.toggle_svchost,
                "3": memory.toggle_csrss, "4": power.toggle_timer,
                "5": network.toggle_msi, "6": network.toggle_affinity,
                "7": memory.toggle_memory, "8": lambda: input.toggle_mouse_fix(),
            }
        elif pg == 2:
            # FPS tweaks page 1
            console.print(f"[{C3}]◈[/] [{C1}]FPS Boost[/]", justify="center")
            console.print()
            items = [
                item("1", "visual_fx", fps.is_visual_fx_off()),
                item("2", "gamebar", fps.is_gamebar_off()),
                item("3", "ntfs", fps.is_ntfs_tweaked()),
                item("4", "services", fps.is_services_optimized()),
                item("5", "dx", fps.is_dx_optimized()),
                item("6", "startup", fps.is_startup_optimized()),
                item("7", "priority", fps.is_priority_optimized()),
                item("8", "defender", fps.is_defender_reduced()),
            ]
            acts = {
                "1": fps.toggle_visual_fx, "2": fps.toggle_gamebar,
                "3": fps.toggle_ntfs, "4": fps.toggle_services,
                "5": fps.toggle_dx, "6": fps.toggle_startup,
                "7": fps.toggle_priority, "8": fps.toggle_defender,
            }
        elif pg == 3:
            # FPS tweaks page 2
            console.print(f"[{C3}]◈[/] [{C1}]FPS Boost 2[/]", justify="center")
            console.print()
            items = [
                item("1", "irq", fps.is_irq_optimized()),
                item("2", "dpc", fps.is_dpc_optimized()),
                item("3", "mmcss", fps.is_mmcss_optimized()),
                item("4", "wer", fps.is_wer_off()),
                item("5", "nagle", fps.is_nagle_off()),
                item("6", "throttle", fps.is_throttle_off()),
                item("7", "parking", fps.is_parking_off()),
                f"[{WARN}][A][/] {tw('all_fps', 'name')}\n[{DIM}]{tw('all_fps', 'desc')}[/]\n[{WARN}]{tw('all_fps', 'risk')}[/]",
            ]
            acts = {
                "1": fps.toggle_irq, "2": fps.toggle_dpc,
                "3": fps.toggle_mmcss, "4": fps.toggle_wer,
                "5": fps.toggle_nagle, "6": fps.toggle_throttle,
                "7": fps.toggle_parking, "a": fps.apply_all_fps,
            }
        elif pg == 4:
            # GPU tweaks
            console.print(f"[{C3}]◈[/] [{C1}]GPU[/]", justify="center")
            console.print()
            items = [item("1", "gpu", gpu_common.is_gpu_tweaks_on())]
            acts = {"1": gpu_common.toggle_gpu_tweaks}
            if gpu == "nvidia":
                items.extend([
                    item("2", "hdcp", nvidia.is_hdcp_off()),
                    item("3", "preemption", nvidia.is_preemption_off()),
                    item("4", "telemetry", nvidia.is_telemetry_off()),
                    item("5", "nvidia_tweaks", nvidia.is_nvidia_tweaks_on()),
                    item("6", "npi", nvidia.is_npi_applied()),
                    item("7", "write_combining", nvidia.is_wc_off()),
                    item("8", "nvidia_gfe", nvidia.is_nvidia_gfe_on()),
                ])
                acts.update({
                    "2": nvidia.toggle_hdcp, "3": nvidia.toggle_preemption,
                    "4": nvidia.toggle_telemetry, "5": nvidia.toggle_nvidia_tweaks,
                    "6": nvidia.toggle_npi, "7": nvidia.toggle_wc,
                    "8": nvidia.toggle_nvidia_gfe,
                })
            elif gpu == "amd":
                items.append(item("2", "amd_tweaks", False))
                acts["2"] = amd.apply_amd_tweaks
            elif gpu == "intel":
                items.append(item("2", "intel_vram", intel.is_vram_increased()))
                acts["2"] = intel.toggle_vram
        else:
            # Network tweaks
            console.print(f"[{C3}]◈[/] [{C1}]{t('network_section')}[/]", justify="center")
            console.print()
            items = [
                item("1", "tcpip", network.is_tcpip_on()),
                item("2", "nic", network.is_nic_on()),
                item("3", "netsh", network.is_netsh_on()),
            ]
            acts = {"1": network.toggle_tcpip, "2": network.toggle_nic, "3": network.toggle_netsh}
        
        grid(items, 3)
        footer(pg, total_pages)
        ch = inp().lower()
        if ch == "b": break
        elif ch == "x": sys.exit(0)
        elif ch == "n": pg = (pg % total_pages) + 1
        elif ch in acts: do(acts[ch])


# === PRIVACY ===

def menu_privacy():
    while True:
        logo()
        console.print(f"[{C1}]─── {t('menu_privacy')} ───[/]", justify="center")
        console.print()
        items = [
            item("1", "win_telemetry", privacy.is_telemetry_off()),
            item("2", "cortana", privacy.is_cortana_off()),
            item("3", "activity", privacy.is_activity_off()),
            item("4", "location", privacy.is_location_off()),
            item("5", "ads", privacy.is_ads_off()),
            item("6", "feedback", privacy.is_feedback_off()),
            item("7", "copilot", privacy.is_copilot_off()),
            item("8", "bg_apps", privacy.is_bg_apps_off()),
            item("9", "bing_search", privacy.is_bing_search_off()),
            f"[{WARN}][A][/] {tw('all_privacy', 'name')}\n[{DIM}]{tw('all_privacy', 'desc')}[/]\n[{OK}]{tw('all_privacy', 'risk')}[/]",
        ]
        acts = {
            "1": privacy.toggle_telemetry, "2": privacy.toggle_cortana,
            "3": privacy.toggle_activity, "4": privacy.toggle_location,
            "5": privacy.toggle_ads, "6": privacy.toggle_feedback,
            "7": privacy.toggle_copilot, "8": privacy.toggle_bg_apps,
            "9": privacy.toggle_bing_search, "a": privacy.apply_all_privacy,
        }
        grid(items, 3)
        footer()
        ch = inp().lower()
        if ch == "b": break
        elif ch == "x": sys.exit(0)
        elif ch in acts: do(acts[ch])


# === DEEP OPTIMIZE (Dangerous Tweaks) ===

def menu_deep_optimize(pg=1):
    gpu = system.get_gpu_type()
    total_pages = 5 if gpu == "nvidia" else 2
    
    while True:
        logo()
        console.print(f"[{C1}]─── {t('menu_deep_optimize')} ───[/] [{DIM}]{t('page')} {pg}/{total_pages}[/]", justify="center")
        console.print(f"[{WARN}]⚠ Cảnh báo: Các tùy chọn nguy hiểm![/]", justify="center")
        console.print()
        
        if pg == 1:
            # System & Power dangerous tweaks
            console.print(f"[{C3}]◈[/] [{C1}]System & Power[/]", justify="center")
            console.print()
            items = [
                item("1", "mitigations", sys_tweaks.is_mitigations_off()),
                item("2", "bcdedit", sys_tweaks.is_bcdedit_on()),
                item("3", "usb_power", sys_tweaks.is_usb_power_off()),
                item("4", "cstates", power.is_cstates_off()),
                item("5", "idle", power.is_idle_disabled()),
            ]
            acts = {
                "1": sys_tweaks.toggle_mitigations, "2": sys_tweaks.toggle_bcdedit,
                "3": sys_tweaks.toggle_usb_power, "4": power.toggle_cstates,
                "5": power.toggle_idle,
            }
            if gpu == "nvidia":
                items.append(item("6", "pstates", power.is_pstates_on()))
                acts["6"] = power.toggle_pstates
        elif pg == 2:
            # System devices
            console.print(f"[{C3}]◈[/] [{C1}]System Devices[/]", justify="center")
            console.print()
            items = [
                item("1", "com_ports", sys_tweaks.is_com_ports_off()),
                item("2", "eisa_pic", sys_tweaks.is_eisa_pic_off()),
                item("3", "hpet", sys_tweaks.is_hpet_off()),
                item("4", "gs_wavetable", sys_tweaks.is_gs_wavetable_off()),
                item("5", "hyperv_driver", sys_tweaks.is_hyperv_driver_off()),
                item("6", "rdp_redirector", sys_tweaks.is_rdp_redirector_off()),
            ]
            acts = {
                "1": sys_tweaks.toggle_com_ports, "2": sys_tweaks.toggle_eisa_pic,
                "3": sys_tweaks.toggle_hpet, "4": sys_tweaks.toggle_gs_wavetable,
                "5": sys_tweaks.toggle_hyperv_driver, "6": sys_tweaks.toggle_rdp_redirector,
            }
        elif pg == 3 and gpu == "nvidia":
            # NVIDIA Power & Latency
            console.print(f"[{C3}]◈[/] [{C1}]NVIDIA - Power & Latency[/]", justify="center")
            console.print()
            items = [
                item("1", "nvidia_dram_active", nvidia.is_nvidia_dram_active_on()),
                item("2", "nvidia_acpi_d3", nvidia.is_nvidia_acpi_d3_on()),
                item("3", "nvidia_bus_clocks", nvidia.is_nvidia_bus_clocks_on()),
                item("4", "nvidia_elpg", nvidia.is_nvidia_elpg_on()),
                item("5", "nvidia_engine_clocks", nvidia.is_nvidia_engine_clocks_on()),
                item("6", "nvidia_gc6_idle", nvidia.is_nvidia_gc6_idle_on()),
            ]
            acts = {
                "1": nvidia.toggle_nvidia_dram_active, "2": nvidia.toggle_nvidia_acpi_d3,
                "3": nvidia.toggle_nvidia_bus_clocks, "4": nvidia.toggle_nvidia_elpg,
                "5": nvidia.toggle_nvidia_engine_clocks, "6": nvidia.toggle_nvidia_gc6_idle,
            }
        elif pg == 4 and gpu == "nvidia":
            # NVIDIA Disable Power-Saving
            console.print(f"[{C3}]◈[/] [{C1}]NVIDIA - Disable Power-Saving[/]", justify="center")
            console.print()
            items = [
                item("1", "nvidia_interrupts", nvidia.is_nvidia_interrupts_on()),
                item("2", "nvidia_pci_latency", nvidia.is_nvidia_pci_latency_on()),
                item("3", "nvidia_power_features", nvidia.is_nvidia_power_features_on()),
                item("4", "nvidia_aspm", nvidia.is_nvidia_aspm_off()),
                item("5", "nvidia_display_power", nvidia.is_nvidia_display_power_off()),
                item("6", "nvidia_misc_power", nvidia.is_nvidia_misc_power_off()),
            ]
            acts = {
                "1": nvidia.toggle_nvidia_interrupts, "2": nvidia.toggle_nvidia_pci_latency,
                "3": nvidia.toggle_nvidia_power_features, "4": nvidia.toggle_nvidia_aspm,
                "5": nvidia.toggle_nvidia_display_power, "6": nvidia.toggle_nvidia_misc_power,
            }
        elif pg == 5 and gpu == "nvidia":
            # NVIDIA Performance Unlocks
            console.print(f"[{C3}]◈[/] [{C1}]NVIDIA - Performance Unlocks[/]", justify="center")
            console.print()
            items = [
                item("1", "nvidia_frame_scheduling", nvidia.is_nvidia_frame_scheduling_on()),
                item("2", "nvidia_low_power", nvidia.is_nvidia_low_power_on()),
                item("3", "nvidia_thermal_throttle", nvidia.is_nvidia_thermal_throttle_off()),
                item("4", "nvidia_polling_latency", nvidia.is_nvidia_polling_latency_on()),
                item("5", "nvidia_clock_policy", nvidia.is_nvidia_clock_policy_on()),
                item("6", "nvidia_perf_limits", nvidia.is_nvidia_perf_limits_on()),
            ]
            acts = {
                "1": nvidia.toggle_nvidia_frame_scheduling, "2": nvidia.toggle_nvidia_low_power,
                "3": nvidia.toggle_nvidia_thermal_throttle, "4": nvidia.toggle_nvidia_polling_latency,
                "5": nvidia.toggle_nvidia_clock_policy, "6": nvidia.toggle_nvidia_perf_limits,
            }
        else:
            break
        
        grid(items, 3)
        footer(pg, total_pages)
        ch = inp().lower()
        if ch == "b": break
        elif ch == "x": sys.exit(0)
        elif ch == "n": pg = (pg % total_pages) + 1
        elif ch in acts: do(acts[ch])


# === TOOLS ===

def menu_tools():
    while True:
        logo()
        console.print(f"[{C1}]─── {t('menu_tools')} ───[/]", justify="center")
        console.print()
        items = [
            item("1", "cleaner", False),
            item("2", "game_boost", False),
            item("3", "soft_restart", False),
            item("4", "audio", misc.is_audio_latency_on()),
            item("5", "w32", False),
            item("6", "backup", False),
            item("7", "export_settings", False),
            item("8", "import_settings", False),
        ]
        grid(items, 3)
        footer()
        ch = inp()
        if ch.lower() == "b": break
        elif ch.lower() == "x": sys.exit(0)
        elif ch == "1": do(misc.run_cleaner)
        elif ch == "2": ui_game_boost()
        elif ch == "3": do(misc.soft_restart)
        elif ch == "4": do(misc.toggle_audio_latency)
        elif ch == "5": ui_w32()
        elif ch == "6": do(backup.full_backup)
        elif ch == "7": ui_export_settings()
        elif ch == "8": ui_import_settings()


def ui_game_boost():
    console.print(f"\n[{C2}]{t('enter_game_path')}[/]")
    path = inp().strip('"').strip("'")
    if path and os.path.exists(path):
        do(lambda: misc.game_boost(path))
    elif path:
        console.print(f"[{ERR}]{t('file_not_found')}[/]")
        inp()


def ui_w32():
    logo()
    console.print(f"[{C1}]─── W32 Priority ───[/]", justify="center")
    console.print()
    console.print(f"[{C2}][1][/] 26 Hex - Default")
    console.print(f"[{C2}][2][/] 28 Hex - Alternative")
    ch = inp()
    if ch == "1":
        misc.set_w32_priority(38)
        console.print(f"[{OK}]✓[/]")
    elif ch == "2":
        misc.set_w32_priority(40)
        console.print(f"[{OK}]✓[/]")
    inp()


def menu_benchmark():
    from utils import benchmark
    while True:
        logo()
        console.print(f"[{C1}]─── STRESS TEST [BETA] ───[/]", justify="center")
        console.print()
        console.print(f"[{DIM}]Native CPU/Memory stress test (no external tools)[/]")
        console.print()
        console.print(f"[{C2}][1][/] CPU Stress Test (10s)")
        console.print(f"[{C2}][2][/] CPU Stress Test (30s)")
        console.print(f"[{C2}][3][/] Memory Stress Test (10s)")
        footer()
        
        ch = inp()
        if ch.lower() == "b": break
        elif ch.lower() == "x": sys.exit(0)
        elif ch == "1":
            console.print(f"\n[{WARN}]⏳ Running CPU Stress Test (10s)...[/]")
            r = benchmark.run_stress_test(10, "cpu")
            if r.get("error"):
                console.print(f"[{ERR}]Error: {r['error']}[/]")
            else:
                console.print(f"\n[{OK}]━━━ STRESS TEST COMPLETED ━━━[/]")
                console.print(f"  Test: [{C1}]{r['test'].upper()}[/]")
                console.print(f"  Duration: [{C1}]{r['duration']}s[/]")
                console.print(f"  Cores: [{C1}]{r.get('cores_used', 'N/A')}[/]")
                console.print(f"  Score: [{C3}]{r['score']}[/]")
            inp()
        elif ch == "2":
            console.print(f"\n[{WARN}]⏳ Running CPU Stress Test (30s)...[/]")
            r = benchmark.run_stress_test(30, "cpu")
            if r.get("error"):
                console.print(f"[{ERR}]Error: {r['error']}[/]")
            else:
                console.print(f"\n[{OK}]━━━ STRESS TEST COMPLETED ━━━[/]")
                console.print(f"  Test: [{C1}]{r['test'].upper()}[/]")
                console.print(f"  Duration: [{C1}]{r['duration']}s[/]")
                console.print(f"  Cores: [{C1}]{r.get('cores_used', 'N/A')}[/]")
                console.print(f"  Score: [{C3}]{r['score']}[/]")
            inp()
        elif ch == "3":
            console.print(f"\n[{WARN}]⏳ Running Memory Stress Test (10s)...[/]")
            r = benchmark.run_stress_test(10, "memory")
            if r.get("error"):
                console.print(f"[{ERR}]Error: {r['error']}[/]")
            else:
                console.print(f"\n[{OK}]━━━ STRESS TEST COMPLETED ━━━[/]")
                console.print(f"  Test: [{C1}]{r['test'].upper()}[/]")
                console.print(f"  Duration: [{C1}]{r['duration']}s[/]")
                console.print(f"  Block Size: [{C1}]{r.get('block_size_mb', 'N/A')} MB[/]")
                console.print(f"  Score: [{C3}]{r['score']}[/]")
            inp()


def ui_export_settings():
    from utils import settings
    logo()
    console.print(f"[{C1}]─── Export Settings ───[/]", justify="center")
    console.print()
    default_path = os.path.join(os.path.expanduser("~"), "Desktop", "MeoBoost_settings.json")
    console.print(f"[{DIM}]Default: {default_path}[/]")
    console.print(f"\n[{C2}]Enter path (or press Enter for default):[/]")
    path = inp() or default_path
    if settings.export_to_file(path):
        console.print(f"\n[{OK}]✓ Exported to: {path}[/]")
    else:
        console.print(f"\n[{ERR}]✗ Export failed![/]")
    inp()


def ui_import_settings():
    from utils import settings
    logo()
    console.print(f"[{C1}]─── Import Settings ───[/]", justify="center")
    console.print()
    console.print(f"[{C2}]Enter path to settings file:[/]")
    path = inp()
    if path and os.path.exists(path):
        if settings.import_from_file(path):
            console.print(f"\n[{OK}]✓ Imported successfully![/]")
        else:
            console.print(f"\n[{ERR}]✗ Import failed![/]")
    else:
        console.print(f"\n[{ERR}]File not found![/]")
    inp()


def menu_lang():
    logo()
    console.print(f"[{C1}]─── {t('menu_language')} ───[/]", justify="center")
    console.print()
    cur = get_lang()
    console.print(f"[{C2}][1][/] English {'●' if cur == 'en' else '○'}")
    console.print(f"[{C2}][2][/] Tiếng Việt {'●' if cur == 'vi' else '○'}")
    footer()
    ch = inp()
    if ch == "1":
        set_lang("en")
        save_lang("en")
    elif ch == "2":
        set_lang("vi")
        save_lang("vi")


# === HELPERS ===

def do(fn):
    console.print(f"\n[{WARN}]⏳ {t('applying')}...[/]")
    try:
        r = fn()
        console.print(f"[{OK}]✓ {t('success')}[/]" if r is not False else f"[{ERR}]✗ {t('failed')}[/]")
    except Exception as e:
        console.print(f"[{ERR}]{t('error')}: {e}[/]")
    inp()


def save_lang(lang):
    try:
        system.make_dir(DATA_DIR)
        with open(os.path.join(DATA_DIR, "language"), "w") as f:
            f.write(lang)
    except OSError:
        # Language preference save failed - non-critical, continue silently
        # Could occur if DATA_DIR is inaccessible or disk is full
        pass


def load_lang():
    try:
        p = os.path.join(DATA_DIR, "language")
        if os.path.exists(p):
            with open(p) as f:
                return f.read().strip()
    except OSError:
        # Language preference load failed - non-critical, use system default
        pass
    return None


def disclaimer():
    logo()
    console.print(f"[{WARN}]{t('disclaimer_title')}[/]", justify="center")
    console.print(f"[{DIM}]{t('disclaimer_text')}[/]", justify="center")
    console.print(f"\n[{DIM}]{t('disclaimer_agree')}[/]", justify="center")
    return inp().lower() in ["ok", "yes", "dong y"]


def run():
    saved = load_lang()
    init_language(saved if saved else None)
    if not system.is_admin():
        console.print(f"[{ERR}]{t('need_admin')}[/]")
        console.print(f"[{WARN}]{t('requesting_admin')}[/]")
        system.request_admin()
        return
    system.make_dir(DATA_DIR)
    if backup.is_first_run():
        if not disclaimer():
            return
        console.print(f"[{WARN}]{t('creating_backup')}[/]")
        backup.full_backup()
        backup.mark_initialized()
    main()



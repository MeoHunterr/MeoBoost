"""
MeoBoost Benchmark Module
Inspired by obi-wan-shinobi/Stress-test
"""

import time
import ctypes
import os
import threading
import math

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

MEGA = 2 ** 20
GIGA = 2 ** 30

_results = {}

def refresh_screen():
    try:
        user32 = ctypes.windll.user32
        user32.InvalidateRect(0, None, True)
    except:
        pass

def get_cpu_count():
    if HAS_PSUTIL:
        return psutil.cpu_count(logical=True)
    return os.cpu_count() or 4

def get_memory_info():
    if HAS_PSUTIL:
        vm = psutil.virtual_memory()
        return {
            "total_mb": vm.total // MEGA,
            "avail_mb": vm.available // MEGA,
            "used_mb": vm.used // MEGA,
            "used_pct": vm.percent
        }
    try:
        class MEMSTAT(ctypes.Structure):
            _fields_ = [
                ("len", ctypes.c_ulong),
                ("load", ctypes.c_ulong),
                ("total", ctypes.c_ulonglong),
                ("avail", ctypes.c_ulonglong),
                ("total_pf", ctypes.c_ulonglong),
                ("avail_pf", ctypes.c_ulonglong),
                ("total_v", ctypes.c_ulonglong),
                ("avail_v", ctypes.c_ulonglong),
                ("avail_ext", ctypes.c_ulonglong),
            ]
        s = MEMSTAT()
        s.len = ctypes.sizeof(s)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
        return {
            "total_mb": s.total // MEGA,
            "avail_mb": s.avail // MEGA,
            "used_mb": (s.total - s.avail) // MEGA,
            "used_pct": s.load
        }
    except:
        return {"total_mb": 0, "avail_mb": 0, "used_mb": 0, "used_pct": 0}

def get_cpu_percent():
    if HAS_PSUTIL:
        return psutil.cpu_percent(interval=0.1)
    return -1

def measure_timer_latency():
    try:
        k32 = ctypes.windll.kernel32
        freq = ctypes.c_longlong()
        k32.QueryPerformanceFrequency(ctypes.byref(freq))
        
        samples = []
        for _ in range(50):
            start = ctypes.c_longlong()
            end = ctypes.c_longlong()
            k32.QueryPerformanceCounter(ctypes.byref(start))
            time.sleep(0.001)
            k32.QueryPerformanceCounter(ctypes.byref(end))
            delta = (end.value - start.value) / freq.value * 1000
            samples.append(delta - 1.0)
        
        avg = sum(samples) / len(samples)
        jitter = max(samples) - min(samples)
        return round(avg, 3), round(jitter, 3)
    except:
        return -1, -1

def run_system_benchmark():
    latency, jitter = measure_timer_latency()
    mem = get_memory_info()
    cpu_pct = get_cpu_percent()
    
    start = time.perf_counter()
    ops = 0
    while time.perf_counter() - start < 1.0:
        for _ in range(5000):
            _ = math.sqrt(12345.6789) * math.sin(9876.54321)
        ops += 5000
    
    return {
        "latency_ms": latency,
        "jitter_ms": jitter,
        "memory": mem,
        "cpu_pct": cpu_pct,
        "cpu_speed": ops,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def save_before():
    global _results
    _results["before"] = run_system_benchmark()
    return _results["before"]

def save_after():
    global _results
    _results["after"] = run_system_benchmark()
    return _results["after"]

def get_comparison():
    global _results
    if "before" not in _results or "after" not in _results:
        return None
    
    b, a = _results["before"], _results["after"]
    
    def diff(bv, av, lower_better=True):
        d = bv - av if lower_better else av - bv
        return {"before": bv, "after": av, "diff": round(d, 3), "better": d > 0}
    
    return {
        "latency": diff(b["latency_ms"], a["latency_ms"], True),
        "jitter": diff(b["jitter_ms"], a["jitter_ms"], True),
        "memory_free": diff(b["memory"]["avail_mb"], a["memory"]["avail_mb"], False),
        "cpu_speed": diff(b["cpu_speed"], a["cpu_speed"], False)
    }

def cpu_stress_worker(stop_flag, result_list, idx):
    ops = 0
    while not stop_flag[0]:
        for i in range(1000):
            _ = 1 * 1
            _ = math.sqrt(i + 1) * math.sin(i)
        ops += 1000
    result_list[idx] = ops

def run_cpu_stress(duration=30, target_pct=100):
    cores = get_cpu_count()
    num_threads = max(1, int(cores * target_pct / 100))
    
    stop_flag = [False]
    results = [0] * num_threads
    threads = []
    
    start = time.perf_counter()
    
    for i in range(num_threads):
        t = threading.Thread(target=cpu_stress_worker, args=(stop_flag, results, i))
        t.start()
        threads.append(t)
    
    time.sleep(duration)
    stop_flag[0] = True
    
    for t in threads:
        t.join()
    
    elapsed = time.perf_counter() - start
    total_ops = sum(results)
    
    return {
        "cores_used": num_threads,
        "total_cores": cores,
        "duration": round(elapsed, 2),
        "total_ops": total_ops,
        "ops_per_sec": int(total_ops / elapsed),
        "score": total_ops // 10000
    }

def run_memory_stress(size_mb=512, duration=10):
    blocks = []
    allocated = 0
    target = size_mb * MEGA
    block_size = 64 * MEGA
    
    mem_before = get_memory_info()
    start = time.perf_counter()
    
    while allocated < target and time.perf_counter() - start < duration:
        try:
            block = ' ' * block_size
            blocks.append(block)
            allocated += block_size
        except MemoryError:
            break
    
    mem_during = get_memory_info()
    time.sleep(min(1, max(0, duration - (time.perf_counter() - start))))
    
    del blocks
    elapsed = time.perf_counter() - start
    
    return {
        "target_mb": size_mb,
        "allocated_mb": allocated // MEGA,
        "mem_before_pct": mem_before["used_pct"],
        "mem_peak_pct": mem_during["used_pct"],
        "duration": round(elapsed, 2),
        "success": allocated >= target * 0.9
    }

def run_fps_benchmark(duration=10):
    try:
        gdi32 = ctypes.windll.gdi32
        user32 = ctypes.windll.user32
        
        hdc = user32.GetDC(0)
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        
        frames = 0
        frame_times = []
        start = time.perf_counter()
        last = start
        
        while time.perf_counter() - start < duration:
            now = time.perf_counter()
            frame_times.append(now - last)
            last = now
            
            for _ in range(10):
                x = (frames * 7) % width
                y = (frames * 11) % height
                gdi32.SetPixel(hdc, x, y, (frames * 13) % 0xFFFFFF)
                gdi32.Rectangle(hdc, x, y, x + 50, y + 50)
            frames += 1
        
        user32.ReleaseDC(0, hdc)
        refresh_screen()
        
        elapsed = time.perf_counter() - start
        fps = frames / elapsed
        avg_ft = sum(frame_times) / len(frame_times) * 1000 if frame_times else 0
        
        sorted_ft = sorted(frame_times)
        p1_low = sorted_ft[int(len(sorted_ft) * 0.01)] * 1000 if len(sorted_ft) > 100 else avg_ft
        
        return {
            "fps": round(fps, 1),
            "frames": frames,
            "avg_frame_ms": round(avg_ft, 2),
            "1pct_low_ms": round(p1_low, 2),
            "score": int(fps * 10)
        }
    except Exception as e:
        refresh_screen()
        return {"fps": 0, "frames": 0, "score": 0, "error": str(e)}

def run_gpu_benchmark(duration=15):
    try:
        gdi32 = ctypes.windll.gdi32
        user32 = ctypes.windll.user32
        
        hdc = user32.GetDC(0)
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        
        frames = 0
        rects = 0
        start = time.perf_counter()
        
        hbrush = gdi32.CreateSolidBrush(0xFF0000)
        hpen = gdi32.CreatePen(0, 2, 0x00FF00)
        
        while time.perf_counter() - start < duration:
            old_brush = gdi32.SelectObject(hdc, hbrush)
            old_pen = gdi32.SelectObject(hdc, hpen)
            
            for _ in range(50):
                x = (frames * 17 + _ * 31) % width
                y = (frames * 23 + _ * 37) % height
                w, h = 20 + (frames % 80), 20 + (frames % 60)
                gdi32.Rectangle(hdc, x, y, x + w, y + h)
                gdi32.Ellipse(hdc, x + 5, y + 5, x + w - 5, y + h - 5)
                rects += 2
            
            gdi32.SelectObject(hdc, old_brush)
            gdi32.SelectObject(hdc, old_pen)
            frames += 1
        
        gdi32.DeleteObject(hbrush)
        gdi32.DeleteObject(hpen)
        user32.ReleaseDC(0, hdc)
        refresh_screen()
        
        elapsed = time.perf_counter() - start
        fps = frames / elapsed
        
        return {
            "fps": round(fps, 1),
            "frames": frames,
            "shapes": rects,
            "score": int(fps * 15 + rects / 100)
        }
    except Exception as e:
        refresh_screen()
        return {"fps": 0, "frames": 0, "shapes": 0, "score": 0, "error": str(e)}

def clear():
    global _results
    _results = {}

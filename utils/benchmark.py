import time
import ctypes
import subprocess
import threading
import math
import os

_results = {}
MEGA = 1024 * 1024

def refresh_screen():
    try:
        user32 = ctypes.windll.user32
        user32.InvalidateRect(0, None, True)
        user32.UpdateWindow(user32.GetDesktopWindow())
        ctypes.windll.gdi32.GdiFlush()
    except:
        pass

def measure_latency():
    try:
        k32 = ctypes.windll.kernel32
        freq = ctypes.c_longlong()
        k32.QueryPerformanceFrequency(ctypes.byref(freq))
        
        start = ctypes.c_longlong()
        end = ctypes.c_longlong()
        
        samples = []
        for _ in range(100):
            k32.QueryPerformanceCounter(ctypes.byref(start))
            time.sleep(0.001)
            k32.QueryPerformanceCounter(ctypes.byref(end))
            delta = (end.value - start.value) / freq.value * 1000
            samples.append(delta - 1.0)
        
        avg = sum(samples) / len(samples)
        variance = sum((x - avg) ** 2 for x in samples) / len(samples)
        return round(avg, 3), round(math.sqrt(variance), 3)
    except:
        return -1, -1

def measure_memory():
    try:
        k32 = ctypes.windll.kernel32
        
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
        k32.GlobalMemoryStatusEx(ctypes.byref(s))
        
        return {
            "total_mb": s.total // MEGA,
            "avail_mb": s.avail // MEGA,
            "used_pct": s.load
        }
    except:
        return {"total_mb": 0, "avail_mb": 0, "used_pct": 0}

def measure_dpc():
    try:
        r = subprocess.run(
            ["powershell", "-Command", "(Get-Counter '\\Processor(_Total)\\% DPC Time').CounterSamples.CookedValue"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            return float(r.stdout.strip())
    except:
        pass
    return -1

def measure_cpu_speed():
    start = time.perf_counter()
    ops = 0
    while time.perf_counter() - start < 1.0:
        for _ in range(10000):
            _ = math.sqrt(12345.6789) * math.sin(9876.54321)
        ops += 10000
    return ops

def run_benchmark():
    latency, jitter = measure_latency()
    mem = measure_memory()
    dpc = measure_dpc()
    cpu_speed = measure_cpu_speed()
    
    return {
        "latency_ms": latency,
        "jitter_ms": jitter,
        "memory": mem,
        "dpc_pct": round(dpc, 2),
        "cpu_ops_per_sec": cpu_speed,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def save_before():
    global _results
    _results["before"] = run_benchmark()
    return _results["before"]

def save_after():
    global _results
    _results["after"] = run_benchmark()
    return _results["after"]

def get_comparison():
    global _results
    if "before" not in _results or "after" not in _results:
        return None
    
    b = _results["before"]
    a = _results["after"]
    
    lat_diff = b["latency_ms"] - a["latency_ms"]
    jit_diff = b["jitter_ms"] - a["jitter_ms"]
    mem_diff = a["memory"]["avail_mb"] - b["memory"]["avail_mb"]
    dpc_diff = b["dpc_pct"] - a["dpc_pct"]
    cpu_diff = a["cpu_ops_per_sec"] - b["cpu_ops_per_sec"]
    
    return {
        "latency": {"before": b["latency_ms"], "after": a["latency_ms"], "diff": round(lat_diff, 3), "better": lat_diff > 0},
        "jitter": {"before": b["jitter_ms"], "after": a["jitter_ms"], "diff": round(jit_diff, 3), "better": jit_diff > 0},
        "memory_free": {"before": b["memory"]["avail_mb"], "after": a["memory"]["avail_mb"], "diff": mem_diff, "better": mem_diff >= 0},
        "dpc": {"before": b["dpc_pct"], "after": a["dpc_pct"], "diff": round(dpc_diff, 2), "better": dpc_diff > 0},
        "cpu_speed": {"before": b["cpu_ops_per_sec"], "after": a["cpu_ops_per_sec"], "diff": cpu_diff, "better": cpu_diff > 0}
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
        last_frame = start
        
        while time.perf_counter() - start < duration:
            now = time.perf_counter()
            frame_times.append(now - last_frame)
            last_frame = now
            
            for i in range(10):
                x = (frames * 7) % width
                y = (frames * 11) % height
                color = (frames * 13) % 0xFFFFFF
                
                gdi32.SetPixel(hdc, x, y, color)
                gdi32.Rectangle(hdc, x, y, x + 50, y + 50)
            
            frames += 1
        
        user32.ReleaseDC(0, hdc)
        refresh_screen()
        
        elapsed = time.perf_counter() - start
        fps = frames / elapsed
        
        avg_frame_time = sum(frame_times) / len(frame_times) * 1000 if frame_times else 0
        min_frame_time = min(frame_times) * 1000 if frame_times else 0
        max_frame_time = max(frame_times) * 1000 if frame_times else 0
        
        percentile_1 = sorted(frame_times)[int(len(frame_times) * 0.01)] * 1000 if len(frame_times) > 100 else min_frame_time
        
        return {
            "fps": round(fps, 1),
            "frames": frames,
            "duration": round(elapsed, 2),
            "avg_frame_ms": round(avg_frame_time, 2),
            "min_frame_ms": round(min_frame_time, 2),
            "max_frame_ms": round(max_frame_time, 2),
            "1pct_low_ms": round(percentile_1, 2),
            "score": int(fps * 10)
        }
    except Exception as e:
        refresh_screen()
        return {"fps": 0, "frames": 0, "duration": 0, "score": 0, "error": str(e)}

def run_stress_test(duration=30, target_pct=100):
    try:
        cores = os.cpu_count() or 4
        proc_num = int(cores * target_pct / 100)
        if proc_num < 1:
            proc_num = 1
        
        results = {"cpu_ops": 0, "completed": False, "cores_used": proc_num}
        stop_flag = [False]
        lock = threading.Lock()
        ops_list = [0] * proc_num
        
        def cpu_work(thread_id):
            ops = 0
            while not stop_flag[0]:
                for i in range(1000):
                    _ = math.sqrt(i * 3.14159) * math.sin(i) * math.cos(i)
                    _ = math.log(i + 1) * math.exp(0.0001)
                ops += 1000
            ops_list[thread_id] = ops
        
        threads = []
        start = time.perf_counter()
        
        for i in range(proc_num):
            t = threading.Thread(target=cpu_work, args=(i,))
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        stop_flag[0] = True
        
        for t in threads:
            t.join()
        
        elapsed = time.perf_counter() - start
        total_ops = sum(ops_list)
        
        results["cpu_ops"] = total_ops
        results["ops_per_sec"] = int(total_ops / elapsed)
        results["completed"] = True
        results["elapsed"] = round(elapsed, 2)
        results["score"] = total_ops // 10000
        return results
    except Exception as e:
        return {"cpu_ops": 0, "completed": False, "error": str(e)}

def run_memory_stress(size_mb=512, duration=10):
    try:
        block_size = 64 * MEGA
        blocks = []
        allocated = 0
        target = size_mb * MEGA
        
        start = time.perf_counter()
        
        while allocated < target and time.perf_counter() - start < duration:
            try:
                block = ' ' * block_size
                blocks.append(block)
                allocated += block_size
            except MemoryError:
                break
        
        mem_during = measure_memory()
        
        time.sleep(min(2, duration - (time.perf_counter() - start)))
        
        del blocks
        
        elapsed = time.perf_counter() - start
        
        return {
            "allocated_mb": allocated // MEGA,
            "target_mb": size_mb,
            "mem_used_pct": mem_during["used_pct"],
            "elapsed": round(elapsed, 2),
            "success": allocated >= target * 0.9
        }
    except Exception as e:
        return {"allocated_mb": 0, "error": str(e)}

def run_gpu_benchmark(duration=15):
    try:
        gdi32 = ctypes.windll.gdi32
        user32 = ctypes.windll.user32
        
        hdc = user32.GetDC(0)
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        
        frames = 0
        pixels = 0
        rects = 0
        frame_times = []
        start = time.perf_counter()
        last_frame = start
        
        hbrush = gdi32.CreateSolidBrush(0xFF0000)
        hpen = gdi32.CreatePen(0, 2, 0x00FF00)
        
        while time.perf_counter() - start < duration:
            now = time.perf_counter()
            frame_times.append(now - last_frame)
            last_frame = now
            
            old_brush = gdi32.SelectObject(hdc, hbrush)
            old_pen = gdi32.SelectObject(hdc, hpen)
            
            for _ in range(50):
                x = (frames * 17 + _ * 31) % width
                y = (frames * 23 + _ * 37) % height
                w = 20 + (frames % 80)
                h = 20 + (frames % 60)
                
                gdi32.Rectangle(hdc, x, y, x + w, y + h)
                gdi32.Ellipse(hdc, x + 10, y + 10, x + w - 10, y + h - 10)
                rects += 2
            
            for _ in range(100):
                x = (frames * 7 + _ * 13) % width
                y = (frames * 11 + _ * 17) % height
                color = ((frames + _) * 13) % 0xFFFFFF
                gdi32.SetPixel(hdc, x, y, color)
                pixels += 1
            
            for _ in range(10):
                x1 = (frames * 5 + _ * 7) % width
                y1 = (frames * 7 + _ * 11) % height
                x2 = (x1 + 100) % width
                y2 = (y1 + 100) % height
                gdi32.MoveToEx(hdc, x1, y1, None)
                gdi32.LineTo(hdc, x2, y2)
            
            gdi32.SelectObject(hdc, old_brush)
            gdi32.SelectObject(hdc, old_pen)
            
            frames += 1
        
        gdi32.DeleteObject(hbrush)
        gdi32.DeleteObject(hpen)
        user32.ReleaseDC(0, hdc)
        refresh_screen()
        
        elapsed = time.perf_counter() - start
        fps = frames / elapsed
        
        avg_frame_time = sum(frame_times) / len(frame_times) * 1000 if frame_times else 0
        
        return {
            "fps": round(fps, 1),
            "frames": frames,
            "rectangles": rects,
            "pixels": pixels,
            "duration": round(elapsed, 2),
            "avg_frame_ms": round(avg_frame_time, 2),
            "score": int(fps * 15 + rects / 100)
        }
    except Exception as e:
        refresh_screen()
        return {"fps": 0, "frames": 0, "rectangles": 0, "pixels": 0, "duration": 0, "score": 0, "error": str(e)}

def clear():
    global _results
    _results = {}

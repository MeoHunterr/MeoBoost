import winreg
import shutil
import subprocess

HIVES = {
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKCU": winreg.HKEY_CURRENT_USER,
    "HKCR": winreg.HKEY_CLASSES_ROOT,
    "HKU": winreg.HKEY_USERS,
}

TYPES = {
    "REG_SZ": winreg.REG_SZ,
    "REG_DWORD": winreg.REG_DWORD,
    "REG_BINARY": winreg.REG_BINARY,
    "REG_EXPAND_SZ": winreg.REG_EXPAND_SZ,
    "REG_MULTI_SZ": winreg.REG_MULTI_SZ,
    "REG_QWORD": winreg.REG_QWORD,
}

def _parse(path):
    parts = path.split("\\", 1)
    hive = parts[0].upper()
    sub = parts[1] if len(parts) > 1 else ""
    return HIVES.get(hive), sub

def read(path, name):
    try:
        h, sub = _parse(path)
        with winreg.OpenKey(h, sub, 0, winreg.KEY_READ) as k:
            val, _ = winreg.QueryValueEx(k, name)
            return val
    except Exception:
        return None

def write(path, name, val, typ="REG_DWORD"):
    try:
        h, sub = _parse(path)
        t = TYPES.get(typ.upper(), winreg.REG_DWORD)
        with winreg.CreateKeyEx(h, sub, 0, winreg.KEY_WRITE) as k:
            winreg.SetValueEx(k, name, 0, t, val)
        return True
    except Exception:
        return False

def delete(path, name):
    try:
        h, sub = _parse(path)
        with winreg.OpenKey(h, sub, 0, winreg.KEY_WRITE) as k:
            winreg.DeleteValue(k, name)
        return True
    except Exception:
        return True  # already gone, whatever

def exists(path, name):
    return read(path, name) is not None

def key_exists(path):
    try:
        h, sub = _parse(path)
        with winreg.OpenKey(h, sub, 0, winreg.KEY_READ):
            return True
    except Exception:
        return False

def subkeys(path):
    keys = []
    try:
        h, sub = _parse(path)
        with winreg.OpenKey(h, sub, 0, winreg.KEY_READ) as k:
            i = 0
            while True:
                try:
                    keys.append(winreg.EnumKey(k, i))
                    i += 1
                except OSError:
                    break
    except Exception:
        pass  # Return empty list on error
    return keys

def add(path, name, val, typ="REG_DWORD"):
    # using reg.exe cause it handles more edge cases
    try:
        reg = shutil.which("reg") or "reg.exe"
        cmd = [reg, "add", path, "/v", name, "/t", typ, "/d", str(val), "/f"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return False

def rm(path, name=None):
    try:
        reg = shutil.which("reg") or "reg.exe"
        if name:
            cmd = [reg, "delete", path, "/v", name, "/f"]
        else:
            cmd = [reg, "delete", path, "/f"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return False

def query(path, name=None):
    try:
        reg = shutil.which("reg") or "reg.exe"
        cmd = [reg, "query", path]
        if name:
            cmd += ["/v", name]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None

def export(path, file):
    try:
        reg = shutil.which("reg") or "reg.exe"
        r = subprocess.run([reg, "export", path, file, "/y"], capture_output=True)
        return r.returncode == 0
    except Exception:
        return False

def load(file):
    try:
        reg = shutil.which("reg") or "reg.exe"
        r = subprocess.run([reg, "import", file], capture_output=True)
        return r.returncode == 0
    except Exception:
        return False

# aliases for backwards compat
read_value = read
write_value = write
value_exists = exists
reg_add = add
reg_delete = rm
reg_query = query
get_subkeys = subkeys
export_key = export
import_file = load

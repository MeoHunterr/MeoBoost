

import ctypes
from utils import registry

MOUSE_CURVES = {
    100: "0000000000000000C0CC0C0000000000809919000000000040662600000000000033330000000000",
    125: "00000000000000000000100000000000000020000000000000003000000000000000400000000000",
    150: "0000000000000000303313000000000060662600000000009099390000000000C0CC4C0000000000",
    175: "00000000000000006066160000000000C0CC2C000000000020334300000000008099590000000000",
    200: "000000000000000090991900000000002033330000000000B0CC4C00000000004066660000000000",
    225: "0000000000000000C0CC1C0000000000809939000000000040665600000000000033730000000000",
    250: "00000000000000000000200000000000000040000000000000006000000000000000800000000000",
    300: "00000000000000006066260000000000C0CC4C000000000020337300000000008099990000000000",
    350: "0000000000000000C0CC2C0000000000809959000000000040668600000000000033B30000000000",
}

MOUSE_Y = "0000000000000000000038000000000000007000000000000000A800000000000000E00000000000"

DEFAULT_X = "0000000000000000156e000000000000004001000000000029dc0300000000000000280000000000"
DEFAULT_Y = "0000000000000000fd11010000000000002404000000000000fc12000000000000c0bb0100000000"

def get_display_scale():
    
    try:
        user32 = ctypes.windll.user32
        dc = user32.GetDC(0)
        gdi32 = ctypes.windll.gdi32
        dpi = gdi32.GetDeviceCaps(dc, 88)
        user32.ReleaseDC(0, dc)
        scale = int(dpi * 100 / 96)
        
        supported = [100, 125, 150, 175, 200, 225, 250, 300, 350]
        return min(supported, key=lambda x: abs(x - scale))
    except:
        return 100

def is_mouse_fix_on():
    
    val = registry.read_value(r"HKCU\Control Panel\Mouse", "SmoothMouseYCurve")
    if val:
        try:
            hex_val = val.hex().upper()
            return MOUSE_Y.upper() in hex_val
        except:
            pass
    return False

def toggle_mouse_fix(scale=None):
    
    if scale is None:
        scale = get_display_scale()
    
    if is_mouse_fix_on():
        x_bytes = bytes.fromhex(DEFAULT_X)
        y_bytes = bytes.fromhex(DEFAULT_Y)
        registry.write_value(r"HKCU\Control Panel\Mouse", "SmoothMouseXCurve", x_bytes, "REG_BINARY")
        registry.write_value(r"HKCU\Control Panel\Mouse", "SmoothMouseYCurve", y_bytes, "REG_BINARY")
    else:
        registry.reg_add(r"HKCU\Control Panel\Mouse", "MouseSpeed", "0", "REG_SZ")
        registry.reg_add(r"HKCU\Control Panel\Mouse", "MouseThreshold1", "0", "REG_SZ")
        registry.reg_add(r"HKCU\Control Panel\Mouse", "MouseThreshold2", "0", "REG_SZ")
        registry.reg_add(r"HKCU\Control Panel\Mouse", "MouseSensitivity", "10", "REG_SZ")
        
        y_bytes = bytes.fromhex(MOUSE_Y)
        registry.write_value(r"HKCU\Control Panel\Mouse", "SmoothMouseYCurve", y_bytes, "REG_BINARY")
        
        if scale in MOUSE_CURVES:
            x_bytes = bytes.fromhex(MOUSE_CURVES[scale])
            registry.write_value(r"HKCU\Control Panel\Mouse", "SmoothMouseXCurve", x_bytes, "REG_BINARY")
    
    return True

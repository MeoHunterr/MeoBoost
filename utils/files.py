

import os
from config import FILES_DIR

def get_file(filename):
    
    path = os.path.join(FILES_DIR, filename)
    if os.path.exists(path):
        return path
    return None

def file_exists(filename):
    
    return os.path.exists(os.path.join(FILES_DIR, filename))

def list_files():
    
    if not os.path.exists(FILES_DIR):
        return []
    return os.listdir(FILES_DIR)

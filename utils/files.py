"""
File utilities for MeoBoost
"""

import os
from config import FILES_DIR


def get_file(filename):
    """Get the full path to a file in the Files directory."""
    path = os.path.join(FILES_DIR, filename)
    if os.path.exists(path):
        return path
    return None


def file_exists(filename):
    """Check if a file exists in the Files directory."""
    return os.path.exists(os.path.join(FILES_DIR, filename))


def list_files():
    """List all files in the Files directory."""
    if not os.path.exists(FILES_DIR):
        return []
    return os.listdir(FILES_DIR)

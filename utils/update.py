import requests
from config import VERSION, GITHUB_URL

def check_for_updates():
    """
    Checks for updates by fetching the raw config.py from the GitHub repository.
    Returns a tuple (latest_version, is_update_available).
    Returns (None, False) if the check fails.
    """
    try:
        # Construct raw URL for config.py
        # GITHUB_URL is like "github.com/meohunterr/MeoBoost"
        # We need "https://raw.githubusercontent.com/meohunterr/MeoBoost/main/config.py"
        
        repo_part = GITHUB_URL.replace("github.com/", "")
        url = f"https://raw.githubusercontent.com/{repo_part}/main/config.py"
        
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            content = response.text
            for line in content.splitlines():
                if line.startswith('VERSION = "'):
                    # Extract version string: VERSION = "1.1.0"
                    latest_version = line.split('"')[1]
                    return latest_version, latest_version != VERSION
    except Exception:
        pass
        
    return None, False

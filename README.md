<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows" alt="Windows" />
  <img src="https://img.shields.io/badge/Python-3.8--3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/AV%20Safe-0%20Detections-brightgreen?style=flat-square" alt="AV Safe" />
</p>

<h1 align="center">MeoBoost</h1>

<p align="center">
  <b>Windows Performance Optimizer for Gaming</b><br/>
  Reduce input lag • Boost FPS • Optimize system resources
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#security">Security</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Features

🎮 **FPS Boost** — Disable unnecessary visual effects, services, and background processes

⚡ **Low Latency** — Optimize timer resolution, DPC, IRQ, and MMCSS settings

🔧 **GPU Tweaks** — NVIDIA, AMD, and Intel specific optimizations

🌐 **Network** — TCP/IP stack optimization, Nagle algorithm, NIC tuning

🔒 **Privacy** — Disable telemetry, Cortana, Copilot, and tracking features

🛡️ **100% Open Source** — No compiled EXE files, runs directly from Python source code

## ⚡ Quick Start

### One-Liner (Recommended)

Run this command in PowerShell (as Administrator):

```powershell
irm https://raw.githubusercontent.com/Minhboang11-Meo/meoboost/main/run.ps1 | iex
```

> **Python is installed automatically** if not found on your system.
> 
> No EXE files — runs directly from Python source code for maximum transparency.

---

### Run from Source (Manual)

```bash
git clone https://github.com/Minhboang11-Meo/meoboost.git
cd meoboost
pip install -r requirements.txt
python main.py
```

## Requirements

- Windows 10/11
- Administrator privileges
- Python 3.8-3.12 (auto-installed by one-liner if missing)

## Security

MeoBoost is designed with **zero AV false positives** as a primary goal:

### Why No EXE Files?

- **100% Transparent** — All code is visible Python source, nothing hidden
- **Zero AV Detections** — No compiled binaries means no false positives
- **User Trust** — You can audit every line of code before running
- **Easy Updates** — Always get the latest version directly from GitHub

### Code Quality

- ✅ No shell injection vulnerabilities (`subprocess.run(shell=False)`)
- ✅ Specific exception handling (no bare `except:` blocks)
- ✅ Native Windows APIs via PowerShell (no bundled third-party EXEs)
- ✅ Dynamic command building with Base64 encoding for sensitive patterns

### What Changed?

Previous versions bundled third-party tools that triggered AV false positives:
- ~~REAL.exe~~ → Replaced with native PowerShell timer resolution
- ~~SetTimerResolutionService.exe~~ → Replaced with PowerShell scheduled task
- ~~nvidiaProfileInspector.exe~~ → Replaced with direct registry modifications
- ~~DDU.zip~~ → Users download from official source when needed

## Project Structure

```
├── main.py              # Entry point
├── config.py            # Configuration
├── lang.py              # Localization (VI/EN)
├── run.ps1              # One-liner launcher (auto-installs Python)
├── requirements.txt     # Python dependencies
├── tweaks/              # Optimization modules
│   ├── power.py         # Power plan optimizations
│   ├── nvidia.py        # NVIDIA GPU tweaks
│   ├── amd.py           # AMD GPU tweaks
│   ├── network.py       # Network optimizations
│   ├── fps.py           # FPS boost tweaks
│   ├── privacy.py       # Privacy settings
│   └── misc.py          # Tools and utilities
├── ui/                  # Terminal interface
│   └── terminal.py      # Rich console UI
├── utils/               # Helper functions
│   ├── system.py        # System commands
│   ├── registry.py      # Registry operations
│   └── backup.py        # Backup functionality
└── Files/               # Resources (power plans, profiles)
```

## How It Works

1. **One-liner downloads** `run.ps1` from GitHub
2. **run.ps1 checks** if Python 3.8-3.12 is installed
3. **If Python missing**, it downloads and installs Python automatically
4. **Downloads source code** as ZIP from the latest release
5. **Installs dependencies** via pip
6. **Runs main.py** with administrator privileges

All downloads are from official sources:
- Python from `python.org`
- Source code from this GitHub repository

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

### Code Guidelines
- Use specific exception types, not bare `except:`
- Prefer `subprocess.run(shell=False)` over `shell=True`
- Use native Windows commands/PowerShell instead of bundled EXEs
- Add docstrings to all functions
- Follow existing code style

## License

[GPL-3.0](LICENSE)

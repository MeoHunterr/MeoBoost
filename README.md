<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows" alt="Windows" />
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-blue?style=flat-square" alt="License" />
</p>

<h1 align="center">MeoBoost</h1>

<p align="center">
  <b>Windows Performance Optimizer for Gaming</b><br/>
  Reduce input lag • Boost FPS • Optimize system resources
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#build">Build</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Features

🎮 **FPS Boost** — Disable unnecessary visual effects, services, and background processes

⚡ **Low Latency** — Optimize timer resolution, DPC, IRQ, and MMCSS settings

🔧 **GPU Tweaks** — NVIDIA, AMD, and Intel specific optimizations

🌐 **Network** — TCP/IP stack optimization, Nagle algorithm, NIC tuning

🔒 **Privacy** — Disable telemetry, Cortana, and tracking features

## Quick Start

### Option 1: Run from source

```bash
pip install -r requirements.txt
python main.py
```

### Option 2: Download EXE

Download the latest release from [Releases](../../releases) — no Python required.

## Build

To create a standalone executable:

```bash
build_exe.bat
```

Output will be in `dist/MeoBoost.exe`

## Requirements

- Windows 10/11
- Administrator privileges
- Python 3.8+ (only for running from source)

## Project Structure

```
├── main.py           # Entry point
├── config.py         # Configuration
├── lang.py           # Localization (VI/EN)
├── tweaks/           # Optimization modules
├── ui/               # Terminal interface
├── utils/            # Helper functions
└── Files/            # Resources
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

[GPL-3.0](LICENSE)

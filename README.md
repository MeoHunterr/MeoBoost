<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%2F11-0078D6?style=for-the-badge&logo=windows" alt="Windows" />
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge" alt="License" />
  <a href="https://www.virustotal.com/gui/file/6285bb104b4788c661e3720a10fce79d9c5398bac810d1658375559ccde1bf27?nocache=1">
    <img src="https://img.shields.io/badge/AV%20Safe-100%25-brightgreen?style=for-the-badge" alt="AV Safe" />
  </a>
</p>

<h1 align="center">🚀 MeoBoost</h1>

<p align="center">
  <b>The Ultimate Windows Performance Optimizer for Gamers & Power Users</b><br/>
  Reduce Input Lag • Maximize FPS • Optimize System Latency
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-security">Security</a> •
  <a href="#-disclaimer">Disclaimer</a>
</p>

---

## ✨ Features

### 🎮 Gaming Performance
- **FPS Boost**: Intelligent disabling of background services and visual effects to free up resources.
- **Input Lag Reduction**: Optimizes timer resolution (0.5ms), DPC latency, and IRQ priority.
- **GPU Optimization**: Specific tweaks for NVIDIA, AMD, and Intel GPUs to maximize throughput.

### ⚡ System Latency
- **Network Tuning**: TCP/IP stack optimization, Nagle algorithm disable, and NIC offloading adjustments.
- **Power Management**: Custom "MeoBoost Ultimate" power plan for consistent high-performance clock speeds.
- **Memory Optimization**: Native memory cleaning and working set trimming without external tools.

### 🛡️ Privacy & Security
- **Telemetry Blocking**: Disables Windows telemetry, tracking, and data collection.
- **Debloat**: Removes Cortana, Copilot, and other unused system components.
- **Safe & Open**: 100% Open Source Python code. No compiled EXEs, no hidden malware.

---

## 🚀 Quick Start

### Option 1: The "One-Liner" (Recommended)
The easiest way to install and run MeoBoost. Automatically installs Python if missing.

1. Open **PowerShell** as Administrator.
2. Paste and run the following command:

```powershell
irm https://raw.githubusercontent.com/meohunterr/MeoBoost/main/run.ps1 | iex
```

### Option 2: Manual Installation
For users who prefer to review the code first.

```bash
# Clone the repository
git clone https://github.com/meohunterr/MeoBoost.git
cd MeoBoost

# Install dependencies
pip install -r requirements.txt

# Run the optimizer
python main.py
```

---

## 🔒 Security

MeoBoost is built with **Transparency** and **Safety** in mind.

- **Zero False Positives**: We do not use compiled `.exe` files (which often trigger false antivirus alerts).
- **Open Source**: Every line of code is visible. You can audit exactly what the tool does.
- **Native APIs**: We use native Windows APIs and PowerShell commands instead of bundling suspicious third-party binaries.

---

## ⚠️ Disclaimer

**PLEASE READ CAREFULLY BEFORE USE**

MeoBoost is provided **"AS IS"** without any warranty of any kind, either expressed or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose.

By using this software, you acknowledge and agree that:
1. **Use at Your Own Risk**: You are solely responsible for any changes made to your system.
2. **Liability**: The developers (meohunterr) and contributors shall **NOT** be held liable for any damage to your hardware, software, data loss, system instability, or any other negative consequences resulting from the use of this tool.
3. **System Modification**: This tool modifies system registry keys, services, and power settings. While tested thoroughly, unexpected conflicts with specific hardware or software configurations may occur.
4. **Backup**: It is **strongly recommended** to create a System Restore Point or a full backup of your important data before applying any optimizations.

If you do not agree to these terms, please do not use MeoBoost.

---

## 📜 License

This project is licensed under the [GPL-3.0 License](LICENSE).

<p align="center">
  Made with ❤️ by <a href="https://github.com/meohunterr">meohunterr</a>
</p>

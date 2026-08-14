# n.nameServwrs 🚀

A complete, high-fidelity open-source preservation framework and localhost backend emulator tailored specifically for legacy **2018–2019 Rec Room IL2CPP builds**. 

This repository provides all the essential programmatic toolsets required to bypass defunct login servers, customize player metrics via a local web panel, manage custom wardrobes, and force the game client into an entirely offline single-player activity sandbox (Paintball, Laser Tag, and Quests).

---

## 📁 Repository Blueprint

```text
📁 n.nameServwrs/
├── 📁 plugin/
│   └── 📄 SandboxMod.cs     # C# Harmony script to force offline map boot loops
├── 📄 .gitignore            # Excludes local database, backups, and caches from tracking
├── 📄 README.md             # Repository documentation and deployment handbook
├── 📄 app.py                # Flask local master API server and web control panel
├── 📄 cache_installer.py    # Automatic zip extraction utility for map assets
├── 📄 patcher.py            # Automated hex string padding utility for client binaries
└── 📄 start.bat             # One-click micro-launcher engine for Windows users
```

---

## 🛠️ Core Features

* **Authentication Bypass**: Intercepts modern connection limits (e.g., Error 1040) and platform handshakes, convincing the client that your machine is the official server.
* **Local Control Dashboard**: Provides a lightweight dark-themed web browser interface running on port `8080` for modifying character display names, updating level values, and tuning token wallets.
* **Persistent Storage (SQLite)**: Changes made inside the Dorm Room mirror or wardrobe locker panel are saved permanently to a local `reborn_rec.db` schema file.
* **Cosmetic Locker Injection**: Pushes any valid historical item keys into your watch drawer customization layout instantly.
* **Offline Activity Sandbox**: Leverages client-side instrumentation to bypass standard Photon server match queues, enabling local map exploration.

---

## 🚀 Step-by-Step Installation Handbook

### 1. Repository Setup & Extraction
Clone or download this repository, and drop **all files** (`app.py`, `patcher.py`, `cache_installer.py`, `start.bat`) directly into the root folder of your legacy 2018–2019 Rec Room game files (the directory containing `RecRoom.exe` and `GameAssembly.dll`).

### 2. Boot the API Server Engine
Execute the project environment loopback script by double-clicking:
```bash
start.bat
```
*Note: This script will automatically check for Python, safely install required `flask` dependencies quietly, and launch the server pipeline. Keep this terminal window open while playing.*

Open your web browser and navigate to `http://localhost:8080` to access your profile settings panel.

### 3. Patch the Game Executable Binary
To redirect the game client's attention away from official endpoints, open a terminal window in your game directory and execute the binary hook script:
```bash
python patcher.py
```
This process targets `GameAssembly.dll` and `global-metadata.dat`, swapping domain queries to your local address while employing exact byte padding to ensure file structural offsets are preserved.

### 4. Inject Historical Map Asset Cache (Crucial)
Because older builds stream maps from cloud buckets dynamically on demand, you must place the physical level packages locally:
1. Obtain an archived 2018–2019 `CustomCache` map folder from a legacy preservation group.
2. Package those `.assetbundle` and map files into a compressed folder named **`maps_cache.zip`** and drop it right into the main game directory.
3. Run the installer script:
   ```bash
   python cache_installer.py
   ```
This will automatically configure a `RecRoom_Data/CustomCache/` path structure and unzip the levels exactly where the engine expects them.

### 5. Install the Client Sandbox Plugin
1. Download **BepInEx (IL2CPP stable version)** matching your architecture and extract it into your main game directory.
2. Compile the provided source file `plugin/SandboxMod.cs` into a `.dll` payload assembly using Visual Studio, MSBuild, or your preferred C# compiler.
3. Move the compiled `SandboxMod.dll` file directly into the `BepInEx/plugins/` directory.

---

## 🎮 How to Play

1. Verify `start.bat` is running.
2. Boot your legacy Rec Room build (supports standard Screen Mode and VR configurations).
3. The game will automatically load your customized local profile, bypassing title screens, and spawn you directly in front of the Dorm Room mirror.
4. Interact with the watch menu or activity doors to load any game map completely solo.

---

## ⚙️ Troubleshooting Matrix

* **Black Screen / Instant Crash on Boot**: This usually implies a binary mapping conflict. Ensure you are applying `patcher.py` to an unmodded, pristine 2018 or 2019 build. Restore your clean state using the generated `.bak` backup files if needed.
* **Infinite Loading Loop on Doors**: This means your map cache layout is unaligned. Check that your historical files are present inside `RecRoom_Data/CustomCache/` and that the BepInEx framework is actively loading `SandboxMod.dll`.
* **ModuleNotFoundError (Flask)**: Avoid clicking `app.py` directly if Python isn't mapped globally. Always boot via `start.bat`, which installs the prerequisite environments silently.

---

## ⚖️ License & Disclaimer
This project is an open-source educational preservation tool designed strictly for localhost emulation, offline game sandbox research, and abandoned software study. It is not affiliated with, authorized, maintained, or endorsed by Against Gravity, Rec Room Inc., or any of its affiliates.

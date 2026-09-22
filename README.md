# Thorlabs Data Overview

Windows desktop app that walks a Thorlabs data folder, builds TIFF stacks and averages, writes SNR stats, and creates a PDF overview.

## For lab users (Windows)

You do **not** need Python, an IDE, or this repository.

1. Download the latest files from [Releases](https://github.com/RasHerlo/Thorlabs_Data_Overview/releases).
2. Install **or** unzip:
   - `ThorlabsDataOverview-*-Setup.exe` — Next/Next installer, optional desktop shortcut
   - `ThorlabsDataOverview-*-windows-portable.zip` — unzip anywhere (or copy from a USB stick) and double-click `ThorlabsDataOverview.exe`
3. In the app, choose the **parent folder** that contains Thorlabs recordings, then click **Run**.
4. When it finishes, open `overview.pdf` in that folder.

Existing stacks and averages are skipped so reruns do not overwrite them. The PDF is rewritten each run.

If Windows SmartScreen warns that the app is unrecognized: **More info → Run anyway**. The build is unsigned in v1.

## For developers

```text
python app.py
```

`Main_Folder_Walk.py` launches the same window. The walk itself is `run_folder_walk(root_dir, log=..., should_stop=...)`.

### Windows build (installer + portable zip)

From a machine with the project dependencies installed:

```text
powershell -ExecutionPolicy Bypass -File packaging\build_windows.ps1
```

Output lands in `dist/release/`. Inno Setup 6 is required for the installer; without it you still get the portable zip.

To publish: tag `v1.0.0` (or run the **Build Windows app** GitHub Action) and attach the files in `dist/release/` to a GitHub Release. USB copies of those same files are equivalent.

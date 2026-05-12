# Gesture-to-Grid Plugin for Krita

Convert hand-drawn lines into perspective grids using AI-assisted OpenCV detection.

## Installation & Setup

The plugin requires OpenCV and NumPy to work. These are bundled via a one-time setup process:

### Option A: Using the Batch File (Windows - Easiest)

1. Open File Explorer and navigate to:
   ```
   C:\Users\<YourUsername>\AppData\Roaming\krita\pykrita\gesture_2_grid\
   ```

2. Double-click `setup.bat`

3. Wait for the setup to complete (it will install Python packages into a local `python_env` folder)

4. Restart Krita

5. The plugin is now ready to use!

### Option B: Using Python Script

1. Open a terminal/PowerShell in the plugin directory:
   ```
   cd C:\Users\<YourUsername>\AppData\Roaming\krita\pykrita\gesture_2_grid\
   ```

2. Run the setup script:
   ```
   python setup.py
   ```

3. Wait for it to complete, then restart Krita

## Usage

1. In Krita, draw a gesture/line representing perspective lines (e.g., sketch a cube outline or parallel lines)

2. Open the **Gesture-to-Grid** docker panel (Windows → Dockable Dialogs → Gesture-to-Grid)

3. Adjust settings:
   - **Grid Density**: Controls spacing between grid rays (lower = wider spacing)
   - **Line Strength**: Controls line thickness (1-5 pixels)
   - **Perspective Mode**: Auto / 1-Point / 2-Point / 3-Point

4. Click **Generate Grid**

5. The plugin will:
   - Detect lines in your drawing
   - Compute vanishing points
   - Create a perspective grid layer based on the mode

## Troubleshooting

### "Error: OpenCV not installed"
Run `setup.bat` or `setup.py` from the plugin folder to install dependencies.

### "Error: Python executable not found"
Make sure you've run the setup script. If it fails, ensure Python 3.6+ is installed on your system.

### "OpenCV engine error: ..."
Check the Krita console/logs for the actual error message. Most errors relate to:
- Missing input image (draw something first)
- Invalid layer type (use Paint or Vector layers)
- Corrupted image data

### "No grid generated"
- Try drawing more lines (the algorithm needs at least 4-5 hand-drawn lines)
- Adjust **Grid Density** to lower values
- Use **Perspective Mode: Auto** for automatic detection

## What Gets Installed

The setup scripts create a `python_env` folder containing:
- Python 3.x interpreter
- opencv-python (computer vision)
- numpy (numerical computing)

All isolated to the plugin folder—no system-wide changes.

## Uninstall

Simply delete the `python_env` folder, or remove the entire plugin folder from:
```
C:\Users\<YourUsername>\AppData\Roaming\krita\pykrita\gesture_2_grid\
```

Krita will continue to work normally.

## Support

If you encounter issues:
1. Check the status message in the plugin dock panel
2. Consult Krita's console window (Help → Show Console)
3. Re-run `setup.bat` to reinstall dependencies

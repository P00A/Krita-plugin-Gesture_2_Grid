#!/usr/bin/env python3
"""
Setup script for Gesture-to-Grid Krita Plugin
Creates a Python virtual environment with OpenCV pre-installed
"""

import os
import sys
import subprocess
import shutil

def main():
    print("=" * 50)
    print("Gesture-to-Grid Plugin Setup")
    print("=" * 50)
    print()
    
    # Get the plugin directory (where this script is located)
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(plugin_dir, "python_env")
    
    print(f"Plugin directory: {plugin_dir}")
    print(f"Virtual environment will be created at: {venv_dir}")
    print()
    
    # Check if python_env already exists
    if os.path.exists(venv_dir):
        print("python_env folder already exists. Reusing existing environment.")
        if sys.platform == "win32":
            python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            python_exe = os.path.join(venv_dir, "bin", "python")

        if os.path.exists(python_exe):
            print(f"Found existing environment at: {python_exe}")
            check = subprocess.run([python_exe, "-c", "import cv2"], capture_output=True, text=True)
            if check.returncode == 0:
                print("Existing python_env is valid and already has OpenCV installed.")
                return True
            print("Existing python_env is missing OpenCV. Installing required packages...")
        else:
            print("WARNING: Existing python_env folder does not contain a valid Python executable.")
            print("Please remove the folder and rerun setup, or run setup.py again after fixing the environment.")
            return False
    else:
        # Create virtual environment
        print("Creating Python virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        except subprocess.CalledProcessError:
            print("ERROR: Failed to create virtual environment.")
            print("Make sure you have Python 3.6+ installed.")
            return False
    
    # Determine the Python executable inside the virtual environment
    if sys.platform == "win32":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
    
    # Upgrade pip via python -m pip
    print()
    print("Upgrading pip...")
    try:
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    except subprocess.CalledProcessError:
        print("WARNING: Failed to upgrade pip (non-critical)")
    
    # Install packages
    print()
    print("Installing OpenCV and dependencies...")
    packages = ["opencv-python", "numpy"]
    
    try:
        subprocess.run([python_exe, "-m", "pip", "install"] + packages, check=True)
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install packages.")
        return False
    
    print()
    print("=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print()
    print("✓ The plugin is now ready to use in Krita.")
    print("✓ Restart Krita if it was running.")
    print("✓ Try the 'Generate Grid' button.")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

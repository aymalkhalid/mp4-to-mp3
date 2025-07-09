#!/usr/bin/env python3
"""
Build script for MP4 to MP3 Converter
This script creates an executable from the Tkinter GUI application
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error:")
        print(e.stderr)
        return False

def main():
    print("MP4 to MP3 Converter - Build Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("mp4_to_mp3_gui.py").exists():
        print("Error: mp4_to_mp3_gui.py not found in current directory")
        print("Please run this script from the mp4tomp3 folder")
        sys.exit(1)
    
    # Install/upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements_gui.txt", "Installing requirements"):
        sys.exit(1)
    
    # Build executable
    pyinstaller_cmd = (
        f"{sys.executable} -m PyInstaller "
        "--onefile "
        "--windowed "
        "--name MP4_to_MP3_Converter "
        "--distpath ./dist "
        "--workpath ./build "
        "--specpath ./build "
        "mp4_to_mp3_gui.py"
    )
    
    if not run_command(pyinstaller_cmd, "Building executable with PyInstaller"):
        sys.exit(1)
    
    # Check if executable was created
    exe_path = Path("dist/MP4_to_MP3_Converter.exe")
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
        print(f"\n✓ Build completed successfully!")
        print(f"Executable location: {exe_path.absolute()}")
        print(f"Executable size: {exe_size:.1f} MB")
        print("\nYou can now distribute the executable file to run the application without Python installed.")
    else:
        print("\n✗ Build failed - executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()

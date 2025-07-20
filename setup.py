"""
Setup script for Voice-Controlled Clash Royale
This script helps prepare the environment and build the executable
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_platform():
    """Check if running on Windows"""
    if platform.system() != "Windows":
        print("WARNING: This build script is designed for Windows")
        print(f"Current platform: {platform.system()}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install requirements: {e}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # First build a console version for testing/debugging
    print("Building console version (for testing)...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--onefile", "--console", "--name", "ClashRoyaleVoiceControl_Console",
            "--add-data", ".env;.",
            "--add-data", "config.py;.",
            "--hidden-import", "speech_recognition",
            "--hidden-import", "pyaudio",
            "--hidden-import", "google.generativeai",
            "--hidden-import", "PIL",
            "--hidden-import", "mss",
            "--hidden-import", "pygetwindow",
            "--hidden-import", "pyautogui",
            "--hidden-import", "dotenv",
            "main.py"
        ])
        print("Console version built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to build console version: {e}")
        return False
    
    # Then build the windowed version for release
    print("Building windowed version (for release)...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--onefile", "--windowed", "--name", "ClashRoyaleVoiceControl",
            "--add-data", ".env;.",
            "--add-data", "config.py;.",
            "--hidden-import", "speech_recognition",
            "--hidden-import", "pyaudio",
            "--hidden-import", "google.generativeai",
            "--hidden-import", "PIL",
            "--hidden-import", "mss",
            "--hidden-import", "pygetwindow",
            "--hidden-import", "pyautogui",
            "--hidden-import", "dotenv",
            "main.py"
        ])
        print("Windowed version built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to build windowed version: {e}")
        return False

def create_distribution():
    """Create a distribution folder with all necessary files"""
    print("Creating distribution package...")
    
    dist_folder = "dist/ClashRoyaleVoiceControl_Package"
    
    # Create distribution folder
    os.makedirs(dist_folder, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        ("dist/ClashRoyaleVoiceControl.exe", "ClashRoyaleVoiceControl.exe"),
        ("dist/ClashRoyaleVoiceControl_Console.exe", "ClashRoyaleVoiceControl_Console.exe"),
        (".env", ".env"),
        ("README.md", "README.md"),
        ("config.py", "config.py"),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, os.path.join(dist_folder, dst))
            print(f"Copied {src} -> {dst}")
        else:
            print(f"WARNING: {src} not found, skipping...")
    
    # Create launcher script
    launcher_content = """@echo off
echo ========================================
echo Voice-Controlled Clash Royale Launcher
echo ========================================
echo.
echo Make sure Clash Royale is running and visible!
echo Make sure your .env file has your GEMINI_API_KEY!
echo.
echo Choose version to run:
echo 1. Release version (no console output)
echo 2. Debug version (with console output)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo Starting release version...
    ClashRoyaleVoiceControl.exe
) else if "%choice%"=="2" (
    echo Starting debug version...
    ClashRoyaleVoiceControl_Console.exe
) else (
    echo Invalid choice. Starting release version...
    ClashRoyaleVoiceControl.exe
)

pause
"""
    
    with open(os.path.join(dist_folder, "run.bat"), "w") as f:
        f.write(launcher_content)
    
    print(f"Distribution package created in: {dist_folder}")
    return True

def main():
    """Main setup function"""
    print("=" * 50)
    print("Voice-Controlled Clash Royale - Setup & Build")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_platform():
        print("Continuing anyway, but build may fail on non-Windows platforms...")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create distribution
    if not create_distribution():
        return False
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nYour executable is ready in: dist/ClashRoyaleVoiceControl_Package/")
    print("\nTo run the application:")
    print("1. Make sure your .env file contains your GEMINI_API_KEY")
    print("2. Run ClashRoyaleVoiceControl.exe or use run.bat")
    print("3. Ensure Clash Royale is running and visible")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
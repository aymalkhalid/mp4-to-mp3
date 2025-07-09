@echo off
echo Building MP4 to MP3 Converter Executable...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements_gui.txt

REM Build executable
echo Building executable with PyInstaller...
pyinstaller --onefile --windowed --name "MP4_to_MP3_Converter" --icon=icon.ico mp4_to_mp3_gui.py

echo.
echo Build complete! Check the 'dist' folder for the executable.
echo.
pause

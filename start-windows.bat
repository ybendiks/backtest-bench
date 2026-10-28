@echo off
cd /d "%~dp0"
echo Starting Backtest Bench setup...
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 get_data.py
  goto done
)
python --version >nul 2>nul
if %errorlevel%==0 (
  python get_data.py
  goto done
)
echo Python is not installed on this computer.
echo.
echo 1. Go to https://www.python.org/downloads/ and click the yellow Download button.
echo 2. Run the installer and TICK the box "Add python.exe to PATH" on the first screen.
echo 3. When it finishes, double-click start-windows.bat again.
:done
echo.
pause

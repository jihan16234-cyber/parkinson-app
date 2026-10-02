@echo off
REM ===== Double-click this file. It installs, trains, and opens the app. =====
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py

REM stop Streamlit's first-run email prompt
if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
  echo [general]> "%USERPROFILE%\.streamlit\credentials.toml"
  echo email = "">> "%USERPROFILE%\.streamlit\credentials.toml"
)

echo [1/3] Installing libraries...
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto :err

echo [2/3] Training models (about 1-2 minutes)...
%PY% train.py
if errorlevel 1 goto :err

echo [3/3] Opening the app in your browser...
%PY% -m streamlit run app.py
goto :eof

:err
echo.
echo ERROR happened. Copy the red text above and send it to get help.
pause

@echo off
:: Load the version from the .env file
for /f "tokens=2 delims==" %%A in ('findstr APP_VERSION .env') do set APP_VERSION=%%A

:: Ensure that APP_VERSION has 4 components (e.g., 1.1.6.0)
setlocal enabledelayedexpansion
set dot_count=0
for /l %%i in (1,1,255) do (
    if "!APP_VERSION:~%%i,1!"=="" goto check_done
    if "!APP_VERSION:~%%i,1!"=="." set /a dot_count+=1
)

:check_done
if not "%dot_count%"=="3" (
    echo Error: The APP_VERSION is not formatted as major.minor.build.revision
    exit /b 1
)

:: Activate the virtual environment
call venv37\Scripts\activate

:: Run PyInstaller with the version passed to the .spec file
venv37\Scripts\python.exe -m PyInstaller app.spec --noconfirm

echo Version loaded from .env: %APP_VERSION%

:: Run Inno Setup to build the installer with the version
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup37.iss /DMyAppVersion="%APP_VERSION%"

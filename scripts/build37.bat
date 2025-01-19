@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd ../

:: Enable immediate exit on error (like set -e in bash)
set "ErrorActionPreference=Stop"

:: Load the version from version.py using Python
for /f "tokens=*" %%i in ('venv37\Scripts\python.exe -c "from lib.version import __version__; print(__version__)"') do set APP_VERSION=%%i

:: Ensure that APP_VERSION has 4 components (e.g., 1.1.6.0)
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

:: Load the version from version.py
echo Version format to be used in Inno Setup: %APP_VERSION%

:: Create a temporary .iss file with AppVersion and VersionInfoVersion replaced
(for /f "usebackq delims=" %%i in ("setup37.iss") do (
    set "line=%%i"
    if "!line!"=="AppVersion={#MyAppVersion}" (
        echo AppVersion=%APP_VERSION%
    ) else if "!line!"=="VersionInfoVersion={#MyAppVersion}" (
        echo VersionInfoVersion=%APP_VERSION%
    ) else (
        echo !line!
    )
)) > setup_temp.iss

:: Run Inno Setup with the temporary file
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup_temp.iss

del setup_temp.iss

:: Update the version and date in index.html
venv37\Scripts\python.exe -c "import re, datetime; \
content = open('docs/index.html', 'r').read(); \
print('Original content:', content[:200]); \
today = datetime.datetime.now().strftime('%%Y-%%m-%%d'); \
content = re.sub(r'<td>v[\d\.]+</td>', f'<td>v%APP_VERSION%</td>', content); \
content = re.sub(r'<td>\d{4}-\d{2}-\d{2}</td>', f'<td>{today}</td>', content); \
print('Modified content:', content[:200]); \
open('docs/index.html', 'w').write(content); \
print('File written successfully')"

echo Updated version to %APP_VERSION% and date to %date% in index.html



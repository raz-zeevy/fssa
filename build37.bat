@echo off
:: Load the version from the .env file
for /f "tokens=2 delims==" %%A in ('findstr APP_VERSION .env') do set APP_VERSION=%%A

:: Activate the virtual environment
call venv37\Scripts\activate

:: Run PyInstaller with the version passed to the .spec file
venv37\Scripts\python.exe -m PyInstaller app.spec --noconfirm

:: Run Inno Setup to build the installer with the version
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup37.iss /DMyAppVersion=%APP_VERSION%

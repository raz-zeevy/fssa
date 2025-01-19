call venv37\Scripts\activate
venv37\Scripts\python.exe -m PyInstaller app_debug.spec --noconfirm

@echo off
venv37\Scripts\python.exe -c "import chardet; \
with open('docs/index.html', 'rb') as file: \
    raw = file.read(); \
    result = chardet.detect(raw); \
    print('File encoding:', result); \
    print('Has CRLF:', b'\r\n' in raw); \
    print('Has LF:', b'\n' in raw and not b'\r\n' in raw)"


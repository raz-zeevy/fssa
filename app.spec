# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define which files to exclude from datas
def exclude_files(dir_path):
    import os
    result = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.SCR'):  # Exclude .SCR files
                # Keep the full lib/scripts/fssa-21 path structure
                source = os.path.join(root, file)
                dest = os.path.join('lib/scripts/fssa-21', os.path.relpath(source, dir_path))
                result.append((source, os.path.dirname(dest)))
    return result

a = Analysis(['app.py'],
             pathex=['C:\\Users\\Raz_Z\\Projects\\Shmuel\\fssaDist\fssa'],
             binaries=[],
             datas=[
                 ('lib/assets', 'lib/assets'), 
                 ('lib/assets/toolbar', 'lib/assets/toolbar'),
                 # Use function to exclude .SCR files while preserving path
                 *exclude_files('lib/scripts/fssa-21'),
                 ('README.txt', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tests'],  # .SCR exclusion moved to datas handling
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='fssa',
          debug=False,
          bootloader_ignore_signals=False,
		  uac_admin=False,
          strip=False,
          upx=True,
          console=False,
		  icon='lib\\assets\\icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='fssa')

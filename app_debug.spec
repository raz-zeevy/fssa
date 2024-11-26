# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\Raz_Z\\Projects\\Shmuel\\fssaDist\fssa'],
             binaries=[],
             datas=[('lib/assets','.'), ('lib/scripts/fssa-21/*','lib/scripts/fssa-21/'),
			 ('README.txt', '.'),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tests'],
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
		  uac_admin=True,
          strip=False,
          upx=True,
          console=True,
		  icon='lib\\assets\\icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='fssa')

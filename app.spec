# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\Raz_Z\\Projects\\Shmuel\\fssaDist\fssa'],
             binaries=[],
             datas=[('lib/assets', 'lib/assets'), ('lib/assets/toolbar', 'lib/assets/toolbar'),
			 ('lib/scripts/fssa-21/*','lib/scripts/fssa-21/'),
			 ('README.txt', '.'),
            ('.env', '.')  # Include .env file in the root of the bundle
			 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tests', '*.SCR'],
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

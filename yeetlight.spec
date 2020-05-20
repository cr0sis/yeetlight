# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['yeetlight.py'],
             pathex=['C:\Program Files\Python38', 'C:\\Users\\Fred\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\Fred\\Code\\yeetlight'],
             binaries=[],
             datas=[
                 ('config.json', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='yeetlight',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='bulb_off.ico')

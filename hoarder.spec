# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['hoarder.py'],
             pathex=['C:\\Users\\K\\Desktop\\latest_hoarder\\Hoarder4.1.0'],
             binaries=[('.\\msvcp140.dll', '.'), ('.\\vcruntime140_1.dll', '.')],
             datas=[('.\\Hoarder.yml', '.'), ('.\\parsers.zip', '.')],
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
          name='hoarder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='hoarder.ico')

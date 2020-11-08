# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None


a = Analysis(['MasterParser.py'],
             pathex=['C:\\Users\\K\\Desktop\\latest_hoarder\\MasterParser'],
             binaries=[],
             datas=[('.\\JLParser_AppID.csv', '.')],
             hiddenimports=['yarp.RegistryRecover', 'yarp.RegistryCarve'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

for root,dirs,files in os.walk(".\\parsers\\"):
    for d in dirs:
        if d.startswith("__pycache__") or d.startswith("."):
            continue
        path = os.path.join(root, d)
        f = os.path.join(path,"configuration.json")
        a.datas += [(f,f,'DATA')]
    break


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MasterParser',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Icon.ico')

# -*- mode: python ; coding: utf-8 -*-
import logging

block_cipher = None

logger = logging.getLogger("pyinstaller")

f = open("../oddish.py", "w")
f.write("import src")
f.close()

logger.info('pyuic5 ../src/ui/oddish.ui -o ../src/ui/oddish_base.py')
os.system('pyuic5 ../src/ui/oddish.ui -o ../src/ui/oddish_base.py')

logger.info('cd ../src/ui/res/&&pyrcc5 res.qrc -o ../res_rc.py')
os.system('cd ../src/ui/res/&&pyrcc5 res.qrc -o ../res_rc.py')

a = Analysis(['../oddish.py'],
             pathex=[''],
             binaries=[],
             datas=[('../config','config')],
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
          [],
          exclude_binaries=True,
          name='oddish',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          console=False , icon='oddish.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='oddish')

os.remove("../oddish.py")
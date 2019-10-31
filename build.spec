# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'ui/assets/images/*.png', 'ui/assets/images' )
         ]

a = Analysis(['run.py'],
             pathex=['F:\\Projetos\\replic8'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy'],
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
          name='Replic8',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='replic8.ico',
          console=False )

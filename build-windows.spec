# -*- mode: python -*-

block_cipher = None

added_files = [
    ('.\\gui', 'gui'),
    ('src/data', 'data'),
    ('src/assets', 'assets')
]

a = Analysis(['.\\src\\index.py'],
             pathex=['.\\dist'],
             binaries=None,
             datas=added_files,
             hiddenimports=['clr', 'json', 'threading', 'PIL', 'sys', 'abc'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             )
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='carboncount',
          debug=False,
          strip=True,
          icon='.\\src\\assets\\logo.ico',
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='carboncount')

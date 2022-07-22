# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

hooks = ['Guis/Settings/beads.py', 'Participants/beadsp.py', 'Guis/Experiments/beadsgui.py',
        'Guis/Settings/discount.py', 'Participants/discountp.py', 'Guis/Experiments/discountgui.py',
        'Guis/Settings/gamble.py', 'Participants/gamblep.py', 'Guis/Experiments/gamblegui.py',
        'Guis/Settings/memory.py', 'Participants/memoryp.py', 'Guis/Experiments/memorygui.py', 'Guis/Settings/nact.py',
        'Participants/nactp.py', 'Guis/Experiments/nactgui.py', 'Guis/Settings/pbt.py', 'Participants/pbtp.py',
        'Guis/Experiments/pbtgui.py', 'Guis/Settings/reaction.py', 'Participants/reactionp.py',
        'Guis/Experiments/reactiongui.py' ]

addedfiles = [('assets/', 'assets'),
             ('TM.icns', '.'),
             ('TM.ico', '.')]

a = Analysis(
    ['cli.py'],
    pathex=['C:/Users/dgara/PycharmProjects/TaskMaster/venv/Lib/site-packages'],
    binaries=[],
    datas=addedfiles,
    hiddenimports=['numpy', 'scipy', 'pandas', 'xlsxwriter', 'pkg_resources', 'jinja2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=hooks,
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TaskMaster',
    debug=True,
    bootloader_ignore_signals=False,
    icon='C:/Users/dgara/PycharmProjects/TaskMaster/TM.ico',
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

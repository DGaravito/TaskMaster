# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

hooks = ['Guis/Settings/beadsset.py', 'Participants/beadsp.py', 'Guis/Experiments/beadsexp.py',
        'Guis/Settings/discountset.py', 'Participants/discountp.py', 'Guis/Experiments/discountexp.py',
        'Guis/Settings/dwellset.py', 'Participants/dwellp.py', 'Guis/Experiments/dwellexp.py',
        'Guis/Settings/gambleset.py', 'Participants/gamblep.py', 'Guis/Experiments/gambleexp.py',
        'Guis/Settings/memoryset.py', 'Participants/memoryp.py', 'Guis/Experiments/memoryexp.py',
        'Guis/Settings/nactset.py', 'Participants/nactp.py', 'Guis/Experiments/nactexp.py', 'Guis/Settings/pbtset.py',
        'Participants/pbtp.py', 'Guis/Experiments/pbtexp.py', 'Guis/Settings/reactionset.py',
        'Participants/reactionp.py', 'Guis/Experiments/reactionexp.py', 'Guis/Settings/stroopset.py',
        'Participants/stroopp.py', 'Guis/Experiments/stroopexp.py']

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
    debug=False,
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

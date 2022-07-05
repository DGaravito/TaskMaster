"""
py2app/py2exe build script for TaskMaster. Should automatically work with both py2exe and py2app
"""
import glob
import sys
from setuptools import setup

mainscript = 'main.py'
data = [('assets', glob.glob('assets/*.*'))]

if sys.platform == 'darwin':
    OPTIONS = {
        'argv_emulation': True,
        'site_packages': True,
        'iconfile': 'TM.icns',
        'packages': []
    }
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options={'py2app': OPTIONS}
    )

elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript]
    )

else:
    extra_options = dict(
        scripts=[mainscript]
    )

setup(
    name='TaskMaster',
    version='1.0',
    description='A python-based application that can run common psych research tasks from on any system using PyQt.',
    author='David Michael Nolta Garavito',
    author_email='d.garavito2@gmail.com',
    **extra_options
)

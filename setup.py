"""
py2app build script for TaskMaster.
"""
import glob
from setuptools import setup

mainscript = 'main.py'
data = [('assets', glob.glob('assets/*.*'))]

OPTIONS = {
    'argv_emulation': True,
    'site_packages': True,
    'iconfile': 'TM.icns',
    'packages': []
}

setup(
    name='TaskMaster',
    version='1.0',
    description='A python-based application that can run common psych research tasks from on any system using PyQt.',
    author='David Michael Nolta Garavito',
    author_email='d.garavito2@gmail.com',
    setup_requires=['py2app'],
    app=[mainscript],
    options={'py2app': OPTIONS}
)

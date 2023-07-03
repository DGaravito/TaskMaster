"""
Build script for TaskMaster.
"""
import glob
from setuptools import setup
import sys

mainscript = 'cli.py'
data = [('Assets', glob.glob('Assets/*'))]

if sys.platform == 'darwin':

    OPTIONS = {
        'argv_emulation': True,
        'site_packages': True,
        'iconfile': 'TM.icns'
    }

    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        data_files=data,
        options=dict(py2app=OPTIONS)
    )

elif sys.platform == 'win32':

    OPTIONS = {
        'iconfile': 'TM.ico'
    }

    extra_options = dict(
         setup_requires=['py2exe'],
         app=[mainscript],
         data_files=data,
         options=dict(py2exe=OPTIONS)
    )

else:
     extra_options = dict(
         scripts=[mainscript],
         data_files=data
     )

setup(
    name='TaskMaster',
    version='1.0.0',
    url='https://github.com/DGaravito/TaskMaster',
    description='A python-based application that can run common psych research tasks on any system using PyQt.',
    author='David Michael Nolta Garavito',
    author_email='d.garavito2@gmail.com',
    install_requires=[
                         'PyQt6',
                         'numpy',
                         'scipy',
                         'pandas',
                         'xlsxwriter'
                     ],
    **extra_options
)

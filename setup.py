from cx_Freeze import setup, Executable

setup(  name = 'wUndergroundImport',
        version = '0.1',
        description = 'Imports Weather Data from WU',
        executables = [Executable('main.py')]
        )
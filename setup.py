import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "upemtk","tkinter","datetime","doctest"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "reversi",
        version = "1",
        description = "Simple reversi",
        options = {"build_exe": build_exe_options},
        executables = [Executable("menu_reversi_v1.py", base=base)])
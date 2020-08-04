import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": ["pygame", "random", "math", "datetime", "csv"],
                     "include_files": ["score_log.txt", "space-invaders.png", "laser.wav", "explosion.wav", "enemy.png", "bullet.png", "background_mainmenu.png", "background.wav", "background.PNG", "001-ufo.png"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="SpaceInvaders",
      version="1.0",
      description="Kill Enemies",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="main.py", base=base)])

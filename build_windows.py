import PyInstaller.__main__
import os
import shutil

def build_windows():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Windows uses semicolon as path separator in --add-data
    PyInstaller.__main__.run([
        'knight_survival.py',
        '--onefile',
        '--windowed',
        '--name=KnightSurvival',
        '--add-data=sprites/*;sprites',  # Windows uses semicolon instead of colon
        '--clean',
    ])

if __name__ == "__main__":
    build_windows()
# build_mac.py
import PyInstaller.__main__
import os
import shutil

def build_mac():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # The key is using the correct path separator and being explicit about data files
    PyInstaller.__main__.run([
        'knight_survival.py',
        '--onefile',
        '--windowed',
        '--name=KnightSurvival',
        '--add-data=sprites/*:sprites',  # This is the key change - copy all sprite files
        '--clean',
    ])

if __name__ == "__main__":
    build_mac()
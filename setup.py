from setuptools import setup, Extension
from Cython.Build import cythonize
import os

extensions = []
for path, dirnames, filenames in os.walk(f'.{os.sep}mypytools{os.sep}'):
    for file in filenames:
        if file[-4:] != '.pyx':
            continue
        file = os.path.join(path, file)
        ext = Extension(file.replace(os.sep, '.').strip('.pyx'), [file],
                        include_dirs=[], libraries=[], library_dirs=[])
        extensions.append(ext)

setup(
    ext_modules=cythonize(extensions)
)

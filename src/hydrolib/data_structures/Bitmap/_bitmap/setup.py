from setuptools import setup, Extension

module = Extension(
    'pybitmap',
    sources=['bitmap_c.c'],
    language='c',
)

setup(
    name='pybitmap',
    version='1.0',
    description='Python C extension for bitmap operations',
    ext_modules=[module],
)

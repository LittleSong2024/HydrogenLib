from setuptools import setup, Extension

module = Extension(
    'hybitmap',
    sources=['hybitmap_capi.c'],
    language='c',
)

setup(
    name='hybitmap',
    version='1.0',
    description='Python C extension for bitmap operations',
    ext_modules=[module],
    python_requires='>=3.8',
    author='LittleSong2024',
    author_email='idesong6@qq.com',
    url='',
    license='HydrogenLib License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ]
)

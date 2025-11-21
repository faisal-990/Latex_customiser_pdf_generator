from setuptools import setup, find_packages
import os

VERSION = '1.0.0'

def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='latex-selector',
    version=VERSION,
    description='GUI tool for selecting LaTeX components',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Sawez',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['data/*.tex'],
    },
    install_requires=[
        'PyQt5>=5.15.7',
    ],
    entry_points={
        'console_scripts': [
            'latex-selector=main:main',  # Fixed: removed 'src.' prefix
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

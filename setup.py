#!/usr/bin/env python3
"""Setup script for MemInspector"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='meminspector',
    version='1.1.0',
    description='Memory Inspector for macOS - Analyze memory consumption of applications and threads',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Jaccon',
    author_email='jaccon@example.com',
    url='https://github.com/jaccon/meminspector',
    license='MIT',
    
    py_modules=['meminspector'],
    
    install_requires=[
        'psutil>=5.9.0',
        'tqdm>=4.65.0',
        'matplotlib>=3.5.0',
        'rich>=13.0.0',
        'docker>=6.0.0',
    ],
    
    entry_points={
        'console_scripts': [
            'meminspector=meminspector:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    
    python_requires='>=3.7',
    
    keywords='memory monitor macos inspector system profiling',
    
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/meminspector/issues',
        'Source': 'https://github.com/yourusername/meminspector',
    },
)

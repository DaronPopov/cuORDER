#!/usr/bin/env python3
"""
CUDA Environment Resolver - Python Wheel Package
Locked-down but programmable through cuORDER
"""

from setuptools import setup, find_packages
import os
import shutil

# Check the compiled binary is available
def copy_binary():
    """Ensure the CUDA resolver binary is available"""
    binary_path = "cuorder/bin/cuda_env_resolver"

    if os.path.exists(binary_path):
        # Make sure it's executable
        os.chmod(binary_path, 0o755)
        print(f"✅ Binary ready: {binary_path}")
    else:
        print(f"❌ Warning: Binary not found at {binary_path}")
        print("Run 'make' in the cuda_env_resolver directory first")

# Check essential config/data files
def copy_assets():
    """Ensure configuration and data files are available"""
    assets = [
        "cuorder/config",
        "cuorder/scripts",
        "cuorder/docker"
    ]

    for asset in assets:
        if os.path.exists(asset):
            print(f"✅ Assets ready: {asset}")
        else:
            print(f"❌ Warning: Assets not found at {asset}")

if __name__ == "__main__":
    copy_binary()
    copy_assets()

setup(
    name="cuorder-cuda-env",
    version="1.0.0",
    author="cuORDER",
    description="Locked-down CUDA Environment Resolver programmable through cuORDER",
    packages=find_packages(),
    package_data={
        'cuorder': [
            'bin/cuda_env_resolver',
            'config/*',
            'scripts/*',
            'docker/*'
        ]
    },
    include_package_data=True,
    install_requires=[
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'cuorder-cuda=cuorder.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: System :: Hardware',
    ],
    python_requires='>=3.8',
)
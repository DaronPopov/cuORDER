#!/usr/bin/env python3
"""
CUDA Environment Resolver - Python Wheel Package
Locked-down but programmable through cuORDER
"""

from setuptools import setup, find_packages
import os
import shutil

# Copy the compiled binary to package data
def copy_binary():
    """Copy the compiled CUDA resolver binary to package"""
    binary_src = "../cuda_env_resolver"
    binary_dst = "cuorder/bin/cuda_env_resolver"

    if os.path.exists(binary_src):
        os.makedirs(os.path.dirname(binary_dst), exist_ok=True)
        shutil.copy2(binary_src, binary_dst)
        # Make executable
        os.chmod(binary_dst, 0o755)
        print(f"Copied binary: {binary_src} -> {binary_dst}")
    else:
        print(f"Warning: Binary not found at {binary_src}")

# Copy essential config/data files
def copy_assets():
    """Copy configuration and data files"""
    assets = [
        ("../config", "cuorder/config"),
        ("../scripts", "cuorder/scripts"),
        ("../docker", "cuorder/docker")
    ]

    for src, dst in assets:
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copied assets: {src} -> {dst}")

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
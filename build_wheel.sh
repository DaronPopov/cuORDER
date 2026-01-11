#!/bin/bash

# Build cuORDER CUDA Environment Resolver Wheel

set -e

echo "🔨 Building cuORDER CUDA Environment Resolver..."

# Build the C binary first
echo "📦 Building CUDA resolver binary..."
cd ..
make clean
make
cd cuorder_wrapper

# Build the wheel
echo "📦 Building Python wheel..."
python3 setup.py sdist bdist_wheel

echo "✅ Wheel built successfully!"
echo "📁 Distribution files:"
ls -la dist/

echo ""
echo "🧪 Test the wheel:"
echo "pip install dist/cuorder_cuda_env-1.0.0-py3-none-any.whl --force-reinstall"
echo "cuorder-cuda --info"
echo "cuorder-cuda examples/basic_env.cuorder"
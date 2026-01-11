#!/bin/bash

# CUDA Environment Docker Entrypoint Script
# This script sets up the CUDA environment and provides helpful information

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  CUDA Environment Container   ${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Display CUDA information
echo -e "${GREEN}CUDA Information:${NC}"
if command -v nvcc &> /dev/null; then
    echo "CUDA Compiler: $(nvcc --version | grep "release" | sed 's/.*release //' | sed 's/,.*//')"
fi

if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits)"
    echo "GPU Devices:"
    nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader,nounits | while IFS=',' read -r index name memory; do
        echo "  GPU $index: $name ($memory MB)"
    done
else
    echo -e "${YELLOW}Warning: nvidia-smi not found. GPU access may not be available.${NC}"
fi
echo ""

# Set up environment
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$CUDA_HOME/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Display helpful commands
echo -e "${GREEN}Available commands:${NC}"
echo "  nvcc --version          # Check CUDA compiler version"
echo "  nvidia-smi              # GPU status and monitoring"
echo "  python3 -c \"import torch; print(torch.cuda.is_available())\"  # Check PyTorch CUDA support"
echo ""

# Check if CUDA samples are available
if [ -d "/usr/local/cuda/samples" ]; then
    echo -e "${GREEN}CUDA Samples available at:${NC} /usr/local/cuda/samples"
    echo "  Run: make -C /usr/local/cuda/samples/0_Simple/vectorAdd"
    echo ""
fi

# Display workspace information
echo -e "${GREEN}Workspace:${NC} /workspace"
echo "  Projects: /workspace/projects"
echo "  Data: /workspace/data"
echo ""

# Execute the command passed to docker run
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No command specified. Starting interactive shell...${NC}"
    echo -e "${YELLOW}Type 'exit' to leave the container.${NC}"
    echo ""
    exec /bin/bash
else
    echo -e "${BLUE}Executing: $@${NC}"
    echo ""
    exec "$@"
fi
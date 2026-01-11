#!/bin/bash

# CUDA Environment Resolver - Hardware Detection Script
# This script detects hardware specifications for CUDA environment setup

set -e

OUTPUT_FILE="${1:-hardware_info.json}"

# Initialize JSON output
echo "{" > "$OUTPUT_FILE"
echo '  "timestamp": "'$(date -Iseconds)'",' >> "$OUTPUT_FILE"

# Detect OS and kernel
echo '  "os": {' >> "$OUTPUT_FILE"
echo '    "name": "'$(lsb_release -si 2>/dev/null || echo "Unknown")'",' >> "$OUTPUT_FILE"
echo '    "version": "'$(lsb_release -sr 2>/dev/null || uname -r)'",' >> "$OUTPUT_FILE"
echo '    "kernel": "'$(uname -r)'"' >> "$OUTPUT_FILE"
echo '  },' >> "$OUTPUT_FILE"

# CPU Detection
echo '  "cpu": {' >> "$OUTPUT_FILE"
CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | sed 's/^ *//')
CPU_CORES=$(nproc)
CPU_THREADS=$(grep -c processor /proc/cpuinfo)
CPU_ARCH=$(uname -m)

echo '    "model": "'$CPU_MODEL'",' >> "$OUTPUT_FILE"
echo '    "cores": '$CPU_CORES',' >> "$OUTPUT_FILE"
echo '    "threads": '$CPU_THREADS',' >> "$OUTPUT_FILE"
echo '    "architecture": "'$CPU_ARCH'"' >> "$OUTPUT_FILE"
echo '  },' >> "$OUTPUT_FILE"

# Memory Detection
echo '  "memory": {' >> "$OUTPUT_FILE"
TOTAL_MEM=$(free -g | grep Mem | awk '{print $2}')
echo '    "total_gb": '$TOTAL_MEM >> "$OUTPUT_FILE"
echo '  },' >> "$OUTPUT_FILE"

# GPU Detection
echo '  "gpu": [' >> "$OUTPUT_FILE"

# Check if nvidia-smi is available
if command -v nvidia-smi &> /dev/null; then
    # Get GPU information using nvidia-smi
    GPU_COUNT=$(nvidia-smi --query-gpu=count --format=csv,noheader,nounits | tail -1)

    for ((i=0; i<GPU_COUNT; i++)); do
        if [ $i -gt 0 ]; then echo '    ,' >> "$OUTPUT_FILE"; fi

        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits -i $i)
        GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits -i $i | sed 's/ MiB//')
        GPU_CUDA_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits -i $i)
        GPU_COMPUTE_CAP=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader,nounits -i $i)

        echo '    {' >> "$OUTPUT_FILE"
        echo '      "index": '$i',' >> "$OUTPUT_FILE"
        echo '      "name": "'$GPU_NAME'",' >> "$OUTPUT_FILE"
        echo '      "memory_mb": '$GPU_MEMORY',' >> "$OUTPUT_FILE"
        echo '      "driver_version": "'$GPU_CUDA_VERSION'",' >> "$OUTPUT_FILE"
        echo '      "compute_capability": "'$GPU_COMPUTE_CAP'"' >> "$OUTPUT_FILE"
        echo '    }' >> "$OUTPUT_FILE"
    done
else
    # Fallback: try to detect GPUs using lspci
    GPU_INFO=$(lspci | grep -i nvidia | head -5)
    if [ ! -z "$GPU_INFO" ]; then
        echo '    {' >> "$OUTPUT_FILE"
        echo '      "index": 0,' >> "$OUTPUT_FILE"
        echo '      "name": "NVIDIA GPU (detected via lspci)",' >> "$OUTPUT_FILE"
        echo '      "memory_mb": 0,' >> "$OUTPUT_FILE"
        echo '      "driver_version": "unknown",' >> "$OUTPUT_FILE"
        echo '      "compute_capability": "unknown"' >> "$OUTPUT_FILE"
        echo '    }' >> "$OUTPUT_FILE"
    else
        echo '    {' >> "$OUTPUT_FILE"
        echo '      "index": 0,' >> "$OUTPUT_FILE"
        echo '      "name": "No NVIDIA GPU detected",' >> "$OUTPUT_FILE"
        echo '      "memory_mb": 0,' >> "$OUTPUT_FILE"
        echo '      "driver_version": "none",' >> "$OUTPUT_FILE"
        echo '      "compute_capability": "none"' >> "$OUTPUT_FILE"
        echo '    }' >> "$OUTPUT_FILE"
    fi
fi

echo '  ]' >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

echo "Hardware detection completed. Results saved to $OUTPUT_FILE"
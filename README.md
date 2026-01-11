# cuORDER - CUDA Environment Manager

**Stop fighting CUDA versions. Let cuORDER handle it.**

Automatically generate working CUDA + Python + ML Docker environments tailored to your specific machine. 

> [!IMPORTANT]
> **Prerequisites:** This tool automates the configuration for the **NVIDIA Container Toolkit**. You must have an NVIDIA GPU, NVIDIA Drivers, and the NVIDIA Docker runtime installed on your host machine to run the generated environments.

## Quick Start (3 steps)

### 1. Install

```bash
pip install cuorder-cuda-env
```

### 2. Create Config (`my_env.cuorder`)

```yaml
cuda_env:
  hardware_detection: true
  output_dir: "my_cuda_env"
  python:
    packages: [numpy, torch, transformers]
```

### 3. Generate & Build

```bash
# Generate (auto-detects your GPU & sets up Docker)
cuorder-cuda my_env.cuorder

# Build & Run
cd my_cuda_env
./build_cuda_env.sh
```

## Why it's magic ✨

- ✅ **Smart Hardware Detection**: Picks the optimal CUDA version for your GPU/Driver.
- ✅ **Auto-fixes Dockerfiles**: Cleans up redundant packages and fixes entrypoints.
- ✅ **Works Everywhere**: The same config works on a 1080, 3070, or 4090.
- ✅ **Permission Helper**: Detects Docker permission issues and tells you how to fix them.

## Commands

```bash
cuorder-cuda --info              # Test system, permissions, and available CUDA
cuorder-cuda config.cuorder      # Generate your environment
```

The same `.cuorder` file works on different machines:

- **PC 1** (RTX 3070, driver 560) → Gets CUDA 12.2 environment
- **PC 2** (GTX 1080, driver 470) → Gets CUDA 11.8 environment  
- **PC 3** (RTX 4090, driver 550) → Gets CUDA 12.2 environment

cuORDER automatically detects each machine's hardware and creates the right environment. No manual configuration needed.

## Examples

**Basic ML Setup:**
```yaml
cuda_env:
  hardware_detection: true
  python:
    enabled: true
    packages: [numpy, torch, torchvision]
```

**Full Research Stack:**
```yaml
cuda_env:
  hardware_detection: true
  python:
    enabled: true
    packages:
      - numpy
      - torch
      - torchvision
      - transformers
      - jupyter
      - matplotlib
```

## Commands

```bash
cuorder-cuda --info              # Check system & available CUDA versions
cuorder-cuda config.cuorder      # Generate environment
```

## What Gets Generated

When you run `cuorder-cuda config.cuorder`, you get:

- `Dockerfile.cuda` - Working Dockerfile (fixed automatically)
- `docker-compose.cuda.yml` - Ready-to-use compose file
- `build_cuda_env.sh` - Build script
- `docker-entrypoint.sh` - Environment info script
- `hardware_info.json` - Detected hardware details

## Troubleshooting

**Docker permission denied?**
```bash
sudo usermod -aG docker $USER
newgrp docker  # or logout/login
```

**Docker not running?**
```bash
sudo systemctl start docker
```

**Check what cuORDER sees:**
```bash
cuorder-cuda --info
```

## Requirements

- Linux
- Docker installed and running
- NVIDIA GPU (optional but recommended)
- Python 3.8+

## Installation Options


**From Source:**
```bash
git clone https://github.com/DaronPopov/cuORDER.git
cd cuORDER
./build_wheel.sh
pip install dist/cuorder_cuda_env-*.whl
```

## How It Works

1. You write a simple YAML config
2. cuORDER detects your GPU/CPU/driver
3. It picks the optimal CUDA version
4. Generates a working Dockerfile
5. You build and run - done!

## License

MIT License

---

**Made for the CUDA + ML community** ❤️

*No more fighting CUDA versions. Just write YAML and go.*

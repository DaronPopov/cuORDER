# cuORDER CUDA Environment Resolver

[![PyPI version](https://badge.fury.io/py/cuorder-cuda-env.svg)](https://pypi.org/project/cuorder-cuda-env/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Automatically generate optimized CUDA + Python + ML Docker environments from simple YAML files.**

cuORDER is a programmable system that detects your hardware and creates perfectly configured CUDA development environments. No more struggling with CUDA versions, driver compatibility, or complex Docker setups - just write a YAML file and let cuORDER handle the rest.

## 🚀 Quick Start

Follow these steps to get your CUDA environment up and running:

### Step 1: Install Dependencies

```bash
# Install system dependencies
sudo apt update
sudo apt install -y build-essential docker.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (logout/login after this)
sudo usermod -aG docker $USER
```

### Step 2: Install cuORDER

**Option A: Install from PyPI (Recommended)**
```bash
pip install cuorder-cuda-env
```

**Option B: Install from GitHub**
```bash
pip install git+https://github.com/DaronPopov/cuORDER.git
```

**Option C: Clone and Install Locally**
```bash
# Clone the repository
git clone https://github.com/DaronPopov/cuORDER.git
cd cuORDER

# Build and install
./build_wheel.sh
pip install dist/cuorder_cuda_env-*.whl
```

### Step 3: Verify Installation

```bash
# Check that cuORDER is installed
cuorder-cuda --info

# You should see output like:
# 🔍 cuORDER CUDA Environment Resolver
# Binary Available: ✅
# Config Available: ✅
# Available CUDA Versions: 11.8, 12.0, 12.1, 12.2
```

### Step 4: Create Your CUDA Environment

```bash
# Create a cuORDER configuration file
cat > my_cuda_env.cuorder << 'EOF'
cuda_env:
  hardware_detection: true
  output_dir: "my_cuda_env"
  python:
    enabled: true
    version: "3.11"
    packages: [numpy, torch, torchvision, torchaudio]
EOF
```

### Step 5: Generate Your Environment

```bash
# Generate the CUDA environment
cuorder-cuda my_cuda_env.cuorder

# This will create a 'my_cuda_env' directory with:
# - Dockerfile.cuda (your custom CUDA container)
# - build_cuda_env.sh (build script)
# - docker-compose.cuda.yml (multi-container setup)
# - .cuda_env (configuration file)
```

### Step 6: Build and Run

```bash
# Navigate to the generated environment
cd my_cuda_env

# Build your CUDA container (this may take a few minutes)
./build_cuda_env.sh

# Your container is now ready! Run it with:
docker run --rm --runtime=nvidia -it your_cuda_env
```

### Step 7: Verify Everything Works

```bash
# Inside the container, test CUDA:
nvidia-smi

# Test Python and your installed packages:
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**🎉 Congratulations!** You now have a fully optimized CUDA environment with Python and ML libraries!

## 🎛️ How cuORDER Works

cuORDER uses a **unique programmable approach**:

1. **YAML Configuration Files**: Define your environment requirements in simple `.cuorder` files
2. **Hardware Auto-Detection**: Automatically detects your GPU/CPU and selects optimal CUDA versions
3. **Locked-Down Core**: Immutable C binary ensures security and consistency
4. **Docker Generation**: Creates production-ready containers with all dependencies
5. **One-Click Deployment**: Build scripts handle the complex setup automatically

### Example cuORDER Files

**Basic CUDA Setup:**
```yaml
cuda_env:
  hardware_detection: true
  python:
    enabled: true
    packages: [numpy, torch]
```

**ML Research Environment:**
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
```

**Enterprise Setup:**
```yaml
cuda_env:
  hardware_detection: false  # Use specific versions
  cuda_version: "12.2"
  python:
    enabled: true
    version: "3.11"
    packages: [tensorflow, pytorch, jax]
```

Each `.cuorder` file produces a complete, reproducible environment!

## 📋 What It Does

1. **Auto-detects** your GPU/CPU hardware
2. **Picks optimal** CUDA version for your setup
3. **Generates** custom Docker containers
4. **Includes** Python + ML libraries you specify
5. **Creates** ready-to-run build scripts

## 📁 cuORDER Configuration

Create `.cuorder` files (YAML) to define your environments:

### Basic Setup
```yaml
cuda_env:
  hardware_detection: true
  output_dir: "my_env"

  python:
    enabled: true
    version: "3.11"
    packages: [numpy, torch, torchvision]
```

### ML Research Environment
```yaml
cuda_env:
  hardware_detection: true
  output_dir: "ml_research"

  python:
    enabled: true
    version: "3.11"
    packages:
      - numpy
      - torch
      - torchvision
      - torchaudio
      - transformers
      - jupyter
      - matplotlib
      - scikit-learn
```

## 🛠️ Commands

```bash
cuorder-cuda --help                    # Show help
cuorder-cuda --info                    # System info & CUDA versions
cuorder-cuda config.cuorder            # Generate environment
cuorder-cuda config.cuorder --validate # Validate config only
cuorder-cuda config.cuorder -o /path   # Custom output directory
```

## 📦 Examples

See `examples/` for ready-to-use configurations:

- `basic_env.cuorder` - Simple CUDA + Python
- `ml_research.cuorder` - Full ML research stack

## 🔒 Security & Architecture

**Locked-down core with programmable interface:**

- **Immutable C binary** - Hardware detection & Docker generation
- **cuORDER control** - Only configuration can be modified
- **Audit trail** - Every environment includes its source config
- **Reproducible** - Same cuORDER file = same environment

## 🏗️ Development

```bash
# Clone
git clone https://github.com/yourusername/cuorder-cuda-env
cd cuorder-cuda-env

# Build wheel
./build_wheel.sh

# Install locally
pip install dist/cuorder_cuda_env-*.whl --force-reinstall

# Test
cuorder-cuda examples/basic_env.cuorder
```

## 📋 Requirements

- Linux system
- Docker installed **and running** (cuORDER does NOT auto-start Docker)
- NVIDIA GPU (optional, but recommended for CUDA)
- Python 3.8+

## 🔧 Troubleshooting

### Docker Issues

**"Error: Docker is not running"**

cuORDER does NOT automatically start Docker. Start it manually:

```bash
# Start Docker daemon
sudo systemctl start docker

# Add user to docker group (one-time setup)
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker works
docker ps
```

### Build Issues

**"manifest unknown" errors**

This usually means the CUDA version is too new. cuORDER supports CUDA 11.8-12.2. Check your GPU compatibility:

```bash
cuorder-cuda --info
```

### Permission Issues

**"permission denied" with Docker**

Add your user to the docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add cuORDER examples for new use cases
4. Test with different hardware configurations
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the CUDA + ML community**

*Automate your CUDA environments with cuORDER - the programmable, locked-down way.*
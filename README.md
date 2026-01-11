# cuORDER CUDA Environment Resolver

[![PyPI version](https://badge.fury.io/py/cuorder-cuda-env.svg)](https://pypi.org/project/cuorder-cuda-env/)


A **locked-down but programmable** CUDA environment generator controlled through cuORDER configuration files. Generate optimized CUDA + Python + ML Docker environments with simple YAML configurations.

## 🚀 Quick Start

```bash
# Install
pip install cuorder-cuda-env

# Create your environment config
cat > my_cuda_env.cuorder << 'EOF'
cuda_env:
  hardware_detection: true
  output_dir: "my_cuda_env"
  python:
    enabled: true
    version: "3.11"
    packages: [numpy, torch, torchvision, torchaudio]
EOF

# Generate your CUDA environment
cuorder-cuda my_cuda_env.cuorder

# Build the container
cd my_cuda_env && ./build_cuda_env.sh
```

**That's it!** You get a Docker container perfectly optimized for your hardware.

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
- Docker installed & running
- NVIDIA GPU (optional)
- Python 3.8+

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

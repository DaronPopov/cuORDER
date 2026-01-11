"""
cuORDER Engine for CUDA Environment Resolver
Reads cuORDER configuration files and executes CUDA environment generation
"""

import os
import yaml
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional


class CuOrderEngine:
    """cuORDER engine for programmable CUDA environment generation"""

    def __init__(self):
        self.package_dir = Path(__file__).parent
        self.binary_path = self.package_dir / "bin" / "cuda_env_resolver"
        self.config_dir = self.package_dir / "config"
        self.scripts_dir = self.package_dir / "scripts"
        self.docker_dir = self.package_dir / "docker"

    def load_cuorder_file(self, cuorder_path: str) -> Dict[str, Any]:
        """Load and parse a .cuorder configuration file"""
        with open(cuorder_path, 'r') as f:
            if cuorder_path.endswith('.yaml') or cuorder_path.endswith('.yml') or cuorder_path.endswith('.cuorder'):
                config = yaml.safe_load(f)
            else:
                # Assume JSON for files without specific extensions
                import json
                config = json.load(f)

        return config

    def validate_cuorder_config(self, config: Dict[str, Any]) -> bool:
        """Validate cuORDER configuration"""
        required_fields = ['cuda_env']
        if 'cuda_env' not in config:
            raise ValueError("cuORDER config must contain 'cuda_env' section")

        cuda_env = config['cuda_env']

        # Validate CUDA environment settings
        if 'hardware_detection' not in cuda_env:
            cuda_env['hardware_detection'] = True

        if 'output_dir' not in cuda_env:
            cuda_env['output_dir'] = 'cuda_output'

        # Set defaults for Python/ML settings
        if 'python' not in cuda_env:
            cuda_env['python'] = {}

        python_config = cuda_env['python']
        if 'enabled' not in python_config:
            python_config['enabled'] = True

        if 'version' not in python_config:
            python_config['version'] = '3.11'

        if 'packages' not in python_config:
            python_config['packages'] = ['numpy', 'torch', 'torchvision', 'torchaudio']

        return True

    def generate_temp_config(self, cuorder_config: Dict[str, Any]) -> str:
        """Generate temporary app_config.json from cuORDER config"""
        cuda_env = cuorder_config['cuda_env']

        app_config = {
            "hardware_script": str(self.scripts_dir / "detect_hardware.sh"),
            "cuda_config_file": str(self.config_dir / "cuda_compatibility.json"),
            "output_directory": cuda_env['output_dir'],
            "docker_base_path": str(self.docker_dir),
            "python_version": cuda_env['python']['version'],
            "pip_packages": " ".join(cuda_env['python']['packages']),
            "log_level": cuda_env.get('log_level', 1),
            "auto_detect": cuda_env['hardware_detection'],
            "generate_compose": cuda_env.get('generate_compose', True),
            "include_examples": cuda_env.get('include_examples', False),
            "include_python": cuda_env['python']['enabled']
        }

        # Write to temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
        try:
            with os.fdopen(temp_fd, 'w') as f:
                import json
                json.dump(app_config, f, indent=2)
        except:
            os.close(temp_fd)
            raise

        return temp_path

    def execute_cuda_resolver(self, config_path: str, output_dir: str) -> bool:
        """Execute the CUDA environment resolver binary"""
        if not self.binary_path.exists():
            raise FileNotFoundError(f"CUDA resolver binary not found: {self.binary_path}")

        cmd = [
            str(self.binary_path),
            '-c', config_path,
            '-o', output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.package_dir)

        if result.returncode != 0:
            print("CUDA Resolver Error:")
            print(result.stderr)
            return False

        print("CUDA Environment Generated Successfully!")
        print(result.stdout)
        return True

    def deploy_environment(self, cuorder_config: Dict[str, Any], target_dir: str = None) -> bool:
        """Deploy CUDA environment based on cuORDER configuration"""
        # Validate configuration
        self.validate_cuorder_config(cuorder_config)

        # Generate temporary config file
        temp_config = self.generate_temp_config(cuorder_config)

        try:
            # Determine output directory - always relative to user's current working directory
            output_dir = cuorder_config['cuda_env']['output_dir']
            if target_dir:
                output_dir = os.path.join(target_dir, output_dir)
            else:
                # Make sure output is relative to user's current working directory
                output_dir = os.path.join(os.getcwd(), output_dir)

            # Execute CUDA resolver
            success = self.execute_cuda_resolver(temp_config, output_dir)

            if success:
                # Ensure docker-entrypoint.sh is copied if Dockerfile references it
                entrypoint_src = self.docker_dir / "docker-entrypoint.sh"
                entrypoint_dst = os.path.join(output_dir, "docker-entrypoint.sh")
                dockerfile_path = os.path.join(output_dir, "Dockerfile.cuda")
                
                # Check if Dockerfile references entrypoint and copy it if missing
                if entrypoint_src.exists() and os.path.exists(dockerfile_path):
                    with open(dockerfile_path, 'r') as f:
                        dockerfile_content = f.read()
                        if 'docker-entrypoint.sh' in dockerfile_content and not os.path.exists(entrypoint_dst):
                            shutil.copy2(entrypoint_src, entrypoint_dst)
                            print(f"📋 Copied docker-entrypoint.sh to output directory")

                print(f"\n✅ CUDA environment deployed to: {output_dir}")
                print("📁 Generated files:")
                for file in os.listdir(output_dir):
                    print(f"   - {file}")

                # Copy cuORDER file for reference
                if 'source_file' in cuorder_config.get('_meta', {}):
                    cuorder_src = cuorder_config['_meta']['source_file']
                    cuorder_dst = os.path.join(output_dir, os.path.basename(cuorder_src))
                    shutil.copy2(cuorder_src, cuorder_dst)
                    print(f"   - {os.path.basename(cuorder_src)} (cuORDER config)")

            return success

        finally:
            # Clean up temporary config
            os.unlink(temp_config)

    def list_available_cuda_versions(self) -> list:
        """List available CUDA versions in compatibility matrix"""
        compat_file = self.config_dir / "cuda_compatibility.json"
        if not compat_file.exists():
            return []

        import json
        with open(compat_file, 'r') as f:
            data = json.load(f)

        return list(data.get('cuda_versions', {}).keys())

    def get_system_info(self) -> Dict[str, Any]:
        """Get current system information"""
        info = {
            'binary_available': self.binary_path.exists(),
            'config_available': self.config_dir.exists(),
            'scripts_available': self.scripts_dir.exists(),
            'docker_available': self.docker_dir.exists(),
            'available_cuda_versions': self.list_available_cuda_versions()
        }
        return info
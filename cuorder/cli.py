#!/usr/bin/env python3
"""
cuORDER CLI for CUDA Environment Resolver
Command-line interface for cuORDER-powered CUDA environment generation
"""

import argparse
import sys
import json
from pathlib import Path
from .engine import CuOrderEngine


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="cuORDER CUDA Environment Resolver - Generate optimized CUDA environments"
    )

    parser.add_argument(
        'cuorder_file',
        nargs='?',
        help='Path to .cuorder configuration file (YAML or JSON)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output directory for generated files (overrides cuORDER config)'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Show system information and available CUDA versions'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate cuORDER file without generating environment'
    )

    args = parser.parse_args()

    try:
        engine = CuOrderEngine()

        if args.info:
            info = engine.get_system_info()
            print("🔍 cuORDER CUDA Environment Resolver")
            print("=" * 40)
            print(f"Binary Available: {'✅' if info['binary_available'] else '❌'}")
            print(f"Config Available: {'✅' if info['config_available'] else '❌'}")
            print(f"Scripts Available: {'✅' if info['scripts_available'] else '❌'}")
            print(f"Docker Available: {'✅' if info['docker_available'] else '❌'}")
            
            if info['docker_available']:
                perm_status = "✅" if info['docker_permission'] else "❌ (Permission Denied)"
                print(f"Docker Permission: {perm_status}")
                print(f"Docker Compose:   {info['compose_cmd']}")
                
                if not info['docker_permission']:
                    print("\n💡 Tip: To fix Docker permissions, run:")
                    print(f"   sudo usermod -aG docker $USER && newgrp docker")
            
            print(f"Available CUDA Versions: {', '.join(info['available_cuda_versions'])}")
            return

        if not args.cuorder_file:
            parser.error("cuorder_file is required unless --info is used")

        # Load and validate cuORDER file
        print(f"📄 Loading cuORDER file: {args.cuorder_file}")
        config = engine.load_cuorder_file(args.cuorder_file)

        # Add metadata about source file
        config.setdefault('_meta', {})['source_file'] = args.cuorder_file

        if args.validate:
            print("🔍 Validating cuORDER configuration...")
            engine.validate_cuorder_config(config)
            print("✅ cuORDER configuration is valid!")
            return

        # Deploy environment
        print("🚀 Deploying CUDA environment via cuORDER...")
        target_dir = args.output if args.output else None

        if engine.deploy_environment(config, target_dir):
            info = engine.get_system_info()
            compose_cmd = info['compose_cmd']
            
            print("\n🎉 Success! Your CUDA environment is ready.")
            print(f"💡 To build and run:")
            print(f"   cd {config['cuda_env']['output_dir']}")
            print(f"   ./build_cuda_env.sh")
            print(f"   {compose_cmd} -f docker-compose.cuda.yml up -d")
            
            if not info['docker_permission']:
                print("\n⚠️ Note: You might need to use 'sudo' or fix Docker permissions via 'newgrp docker'.")
        else:
            print("\n❌ Failed to deploy CUDA environment.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
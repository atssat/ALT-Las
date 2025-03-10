import os
import sys
import shutil
from pathlib import Path
from setuptools import setup, find_packages

def create_directories():
    """Create all required project directories"""
    directories = [
        'modules',
        'ai_models',
        'core',
        'utils',
        'ui',
        'config',
        'tests',
        'logs',
        'macros'
    ]
    
    base_dir = Path(__file__).parent
    for dir_name in directories:
        dir_path = base_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        (dir_path / '__init__.py').touch()

def create_config_files():
    """Create necessary config files"""
    base_dir = Path(__file__).parent
    config_files = {
        '.env': '''# OpenAI
OPENAI_API_KEY=your-openai-key

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Other APIs
COHERE_API_KEY=your-cohere-key
AI21_API_KEY=your-ai21-key
DEEPSEEK_API_KEY=your-deepseek-key
ANTHROPIC_API_KEY=your-anthropic-key''',

        'config/config.json': '''{
    "debug": false,
    "performance_mode": "balanced",
    "log_level": "INFO",
    "cuda_enabled": true
}'''
    }
    
    for filename, content in config_files.items():
        filepath = base_dir / filename
        filepath.parent.mkdir(exist_ok=True)
        filepath.write_text(content)

def setup_environment():
    """Set up Python environment and dependencies"""
    try:
        import pip
        pip.main(['install', '-r', 'requirements.txt'])
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        return False
    return True

def main():
    try:
        print("Setting up ALT-Las project...")
        
        print("Creating directory structure...")
        create_directories()
        
        print("Creating configuration files...")
        create_config_files()
        
        print("Installing dependencies...")
        if not setup_environment():
            return 1
            
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Update API keys in .env file")
        print("2. Configure settings in config/config.json")
        print("3. Run 'python alT_Las.py --debug' to start")
        
        return 0
        
    except Exception as e:
        print(f"\nSetup failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
version = (this_directory / "VERSION").read_text().strip()

setup(
    name="alt-las",
    version=version,
    description="AI-powered debugging and monitoring interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="atssat",
    author_email="ozgurgoca@gmail.com",
    url="https://github.com/atssat/ALT-Las",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in (this_directory / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("-")
    ],
    entry_points={
        "console_scripts": [
            "alt-las=alT_Las:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
)

#!/usr/bin/env python3
"""
Quick Start Script for Azure Toolbox Demo
Helps set up the demo environment with minimal manual configuration.
"""

import os
import sys
import shutil
import subprocess
import asyncio
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          🚀 Azure Toolbox for Smart Agents - Setup          ║
    ║                                                              ║
    ║     Welcome! This script will help you set up the demo      ║
    ║            environment for the Azure AI agent.              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_prerequisites():
    """Check if required tools are installed."""
    print("🔍 Checking prerequisites...")
    
    required_tools = [
        ("python", "Python 3.11+"),
        ("pip", "Python package manager"),
        ("az", "Azure CLI (optional, for deployment)")
    ]
    
    missing_tools = []
    
    for tool, description in required_tools:
        if shutil.which(tool):
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} - Not found")
            missing_tools.append((tool, description))
    
    if missing_tools:
        print(f"\n⚠️  Missing tools detected:")
        for tool, description in missing_tools:
            if tool == "az":
                print(f"  • {description}: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
            elif tool == "python":
                print(f"  • {description}: https://www.python.org/downloads/")
        
        if "python" in [tool for tool, _ in missing_tools]:
            print("\n❌ Python is required. Please install Python 3.11+ and try again.")
            return False
    
    return True

def setup_virtual_environment():
    """Set up Python virtual environment."""
    print("\n🐍 Setting up Python virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("  ✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("  ✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to create virtual environment: {e}")
        return False

def get_activation_command():
    """Get the command to activate virtual environment based on OS."""
    if os.name == 'nt':  # Windows
        return r"venv\Scripts\activate"
    else:  # Unix-like (Linux, macOS)
        return "source venv/bin/activate"

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # Unix-like
        pip_path = Path("venv/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("  ✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Set up environment configuration file."""
    print("\n⚙️  Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example_file = Path(".env.example")
    
    if env_file.exists():
        print("  ✅ .env file already exists")
        return True
    
    if not env_example_file.exists():
        print("  ❌ .env.example file not found")
        return False
    
    try:
        shutil.copy(env_example_file, env_file)
        print("  ✅ Created .env file from template")
        print("  ⚠️  Please edit .env file with your Azure credentials")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create .env file: {e}")
        return False

def display_next_steps():
    """Display next steps for the user."""
    activation_cmd = get_activation_command()
    
    print(f"""
    ✨ Setup completed successfully! 

    📋 Next Steps:
    
    1. 🔑 Configure Azure credentials:
       • Edit the .env file with your Azure service credentials
       • Get credentials from Azure Portal for:
         - Azure OpenAI Service
         - Azure AI Search
         - Azure Storage (optional)
         - Azure Functions (optional)
    
    2. 🧪 Verify setup:
       {activation_cmd}
       python verify_setup.py
    
    3. 🚀 Start the demo:
       python web_interface.py
       
    4. 🌐 Open your browser:
       http://localhost:8000
    
    📚 Additional Resources:
    • README.md - Detailed setup instructions
    • TROUBLESHOOTING.md - Common issues and solutions
    • PRODUCTION_GUIDE.md - Production deployment guide
    
    🎯 Demo Day Tips:
    • Upload sample documents from the sample-documents/ folder
    • Try questions like "What is our AI strategy?" 
    • Demonstrate the function calling capabilities
    
    Happy coding! 🎉
    """)

def main():
    """Main setup function."""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment file", setup_environment_file),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    # Success!
    display_next_steps()

if __name__ == "__main__":
    main()

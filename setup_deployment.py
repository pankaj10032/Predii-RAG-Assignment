#!/usr/bin/env python3
"""
Deployment Setup Script
Automates the setup process for GitHub to Hugging Face Spaces deployment
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return None


def check_git_repo():
    """Check if we're in a git repository"""
    if not Path('.git').exists():
        print("❌ Not in a git repository. Please run 'git init' first.")
        return False
    return True


def setup_git_lfs():
    """Setup Git LFS for large files"""
    print("\n🗂️  Setting up Git LFS...")
    
    # Check if Git LFS is installed
    result = run_command("git lfs version", "Checking Git LFS installation")
    if result is None:
        print("⚠️  Git LFS not installed. Please install it from: https://git-lfs.github.io/")
        return False
    
    # Initialize Git LFS
    run_command("git lfs install", "Initializing Git LFS")
    
    # Track large files
    large_file_patterns = [
        "*.bin",
        "*.sqlite3",
        "*.pickle",
        "*.pdf",
        "chroma_db/**"
    ]
    
    for pattern in large_file_patterns:
        run_command(f'git lfs track "{pattern}"', f"Tracking {pattern} with LFS")
    
    return True


def create_huggingface_readme():
    """Create or update README.md for Hugging Face Spaces"""
    readme_content = '''---
title: Predii RAG Assignment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Ford F-150 Service Manual RAG System
---

# Ford F-150 Service Manual RAG System

A production-ready Retrieval-Augmented Generation (RAG) system for querying Ford F-150 service manual information.

## Features

- **Query Rewriting**: Step-back prompting for better retrieval
- **Hybrid Search**: Dense (vector) + Sparse (BM25) retrieval  
- **Cohere Reranking**: Precision ranking of results
- **Dynamic Chunk Selection**: 1-20 chunks based on query complexity
- **MMR Diversification**: Reduced redundancy in results
- **Faithfulness Evaluation**: Quality assurance using LLM-as-judge
- **Comprehensive Audit Logging**: Track all queries and responses

## Usage

Simply type your question about Ford F-150 suspension and repair procedures in the interface above.

## Technology Stack

- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-large
- **Vector DB**: ChromaDB
- **Reranking**: Cohere rerank-english-v3.0
- **Web Framework**: Gradio

## Development

This application is automatically deployed from GitHub using CI/CD pipeline.

Repository: [RAG-Assignment](https://github.com/your-username/RAG-Assignment)
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created/updated README.md for Hugging Face Spaces")


def verify_requirements():
    """Verify and update requirements.txt"""
    print("\n📦 Checking requirements.txt...")
    
    essential_packages = [
        "gradio>=4.0.0",
        "openai>=1.0.0", 
        "chromadb>=0.4.0",
        "cohere>=4.0.0",
        "rank-bm25>=0.2.2",
        "sentence-transformers>=2.2.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "python-dotenv>=0.19.0"
    ]
    
    if Path('requirements.txt').exists():
        with open('requirements.txt', 'r') as f:
            current_requirements = f.read()
    else:
        current_requirements = ""
    
    # Add missing packages
    missing_packages = []
    for package in essential_packages:
        package_name = package.split('>=')[0].split('==')[0]
        if package_name not in current_requirements:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📝 Adding missing packages: {', '.join(missing_packages)}")
        with open('requirements.txt', 'a') as f:
            if current_requirements and not current_requirements.endswith('\n'):
                f.write('\n')
            for package in missing_packages:
                f.write(f"{package}\n")
    
    print("✅ requirements.txt verified")


def setup_gitignore():
    """Create or update .gitignore"""
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Jupyter
.jupyter/
.ipynb_checkpoints/

# Local development
test_results_*.json
comprehensive_test_results_*.json
audit_logs.jsonl
'''
    
    if not Path('.gitignore').exists():
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")
    else:
        print("✅ .gitignore already exists")


def main():
    """Main setup function"""
    print("🚀 GitHub to Hugging Face Spaces Deployment Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_git_repo():
        sys.exit(1)
    
    try:
        # Setup steps
        setup_gitignore()
        verify_requirements()
        create_huggingface_readme()
        
        # Git LFS setup
        if setup_git_lfs():
            print("✅ Git LFS setup completed")
        else:
            print("⚠️  Git LFS setup skipped (not critical)")
        
        print(f"\n🎯 Setup Complete!")
        print("=" * 30)
        print("✅ All deployment files are ready")
        print("✅ GitHub Actions workflow is configured")
        print("✅ Hugging Face Space configuration created")
        
        print(f"\n📋 Next Steps:")
        print("1. 🔐 Create Hugging Face token (Write permissions)")
        print("   → https://huggingface.co/settings/tokens")
        
        print("2. 🏗️  Create Hugging Face Space:")
        print("   → https://huggingface.co/new-space")
        print("   → Name: pankaj10346/Predii-RAG-Assignment")
        print("   → SDK: Gradio")
        
        print("3. 🔒 Add HF_TOKEN to GitHub Secrets:")
        print("   → Go to your repo → Settings → Secrets and variables → Actions")
        print("   → New repository secret: HF_TOKEN")
        
        print("4. 🚀 Deploy:")
        print("   → git add .")
        print("   → git commit -m 'Setup CI/CD deployment'")
        print("   → git push origin main")
        
        print(f"\n🌐 After deployment, your app will be at:")
        print("   https://pankaj10346-predii-rag-assignment.hf.space")
        
        # Run verification
        print(f"\n🔍 Running deployment verification...")
        try:
            import verify_deployment
            verifier = verify_deployment.DeploymentVerifier()
            verifier.run_all_checks()
        except ImportError:
            print("⚠️  Verification script not found, skipping...")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
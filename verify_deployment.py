#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if the application is ready for deployment to Hugging Face Spaces
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path
import json


class DeploymentVerifier:
    """Verifies deployment readiness"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.total_checks = 0
    
    def check(self, condition, success_msg, error_msg, is_warning=False):
        """Perform a check and record result"""
        self.total_checks += 1
        
        if condition:
            print(f"✅ {success_msg}")
            self.checks_passed += 1
        else:
            if is_warning:
                print(f"⚠️  {error_msg}")
                self.warnings.append(error_msg)
            else:
                print(f"❌ {error_msg}")
                self.errors.append(error_msg)
    
    def verify_file_structure(self):
        """Verify required files and directories exist"""
        print("\n🔍 Checking File Structure...")
        
        # Required files
        required_files = [
            'app.py',
            'requirements.txt',
            'unified_rag_system.py',
            '.github/workflows/deploy.yml'
        ]
        
        for file_path in required_files:
            self.check(
                Path(file_path).exists(),
                f"Required file exists: {file_path}",
                f"Missing required file: {file_path}"
            )
        
        # Required directories
        required_dirs = [
            'preprocessing',
            'retrieval',
            'reranking',
            'utils',
            'chunks',
            'chroma_db'
        ]
        
        for dir_path in required_dirs:
            self.check(
                Path(dir_path).exists() and Path(dir_path).is_dir(),
                f"Required directory exists: {dir_path}",
                f"Missing required directory: {dir_path}"
            )
    
    def verify_python_syntax(self):
        """Verify Python files have valid syntax"""
        print("\n🐍 Checking Python Syntax...")
        
        python_files = [
            'app.py',
            'unified_rag_system.py'
        ]
        
        for file_path in python_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), file_path, 'exec')
                    self.check(
                        True,
                        f"Valid Python syntax: {file_path}",
                        f"Invalid Python syntax: {file_path}"
                    )
                except SyntaxError as e:
                    self.check(
                        False,
                        f"Valid Python syntax: {file_path}",
                        f"Syntax error in {file_path}: {e}"
                    )
    
    def verify_dependencies(self):
        """Verify requirements.txt and dependencies"""
        print("\n📦 Checking Dependencies...")
        
        if Path('requirements.txt').exists():
            with open('requirements.txt', 'r') as f:
                requirements = f.read()
            
            # Check for essential packages
            essential_packages = [
                'gradio',
                'openai',
                'chromadb',
                'huggingface_hub'
            ]
            
            for package in essential_packages:
                self.check(
                    package in requirements.lower(),
                    f"Essential package found: {package}",
                    f"Missing essential package: {package}",
                    is_warning=(package == 'huggingface_hub')
                )
        else:
            self.check(
                False,
                "requirements.txt exists",
                "requirements.txt not found"
            )
    
    def verify_gradio_app(self):
        """Verify Gradio app structure"""
        print("\n🎨 Checking Gradio Application...")
        
        if Path('app.py').exists():
            try:
                with open('app.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for Gradio imports and interface
                self.check(
                    'import gradio' in content or 'from gradio' in content,
                    "Gradio import found in app.py",
                    "No Gradio import found in app.py"
                )
                
                self.check(
                    'gr.Interface' in content or 'gr.Blocks' in content or '.launch()' in content,
                    "Gradio interface/launch found in app.py",
                    "No Gradio interface or launch found in app.py"
                )
                
            except Exception as e:
                self.check(
                    False,
                    "app.py readable",
                    f"Cannot read app.py: {e}"
                )
    
    def verify_environment_config(self):
        """Verify environment configuration"""
        print("\n⚙️  Checking Environment Configuration...")
        
        # Check for .env file (should not be deployed)
        self.check(
            Path('.env').exists(),
            ".env file exists for local development",
            "No .env file found (create for local development)",
            is_warning=True
        )
        
        # Check .gitignore
        if Path('.gitignore').exists():
            with open('.gitignore', 'r') as f:
                gitignore = f.read()
            
            self.check(
                '.env' in gitignore,
                ".env is in .gitignore (good for security)",
                ".env should be in .gitignore for security",
                is_warning=True
            )
        
        # Check GitHub workflow
        workflow_path = Path('.github/workflows/deploy.yml')
        if workflow_path.exists():
            with open(workflow_path, 'r') as f:
                workflow = f.read()
            
            self.check(
                'HF_TOKEN' in workflow,
                "GitHub workflow uses HF_TOKEN",
                "GitHub workflow missing HF_TOKEN reference"
            )
            
            self.check(
                'pankaj10346/Predii-RAG-Assignment' in workflow,
                "Correct Hugging Face space name in workflow",
                "Incorrect or missing Hugging Face space name"
            )
    
    def verify_data_files(self):
        """Verify data files are present"""
        print("\n📊 Checking Data Files...")
        
        # Check chunks directory
        chunks_dir = Path('chunks')
        if chunks_dir.exists():
            chunk_files = list(chunks_dir.glob('*.md'))
            self.check(
                len(chunk_files) > 0,
                f"Document chunks found: {len(chunk_files)} files",
                "No document chunks found in chunks/ directory"
            )
        
        # Check ChromaDB
        chroma_dir = Path('chroma_db')
        if chroma_dir.exists():
            chroma_files = list(chroma_dir.rglob('*'))
            self.check(
                len(chroma_files) > 0,
                f"ChromaDB files found: {len(chroma_files)} files",
                "No ChromaDB files found"
            )
    
    def verify_git_lfs(self):
        """Verify Git LFS configuration"""
        print("\n🗂️  Checking Git LFS Configuration...")
        
        gitattributes_path = Path('.gitattributes')
        self.check(
            gitattributes_path.exists(),
            ".gitattributes file exists for LFS",
            "No .gitattributes file (recommended for large files)",
            is_warning=True
        )
        
        if gitattributes_path.exists():
            with open(gitattributes_path, 'r') as f:
                gitattributes = f.read()
            
            self.check(
                'filter=lfs' in gitattributes,
                "Git LFS configuration found",
                "No Git LFS configuration in .gitattributes",
                is_warning=True
            )
    
    def run_all_checks(self):
        """Run all verification checks"""
        print("🚀 Deployment Readiness Verification")
        print("=" * 50)
        
        self.verify_file_structure()
        self.verify_python_syntax()
        self.verify_dependencies()
        self.verify_gradio_app()
        self.verify_environment_config()
        self.verify_data_files()
        self.verify_git_lfs()
        
        # Summary
        print(f"\n📊 Verification Summary")
        print("=" * 30)
        print(f"✅ Checks Passed: {self.checks_passed}/{self.total_checks}")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ Critical Issues (Must Fix):")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings (Recommended):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        # Final verdict
        print(f"\n🎯 Deployment Readiness:")
        if len(self.errors) == 0:
            print("✅ READY FOR DEPLOYMENT!")
            print("   Your application is ready to deploy to Hugging Face Spaces.")
            print("   Run: git add . && git commit -m 'Deploy to HF' && git push origin main")
            return True
        else:
            print("❌ NOT READY FOR DEPLOYMENT")
            print("   Please fix the critical issues above before deploying.")
            return False


def main():
    """Main verification function"""
    verifier = DeploymentVerifier()
    
    try:
        is_ready = verifier.run_all_checks()
        
        if is_ready:
            print(f"\n🌐 After deployment, your app will be available at:")
            print("   https://huggingface.co/spaces/pankaj10346/Predii-RAG-Assignment")
            print("   https://pankaj10346-predii-rag-assignment.hf.space")
        
        sys.exit(0 if is_ready else 1)
        
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
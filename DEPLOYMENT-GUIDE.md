# CI/CD Deployment Guide: GitHub → Hugging Face Spaces

This guide provides complete instructions for setting up automatic deployment from GitHub to Hugging Face Spaces for your RAG application.

## 📋 Overview

**Deployment Flow:**
```
GitHub Push → GitHub Actions → Hugging Face Spaces → Live Application
```

**What Gets Deployed:**
- Gradio application (`app.py`)
- All Python modules and dependencies
- Document chunks and vector database
- Configuration files
- Requirements and documentation

## 🏗️ Project Structure

Your repository should have this structure:

```
RAG-Assignment/
├── .github/
│   └── workflows/
│       └── deploy.yml              # 🆕 GitHub Actions workflow
├── app.py                          # Main Gradio application
├── requirements.txt                # Python dependencies
├── README.md                       # Will be created/updated for HF
├── preprocessing/                  # Document processing modules
├── retrieval/                      # Retrieval and generation
├── reranking/                      # Reranking and diversification
├── utils/                          # Shared utilities
├── chunks/                         # Document chunks (2916 files)
├── chroma_db/                      # Vector database
├── unified_rag_system.py          # Core RAG system
└── .env                           # Environment variables (not deployed)
```

## 🔐 Step 1: Create Hugging Face Access Token

### 1.1 Generate Token

1. **Go to Hugging Face Settings:**
   - Visit: https://huggingface.co/settings/tokens
   - Log in to your account

2. **Create New Token:**
   - Click "New token"
   - **Name:** `GitHub-Actions-Deploy`
   - **Type:** Select "Write" (required for Spaces)
   - **Scope:** Leave default (full access)

3. **Copy Token:**
   - Copy the generated token immediately
   - **⚠️ Important:** Save it securely - you won't see it again!

### 1.2 Token Format
Your token should look like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 🔒 Step 2: Add Token to GitHub Secrets

### 2.1 Navigate to Repository Settings

1. Go to your GitHub repository
2. Click **Settings** tab
3. In left sidebar, click **Secrets and variables** → **Actions**

### 2.2 Add Secret

1. Click **New repository secret**
2. **Name:** `HF_TOKEN`
3. **Secret:** Paste your Hugging Face token
4. Click **Add secret**

### 2.3 Verify Secret

- You should see `HF_TOKEN` listed in your repository secrets
- The value will be hidden for security

## 🚀 Step 3: Configure Hugging Face Space

### 3.1 Create Space (if not exists)

1. **Go to Hugging Face:**
   - Visit: https://huggingface.co/new-space

2. **Configure Space:**
   - **Owner:** `pankaj10346`
   - **Space name:** `Predii-RAG-Assignment`
   - **License:** MIT
   - **SDK:** Gradio
   - **Visibility:** Public (or Private if preferred)

3. **Create Space:**
   - Click "Create Space"
   - Note the full name: `pankaj10346/Predii-RAG-Assignment`

### 3.2 Space Configuration

The workflow will automatically create/update these files:

**README.md** (Hugging Face Space header):
```yaml
---
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
```

## ⚙️ Step 4: Workflow Configuration

### 4.1 Workflow Features

The `deploy.yml` workflow includes:

- **Trigger:** Automatic on push to `main` branch
- **Smart Filtering:** Ignores documentation-only changes
- **Validation:** Checks Python syntax and required files
- **Authentication:** Secure token handling
- **Error Handling:** Comprehensive error reporting
- **Verification:** Post-deployment checks

### 4.2 Environment Variables

Update these in `.github/workflows/deploy.yml` if needed:

```yaml
env:
  HF_SPACE_NAME: "pankaj10346/Predii-RAG-Assignment"  # Your space
  PYTHON_VERSION: "3.9"                               # Python version
```

### 4.3 Deployment Triggers

**Automatic Triggers:**
- Push to `main` branch
- Changes to application files

**Ignored Files:**
- Documentation files (`README.md`, `ARCHITECTURE.md`)
- Documentation folder (`RAG-Documentation/`)
- Git files (`.gitignore`, `LICENSE`)

**Manual Trigger:**
- Go to Actions tab → Select workflow → "Run workflow"

## 🔧 Step 5: Prepare Your Application

### 5.1 Ensure Required Files

**Check these files exist:**
```bash
# Required files
ls app.py                    # ✅ Main Gradio app
ls requirements.txt          # ✅ Dependencies
ls unified_rag_system.py    # ✅ Core system

# Required directories
ls -d preprocessing/         # ✅ Processing modules
ls -d retrieval/            # ✅ Retrieval modules
ls -d reranking/            # ✅ Reranking modules
ls -d utils/                # ✅ Utilities
ls -d chunks/               # ✅ Document chunks
ls -d chroma_db/            # ✅ Vector database
```

### 5.2 Update requirements.txt

Ensure your `requirements.txt` includes all dependencies:

```txt
gradio>=4.0.0
openai>=1.0.0
chromadb>=0.4.0
cohere>=4.0.0
rank-bm25>=0.2.2
sentence-transformers>=2.2.0
numpy>=1.21.0
pandas>=1.3.0
python-dotenv>=0.19.0
```

### 5.3 Environment Variables

**For Local Development (.env):**
```bash
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
```

**For Hugging Face Spaces:**
- Add these as Space secrets in HF Space settings
- Or modify `app.py` to use Gradio's secret management

## 🚀 Step 6: Deploy Your Application

### 6.1 Initial Deployment

1. **Commit and Push:**
   ```bash
   git add .
   git commit -m "Add CI/CD deployment workflow"
   git push origin main
   ```

2. **Monitor Deployment:**
   - Go to GitHub → Actions tab
   - Watch the "Deploy to Hugging Face Spaces" workflow
   - Check for any errors in the logs

### 6.2 Deployment Process

The workflow will:

1. ✅ **Checkout** your repository
2. ✅ **Setup** Python environment
3. ✅ **Install** dependencies
4. ✅ **Validate** application structure
5. ✅ **Create** HF Space configuration
6. ✅ **Authenticate** with Hugging Face
7. ✅ **Deploy** files to your Space
8. ✅ **Verify** deployment success

### 6.3 Expected Output

**Successful Deployment Log:**
```
🚀 Deploying to Hugging Face Spaces...
📡 Deploying to space: pankaj10346/Predii-RAG-Assignment
✅ Space pankaj10346/Predii-RAG-Assignment exists
📥 Cloning space repository...
📋 Copying files to space...
  ✅ Copied file: app.py
  ✅ Copied file: requirements.txt
  ✅ Copied directory: chunks/
  ✅ Copied directory: chroma_db/
📤 Committing and pushing changes...
✅ Successfully deployed to Hugging Face Spaces!
🌐 Your space is available at: https://huggingface.co/spaces/pankaj10346/Predii-RAG-Assignment
```

## 🌐 Step 7: Access Your Deployed Application

### 7.1 URLs

**Space Page:**
- https://huggingface.co/spaces/pankaj10346/Predii-RAG-Assignment

**Direct App:**
- https://pankaj10346-predii-rag-assignment.hf.space

### 7.2 First Launch

- Initial deployment may take 5-10 minutes
- Hugging Face will install dependencies
- Large files (chunks, vector DB) may take time to sync

## 🔄 How Automatic Redeployment Works

### 7.1 Trigger Conditions

**Automatic Deployment Triggers:**
```bash
# Any push to main branch with relevant changes
git push origin main

# Changes to these files/folders trigger deployment:
- app.py
- requirements.txt
- preprocessing/
- retrieval/
- reranking/
- utils/
- unified_rag_system.py
- chunks/ (if modified)
- chroma_db/ (if modified)
```

**Ignored Changes:**
```bash
# These changes DON'T trigger deployment:
- README.md
- ARCHITECTURE.md
- RAG-Documentation/
- .gitignore
- LICENSE
```

### 7.2 Deployment Flow

1. **Developer pushes code** to `main` branch
2. **GitHub Actions detects** the push
3. **Workflow validates** the changes
4. **Files are synced** to Hugging Face Space
5. **Hugging Face rebuilds** the application
6. **New version goes live** automatically

### 7.3 Deployment Time

- **Code changes:** 2-5 minutes
- **Dependency changes:** 5-10 minutes
- **Large file changes:** 10-20 minutes

## 🛠️ Troubleshooting

### 8.1 Common Issues

#### **Issue: Authentication Failed**
```
❌ Error: HF_TOKEN secret not found
```

**Solution:**
1. Verify `HF_TOKEN` is added to GitHub Secrets
2. Check token has "Write" permissions
3. Regenerate token if expired

#### **Issue: Space Not Found**
```
❌ Space pankaj10346/Predii-RAG-Assignment not found
```

**Solution:**
1. Create the Space manually on Hugging Face
2. Verify the space name in `deploy.yml`
3. Check space visibility (public vs private)

#### **Issue: File Too Large**
```
❌ Error: File size exceeds limit
```

**Solution:**
1. Use Git LFS for large files:
   ```bash
   git lfs track "*.bin"
   git lfs track "chroma_db/**"
   git add .gitattributes
   ```

#### **Issue: Python Syntax Error**
```
❌ Error: app.py syntax is invalid
```

**Solution:**
1. Test locally: `python -m py_compile app.py`
2. Fix syntax errors
3. Commit and push again

#### **Issue: Missing Dependencies**
```
❌ ModuleNotFoundError: No module named 'xyz'
```

**Solution:**
1. Add missing package to `requirements.txt`
2. Test locally: `pip install -r requirements.txt`
3. Commit and push

### 8.2 Debugging Steps

#### **Check Workflow Logs:**
1. Go to GitHub → Actions tab
2. Click on failed workflow run
3. Expand failed step to see error details

#### **Check Hugging Face Logs:**
1. Go to your Space page
2. Click "Logs" tab
3. Look for build/runtime errors

#### **Test Locally:**
```bash
# Test your app locally first
python app.py

# Check dependencies
pip install -r requirements.txt

# Validate Python files
python -m py_compile app.py
```

### 8.3 Manual Deployment

If automatic deployment fails, deploy manually:

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Clone your space
git clone https://huggingface.co/spaces/pankaj10346/Predii-RAG-Assignment
cd Predii-RAG-Assignment

# Copy your files
cp -r /path/to/your/app/* .

# Commit and push
git add .
git commit -m "Manual deployment"
git push
```

## ✅ Final Checklist

### Pre-Deployment Checklist

- [ ] ✅ Hugging Face account created
- [ ] ✅ Hugging Face token generated (Write permissions)
- [ ] ✅ Token added to GitHub Secrets as `HF_TOKEN`
- [ ] ✅ Hugging Face Space created: `pankaj10346/Predii-RAG-Assignment`
- [ ] ✅ `app.py` exists and runs locally
- [ ] ✅ `requirements.txt` includes all dependencies
- [ ] ✅ `.github/workflows/deploy.yml` created
- [ ] ✅ All required directories exist (preprocessing/, retrieval/, etc.)

### Post-Deployment Verification

- [ ] ✅ GitHub Actions workflow completed successfully
- [ ] ✅ No errors in workflow logs
- [ ] ✅ Hugging Face Space shows "Running" status
- [ ] ✅ Application accessible at: https://pankaj10346-predii-rag-assignment.hf.space
- [ ] ✅ All features work correctly in deployed version
- [ ] ✅ Test queries return expected results

### Ongoing Maintenance

- [ ] ✅ Monitor GitHub Actions for failed deployments
- [ ] ✅ Check Hugging Face Space logs for runtime errors
- [ ] ✅ Update dependencies regularly
- [ ] ✅ Test major changes locally before pushing
- [ ] ✅ Keep Hugging Face token secure and rotate periodically

## 🎯 Production Best Practices

### Security
- Never commit API keys or tokens to repository
- Use GitHub Secrets for sensitive data
- Rotate Hugging Face tokens periodically
- Monitor access logs

### Performance
- Optimize file sizes for faster deployment
- Use Git LFS for large binary files
- Cache dependencies when possible
- Monitor Space resource usage

### Reliability
- Test changes locally before pushing
- Use staging branches for major changes
- Monitor deployment success rates
- Have rollback procedures ready

---

**Created:** June 1, 2026  
**For:** RAG Assignment CI/CD Pipeline  
**Space:** https://huggingface.co/spaces/pankaj10346/Predii-RAG-Assignment
# Deployment Guide for Paper2Poster

## 🚀 Deploy Your Paper2Poster Web Application

Your Paper2Poster application can be deployed to the cloud! Here are the best options and setup instructions.

## 📋 Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **OpenAI API Key**: Required for poster generation
3. **Choose a Platform**: Railway (recommended), Render, or Heroku

## 🥇 Option 1: Railway (Recommended)

### Why Railway?
- ✅ **Free tier**: 500 hours/month
- ✅ **FastAPI optimized**
- ✅ **Automatic deployments from GitHub**
- ✅ **Built-in environment variables**
- ✅ **No Docker knowledge required**

### Setup Steps:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/Paper2Poster.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your Paper2Poster repository
   - Railway will auto-detect it's a Python app

3. **Set Environment Variables**:
   - In Railway dashboard → Variables tab
   - Add: `OPENAI_API_KEY=your_api_key_here`
   - Add: `PORT=8000`

4. **Custom Start Command** (if needed):
   - In Railway settings, set start command to:
   ```
   python frontend.py
   ```

## 🥈 Option 2: Render

### Setup Steps:

1. **Push to GitHub** (same as above)

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New Web Service"
   - Connect your GitHub repository

3. **Configure Service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python frontend.py`
   - **Environment**: Python 3

4. **Environment Variables**:
   - Add `OPENAI_API_KEY=your_api_key_here`

## 🥉 Option 3: Heroku

### Setup Steps:

1. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_api_key_here
   git push heroku main
   ```

## 📁 Required Files for Deployment

Your repository needs these files (already created):

1. **requirements.txt** ✅ (already exists)
2. **frontend.py** ✅ (your main app)
3. **Procfile** (for Heroku - will create)
4. **railway.toml** (for Railway - optional)

## 🔧 Production Considerations

### 1. **File Storage**
- **Current**: Local file storage (uploads/, results/)
- **Production**: Consider cloud storage (AWS S3, Cloudinary)
- **Note**: Most platforms have ephemeral file systems

### 2. **Memory Requirements**
- Your CPU-only pipeline is deployment-friendly
- Consider upgrading to paid tiers for better performance

### 3. **API Rate Limits**
- Monitor OpenAI API usage
- Consider implementing rate limiting for users

### 4. **Domain Name**
- Free deployments get random URLs
- Can add custom domain on paid plans

## 🎯 Quick Start Recommendation

**For immediate deployment, I recommend Railway**:

1. It's the easiest for Python FastAPI apps
2. Free tier is generous
3. Automatic GitHub integration
4. No complex configuration needed

Would you like me to help you set up the deployment files and walk through the Railway deployment process?

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Render Python Guide](https://render.com/docs/deploy-fastapi)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

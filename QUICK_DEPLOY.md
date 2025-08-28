# 🚀 Quick Deployment Guide

## Step-by-Step Railway Deployment (Recommended)

### 1. Prepare Your Repository

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit your code
git commit -m "Add Paper2Poster web application"

# Push to GitHub (replace with your username/repo)
git remote add origin https://github.com/YOUR_USERNAME/Paper2Poster.git
git push -u origin main
```

### 2. Deploy on Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your Paper2Poster repository**
6. **Railway will automatically detect it's a Python app**

### 3. Configure Environment Variables

In your Railway project dashboard:
- Go to **Variables** tab
- Add: `OPENAI_API_KEY` = `your_openai_api_key_here`
- Add: `PORT` = `8000` (optional, Railway sets this automatically)

### 4. Deploy!

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run your application using the start command
- Provide you with a public URL

## 🎯 Your App Will Be Live!

After deployment, your Paper2Poster application will be accessible at:
`https://your-app-name.railway.app`

## ✅ What Works in Production

- ✅ **Web interface**: Full drag & drop upload functionality
- ✅ **Real-time progress**: Status updates during poster generation
- ✅ **CPU processing**: No GPU dependencies (deployment-friendly)
- ✅ **File downloads**: Generated posters available as PNG/PPTX
- ✅ **Multi-user**: Each upload gets unique directory
- ✅ **Error handling**: Graceful error messages and logging

## 📊 Cost Estimate

### Railway Free Tier
- **500 execution hours/month** (enough for moderate usage)
- **Automatic sleep** after inactivity
- **No credit card required**

### Usage Calculation
- Each poster generation: ~2-5 minutes
- Approx. 100-250 posters per month on free tier

## 🔄 Continuous Deployment

Once set up, any push to your GitHub main branch will automatically redeploy your application!

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` dependencies
2. **API errors**: Verify `OPENAI_API_KEY` is set correctly
3. **Memory issues**: Consider upgrading to paid tier for heavy usage

### Support Resources:
- Railway Discord: Great community support
- Railway Docs: Comprehensive guides
- GitHub Issues: For app-specific problems

## 🎉 You're Ready to Deploy!

Your Paper2Poster application is production-ready and can serve users worldwide!

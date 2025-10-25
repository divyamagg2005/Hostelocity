# 🚀 Render Deployment Guide for Hostelocity

This guide will help you deploy your Hostel Management System on Render.

---

## 📋 Prerequisites

1. ✅ GitHub account
2. ✅ Render account (free at [render.com](https://render.com))
3. ✅ Supabase database (already configured)
4. ✅ Your code pushed to GitHub

---

## 🔧 Step 1: Push Code to GitHub

Make sure your latest code (including `build.sh`) is pushed to GitHub:

```bash
cd /Users/dakshmanchanda/Desktop/Hostelocity
chmod +x build.sh
git add .
git commit -m "Add Render deployment configuration"
git push origin daksh --force
```

---

## 🗄️ Step 2: Create PostgreSQL Database on Render (Optional)

**Note**: You're already using Supabase, so you can skip this step! Just use your existing Supabase credentials.

If you want to use Render's database instead:
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `hostelocity-db`
   - **Database**: `hostelocity`
   - **User**: `hostelocity_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **"Create Database"**
5. Save the **Internal Database URL** (you'll need this)

---

## 🌐 Step 3: Create Web Service on Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**

### Connect Repository:
3. Click **"Connect Account"** to link your GitHub
4. Find and select your repository: `divyamagg2005/Hostelocity`
5. Click **"Connect"**

### Configure Service:
6. **Name**: `hostelocity` (or your choice)
7. **Region**: Choose closest to your users (e.g., Singapore for India)
8. **Branch**: `daksh`
9. **Root Directory**: (leave blank)
10. **Runtime**: `Python 3`
11. **Build Command**:
```bash
./build.sh
```
12. **Start Command**:
```bash
gunicorn hostel_management.wsgi:application
```

---

## 🔐 Step 4: Configure Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add the following variables:

### Required Variables:

| Key | Value | Example |
|-----|-------|---------|
| `SECRET_KEY` | Your Django secret key | `django-insecure-xyz123...` |
| `DEBUG` | `False` | `False` |
| `PYTHON_VERSION` | `3.11.0` | `3.11.0` |

### Database Variables (Supabase):

| Key | Value | Where to Find |
|-----|-------|---------------|
| `SUPABASE_HOST` | Your Supabase host | Supabase Dashboard → Settings → Database → Host |
| `SUPABASE_DB_NAME` | `postgres` | Default is `postgres` |
| `SUPABASE_USER` | `postgres` | Default is `postgres` |
| `SUPABASE_PASSWORD` | Your database password | Supabase Dashboard → Settings → Database → Password |
| `SUPABASE_PORT` | `5432` | Default port |

### Optional Variables:

| Key | Value | Purpose |
|-----|-------|---------|
| `SUPABASE_URL` | Your Supabase URL | For Supabase client SDK |
| `SUPABASE_KEY` | Your Supabase anon key | For Supabase client SDK |

---

## 🔑 How to Get Supabase Database Credentials:

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project
3. Click **Settings** (gear icon) in left sidebar
4. Click **Database**
5. Scroll down to **Connection Info**
   - **Host**: Copy this to `SUPABASE_HOST`
   - **Database name**: Usually `postgres`
   - **Port**: Usually `5432`
   - **User**: Usually `postgres.xxxxx`
   - **Password**: Click "Reset Database Password" if you forgot it

---

## 🔑 How to Generate a New SECRET_KEY:

Run this in your terminal:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as your `SECRET_KEY`.

---

## 📧 Step 5: Email Configuration (Optional)

If you want email notifications to work, add these variables:

| Key | Value |
|-----|-------|
| `EMAIL_HOST_USER` | `projectsmatter85@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `vips lgkk ypvy uqud` |

**⚠️ Security Note**: Consider using environment variables for email credentials instead of hardcoding them in `settings.py`.

---

## 🚀 Step 6: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application

3. Wait 5-10 minutes for the first deployment

---

## ✅ Step 7: Verify Deployment

Once deployed, Render will give you a URL like:
```
https://hostelocity.onrender.com
```

### Test Your Deployment:

1. **Visit your URL**: Open the provided URL in your browser
2. **Check Login**: Try logging in with your credentials
3. **Test Admin Portal**: Navigate through admin features
4. **Test Student Portal**: Check student dashboard
5. **Verify Database**: Ensure data is displaying correctly

---

## 🔧 Post-Deployment Configuration

### Create Superuser (if needed):

1. Go to Render Dashboard
2. Click on your web service
3. Click **"Shell"** tab
4. Run:
```bash
python manage.py createsuperuser
```

---

## 🎨 Custom Domain (Optional)

To use your own domain:

1. Go to your web service on Render
2. Click **"Settings"**
3. Scroll to **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter your domain (e.g., `hostelocity.com`)
6. Follow DNS configuration instructions

---

## 🔄 Automatic Deploys

Render automatically deploys when you push to your GitHub branch!

```bash
git add .
git commit -m "Update feature"
git push origin daksh
```

Render will detect the push and redeploy automatically.

---

## 📊 Monitoring & Logs

### View Logs:
1. Go to your web service dashboard
2. Click **"Logs"** tab
3. See real-time application logs

### Monitor Performance:
1. Click **"Metrics"** tab
2. View CPU, memory, and request metrics

---

## 🐛 Troubleshooting

### Issue: "Build Failed"
**Solution**: Check build logs for errors. Common fixes:
- Ensure `build.sh` has execute permissions
- Check `requirements.txt` for missing packages

### Issue: "Application Error"
**Solution**: 
- Check logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure database credentials are correct

### Issue: "Static Files Not Loading"
**Solution**:
- Verify `STATIC_ROOT` is set correctly
- Check that `collectstatic` ran successfully
- Ensure WhiteNoise is configured

### Issue: "Database Connection Error"
**Solution**:
- Verify Supabase credentials
- Check if Supabase database is running
- Ensure IP whitelist includes `0.0.0.0/0` in Supabase

### Issue: "502 Bad Gateway"
**Solution**:
- Check if gunicorn is running correctly
- Verify start command is correct
- Check application logs for Python errors

---

## 🔐 Security Checklist

Before going live:

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Email credentials in environment variables
- [ ] Database password is secure
- [ ] HTTPS is enabled (Render provides this automatically)
- [ ] CORS configured if needed
- [ ] Regular database backups enabled

---

## 📱 Render Free Tier Limitations

**Important**: Render free tier services:
- ✅ 750 hours/month (enough for one app)
- ⚠️ **Spin down after 15 minutes of inactivity**
- ⏱️ **First request after inactivity takes ~30-60 seconds** (cold start)
- 💾 Free PostgreSQL: 1GB storage, expires after 90 days

### To Keep Service Always Running:
Upgrade to paid plan ($7/month) for:
- ✅ No spin down
- ✅ Instant response times
- ✅ More resources

---

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations run successfully
- [ ] Static files collected
- [ ] Superuser account created
- [ ] Test login functionality
- [ ] Test all major features
- [ ] Email notifications working
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring enabled
- [ ] Backups configured

---

## 📞 Support

### Render Documentation:
- [Render Docs](https://render.com/docs)
- [Deploy Django Guide](https://render.com/docs/deploy-django)

### Your App Settings:
- **Repository**: `https://github.com/divyamagg2005/Hostelocity`
- **Branch**: `daksh`
- **Python Version**: `3.11.0`
- **Database**: Supabase PostgreSQL

---

## 🎉 Success!

Once deployed, your Hostel Management System will be live and accessible to users worldwide!

**Your App URL**: `https://hostelocity.onrender.com` (or your custom domain)

---

## 📝 Quick Reference Commands

```bash
# Deploy to Render (push to GitHub)
git push origin daksh

# View logs locally
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

---

**Happy Deploying! 🚀**


# 🔐 Using .env File on Render (Secret Files Method)

This guide shows you how to use your `.env` file on Render without manually entering variables.

---

## ✅ **Method: Render Secret Files (RECOMMENDED)**

Render's Secret Files feature lets you upload your `.env` file securely!

---

## 📋 **Step-by-Step Guide:**

### **Step 1: Prepare Your .env File**

Create a `.env` file with all your credentials:

```env
# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=False
PYTHON_VERSION=3.11.0

# Supabase Database
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres.xxxxx
SUPABASE_PASSWORD=your-database-password
SUPABASE_PORT=5432

# Optional: Supabase API
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key

# Optional: Email Configuration
EMAIL_HOST_USER=projectsmatter85@gmail.com
EMAIL_HOST_PASSWORD=vips lgkk ypvy uqud
```

**Save this file locally** (it should already be in your project root, ignored by git)

---

### **Step 2: Copy Your .env File Contents**

Open your `.env` file and **copy everything**.

---

### **Step 3: Add Secret File on Render**

#### **During Initial Setup:**

When creating your web service on Render:

1. Scroll down to the **"Environment"** section
2. Click **"Advanced"**
3. Find **"Secret Files"** section
4. Click **"Add Secret File"**

#### **After Service is Created:**

1. Go to your service dashboard
2. Click **"Environment"** tab in the left sidebar
3. Scroll to **"Secret Files"** section
4. Click **"Add Secret File"**

---

### **Step 4: Configure the Secret File**

Fill in the form:

- **Filename**: `.env`  
  *(exactly like this, with the dot)*

- **Contents**: Paste your entire `.env` file content  
  *(everything you copied in Step 2)*

**Example Screenshot Layout:**
```
┌─────────────────────────────────────┐
│ Add Secret File                     │
├─────────────────────────────────────┤
│ Filename: [.env              ]      │
│                                     │
│ Contents:                           │
│ ┌─────────────────────────────────┐ │
│ │ SECRET_KEY=django-insecure-...  │ │
│ │ DEBUG=False                     │ │
│ │ SUPABASE_HOST=db.xxx.supabase..│ │
│ │ SUPABASE_PASSWORD=...           │ │
│ │ ...                             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Save]                              │
└─────────────────────────────────────┘
```

---

### **Step 5: Save and Deploy**

1. Click **"Save"** or **"Add Secret File"**
2. Render will **automatically redeploy** your service
3. The `.env` file will be created in your project root during deployment
4. Your Django app will load variables from it automatically!

---

## 🔍 **How It Works:**

### **During Deployment:**

1. Render clones your GitHub repo
2. Render creates the `.env` file with your secret contents
3. Your `build.sh` runs: installs packages, collects static files, runs migrations
4. Your app starts with `gunicorn`
5. Django's `python-decouple` reads the `.env` file
6. All environment variables are loaded! ✅

### **File Location:**

```
/opt/render/project/src/
├── .env (created by Render Secret Files)
├── build.sh
├── manage.py
├── requirements.txt
└── hostel_management/
    └── settings.py (reads .env)
```

---

## ✅ **Benefits of Secret Files:**

| Feature | Secret Files | Manual Env Vars | Commit .env |
|---------|-------------|-----------------|-------------|
| **Easy to manage** | ✅ Copy-paste | ❌ One by one | ✅ Easy |
| **Secure** | ✅ Not in git | ✅ Not in git | ❌ In git repo |
| **Easy to update** | ✅ Edit one file | ❌ Update each var | ❌ New commit needed |
| **Private repo only** | ✅ Works anywhere | ✅ Works anywhere | ⚠️ Must be private |
| **Accidental exposure** | ✅ Safe | ✅ Safe | ❌ High risk |

---

## 🎯 **Quick Comparison:**

### **Without Secret Files (Manual):**
```
Add 10+ environment variables one by one:
SECRET_KEY=...     [Add]
DEBUG=False        [Add]
SUPABASE_HOST=...  [Add]
SUPABASE_USER=...  [Add]
... 6 more times
```
**Time**: 5-10 minutes 😓

### **With Secret Files:**
```
1. Copy your .env file
2. Paste into Secret Files
3. Done!
```
**Time**: 30 seconds 🚀

---

## 🔧 **Updating Environment Variables:**

### **To Update Variables:**

1. Go to **Environment** tab
2. Find your `.env` under **Secret Files**
3. Click **Edit** (pencil icon)
4. Update the contents
5. Click **Save**
6. Service auto-redeploys with new values!

---

## 🐛 **Troubleshooting:**

### **Issue: Variables not loading**

**Check:**
1. Filename is exactly `.env` (with the dot)
2. File contents don't have extra spaces or quotes
3. `python-decouple` and `python-dotenv` are in requirements.txt
4. Settings.py has `load_dotenv()` at the top

### **Issue: Secret file not visible after adding**

**Solution:**
- Refresh the page
- Check the "Secret Files" section (not "Environment Variables")
- Service needs to redeploy for changes to take effect

### **Issue: Getting "KeyError" for environment variables**

**Solution:**
- Ensure all required variables are in your `.env` secret file
- Check spelling matches exactly what's in `settings.py`
- Verify `config('VARIABLE_NAME')` has a default value in settings

---

## 📝 **Complete .env Template:**

Use this template for your Secret File:

```env
# ==========================================
# DJANGO CONFIGURATION
# ==========================================
SECRET_KEY=generate-using-python-command
DEBUG=False
PYTHON_VERSION=3.11.0

# ==========================================
# DATABASE (SUPABASE POSTGRESQL)
# ==========================================
SUPABASE_HOST=db.xxxxxxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres.xxxxxxxxxxxxx
SUPABASE_PASSWORD=your-database-password
SUPABASE_PORT=5432

# ==========================================
# SUPABASE API (Optional)
# ==========================================
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your-anon-public-key

# ==========================================
# EMAIL CONFIGURATION (Optional)
# ==========================================
EMAIL_HOST_USER=projectsmatter85@gmail.com
EMAIL_HOST_PASSWORD=vips lgkk ypvy uqud

# ==========================================
# ADDITIONAL SETTINGS (If needed)
# ==========================================
# ALLOWED_HOSTS=hostelocity.onrender.com,yourdomain.com
# CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 🔑 **Generate SECRET_KEY:**

Run this locally to generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `SECRET_KEY` value.

---

## ⚡ **Pro Tips:**

### **1. Keep a Local Copy:**
Keep your `.env` file locally and DON'T commit it to git!

Check your `.gitignore` includes:
```
.env
*.env
.env.*
```

### **2. Use env.example:**
Create a template file `env.example` (without secrets) and commit it:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
SUPABASE_HOST=your-supabase-host
# ... etc
```

This helps team members know what variables are needed!

### **3. Different Environments:**
Use different `.env` files for:
- **Local**: `.env` (with DEBUG=True)
- **Production**: Secret Files on Render (with DEBUG=False)

---

## 📊 **Visual Guide:**

```
YOU (Local)                  GITHUB                    RENDER
  │                            │                         │
  ├─ .env (has secrets)        ├─ .gitignore            ├─ Secret Files
  │  ├─ SECRET_KEY             │  └─ .env               │  └─ .env (uploaded)
  │  ├─ DB_PASSWORD            │                        │     ├─ SECRET_KEY
  │  └─ ...                    ├─ env.example           │     ├─ DB_PASSWORD
  │                            │  └─ (no secrets)       │     └─ ...
  ├─ .gitignore                │                        │
  │  └─ .env                   └─ Code (pushed)         └─ Deployed App ✅
  │                               ├─ manage.py                ├─ .env (created)
  └─ Code (pushed) ──────────▶   ├─ settings.py        ◀─────└─ Reads .env
                                  └─ build.sh
```

---

## ✅ **Verification:**

After deploying, check logs on Render:

```bash
# If .env is loaded correctly, you should see:
✓ Installing dependencies
✓ Collecting static files
✓ Running migrations
✓ Starting gunicorn
```

If you see database connection errors, check your Supabase credentials in the Secret File!

---

## 🎉 **That's It!**

You're now using Render Secret Files to manage your environment variables!

**Benefits:**
- ✅ No manual variable entry
- ✅ Easy to update (edit one file)
- ✅ Secure (not in git)
- ✅ Fast deployment
- ✅ Works exactly like local development

---

**Questions? Check the main deployment guide:** `RENDER_DEPLOYMENT_GUIDE.md`


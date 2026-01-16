@echo off
chcp 65001 >nul
color 0C
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║         📤 رفع المشروع على GitHub - Upload to GitHub     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 هذا الملف سيساعدك في رفع المشروع على GitHub
echo    This file will help you upload the project to GitHub
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Git غير مثبت!
    echo    Error: Git is not installed!
    echo.
    echo 📥 يرجى تحميل Git من:
    echo    Please download Git from:
    echo    https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git مثبت - Git is installed
echo.

REM Check if already initialized
if exist ".git" (
    echo ℹ️  المستودع موجود بالفعل - Repository already exists
    echo.
    goto :update
)

echo 🔧 تهيئة Git - Initializing Git...
echo.

REM Get user info
set /p GIT_NAME="أدخل اسمك - Enter your name: "
set /p GIT_EMAIL="أدخل بريدك - Enter your email: "

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo.
echo ✅ تم تهيئة Git - Git configured
echo.

REM Initialize repository
git init
echo ✅ تم إنشاء المستودع المحلي - Local repository created
echo.

REM Add files
echo 📦 إضافة الملفات - Adding files...
git add DED_Control_Panel_Web.py
git add requirements_web.txt
git add licenses.json
git add .gitignore
git add README_STREAMLIT.md
git add STREAMLIT_CLOUD_DEPLOYMENT.md

echo ✅ تم إضافة الملفات - Files added
echo.

REM Commit
git commit -m "Initial commit - DED Control Panel Web Version"
echo ✅ تم حفظ التغييرات - Changes committed
echo.

REM Get GitHub repo URL
echo ════════════════════════════════════════════════════════════
echo.
echo 📝 الآن اذهب إلى GitHub وأنشئ مستودع جديد:
echo    Now go to GitHub and create a new repository:
echo.
echo    1. اذهب إلى: https://github.com/new
echo       Go to: https://github.com/new
echo.
echo    2. اسم المستودع: DED-Control-Panel
echo       Repository name: DED-Control-Panel
echo.
echo    3. اختر Public أو Private
echo       Choose Public or Private
echo.
echo    4. لا تحدد "Add a README file"
echo       Don't check "Add a README file"
echo.
echo    5. اضغط "Create repository"
echo       Click "Create repository"
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

set /p GITHUB_URL="الصق رابط المستودع - Paste repository URL (https://github.com/username/repo.git): "

git remote add origin %GITHUB_URL%
echo ✅ تم ربط المستودع - Repository linked
echo.

REM Push to GitHub
echo 📤 جاري الرفع على GitHub - Uploading to GitHub...
echo.
echo ⚠️  سيطلب منك اسم المستخدم وكلمة المرور
echo    You will be asked for username and password
echo.
echo 💡 استخدم Personal Access Token بدلاً من كلمة المرور
echo    Use Personal Access Token instead of password
echo.
echo    احصل عليه من: https://github.com/settings/tokens
echo    Get it from: https://github.com/settings/tokens
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ فشل الرفع - Upload failed
    echo.
    echo 💡 تأكد من:
    echo    Make sure:
    echo    1. الرابط صحيح - URL is correct
    echo    2. استخدمت Personal Access Token
    echo       You used Personal Access Token
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo.
echo ✅ تم! المشروع على GitHub الآن!
echo    Done! Project is now on GitHub!
echo.
echo 🌍 الخطوة التالية: النشر على Streamlit Cloud
echo    Next step: Deploy to Streamlit Cloud
echo.
echo    1. اذهب إلى: https://streamlit.io/cloud
echo       Go to: https://streamlit.io/cloud
echo.
echo    2. اضغط "Sign up" → "Continue with GitHub"
echo       Click "Sign up" → "Continue with GitHub"
echo.
echo    3. اضغط "New app"
echo       Click "New app"
echo.
echo    4. اختر المستودع: DED-Control-Panel
echo       Select repository: DED-Control-Panel
echo.
echo    5. الملف: DED_Control_Panel_Web.py
echo       File: DED_Control_Panel_Web.py
echo.
echo    6. اضغط "Deploy!"
echo       Click "Deploy!"
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause
exit /b 0

:update
echo 🔄 تحديث المستودع - Updating repository...
echo.

git add .
git commit -m "Update - %date% %time%"
git push

if errorlevel 1 (
    echo.
    echo ❌ فشل التحديث - Update failed
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ تم التحديث! - Updated!
echo.
pause


# دليل النشر (Deployment Guide)

هذا الدليل يشرح كيفية نشر نظام إدارة المخزون المتكامل على بيئات مختلفة.

## المحتويات
- [النشر المحلي](#النشر-المحلي)
- [النشر باستخدام Docker](#النشر-باستخدام-docker)
- [النشر على خادم Linux](#النشر-على-خادم-linux)
- [النشر على السحابة](#النشر-على-السحابة)

---

## النشر المحلي

### Windows

1. **تثبيت Python 3.8+**
   - حمّل من [python.org](https://www.python.org/downloads/)

2. **تشغيل النظام**
   ```cmd
   start.bat
   ```

### Linux/Mac

1. **تثبيت Python 3.8+**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **تشغيل النظام**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

---

## النشر باستخدام Docker

### المتطلبات
- Docker
- Docker Compose

### الخطوات

1. **بناء الصورة**
   ```bash
   docker-compose build
   ```

2. **تشغيل الحاويات**
   ```bash
   docker-compose up -d
   ```

3. **التحقق من الحالة**
   ```bash
   docker-compose ps
   ```

4. **عرض السجلات**
   ```bash
   docker-compose logs -f
   ```

5. **إيقاف الحاويات**
   ```bash
   docker-compose down
   ```

### استخدام PostgreSQL

لاستخدام PostgreSQL بدلاً من SQLite:

1. فك التعليق عن قسم `db` في `docker-compose.yml`
2. غيّر `DATABASE_URL` في ملف `.env`:
   ```
   DATABASE_URL=postgresql://erp_user:password@db:5432/erp_system
   ```

---

## النشر على خادم Linux

### 1. إعداد الخادم

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات
sudo apt install python3 python3-pip python3-venv nginx supervisor -y

# إنشاء مستخدم للتطبيق
sudo useradd -m -s /bin/bash erpuser
```

### 2. نقل الملفات

```bash
# نسخ الملفات إلى الخادم
scp -r DED/ erpuser@your-server:/home/erpuser/

# أو استخدام git
cd /home/erpuser
git clone <repository-url> DED
cd DED
```

### 3. إعداد البيئة الافتراضية

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. إعداد المتغيرات البيئية

```bash
cp .env.example .env
nano .env
```

غيّر القيم التالية:
```
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
```

### 5. تهيئة قاعدة البيانات

```bash
flask init-db
```

### 6. إعداد Gunicorn

```bash
pip install gunicorn

# اختبار
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 7. إعداد Supervisor

إنشاء ملف `/etc/supervisor/conf.d/erp-system.conf`:

```ini
[program:erp-system]
directory=/home/erpuser/DED
command=/home/erpuser/DED/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app
user=erpuser
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/erp-system/err.log
stdout_logfile=/var/log/erp-system/out.log
```

```bash
# إنشاء مجلد السجلات
sudo mkdir -p /var/log/erp-system
sudo chown erpuser:erpuser /var/log/erp-system

# تحديث Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start erp-system
```

### 8. إعداد Nginx

إنشاء ملف `/etc/nginx/sites-available/erp-system`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/erpuser/DED/app/static;
        expires 30d;
    }

    location /uploads {
        alias /home/erpuser/DED/uploads;
        expires 30d;
    }
}
```

```bash
# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/erp-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. إعداد SSL (اختياري)

```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com
```

---

## النشر على السحابة

### AWS (Amazon Web Services)

#### استخدام EC2

1. **إنشاء EC2 Instance**
   - اختر Ubuntu 22.04 LTS
   - نوع Instance: t2.micro (للبداية)
   - افتح المنافذ: 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **اتبع خطوات النشر على Linux أعلاه**

#### استخدام Elastic Beanstalk

```bash
# تثبيت EB CLI
pip install awsebcli

# تهيئة التطبيق
eb init -p python-3.11 erp-system

# إنشاء بيئة
eb create erp-production

# النشر
eb deploy
```

### Google Cloud Platform

```bash
# تثبيت gcloud CLI
# اتبع التعليمات على: https://cloud.google.com/sdk/docs/install

# تهيئة المشروع
gcloud init

# النشر على App Engine
gcloud app deploy
```

### Heroku

```bash
# تثبيت Heroku CLI
# اتبع التعليمات على: https://devcenter.heroku.com/articles/heroku-cli

# تسجيل الدخول
heroku login

# إنشاء تطبيق
heroku create erp-system-app

# إضافة PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# النشر
git push heroku main

# تهيئة قاعدة البيانات
heroku run flask init-db
```

---

## نصائح الأمان

### 1. تغيير المفاتيح السرية

```python
# توليد مفتاح سري قوي
import secrets
print(secrets.token_hex(32))
```

### 2. استخدام HTTPS

- احصل على شهادة SSL (Let's Encrypt مجاني)
- فعّل HTTPS في Nginx
- اضبط `SESSION_COOKIE_SECURE=True` في `.env`

### 3. تأمين قاعدة البيانات

- استخدم كلمات مرور قوية
- لا تعرض قاعدة البيانات للإنترنت
- خذ نسخ احتياطية منتظمة

### 4. جدار الحماية

```bash
# UFW على Ubuntu
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 5. تحديثات الأمان

```bash
# تحديث النظام بانتظام
sudo apt update && sudo apt upgrade -y
```

---

## النسخ الاحتياطي

### نسخ احتياطي يدوي

```bash
# نسخ قاعدة البيانات
cp erp_system.db backups/erp_system_$(date +%Y%m%d).db

# نسخ الملفات المرفوعة
tar -czf backups/uploads_$(date +%Y%m%d).tar.gz uploads/
```

### نسخ احتياطي تلقائي (Cron)

```bash
# تحرير crontab
crontab -e

# إضافة مهمة يومية في الساعة 2 صباحاً
0 2 * * * /home/erpuser/DED/backup.sh
```

---

## المراقبة

### استخدام Logs

```bash
# سجلات Supervisor
tail -f /var/log/erp-system/out.log

# سجلات Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### استخدام أدوات المراقبة

- **New Relic**: مراقبة الأداء
- **Sentry**: تتبع الأخطاء
- **Datadog**: مراقبة شاملة

---

## استكشاف الأخطاء

### التطبيق لا يعمل

```bash
# تحقق من حالة Supervisor
sudo supervisorctl status erp-system

# أعد تشغيل التطبيق
sudo supervisorctl restart erp-system
```

### خطأ في قاعدة البيانات

```bash
# تحقق من الأذونات
ls -la erp_system.db

# أعد تهيئة قاعدة البيانات
flask init-db
```

### مشاكل Nginx

```bash
# اختبر التكوين
sudo nginx -t

# أعد تشغيل Nginx
sudo systemctl restart nginx
```

---

**للمساعدة:** افتح Issue في المستودع أو راجع التوثيق الكامل.


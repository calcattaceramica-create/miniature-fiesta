# الأوامر المفيدة (Commands Reference)

## 📋 نظرة عامة

هذا الملف يحتوي على جميع الأوامر المفيدة لإدارة وتشغيل النظام.

---

## 🚀 التشغيل

### Windows

```cmd
# التشغيل التلقائي (موصى به)
start.bat

# التشغيل اليدوي
python run.py

# التشغيل مع تحديد المنفذ
python run.py --port 8000

# التشغيل في وضع الإنتاج
set FLASK_ENV=production
python run.py
```

### Linux/Mac

```bash
# التشغيل التلقائي (موصى به)
./start.sh

# التشغيل اليدوي
python3 run.py

# التشغيل مع تحديد المنفذ
python3 run.py --port 8000

# التشغيل في وضع الإنتاج
export FLASK_ENV=production
python3 run.py
```

---

## 🐳 Docker

### بناء وتشغيل

```bash
# بناء الصورة
docker build -t erp-system .

# تشغيل الحاوية
docker run -d -p 5000:5000 --name erp erp-system

# تشغيل مع Docker Compose
docker-compose up -d

# إيقاف الحاويات
docker-compose down

# عرض السجلات
docker-compose logs -f

# إعادة البناء
docker-compose up -d --build
```

### إدارة الحاويات

```bash
# عرض الحاويات النشطة
docker ps

# عرض جميع الحاويات
docker ps -a

# إيقاف حاوية
docker stop erp

# بدء حاوية
docker start erp

# حذف حاوية
docker rm erp

# حذف الصورة
docker rmi erp-system
```

---

## 💾 قاعدة البيانات

### التهيئة

```bash
# إنشاء قاعدة البيانات
flask init-db

# إعادة إنشاء قاعدة البيانات (حذف البيانات!)
rm erp_system.db
flask init-db
```

### النسخ الاحتياطي

```bash
# Windows
copy erp_system.db backups\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db

# Linux/Mac
cp erp_system.db backups/backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump -U username dbname > backup.sql

# MySQL
mysqldump -u username -p dbname > backup.sql
```

### الاستعادة

```bash
# SQLite
cp backups/backup_20260110.db erp_system.db

# PostgreSQL
psql -U username dbname < backup.sql

# MySQL
mysql -u username -p dbname < backup.sql
```

---

## 📦 إدارة المكتبات

### التثبيت

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت متطلبات التطوير
pip install -r requirements-dev.txt

# تثبيت مكتبة محددة
pip install flask-sqlalchemy

# تحديث مكتبة
pip install --upgrade flask

# تحديث جميع المكتبات
pip install --upgrade -r requirements.txt
```

### إدارة البيئة الافتراضية

```bash
# Windows
python -m venv venv
venv\Scripts\activate
deactivate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
deactivate
```

---

## 🧪 الاختبار

### تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل مع التغطية
pytest --cov=app

# تشغيل اختبار محدد
pytest tests/test_models.py

# تشغيل مع عرض التفاصيل
pytest -v

# تشغيل مع إيقاف عند أول خطأ
pytest -x
```

### فحص الكود

```bash
# Flake8 - فحص الأخطاء
flake8 app/

# Black - تنسيق الكود
black app/

# isort - ترتيب الاستيرادات
isort app/

# Bandit - فحص الأمان
bandit -r app/

# Safety - فحص المكتبات
safety check
```

---

## 🔧 التطوير

### Flask CLI

```bash
# تشغيل Shell
flask shell

# تشغيل الخادم
flask run

# تشغيل مع Debug
flask run --debug

# تشغيل على منفذ محدد
flask run --port 8000

# تشغيل على جميع الواجهات
flask run --host 0.0.0.0
```

### إدارة قاعدة البيانات

```bash
# إنشاء Migration
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# التراجع عن Migration
flask db downgrade

# عرض السجل
flask db history

# عرض الحالة الحالية
flask db current
```

---

## 📊 المراقبة

### عرض السجلات

```bash
# عرض السجلات الحية
tail -f logs/app.log

# عرض آخر 100 سطر
tail -n 100 logs/app.log

# البحث في السجلات
grep "ERROR" logs/app.log

# عرض السجلات مع التصفية
tail -f logs/app.log | grep "ERROR"
```

### مراقبة الأداء

```bash
# عرض استخدام الموارد
top

# عرض استخدام الذاكرة
free -h

# عرض استخدام القرص
df -h

# عرض العمليات
ps aux | grep python
```

---

## 🌐 النشر

### Gunicorn

```bash
# تشغيل مع Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# تشغيل في الخلفية
gunicorn -w 4 -b 0.0.0.0:5000 run:app --daemon

# تشغيل مع إعادة التحميل التلقائي
gunicorn -w 4 -b 0.0.0.0:5000 run:app --reload

# إيقاف Gunicorn
pkill gunicorn
```

### Nginx

```bash
# اختبار الإعدادات
sudo nginx -t

# إعادة تحميل الإعدادات
sudo nginx -s reload

# إعادة تشغيل Nginx
sudo systemctl restart nginx

# عرض الحالة
sudo systemctl status nginx
```

### Systemd

```bash
# إنشاء خدمة
sudo nano /etc/systemd/system/erp.service

# تفعيل الخدمة
sudo systemctl enable erp

# بدء الخدمة
sudo systemctl start erp

# إيقاف الخدمة
sudo systemctl stop erp

# إعادة تشغيل الخدمة
sudo systemctl restart erp

# عرض الحالة
sudo systemctl status erp

# عرض السجلات
sudo journalctl -u erp -f
```

---

## 🔐 الأمان

### SSL/TLS

```bash
# توليد شهادة ذاتية التوقيع
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# توليد مفتاح سري
python -c "import secrets; print(secrets.token_hex(32))"
```

### الأذونات

```bash
# تعيين أذونات الملفات
chmod 600 erp_system.db
chmod 644 *.py
chmod 755 start.sh

# تعيين المالك
chown www-data:www-data -R /path/to/app
```

---

## 🛠️ الصيانة

### التنظيف

```bash
# حذف ملفات Python المؤقتة
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# حذف ملفات السجلات القديمة
find logs/ -name "*.log" -mtime +30 -delete

# تنظيف pip cache
pip cache purge
```

### التحديث

```bash
# تحديث من Git
git pull origin main

# تحديث المكتبات
pip install --upgrade -r requirements.txt

# تحديث قاعدة البيانات
flask db upgrade

# إعادة تشغيل الخدمة
sudo systemctl restart erp
```

---

## 📝 Make Commands

```bash
# عرض المساعدة
make help

# التثبيت
make install

# التشغيل
make run

# الاختبار
make test

# فحص الكود
make lint

# التنسيق
make format

# التنظيف
make clean

# النشر
make deploy
```

---

## 🔍 استكشاف الأخطاء

### فحص الاتصال

```bash
# فحص المنفذ
netstat -an | grep 5000

# فحص الخدمة
curl http://localhost:5000

# فحص قاعدة البيانات
sqlite3 erp_system.db ".tables"

# فحص المكتبات
pip list
pip show flask
```

### حل المشاكل

```bash
# إعادة تثبيت المكتبات
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# إعادة إنشاء البيئة الافتراضية
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# إعادة إنشاء قاعدة البيانات
rm erp_system.db
flask init-db
```

---

**للمزيد من المعلومات، راجع التوثيق الكامل!**


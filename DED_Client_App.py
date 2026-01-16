import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="DED - تطبيق العملاء",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# License Manager (same as control panel)
class SimpleLicenseManager:
    def __init__(self, filename='licenses.json'):
        self.filename = filename
        self.licenses = self.load_licenses()
    
    def load_licenses(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def verify_license(self, key, username, password):
        """التحقق من صلاحية الترخيص"""
        if key not in self.licenses:
            return False, "❌ مفتاح الترخيص غير صحيح - Invalid license key"
        
        lic = self.licenses[key]
        
        # التحقق من اسم المستخدم وكلمة المرور
        if lic.get('username') != username or lic.get('password') != password:
            return False, "❌ اسم المستخدم أو كلمة المرور غير صحيحة - Invalid credentials"
        
        # التحقق من تاريخ الانتهاء
        expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
        if expiry_date < datetime.now():
            return False, "❌ الترخيص منتهي الصلاحية - License expired"
        
        return True, lic
    
    def get_license_status(self, lic):
        """الحصول على حالة الترخيص"""
        expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
        days_left = (expiry_date - datetime.now()).days
        
        if days_left > 30:
            return "🟢 نشط - Active", days_left, "#10b981"
        elif days_left > 0:
            return f"🟡 ينتهي قريباً - Expiring Soon", days_left, "#f59e0b"
        else:
            return "🔴 منتهي - Expired", days_left, "#ef4444"

# Initialize manager
manager = SimpleLicenseManager()

# Initialize session state
if 'client_authenticated' not in st.session_state:
    st.session_state.client_authenticated = False
if 'client_license_key' not in st.session_state:
    st.session_state.client_license_key = None
if 'client_license_data' not in st.session_state:
    st.session_state.client_license_data = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
    }
    .main-header p {
        color: #e0e7ff;
        margin: 10px 0 0 0;
        font-size: 1.2em;
    }
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid;
    }
    .feature-card {
        background: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 DED - تطبيق العملاء</h1>
    <p>Client Application - نظام إدارة التراخيص</p>
</div>
""", unsafe_allow_html=True)

# Login Page
if not st.session_state.client_authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 تسجيل الدخول - Client Login")
        st.markdown("---")
        
        with st.form("client_login_form"):
            license_key = st.text_input(
                "🔑 مفتاح الترخيص - License Key:",
                placeholder="أدخل مفتاح الترخيص الخاص بك",
                help="المفتاح الذي حصلت عليه من المسؤول"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                username = st.text_input(
                    "👤 اسم المستخدم - Username:",
                    placeholder="اسم المستخدم"
                )
            with col_b:
                password = st.text_input(
                    "🔒 كلمة المرور - Password:",
                    type="password",
                    placeholder="••••••••"
                )

            submitted = st.form_submit_button("🚀 دخول - Login", use_container_width=True)

            if submitted:
                if license_key and username and password:
                    is_valid, result = manager.verify_license(license_key, username, password)

                    if is_valid:
                        st.session_state.client_authenticated = True
                        st.session_state.client_license_key = license_key
                        st.session_state.client_license_data = result
                        st.success(f"✅ مرحباً {result.get('company')}!")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error("❌ الرجاء إدخال جميع البيانات - Please fill all fields")

        st.markdown("---")
        st.info("""
        **📋 معلومات:**
        - احصل على مفتاح الترخيص من المسؤول
        - استخدم اسم المستخدم وكلمة المرور المقدمة لك
        - تأكد من صلاحية الترخيص قبل الدخول
        """)

    st.stop()

# Client Dashboard
st.markdown("---")

# Logout button
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🚪 تسجيل الخروج - Logout", use_container_width=True):
        st.session_state.client_authenticated = False
        st.session_state.client_license_key = None
        st.session_state.client_license_data = None
        st.rerun()

# Get license data
lic = st.session_state.client_license_data
status, days_left, color = manager.get_license_status(lic)

# Welcome message
st.markdown(f"## 👋 مرحباً، {lic.get('company')}")
st.markdown("---")

# License Status Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: {color};">
        <h3 style="color: {color}; margin: 0;">📊 الحالة</h3>
        <p style="font-size: 1.1em; margin: 10px 0 0 0;">{status}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #3b82f6;">
        <h3 style="color: #3b82f6; margin: 0;">⏳ الأيام المتبقية</h3>
        <p style="font-size: 1.5em; margin: 10px 0 0 0; font-weight: bold;">{days_left}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #8b5cf6;">
        <h3 style="color: #8b5cf6; margin: 0;">📅 تاريخ الانتهاء</h3>
        <p style="font-size: 1.1em; margin: 10px 0 0 0;">{lic.get('expiry')}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #10b981;">
        <h3 style="color: #10b981; margin: 0;">⏱️ المدة الكلية</h3>
        <p style="font-size: 1.5em; margin: 10px 0 0 0; font-weight: bold;">{lic.get('duration_days')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# License Information
st.markdown("### 📋 معلومات الترخيص - License Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="feature-card">
        <h4>🏢 معلومات الشركة - Company Info</h4>
        <p><strong>الشركة:</strong> {lic.get('company')}</p>
        <p><strong>اسم المستخدم:</strong> {lic.get('username')}</p>
        <p><strong>رقم الهاتف:</strong> {lic.get('phone', 'غير محدد')}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="feature-card">
        <h4>🔑 معلومات الترخيص - License Details</h4>
        <p><strong>المفتاح:</strong> <code>{st.session_state.client_license_key}</code></p>
        <p><strong>تاريخ الإنشاء:</strong> {lic.get('created_at')}</p>
        <p><strong>الحالة:</strong> {lic.get('status')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features Section
st.markdown("### ✨ الميزات المتاحة - Available Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 لوحة التحكم</h4>
        <p>عرض جميع معلومات الترخيص والإحصائيات</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🔔 التنبيهات</h4>
        <p>تنبيهات تلقائية عند اقتراب انتهاء الترخيص</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>📞 الدعم الفني</h4>
        <p>دعم فني متواصل طوال فترة الترخيص</p>
    </div>
    """, unsafe_allow_html=True)

# Expiry Warning
if days_left <= 30 and days_left > 0:
    st.warning(f"⚠️ **تنبيه:** الترخيص الخاص بك سينتهي خلال {days_left} يوم. الرجاء التواصل مع المسؤول لتجديد الترخيص.")
elif days_left <= 0:
    st.error("❌ **تنبيه:** الترخيص الخاص بك منتهي الصلاحية. الرجاء التواصل مع المسؤول لتجديد الترخيص.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #64748b;'>
    <p>🚀 <strong>DED Control Panel</strong> - نظام إدارة التراخيص</p>
    <p>Powered by Streamlit | © 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)



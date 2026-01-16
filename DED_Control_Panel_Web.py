import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import secrets
import uuid
import pandas as pd
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="DED Control Panel",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication credentials (في الإنتاج، استخدم قاعدة بيانات)
ADMIN_CREDENTIALS = {
    "admin": "admin123",
    "manager": "manager123"
}

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Simple License Manager
class SimpleLicenseManager:
    def __init__(self):
        self.license_file = Path("demo_licenses.json")
        self.licenses = self.load_licenses()
    
    def load_licenses(self):
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_licenses(self):
        with open(self.license_file, 'w', encoding='utf-8') as f:
            json.dump(self.licenses, f, indent=2, ensure_ascii=False)
    
    def create_license_key(self, company):
        timestamp = datetime.now().isoformat()
        random_part = secrets.token_hex(16)
        data = f"{company}-{timestamp}-{random_part}"
        hash_obj = hashlib.sha256(data.encode())
        return f"DED-{hash_obj.hexdigest()[:32].upper()}"
    
    def create_license(self, company, duration_days=365, username="", password="", phone=""):
        key = self.create_license_key(company)
        expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d")

        license_data = {
            'company': company,
            'username': username,
            'password': password,
            'phone': phone,
            'expiry': expiry,
            'duration_days': duration_days,
            'status': 'active',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.licenses[key] = license_data
        self.save_licenses()
        return key, license_data

    def delete_license(self, key):
        if key in self.licenses:
            del self.licenses[key]
            self.save_licenses()
            return True
        return False

    def update_license(self, key, company=None, duration_days=None, username=None, password=None, phone=None):
        if key in self.licenses:
            if company:
                self.licenses[key]['company'] = company
            if username is not None:
                self.licenses[key]['username'] = username
            if password is not None:
                self.licenses[key]['password'] = password
            if phone is not None:
                self.licenses[key]['phone'] = phone
            if duration_days:
                self.licenses[key]['duration_days'] = duration_days
                expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d")
                self.licenses[key]['expiry'] = expiry
            self.save_licenses()
            return True
        return False

    def export_to_excel(self):
        if not self.licenses:
            return None

        data = []
        for key, lic in self.licenses.items():
            expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
            days_left = (expiry_date - datetime.now()).days

            if days_left > 30:
                status = "نشط"
            elif days_left > 0:
                status = f"ينتهي قريباً ({days_left} يوم)"
            else:
                status = "منتهي"

            data.append({
                'المفتاح': key,
                'الشركة': lic.get('company'),
                'اسم المستخدم': lic.get('username', ''),
                'كلمة المرور': lic.get('password', ''),
                'رقم الهاتف': lic.get('phone', ''),
                'تاريخ الانتهاء': lic.get('expiry'),
                'المدة (أيام)': lic.get('duration_days'),
                'الحالة': status,
                'تاريخ الإنشاء': lic.get('created_at'),
                'الأيام المتبقية': days_left
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='التراخيص')

        return output.getvalue()

# Login Page
if not st.session_state.authenticated:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🔐 تسجيل الدخول - Login</h1>
        <p style='color: #e0e7ff; margin: 10px 0 0 0;'>DED Control Panel</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🔑 الرجاء تسجيل الدخول")

        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم - Username:", placeholder="admin")
            password = st.text_input("🔒 كلمة المرور - Password:", type="password", placeholder="••••••••")

            submitted = st.form_submit_button("🚀 تسجيل الدخول - Login", use_container_width=True)

            if submitted:
                if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"✅ مرحباً {username}!")
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

        st.markdown("---")
        st.info("""
        **🔐 بيانات الدخول التجريبية:**
        - المستخدم: `admin` | كلمة المرور: `admin123`
        - المستخدم: `manager` | كلمة المرور: `manager123`
        """)

    st.stop()

# Initialize manager
manager = SimpleLicenseManager()

# Initialize session state
if 'licenses' not in st.session_state:
    st.session_state.licenses = manager.licenses

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;'>
    <h1 style='color: white; margin: 0;'>🚀 DED Control Panel</h1>
    <p style='color: #e0e7ff; margin: 10px 0 0 0;'>نظام إدارة التراخيص - License Management System</p>
</div>
""", unsafe_allow_html=True)

# User info and logout
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**👤 المستخدم:** {st.session_state.username}")
with col2:
    if st.button("🚪 تسجيل الخروج - Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📋 القائمة - Menu")
    page = st.radio(
        "اختر الصفحة - Select Page:",
        ["📝 إنشاء ترخيص - Create License", "📊 عرض التراخيص - View Licenses"],
        label_visibility="collapsed"
    )

# Create License Page
if page == "📝 إنشاء ترخيص - Create License":
    st.markdown("### 📝 إنشاء ترخيص جديد - Create New License")

    with st.form("create_license_form"):
        company = st.text_input("🏢 اسم الشركة - Company Name:", placeholder="مثال: شركة التقنية المتقدمة")

        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("👤 اسم المستخدم - Username:", placeholder="مثال: company_admin")
            phone = st.text_input("📱 رقم الهاتف - Phone:", placeholder="مثال: +966501234567")
        with col2:
            password = st.text_input("🔒 كلمة المرور - Password:", type="password", placeholder="••••••••")
            duration = st.number_input("⏱️ مدة الترخيص (أيام) - Duration (days):", min_value=1, value=365)

        submitted = st.form_submit_button("✨ إنشاء الترخيص - Create License", use_container_width=True)

        if submitted:
            if company and username and password:
                key, data = manager.create_license(company, duration, username, password, phone)
                st.session_state.licenses = manager.licenses

                st.success("✅ تم إنشاء الترخيص بنجاح! - License created successfully!")

                st.markdown("#### 🔑 معلومات الترخيص - License Information")
                st.code(key, language="text")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**🏢 الشركة:** {data['company']}")
                    st.info(f"**👤 المستخدم:** {data['username']}")
                with col2:
                    st.info(f"**🔒 كلمة المرور:** {data['password']}")
                    st.info(f"**📱 الهاتف:** {data['phone']}")
                with col3:
                    st.info(f"**⏱️ المدة:** {data['duration_days']} يوم")
                    st.info(f"**📅 الانتهاء:** {data['expiry']}")
            else:
                st.error("❌ الرجاء إدخال جميع الحقول المطلوبة (الشركة، المستخدم، كلمة المرور)")

# View Licenses Page
else:
    st.markdown("### 📊 عرض التراخيص - View Licenses")

    if st.session_state.licenses:
        # Statistics
        col1, col2, col3 = st.columns(3)

        active_count = 0
        expiring_count = 0
        expired_count = 0

        for key, lic in st.session_state.licenses.items():
            expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
            days_left = (expiry_date - datetime.now()).days

            if days_left > 30:
                active_count += 1
            elif days_left > 0:
                expiring_count += 1
            else:
                expired_count += 1

        with col1:
            st.metric("🟢 نشط", active_count)
        with col2:
            st.metric("🟡 ينتهي قريباً", expiring_count)
        with col3:
            st.metric("🔴 منتهي", expired_count)

        st.markdown("---")

        # Export button
        excel_data = manager.export_to_excel()
        if excel_data:
            st.download_button(
                label="📥 تصدير إلى Excel - Export to Excel",
                data=excel_data,
                file_name=f"licenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.markdown("---")

        # Search
        search_term = st.text_input("🔍 البحث - Search:", placeholder="ابحث عن شركة أو مفتاح...")

        # Filter licenses
        filtered_licenses = {}
        for key, lic in st.session_state.licenses.items():
            if search_term.lower() in lic.get('company', '').lower() or search_term.lower() in key.lower():
                filtered_licenses[key] = lic

        if not search_term:
            filtered_licenses = st.session_state.licenses

        st.markdown(f"**عدد التراخيص - Total Licenses:** {len(filtered_licenses)}")

        for key, lic in filtered_licenses.items():
            expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
            days_left = (expiry_date - datetime.now()).days

            if days_left > 30:
                status = "🟢 نشط - Active"
                status_color = "#10b981"
            elif days_left > 0:
                status = f"🟡 ينتهي قريباً ({days_left} يوم) - Expiring Soon"
                status_color = "#f59e0b"
            else:
                status = "🔴 منتهي - Expired"
                status_color = "#ef4444"

            with st.expander(f"**{lic.get('company')}** - {status}"):
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid {status_color};'>
                    <p><strong>🔑 المفتاح - Key:</strong><br/><code>{key}</code></p>
                    <p><strong>🏢 الشركة - Company:</strong> {lic.get('company')}</p>
                    <p><strong>👤 اسم المستخدم - Username:</strong> {lic.get('username', 'غير محدد')}</p>
                    <p><strong>🔒 كلمة المرور - Password:</strong> {lic.get('password', 'غير محدد')}</p>
                    <p><strong>📱 رقم الهاتف - Phone:</strong> {lic.get('phone', 'غير محدد')}</p>
                    <p><strong>📅 تاريخ الانتهاء - Expiry:</strong> {lic.get('expiry')}</p>
                    <p><strong>⏱️ المدة - Duration:</strong> {lic.get('duration_days')} يوم</p>
                    <p><strong>📊 الحالة - Status:</strong> {status}</p>
                    <p><strong>📅 تاريخ الإنشاء - Created:</strong> {lic.get('created_at')}</p>
                    <p><strong>⏳ الأيام المتبقية - Days Left:</strong> {days_left} يوم</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"✏️ تعديل - Edit", key=f"edit_{key}", use_container_width=True):
                        st.session_state[f'editing_{key}'] = True
                        st.rerun()

                with col2:
                    if st.button(f"🗑️ حذف - Delete", key=f"delete_{key}", use_container_width=True, type="secondary"):
                        if manager.delete_license(key):
                            st.session_state.licenses = manager.licenses
                            st.success(f"✅ تم حذف الترخيص - License deleted")
                            st.rerun()

                # Edit form
                if st.session_state.get(f'editing_{key}', False):
                    st.markdown("---")
                    st.markdown("#### ✏️ تعديل الترخيص - Edit License")

                    with st.form(f"edit_form_{key}"):
                        new_company = st.text_input("🏢 اسم الشركة:", value=lic.get('company'))

                        col1, col2 = st.columns(2)
                        with col1:
                            new_username = st.text_input("👤 اسم المستخدم:", value=lic.get('username', ''))
                            new_phone = st.text_input("📱 رقم الهاتف:", value=lic.get('phone', ''))
                        with col2:
                            new_password = st.text_input("🔒 كلمة المرور:", value=lic.get('password', ''))
                            new_duration = st.number_input("⏱️ المدة (أيام):", min_value=1, value=lic.get('duration_days'))

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 حفظ - Save", use_container_width=True):
                                if manager.update_license(key, new_company, new_duration, new_username, new_password, new_phone):
                                    st.session_state.licenses = manager.licenses
                                    st.session_state[f'editing_{key}'] = False
                                    st.success("✅ تم تحديث الترخيص - License updated")
                                    st.rerun()

                        with col2:
                            if st.form_submit_button("❌ إلغاء - Cancel", use_container_width=True):
                                st.session_state[f'editing_{key}'] = False
                                st.rerun()
    else:
        st.info("لا توجد تراخيص - No licenses found")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p>🚀 DED Control Panel - Demo Version</p>
    <p>Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)


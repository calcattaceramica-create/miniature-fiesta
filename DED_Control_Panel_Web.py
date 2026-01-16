import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import secrets
import uuid

# Page configuration
st.set_page_config(
    page_title="DED Control Panel - Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo mode warning
st.warning("⚠️ **وضع العرض التجريبي - Demo Mode**: هذه نسخة تجريبية للعرض فقط. للاستخدام الكامل، قم بتشغيل التطبيق محلياً.")

# Custom CSS for modern design
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .success-button {
        background-color: #22c55e;
        color: white;
    }
    .danger-button {
        background-color: #ef4444;
        color: white;
    }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    h1 {
        color: #1e293b;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'licenses' not in st.session_state:
    st.session_state.licenses = {}
if 'app_running' not in st.session_state:
    st.session_state.app_running = False
if 'flask_process' not in st.session_state:
    st.session_state.flask_process = None

# Helper Functions
class LicenseManager:
    def __init__(self):
        self.app_dir = Path.cwd()
        self.license_file = self.app_dir / "licenses.json"
        self.db_path = self.app_dir / "erp_system.db"
        
    def load_licenses(self):
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_licenses(self, licenses):
        with open(self.license_file, 'w', encoding='utf-8') as f:
            json.dump(licenses, f, indent=2, ensure_ascii=False)
    
    def get_machine_id(self):
        # Demo mode - return a fixed ID
        return "DEMO-" + str(uuid.uuid4())[:8]
    
    def create_license_key(self, company, machine_id=""):
        timestamp = datetime.now().isoformat()
        random_part = secrets.token_hex(16)
        data = f"{company}-{machine_id}-{timestamp}-{random_part}"
        hash_obj = hashlib.sha256(data.encode())
        full_key = hash_obj.hexdigest()[:32].upper()
        formatted_key = '-'.join([full_key[i:i+4] for i in range(0, 32, 4)])
        return formatted_key
    
    def generate_license(self, company, duration, username, password, email, phone, max_users, notes):
        try:
            days = int(duration)
            max_users_int = int(max_users)
        except:
            return None, "Invalid duration or max users number"
        
        machine_id = self.get_machine_id()
        key = self.create_license_key(company, machine_id)
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        license_data = {
            'company': company,
            'expiry': expiry,
            'created': created_date,
            'duration_days': days,
            'machine_id': machine_id,
            'license_type': 'Standard',
            'max_users': max_users_int,
            'features': ['all'],
            'status': 'active',
            'activation_count': 0,
            'last_check': None,
            'username': username,
            'password': password,
            'contact_email': email,
            'contact_phone': phone,
            'notes': notes
        }
        
        return key, license_data

    def sync_to_database(self, license_key, license_data):
        # Demo mode - database operations disabled
        return False, "⚠️ Database operations are disabled in demo mode"

# Initialize manager
manager = LicenseManager()

# Load licenses
st.session_state.licenses = manager.load_licenses()

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>🚀 DED Control Panel</h1>
    <p style='color: white; margin: 5px 0 0 0; opacity: 0.9;'>لوحة التحكم الشاملة - نظام إدارة متكامل وسهل الاستخدام</p>
</div>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2 = st.tabs(["🔐 مدير التراخيص - License Manager", "⚙️ تشغيل التطبيق - App Control"])

# Tab 1: License Manager
with tab1:
    st.markdown("### ➕ إضافة ترخيص جديد - Add New License")

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("🏢 اسم الشركة - Company:", key="company")
        username = st.text_input("👤 اسم المستخدم - Username:", key="username")
        email = st.text_input("📧 البريد الإلكتروني - Email:", key="email")
        max_users = st.number_input("👥 عدد المستخدمين - Max Users:", min_value=1, value=10, key="max_users")

    with col2:
        duration = st.number_input("⏱️ المدة (أيام) - Duration:", min_value=1, value=365, key="duration")
        password = st.text_input("🔑 كلمة المرور - Password:", type="password", key="password")
        phone = st.text_input("📱 رقم الهاتف - Phone:", key="phone")
        notes = st.text_area("📝 ملاحظات - Notes:", key="notes")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:
        if st.button("✅ إنشاء الترخيص - Generate License", type="primary", use_container_width=True):
            if not company:
                st.error("❌ الرجاء إدخال اسم الشركة! - Please enter company name!")
            elif not username:
                st.error("❌ الرجاء إدخال اسم المستخدم! - Please enter username!")
            elif not password:
                st.error("❌ الرجاء إدخال كلمة المرور! - Please enter password!")
            else:
                key, license_data = manager.generate_license(
                    company, duration, username, password, email, phone, max_users, notes
                )
                if key:
                    st.session_state.licenses[key] = license_data
                    manager.save_licenses(st.session_state.licenses)
                    success, msg = manager.sync_to_database(key, license_data)
                    st.success(f"✅ تم إنشاء الترخيص بنجاح! - License created successfully!\n\n🔑 المفتاح: {key}")
                    st.balloons()
                else:
                    st.error(f"❌ خطأ: {license_data}")

    with col_btn2:
        if st.button("🗑️ مسح النموذج - Clear Form", use_container_width=True):
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 التراخيص المسجلة - Registered Licenses")

    if st.session_state.licenses:
        # Statistics
        total = len(st.session_state.licenses)
        active = sum(1 for lic in st.session_state.licenses.values() if lic.get('status') == 'active')
        expired = sum(1 for lic in st.session_state.licenses.values()
                     if datetime.strptime(lic.get('expiry'), "%Y-%m-%d") < datetime.now())

        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("📊 إجمالي التراخيص - Total", total)
        with stat_col2:
            st.metric("✅ نشط - Active", active)
        with stat_col3:
            st.metric("⚠️ منتهي - Expired", expired)

        # Create DataFrame
        data = []
        for key, lic in st.session_state.licenses.items():
            expiry_date = datetime.strptime(lic.get('expiry'), "%Y-%m-%d")
            status = "⚠️ منتهي" if expiry_date < datetime.now() else "✅ نشط"

            data.append({
                "الشركة - Company": lic.get('company'),
                "المستخدم - Username": lic.get('username'),
                "الانتهاء - Expiry": lic.get('expiry'),
                "الحالة - Status": status,
                "المفتاح - Key": key[:20] + "..."
            })

        # Display as table without pandas
        if data:
            st.table(data)
        else:
            st.info("لا توجد تراخيص - No licenses found")

        # License actions
        st.markdown("#### 🔧 إجراءات - Actions")

        selected_company = st.selectbox(
            "اختر شركة - Select Company:",
            options=[""] + [lic.get('company') for lic in st.session_state.licenses.values()]
        )

        if selected_company:
            # Find license
            selected_key = None
            selected_data = None
            for key, data in st.session_state.licenses.items():
                if data.get('company') == selected_company:
                    selected_key = key
                    selected_data = data
                    break

            if selected_key:
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)

                with action_col1:
                    if st.button("📋 نسخ المفتاح - Copy Key", use_container_width=True):
                        st.code(selected_key, language=None)
                        st.success("✅ المفتاح معروض أعلاه - Key displayed above")

                with action_col2:
                    if st.button("👁️ عرض التفاصيل - View Details", use_container_width=True):
                        st.json(selected_data)

                with action_col3:
                    if st.button("⏸️ تعليق - Suspend", use_container_width=True):
                        st.session_state.licenses[selected_key]['status'] = 'suspended'
                        manager.save_licenses(st.session_state.licenses)
                        st.success("✅ تم تعليق الترخيص - License suspended")
                        st.rerun()

                with action_col4:
                    if st.button("🗑️ حذف - Delete", use_container_width=True):
                        del st.session_state.licenses[selected_key]
                        manager.save_licenses(st.session_state.licenses)
                        st.success("✅ تم حذف الترخيص - License deleted")
                        st.rerun()
    else:
        st.info("📭 لا توجد تراخيص مسجلة - No licenses registered")

# Tab 2: App Control
with tab2:
    st.markdown("### ⚙️ التحكم في التطبيق - Application Control")

    # Status display
    status_col1, status_col2 = st.columns([1, 2])

    with status_col1:
        if st.session_state.app_running:
            st.success("✅ التطبيق يعمل - App Running")
        else:
            st.error("⭕ التطبيق متوقف - App Stopped")

    with status_col2:
        if st.session_state.app_running:
            st.info("🌐 URL: http://127.0.0.1:5000")

    # Control buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("▶️ تشغيل التطبيق - Start App", type="primary", use_container_width=True, disabled=True):
            st.warning("⚠️ App control is disabled in demo mode")

    with btn_col2:
        if st.button("⏹️ إيقاف التطبيق - Stop App", use_container_width=True, disabled=True):
            st.warning("⚠️ App control is disabled in demo mode")

    with btn_col3:
        if st.button("🌐 فتح في المتصفح - Open Browser", use_container_width=True, disabled=True):
            st.warning("⚠️ App control is disabled in demo mode")

    st.markdown("---")

    # Migration section
    st.markdown("### 🔄 تطبيق Migration - Apply Migration")
    st.info("⚠️ Migration is disabled in demo mode")

    if st.button("🔄 تطبيق Migration", use_container_width=True, disabled=True):
        st.warning("⚠️ Migration is disabled in demo mode")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p>🚀 DED Control Panel - Web Version</p>
    <p>Powered by Streamlit | Made with ❤️</p>
</div>
""", unsafe_allow_html=True)


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
st.warning("⚠️ **وضع العرض التجريبي - Demo Mode**: هذه نسخة تجريبية للعرض فقط.")

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
    
    def create_license(self, company, duration_days=365):
        key = self.create_license_key(company)
        expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d")
        
        license_data = {
            'company': company,
            'expiry': expiry,
            'duration_days': duration_days,
            'status': 'active',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.licenses[key] = license_data
        self.save_licenses()
        return key, license_data

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
        company = st.text_input("اسم الشركة - Company Name:", placeholder="مثال: شركة التقنية المتقدمة")
        duration = st.number_input("مدة الترخيص (أيام) - Duration (days):", min_value=1, value=365)
        
        submitted = st.form_submit_button("✨ إنشاء الترخيص - Create License", use_container_width=True)
        
        if submitted:
            if company:
                key, data = manager.create_license(company, duration)
                st.session_state.licenses = manager.licenses
                
                st.success("✅ تم إنشاء الترخيص بنجاح! - License created successfully!")
                
                st.markdown("#### 🔑 معلومات الترخيص - License Information")
                st.code(key, language="text")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**الشركة - Company:** {data['company']}")
                    st.info(f"**المدة - Duration:** {data['duration_days']} يوم")
                with col2:
                    st.info(f"**تاريخ الانتهاء - Expiry:** {data['expiry']}")
                    st.info(f"**الحالة - Status:** {data['status']}")
            else:
                st.error("❌ الرجاء إدخال اسم الشركة - Please enter company name")

# View Licenses Page
else:
    st.markdown("### 📊 عرض التراخيص - View Licenses")
    
    if st.session_state.licenses:
        st.markdown(f"**عدد التراخيص - Total Licenses:** {len(st.session_state.licenses)}")
        
        for key, lic in st.session_state.licenses.items():
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
                    <p><strong>📅 تاريخ الانتهاء - Expiry:</strong> {lic.get('expiry')}</p>
                    <p><strong>⏱️ المدة - Duration:</strong> {lic.get('duration_days')} يوم</p>
                    <p><strong>📊 الحالة - Status:</strong> {status}</p>
                </div>
                """, unsafe_allow_html=True)
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


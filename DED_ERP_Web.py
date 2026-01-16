"""
DED ERP System - Web Version
نظام تخطيط موارد المؤسسات - نسخة الويب
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import hashlib
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="DED ERP System - نظام تخطيط موارد المؤسسات",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple JSON-based data storage
DATA_FILE = "erp_data.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass

    # Default data
    return {
        "users": {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "full_name": "مدير النظام",
                "role": "admin"
            }
        },
        "products": [],
        "customers": [],
        "suppliers": [],
        "sales_invoices": [],
        "purchase_invoices": []
    }

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# Authentication
def check_password(username, password):
    """Check user credentials"""
    data = load_data()

    if username in data["users"]:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return data["users"][username]["password"] == password_hash

    return False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Login page
def login_page():
    """Display login page"""
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h1 style='color: #667eea; font-size: 48px;'>🚀</h1>
            <h1 style='color: #667eea;'>نظام DED ERP</h1>
            <p style='color: #666; font-size: 18px;'>نظام تخطيط موارد المؤسسات المتكامل</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 تسجيل الدخول")
            
            username = st.text_input("👤 اسم المستخدم", placeholder="admin")
            password = st.text_input("🔒 كلمة المرور", type="password", placeholder="admin123")
            
            submit = st.form_submit_button("دخول", use_container_width=True)
            
            if submit:
                if username and password:
                    if check_password(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("✅ تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    st.warning("⚠️ يرجى إدخال اسم المستخدم وكلمة المرور")
        
        st.info("""
            **💡 بيانات الدخول الافتراضية:**
            - المستخدم: `admin`
            - كلمة المرور: `admin123`
        """)

# Dashboard
def dashboard_page():
    """Display dashboard"""
    st.title("📊 لوحة التحكم - Dashboard")

    data = load_data()

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📦 المنتجات", len(data.get("products", [])))

    with col2:
        st.metric("👥 العملاء", len(data.get("customers", [])))

    with col3:
        st.metric("🏭 الموردين", len(data.get("suppliers", [])))

    with col4:
        st.metric("🧾 فواتير المبيعات", len(data.get("sales_invoices", [])))

    st.divider()

    # Quick actions
    st.subheader("⚡ إجراءات سريعة")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ إضافة منتج جديد", use_container_width=True):
            st.info("🚧 قيد التطوير...")

    with col2:
        if st.button("➕ إضافة عميل جديد", use_container_width=True):
            st.info("🚧 قيد التطوير...")

    with col3:
        if st.button("➕ فاتورة مبيعات جديدة", use_container_width=True):
            st.info("🚧 قيد التطوير...")

    st.divider()

    # Recent activity
    st.subheader("📋 النشاط الأخير")
    st.info("لا توجد أنشطة حديثة")

    st.success("✅ النظام يعمل بشكل صحيح!")

# Main app
def main():
    """Main application"""
    
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.title("🚀 DED ERP")
        st.write(f"👤 {st.session_state.username}")
        
        st.divider()
        
        menu = st.radio(
            "القائمة الرئيسية",
            ["📊 لوحة التحكم", "📦 المخزون", "🧾 المبيعات", "📄 المشتريات", 
             "👥 العملاء", "🏭 الموردين", "📊 التقارير", "⚙️ الإعدادات"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Main content
    if menu == "📊 لوحة التحكم":
        dashboard_page()

    elif menu == "📦 المخزون":
        st.title("📦 إدارة المخزون")

        tab1, tab2, tab3 = st.tabs(["المنتجات", "التصنيفات", "المستودعات"])

        with tab1:
            st.subheader("قائمة المنتجات")
            data = load_data()

            if data.get("products"):
                df = pd.DataFrame(data["products"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("لا توجد منتجات. ابدأ بإضافة منتج جديد!")

            if st.button("➕ إضافة منتج"):
                st.info("🚧 قيد التطوير...")

        with tab2:
            st.info("🚧 قسم التصنيفات قيد التطوير...")

        with tab3:
            st.info("🚧 قسم المستودعات قيد التطوير...")

    elif menu == "👥 العملاء":
        st.title("👥 إدارة العملاء")

        data = load_data()

        if data.get("customers"):
            df = pd.DataFrame(data["customers"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا يوجد عملاء. ابدأ بإضافة عميل جديد!")

        if st.button("➕ إضافة عميل"):
            st.info("🚧 قيد التطوير...")

    elif menu == "🏭 الموردين":
        st.title("🏭 إدارة الموردين")

        data = load_data()

        if data.get("suppliers"):
            df = pd.DataFrame(data["suppliers"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا يوجد موردين. ابدأ بإضافة مورد جديد!")

        if st.button("➕ إضافة مورد"):
            st.info("🚧 قيد التطوير...")

    else:
        st.title(menu)
        st.info(f"🚧 قسم {menu} قيد التطوير...")
        st.write("هذا القسم سيتم إضافته قريباً!")

if __name__ == "__main__":
    main()


"""
DED ERP System - Web Version
نظام تخطيط موارد المؤسسات - نسخة الويب
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import hashlib
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="DED ERP System - نظام تخطيط موارد المؤسسات",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
def get_db_connection():
    """Get database connection"""
    db_path = Path("erp_system.db")
    if not db_path.exists():
        st.error("⚠️ قاعدة البيانات غير موجودة! يرجى تشغيل: python init_database.py")
        return None
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

# Authentication
def check_password(username, password):
    """Check user credentials"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check user
        cursor.execute("""
            SELECT id, username, is_active 
            FROM user 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        """, (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        return user is not None
    except Exception as e:
        st.error(f"خطأ في التحقق: {str(e)}")
        conn.close()
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
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Get statistics
        cursor = conn.cursor()
        
        # Products count
        cursor.execute("SELECT COUNT(*) as count FROM product")
        products_count = cursor.fetchone()['count']
        
        # Customers count
        cursor.execute("SELECT COUNT(*) as count FROM customer")
        customers_count = cursor.fetchone()['count']
        
        # Suppliers count
        cursor.execute("SELECT COUNT(*) as count FROM supplier")
        suppliers_count = cursor.fetchone()['count']
        
        # Sales invoices count
        cursor.execute("SELECT COUNT(*) as count FROM sales_invoice")
        sales_count = cursor.fetchone()['count']
        
        conn.close()
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 المنتجات", products_count)
        
        with col2:
            st.metric("👥 العملاء", customers_count)
        
        with col3:
            st.metric("🏭 الموردين", suppliers_count)
        
        with col4:
            st.metric("🧾 فواتير المبيعات", sales_count)
        
        st.success("✅ النظام يعمل بشكل صحيح!")
        
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")
        conn.close()

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
    else:
        st.title(menu)
        st.info(f"🚧 قسم {menu} قيد التطوير...")
        st.write("هذا القسم سيتم إضافته قريباً!")

if __name__ == "__main__":
    main()


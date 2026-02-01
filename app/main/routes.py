from flask import render_template, redirect, url_for, flash, request, make_response, after_this_request
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app.auth.decorators import permission_required
from app.main import bp
from app import db, csrf
from app.models import *
from app.models_license import License
from app.license_manager import LicenseManager
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar
import json
import traceback
from pathlib import Path
import uuid

@bp.after_request
def add_cache_headers(response):
    """Add cache-busting headers to all responses to prevent tenant data caching"""
    if not response.cache_control.no_cache:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

@bp.route('/')
@bp.route('/index')
@login_required
# Temporarily disable permission check for debugging on Render
# @permission_required('dashboard.view')
def index():
    """Dashboard - Main page"""

    # Simple test page to check if user is loaded correctly
    try:
        # Test accessing current_user attributes one by one
        username = getattr(current_user, 'username', 'N/A')
        full_name = getattr(current_user, 'full_name', 'N/A')
        email = getattr(current_user, 'email', 'N/A')
        is_admin = getattr(current_user, 'is_admin', False)
        is_active = getattr(current_user, 'is_active', False)

        # Try to get role
        try:
            role_name = current_user.role.name if current_user.role else 'لا يوجد'
            role_name_ar = current_user.role.name_ar if current_user.role else 'لا يوجد'
        except Exception as role_error:
            role_name = f"Error: {str(role_error)}"
            role_name_ar = f"Error: {str(role_error)}"

        # Try to get branch
        try:
            branch_name = current_user.branch.name if current_user.branch else 'لا يوجد'
        except Exception as branch_error:
            branch_name = f"Error: {str(branch_error)}"

        user_info = f"""
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    max-width: 800px;
                    margin: 0 auto;
                }}
                h1 {{ color: #28a745; }}
                .info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ تم تسجيل الدخول بنجاح!</h1>

                <div class="info">
                    <h3>معلومات المستخدم:</h3>
                    <p><strong>اسم المستخدم:</strong> {username}</p>
                    <p><strong>الاسم الكامل:</strong> {full_name}</p>
                    <p><strong>البريد الإلكتروني:</strong> {email}</p>
                    <p><strong>مدير النظام:</strong> {'نعم' if is_admin else 'لا'}</p>
                    <p><strong>نشط:</strong> {'نعم' if is_active else 'لا'}</p>
                </div>

                <div class="info">
                    <h3>معلومات الدور:</h3>
                    <p><strong>الدور:</strong> {role_name}</p>
                    <p><strong>الدور (عربي):</strong> {role_name_ar}</p>
                </div>

                <div class="info">
                    <h3>معلومات الفرع:</h3>
                    <p><strong>الفرع:</strong> {branch_name}</p>
                </div>

                <p class="success">✅ النظام يعمل بشكل صحيح!</p>
                <p>سيتم تحميل لوحة التحكم الكاملة قريباً...</p>
            </div>
        </body>
        </html>
        """
        return user_info
    except Exception as e:
        # If there's an error, return error details
        return f"""
        <html dir="rtl">
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial; padding: 20px; background: #f8d7da;">
            <h2 style="color: #721c24;">❌ خطأ في تحميل الصفحة</h2>
            <div style="background: white; padding: 20px; border-radius: 5px; border: 1px solid #f5c6cb;">
                <p><strong>الخطأ:</strong> {str(e)}</p>
                <p><strong>النوع:</strong> {type(e).__name__}</p>
                <hr>
                <h3>Traceback:</h3>
                <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">{traceback.format_exc()}</pre>
            </div>
        </body>
        </html>
        """, 500

    # Old code (commented out for now)
    """
    # Wrap in try-except to catch any errors
    try:
        # Get statistics
        stats = {
            'total_products': Product.query.filter_by(is_active=True).count(),
            'total_customers': Customer.query.filter_by(is_active=True).count(),
            'total_suppliers': Supplier.query.filter_by(is_active=True).count(),
            'low_stock_products': 0,
            'total_warehouses': Warehouse.query.filter_by(is_active=True).count(),
        }
    except Exception as e:
        # If there's an error, return a simple page with error details
        return f'''
        <html dir="rtl">
        <body style="font-family: Arial; padding: 20px;">
            <h2>❌ خطأ في تحميل الصفحة الرئيسية</h2>
            <p><strong>الخطأ:</strong> {str(e)}</p>
            <p><strong>المستخدم:</strong> {current_user.username if current_user.is_authenticated else 'غير مسجل'}</p>
            <p><strong>is_admin:</strong> {current_user.is_admin if current_user.is_authenticated else 'N/A'}</p>
            <hr>
            <pre>{traceback.format_exc()}</pre>
        </body>
        </html>
        ''', 500
    """

    # Calculate low stock products
    products = Product.query.filter_by(is_active=True, track_inventory=True).all()
    for product in products:
        current_stock = product.get_stock()
        if product.min_stock and current_stock <= product.min_stock:
            stats['low_stock_products'] += 1

    # Get recent sales
    recent_sales = SalesInvoice.query.order_by(SalesInvoice.created_at.desc()).limit(5).all()

    # Get recent purchases
    recent_purchases = PurchaseInvoice.query.order_by(PurchaseInvoice.created_at.desc()).limit(5).all()

    # Sales this month
    today = datetime.utcnow()
    first_day = today.replace(day=1)
    sales_this_month = db.session.query(func.sum(SalesInvoice.total_amount)).filter(
        SalesInvoice.invoice_date >= first_day,
        SalesInvoice.status != 'cancelled'
    ).scalar() or 0

    # Purchases this month
    purchases_this_month = db.session.query(func.sum(PurchaseInvoice.total_amount)).filter(
        PurchaseInvoice.invoice_date >= first_day,
        PurchaseInvoice.status != 'cancelled'
    ).scalar() or 0

    # Calculate COGS (Cost of Goods Sold) this month
    sales_invoices = SalesInvoice.query.filter(
        SalesInvoice.invoice_date >= first_day,
        SalesInvoice.status != 'cancelled'
    ).all()

    cogs_this_month = 0
    for invoice in sales_invoices:
        for item in invoice.items:
            cogs_this_month += item.product.cost_price * item.quantity

    # Calculate profit this month (Sales - COGS)
    profit_this_month = sales_this_month - cogs_this_month

    stats['sales_this_month'] = sales_this_month
    stats['purchases_this_month'] = purchases_this_month
    stats['profit_this_month'] = profit_this_month

    # Get sales data for last 6 months
    sales_chart_data = []
    purchases_chart_data = []
    chart_labels = []

    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)

        # Get last day of month
        last_day = calendar.monthrange(month_start.year, month_start.month)[1]
        month_end = month_start.replace(day=last_day)

        # Sales for this month
        month_sales = db.session.query(func.sum(SalesInvoice.total_amount)).filter(
            SalesInvoice.invoice_date >= month_start,
            SalesInvoice.invoice_date <= month_end,
            SalesInvoice.status != 'cancelled'
        ).scalar() or 0

        # Purchases for this month
        month_purchases = db.session.query(func.sum(PurchaseInvoice.total_amount)).filter(
            PurchaseInvoice.invoice_date >= month_start,
            PurchaseInvoice.invoice_date <= month_end,
            PurchaseInvoice.status != 'cancelled'
        ).scalar() or 0

        sales_chart_data.append(float(month_sales))
        purchases_chart_data.append(float(month_purchases))

        # Arabic month names
        arabic_months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                        'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        chart_labels.append(arabic_months[month_start.month - 1])

    # Get top selling products
    top_products = db.session.query(
        Product.name,
        func.sum(SalesInvoiceItem.quantity).label('total_qty')
    ).join(SalesInvoiceItem).join(SalesInvoice).filter(
        SalesInvoice.status != 'cancelled',
        SalesInvoice.invoice_date >= first_day
    ).group_by(Product.id).order_by(func.sum(SalesInvoiceItem.quantity).desc()).limit(5).all()

    # Calculate inventory value
    inventory_value = 0
    for product in products:
        stock_qty = product.get_stock()
        inventory_value += stock_qty * product.cost_price

    stats['inventory_value'] = inventory_value

    return render_template('main/index.html',
                         stats=stats,
                         recent_sales=recent_sales,
                         recent_purchases=recent_purchases,
                         sales_chart_data=sales_chart_data,
                         purchases_chart_data=purchases_chart_data,
                         chart_labels=chart_labels,
                         top_products=top_products)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/license-info')
@login_required
@permission_required('dashboard.view')
def license_info():
    """Display license information for current user"""
    from app.license_manager import LicenseManager

    license_data = None

    try:
        # Get active license from database
        is_valid, message, license = LicenseManager.verify_license()

        if license:
            license_data = {
                'key': license.license_key,
                'company': license.client_company or license.client_name,
                'email': license.client_email,
                'phone': license.client_phone,
                'created': license.created_at.strftime('%Y-%m-%d') if license.created_at else 'N/A',
                'expiry': license.expires_at.strftime('%Y-%m-%d') if license.expires_at else 'دائم - Lifetime',
                'days_remaining': license.days_remaining(),
                'license_type': license.license_type.title(),
                'max_users': license.max_users,
                'max_branches': license.max_branches,
                'activation_count': len(license.checks) if hasattr(license, 'checks') else 0,
                'features': ['all'],  # يمكن تخصيصها لاحقاً
                'status': 'active' if is_valid else ('suspended' if license.is_suspended else 'inactive'),
                'machine_id': license.machine_id or 'N/A',
                'is_valid': is_valid,
                'message': message
            }
    except Exception as e:
        print(f"Error loading license info: {e}")
        flash(f'خطأ في تحميل معلومات الترخيص: {str(e)}', 'danger')

    return render_template('license_info.html', license_info=license_data)


@bp.route('/licenses-dashboard')
@csrf.exempt  # Exempt from CSRF protection for public access
def licenses_dashboard():
    """لوحة تحكم التراخيص - عرض جميع التراخيص"""
    try:
        # Get all licenses
        licenses = License.query.order_by(License.created_at.desc()).all()

        # Calculate statistics
        total_licenses = len(licenses)
        active_licenses = sum(1 for lic in licenses if lic.is_active and lic.is_valid()[0] and not lic.is_suspended)
        expired_licenses = sum(1 for lic in licenses if not lic.is_valid()[0])
        trial_licenses = sum(1 for lic in licenses if lic.license_type == 'trial')

        stats = {
            'total': total_licenses,
            'active': active_licenses,
            'expired': expired_licenses,
            'trial': trial_licenses
        }

        return render_template('license_dashboard.html', licenses=licenses, stats=stats)

    except Exception as e:
        print(f"Error in licenses_dashboard: {e}")
        print(traceback.format_exc())
        flash(f'حدث خطأ أثناء تحميل لوحة التحكم: {str(e)}', 'danger')
        return render_template('license_dashboard.html', licenses=[], stats={'total': 0, 'active': 0, 'expired': 0, 'trial': 0})


@bp.route('/license/<int:license_id>/view')
@csrf.exempt
def view_license(license_id):
    """عرض تفاصيل ترخيص معين"""
    try:
        license = License.query.get_or_404(license_id)
        is_valid, message = license.is_valid()

        license_info = {
            'id': license.id,
            'license_key': license.license_key,
            'client_name': license.client_name,
            'client_company': license.client_company,
            'client_email': license.client_email,
            'client_phone': license.client_phone,
            'license_type': license.license_type,
            'max_users': license.max_users,
            'max_branches': license.max_branches,
            'is_active': license.is_active,
            'is_suspended': license.is_suspended,
            'is_valid': is_valid,
            'message': message,
            'created_at': license.created_at,
            'activated_at': license.activated_at,
            'expires_at': license.expires_at,
            'days_remaining': license.days_remaining(),
            'machine_id': license.machine_id,
            'ip_address': license.ip_address,
            'notes': license.notes
        }

        return render_template('license_view.html', license=license_info)

    except Exception as e:
        print(f"Error in view_license: {e}")
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('main.licenses_dashboard'))


@bp.route('/license/<int:license_id>/toggle-suspend', methods=['POST'])
@csrf.exempt
def toggle_suspend_license(license_id):
    """تعليق/تفعيل ترخيص"""
    try:
        license = License.query.get_or_404(license_id)
        data = request.get_json()
        suspend = data.get('suspend', False)

        license.is_suspended = suspend
        db.session.commit()

        return {'success': True, 'message': 'تم تحديث حالة الترخيص بنجاح'}

    except Exception as e:
        print(f"Error in toggle_suspend_license: {e}")
        return {'success': False, 'message': str(e)}, 400


@bp.route('/license/<int:license_id>/delete', methods=['POST'])
@csrf.exempt
def delete_license(license_id):
    """حذف ترخيص"""
    try:
        license = License.query.get_or_404(license_id)
        db.session.delete(license)
        db.session.commit()

        return {'success': True, 'message': 'تم حذف الترخيص بنجاح'}

    except Exception as e:
        print(f"Error in delete_license: {e}")
        return {'success': False, 'message': str(e)}, 400


@bp.route('/license/<int:license_id>/edit', methods=['GET', 'POST'])
@csrf.exempt
def edit_license(license_id):
    """تعديل ترخيص"""
    try:
        license = License.query.get_or_404(license_id)

        if request.method == 'POST':
            # Update license data
            license.client_name = request.form.get('client_name', license.client_name)
            license.client_company = request.form.get('client_company', license.client_company)
            license.client_email = request.form.get('client_email', license.client_email)
            license.client_phone = request.form.get('client_phone', license.client_phone)
            license.max_users = int(request.form.get('max_users', license.max_users))
            license.max_branches = int(request.form.get('max_branches', license.max_branches))
            license.notes = request.form.get('notes', license.notes)

            # Update license type and expiration
            new_type = request.form.get('license_type', license.license_type)
            if new_type != license.license_type:
                license.license_type = new_type
                if new_type == 'trial':
                    license.expires_at = datetime.utcnow() + timedelta(days=30)
                elif new_type == 'annual':
                    license.expires_at = datetime.utcnow() + timedelta(days=365)
                else:  # lifetime
                    license.expires_at = None

            db.session.commit()
            flash('تم تحديث الترخيص بنجاح', 'success')
            return redirect(url_for('main.view_license', license_id=license.id))

        # GET request - show edit form
        return render_template('license_edit.html', license=license)

    except Exception as e:
        print(f"Error in edit_license: {e}")
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('main.licenses_dashboard'))


@bp.route('/create-license', methods=['GET', 'POST'])
@csrf.exempt  # Exempt from CSRF protection for public access
def create_new_license():
    """صفحة إنشاء ترخيص جديد"""
    try:
        if request.method == 'POST':
            # Get form data
            license_type = request.form.get('license_type', 'trial')
            client_name = request.form.get('client_name', '').strip()
            client_company = request.form.get('client_company', '').strip()
            client_email = request.form.get('client_email', '').strip()
            client_phone = request.form.get('client_phone', '').strip()
            max_users = int(request.form.get('max_users', 10))
            max_branches = int(request.form.get('max_branches', 5))
            notes = request.form.get('notes', '').strip()

            # Validate required fields
            if not all([client_name, client_company, client_email, client_phone]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'danger')
                return redirect(url_for('main.create_new_license'))

            # Generate license key
            license_key = '-'.join([uuid.uuid4().hex[:4].upper() for _ in range(4)])

            # Calculate expiration date
            if license_type == 'trial':
                expires_at = datetime.utcnow() + timedelta(days=30)
            elif license_type == 'annual':
                expires_at = datetime.utcnow() + timedelta(days=365)
            else:  # lifetime
                expires_at = None

            # Create new license
            new_license = License(
                license_key=license_key,
                license_hash=License.hash_license_key(license_key),
                client_name=client_name,
                client_company=client_company,
                client_email=client_email,
                client_phone=client_phone,
                license_type=license_type,
                max_users=max_users,
                max_branches=max_branches,
                is_active=True,
                is_suspended=False,
                created_at=datetime.utcnow(),
                activated_at=datetime.utcnow(),
                expires_at=expires_at,
                admin_username='admin',
                notes=notes or f'ترخيص {license_type} - تم الإنشاء تلقائياً'
            )

            db.session.add(new_license)
            db.session.commit()

            flash(f'تم إنشاء الترخيص بنجاح! مفتاح الترخيص: {license_key}', 'success')

            # Redirect to activation page with the license key
            return redirect(url_for('main.activate_license', key=license_key))

        # GET request - show form
        return render_template('license_create.html')

    except Exception as e:
        print(f"Error in create_new_license: {e}")
        print(traceback.format_exc())
        flash(f'حدث خطأ أثناء إنشاء الترخيص: {str(e)}', 'danger')
        return render_template('license_create.html')


@bp.route('/activate-license', methods=['GET', 'POST'])
@bp.route('/license-activation', methods=['GET', 'POST'])
@csrf.exempt  # Exempt from CSRF protection for public access
def activate_license():
    """صفحة تفعيل الترخيص"""
    try:
        # Get license key from URL parameter if available
        url_license_key = request.args.get('key', '').strip().upper()

        if request.method == 'POST':
            license_key = request.form.get('license_key', '').strip().upper()

            if not license_key:
                flash('يرجى إدخال مفتاح الترخيص', 'danger')
                return redirect(url_for('main.activate_license'))

            # التحقق من صحة الترخيص
            license = License.query.filter_by(license_key=license_key).first()

            if not license:
                flash('مفتاح الترخيص غير صحيح', 'danger')
                return redirect(url_for('main.activate_license'))

            # التحقق من صلاحية الترخيص
            is_valid, message = license.is_valid()

            if not is_valid:
                flash(f'الترخيص غير صالح: {message}', 'danger')
                return redirect(url_for('main.activate_license'))

            # ربط الترخيص بالجهاز
            try:
                machine_id = LicenseManager.get_machine_id()
                ip_address = LicenseManager.get_ip_address()
            except Exception as e:
                print(f"Error getting machine info: {e}")
                machine_id = "RENDER_SERVER"
                ip_address = request.remote_addr or "0.0.0.0"

            # إذا كان الترخيص مربوط بجهاز آخر - السماح بإعادة التفعيل على Render
            # (تم تعطيل الفحص للسماح بالنشر على Render)
            # if license.machine_id and license.machine_id != machine_id:
            #     flash('هذا الترخيص مربوط بجهاز آخر', 'danger')
            #     return redirect(url_for('main.activate_license'))

            # تفعيل الترخيص - تحديث machine_id للجهاز الحالي
            license.machine_id = machine_id
            license.ip_address = ip_address
            license.activated_at = datetime.utcnow()
            license.is_active = True

            db.session.commit()

            flash('تم تفعيل الترخيص بنجاح!', 'success')
            return redirect(url_for('auth.login'))

        return render_template('license_activation_modern.html', prefilled_key=url_license_key)

    except Exception as e:
        print(f"Error in activate_license: {e}")
        print(traceback.format_exc())
        flash(f'حدث خطأ أثناء تفعيل الترخيص: {str(e)}', 'danger')
        return render_template('license_activation_modern.html', prefilled_key=url_license_key)


@bp.route('/license-status')
@login_required
def license_status():
    """عرض حالة الترخيص الحالي"""
    if not current_user.license_id:
        flash('لا يوجد ترخيص مرتبط بحسابك', 'warning')
        return redirect(url_for('main.index'))

    license = License.query.get(current_user.license_id)

    if not license:
        flash('الترخيص غير موجود', 'danger')
        return redirect(url_for('main.index'))

    is_valid, message = license.is_valid()

    license_info = {
        'license_key': license.license_key,
        'client_name': license.client_name,
        'client_company': license.client_company,
        'license_type': license.license_type,
        'max_users': license.max_users,
        'max_branches': license.max_branches,
        'is_active': license.is_active,
        'is_valid': is_valid,
        'message': message,
        'created_at': license.created_at,
        'activated_at': license.activated_at,
        'expires_at': license.expires_at,
        'days_remaining': license.days_remaining(),
        'machine_id': license.machine_id,
        'ip_address': license.ip_address
    }

    return render_template('license_status.html', license=license_info)


@bp.route('/emergency-create-license', methods=['GET', 'POST'])
@csrf.exempt
def emergency_create_license():
    """Emergency route to create license with custom credentials"""
    from datetime import datetime
    import hashlib
    from werkzeug.security import generate_password_hash

    if request.method == 'GET':
        # Show form to create license
        return """
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>إنشاء ترخيص جديد</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                }
                h2 { color: #333; margin-bottom: 30px; }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                    color: #555;
                }
                input, select {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                input:focus, select:focus {
                    border-color: #667eea;
                    outline: none;
                }
                button {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 20px;
                }
                button:hover {
                    opacity: 0.9;
                }
                .note {
                    background: #fff3cd;
                    border: 1px solid #ffc107;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    color: #856404;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🔑 إنشاء ترخيص جديد</h2>

                <div class="note">
                    <strong>ملاحظة:</strong> سيتم إنشاء ترخيص جديد مع بيانات الدخول التي تحددها.
                </div>

                <form method="POST">
                    <div class="form-group">
                        <label>🔑 مفتاح الترخيص (License Key)</label>
                        <input type="text" name="license_key" value="RENDER-2026-PROD-LIVE" required>
                    </div>

                    <div class="form-group">
                        <label>👤 اسم المستخدم (Username)</label>
                        <input type="text" name="username" value="admin" required>
                    </div>

                    <div class="form-group">
                        <label>🔒 كلمة المرور (Password)</label>
                        <input type="password" name="password" value="admin123" required>
                    </div>

                    <div class="form-group">
                        <label>🏢 اسم العميل</label>
                        <input type="text" name="client_name" value="DED ERP System - Production" required>
                    </div>

                    <div class="form-group">
                        <label>📧 البريد الإلكتروني</label>
                        <input type="email" name="client_email" value="admin@ded-erp.com" required>
                    </div>

                    <div class="form-group">
                        <label>📅 نوع الترخيص</label>
                        <select name="license_type">
                            <option value="lifetime">مدى الحياة (Lifetime)</option>
                            <option value="annual">سنوي (Annual)</option>
                            <option value="monthly">شهري (Monthly)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>👥 عدد المستخدمين</label>
                        <input type="number" name="max_users" value="100" required>
                    </div>

                    <div class="form-group">
                        <label>🏢 عدد الفروع</label>
                        <input type="number" name="max_branches" value="10" required>
                    </div>

                    <button type="submit">✅ إنشاء الترخيص</button>
                </form>
            </div>
        </body>
        </html>
        """

    # POST request - Create license
    try:
        license_key = request.form.get('license_key')
        username = request.form.get('username')
        password = request.form.get('password')
        client_name = request.form.get('client_name')
        client_email = request.form.get('client_email')
        license_type = request.form.get('license_type', 'lifetime')
        max_users = int(request.form.get('max_users', 100))
        max_branches = int(request.form.get('max_branches', 10))

        # Check if license already exists
        existing_license = License.query.filter_by(license_key=license_key).first()

        if existing_license:
            # Update existing license
            existing_license.is_active = True
            existing_license.is_suspended = False
            existing_license.activated_at = datetime.utcnow()
            existing_license.admin_username = username
            existing_license.admin_password_hash = generate_password_hash(password)
            db.session.commit()

            return f"""
            <html dir="rtl">
            <head><meta charset="UTF-8"></head>
            <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
                <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #28a745;">✅ تم تحديث الترخيص بنجاح!</h2>
                    <hr>
                    <p><strong>🔑 مفتاح الترخيص:</strong> {license_key}</p>
                    <p><strong>👤 اسم المستخدم:</strong> {username}</p>
                    <p><strong>🔒 كلمة المرور:</strong> {password}</p>
                    <hr>
                    <a href="/auth/login" style="display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">تسجيل الدخول الآن</a>
                </div>
            </body>
            </html>
            """
        else:
            # Create new license
            license = License(
                license_key=license_key,
                license_hash=hashlib.sha256(license_key.encode()).hexdigest(),
                client_name=client_name,
                client_email=client_email,
                client_company=client_name,
                license_type=license_type,
                max_users=max_users,
                max_branches=max_branches,
                is_active=True,
                is_suspended=False,
                created_at=datetime.utcnow(),
                activated_at=datetime.utcnow(),
                expires_at=None if license_type == 'lifetime' else None,
                admin_username=username,
                admin_password_hash=generate_password_hash(password),
                notes=f"Created via emergency route on {datetime.utcnow()}"
            )

            db.session.add(license)
            db.session.flush()  # Get license.id before creating user

            # Create admin user in User table
            admin_user = User(
                username=username,
                email=client_email,
                password_hash=generate_password_hash(password),
                full_name=client_name,
                is_active=True,
                is_admin=True,
                license_id=license.id,
                created_at=datetime.utcnow()
            )

            db.session.add(admin_user)
            db.session.commit()

            return f"""
            <html dir="rtl">
            <head><meta charset="UTF-8"></head>
            <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
                <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #28a745;">🎉 تم إنشاء الترخيص والمستخدم بنجاح!</h2>
                    <hr>
                    <p><strong>🔑 مفتاح الترخيص:</strong> {license_key}</p>
                    <p><strong>👤 اسم المستخدم:</strong> {username}</p>
                    <p><strong>🔒 كلمة المرور:</strong> {password}</p>
                    <p><strong>📧 البريد الإلكتروني:</strong> {client_email}</p>
                    <p><strong>📅 النوع:</strong> {license_type}</p>
                    <p><strong>👥 عدد المستخدمين:</strong> {max_users}</p>
                    <p><strong>🏢 عدد الفروع:</strong> {max_branches}</p>
                    <hr>
                    <p style="color: #28a745; font-weight: bold;">✅ تم إنشاء المستخدم الإداري في قاعدة البيانات</p>
                    <a href="/auth/login" style="display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">تسجيل الدخول الآن</a>
                </div>
            </body>
            </html>
            """

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"""
        <html dir="rtl">
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #dc3545;">❌ حدث خطأ!</h2>
                <hr>
                <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">{error_details}</pre>
            </div>
        </body>
        </html>
        """


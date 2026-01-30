from flask import render_template, redirect, url_for, flash, request, make_response, after_this_request
from flask_login import login_required, current_user
from app.auth.decorators import permission_required
from app.main import bp
from app import db
from app.models import *
from app.models_license import License
from app.license_manager import LicenseManager
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar
import json
from pathlib import Path

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
@permission_required('dashboard.view')
def index():
    """Dashboard - Main page"""

    # Get statistics
    stats = {
        'total_products': Product.query.filter_by(is_active=True).count(),
        'total_customers': Customer.query.filter_by(is_active=True).count(),
        'total_suppliers': Supplier.query.filter_by(is_active=True).count(),
        'low_stock_products': 0,
        'total_warehouses': Warehouse.query.filter_by(is_active=True).count(),
    }

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


@bp.route('/activate-license', methods=['GET', 'POST'])
def activate_license():
    """صفحة تفعيل الترخيص"""
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
        machine_id = LicenseManager.get_machine_id()
        ip_address = LicenseManager.get_ip_address()

        # إذا كان الترخيص مربوط بجهاز آخر
        if license.machine_id and license.machine_id != machine_id:
            flash('هذا الترخيص مربوط بجهاز آخر', 'danger')
            return redirect(url_for('main.activate_license'))

        # تفعيل الترخيص
        license.machine_id = machine_id
        license.ip_address = ip_address
        license.activated_at = datetime.utcnow()
        license.is_active = True

        db.session.commit()

        flash('تم تفعيل الترخيص بنجاح!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('license_activation.html')


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


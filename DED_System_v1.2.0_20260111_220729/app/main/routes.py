from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import *
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar

@bp.route('/')
@bp.route('/index')
@login_required
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
        if current_stock <= product.min_stock:
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

    # Calculate profit this month
    profit_this_month = sales_this_month - purchases_this_month

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


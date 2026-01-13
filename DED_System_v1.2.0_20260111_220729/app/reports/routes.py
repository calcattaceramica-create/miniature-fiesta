from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app.reports import bp
from app import db
from app.models import *
from sqlalchemy import func
from datetime import datetime, timedelta

@bp.route('/')
@login_required
def index():
    """Reports dashboard"""
    return render_template('reports/index.html')

@bp.route('/sales')
@login_required
def sales_report():
    """Sales report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = SalesInvoice.query.filter_by(status='confirmed')
    
    if start_date:
        query = query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    invoices = query.all()
    
    total_sales = sum(inv.total_amount for inv in invoices)
    total_tax = sum(inv.tax_amount for inv in invoices)
    
    return render_template('reports/sales.html',
                         invoices=invoices,
                         total_sales=total_sales,
                         total_tax=total_tax,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/purchases')
@login_required
def purchases_report():
    """Purchases report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = PurchaseInvoice.query.filter_by(status='confirmed')
    
    if start_date:
        query = query.filter(PurchaseInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(PurchaseInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    invoices = query.all()
    
    total_purchases = sum(inv.total_amount for inv in invoices)
    total_tax = sum(inv.tax_amount for inv in invoices)
    
    return render_template('reports/purchases.html',
                         invoices=invoices,
                         total_purchases=total_purchases,
                         total_tax=total_tax,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/inventory')
@login_required
def inventory_report():
    """Inventory report"""
    products = Product.query.filter_by(is_active=True, track_inventory=True).all()
    
    inventory_data = []
    for product in products:
        stock_qty = product.get_stock()
        inventory_data.append({
            'product': product,
            'stock': stock_qty,
            'value': stock_qty * product.cost_price
        })
    
    total_value = sum(item['value'] for item in inventory_data)
    
    return render_template('reports/inventory.html',
                         inventory_data=inventory_data,
                         total_value=total_value)

@bp.route('/profit-loss')
@login_required
def profit_loss():
    """Profit and Loss statement"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Calculate revenue
    revenue_query = db.session.query(func.sum(SalesInvoice.total_amount)).filter_by(status='confirmed')
    if start_date:
        revenue_query = revenue_query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        revenue_query = revenue_query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    total_revenue = revenue_query.scalar() or 0

    # Calculate cost of goods sold
    cogs_query = db.session.query(func.sum(PurchaseInvoice.total_amount)).filter_by(status='confirmed')
    if start_date:
        cogs_query = cogs_query.filter(PurchaseInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        cogs_query = cogs_query.filter(PurchaseInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    total_cogs = cogs_query.scalar() or 0

    gross_profit = total_revenue - total_cogs

    return render_template('reports/profit_loss.html',
                         total_revenue=total_revenue,
                         total_cogs=total_cogs,
                         gross_profit=gross_profit,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/low-stock')
@login_required
def low_stock_report():
    """Low stock products report"""
    products = Product.query.filter_by(is_active=True, track_inventory=True).all()

    low_stock_products = []
    for product in products:
        stock_qty = product.get_stock()
        if stock_qty <= product.min_stock:
            low_stock_products.append({
                'product': product,
                'current_stock': stock_qty,
                'min_stock': product.min_stock,
                'shortage': product.min_stock - stock_qty
            })

    return render_template('reports/low_stock.html',
                         low_stock_products=low_stock_products)

@bp.route('/stock-movement')
@login_required
def stock_movement_report():
    """Stock movement report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    product_id = request.args.get('product_id', type=int)
    warehouse_id = request.args.get('warehouse_id', type=int)

    query = StockMovement.query

    if start_date:
        query = query.filter(StockMovement.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(StockMovement.created_at <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    if product_id:
        query = query.filter_by(product_id=product_id)
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)

    movements = query.order_by(StockMovement.created_at.desc()).all()

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    warehouses = Warehouse.query.filter_by(is_active=True).order_by(Warehouse.name).all()

    return render_template('reports/stock_movement.html',
                         movements=movements,
                         products=products,
                         warehouses=warehouses,
                         start_date=start_date,
                         end_date=end_date,
                         selected_product_id=product_id,
                         selected_warehouse_id=warehouse_id)

@bp.route('/sales-by-product')
@login_required
def sales_by_product():
    """Sales report by product"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = db.session.query(
        Product.name,
        Product.code,
        func.sum(SalesInvoiceItem.quantity).label('total_qty'),
        func.sum(SalesInvoiceItem.total).label('total_amount')
    ).join(SalesInvoiceItem).join(SalesInvoice).filter(
        SalesInvoice.status != 'cancelled'
    )

    if start_date:
        query = query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    results = query.group_by(Product.id).order_by(func.sum(SalesInvoiceItem.total).desc()).all()

    total_qty = sum(r.total_qty for r in results)
    total_amount = sum(r.total_amount for r in results)

    return render_template('reports/sales_by_product.html',
                         results=results,
                         total_qty=total_qty,
                         total_amount=total_amount,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/sales-by-customer')
@login_required
def sales_by_customer():
    """Sales report by customer"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = db.session.query(
        Customer.name,
        Customer.code,
        func.count(SalesInvoice.id).label('invoice_count'),
        func.sum(SalesInvoice.total_amount).label('total_amount')
    ).join(SalesInvoice).filter(
        SalesInvoice.status != 'cancelled'
    )

    if start_date:
        query = query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    results = query.group_by(Customer.id).order_by(func.sum(SalesInvoice.total_amount).desc()).all()

    total_invoices = sum(r.invoice_count for r in results)
    total_amount = sum(r.total_amount for r in results)

    return render_template('reports/sales_by_customer.html',
                         results=results,
                         total_invoices=total_invoices,
                         total_amount=total_amount,
                         start_date=start_date,
                         end_date=end_date)


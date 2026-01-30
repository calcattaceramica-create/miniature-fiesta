from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required
from app.auth.decorators import permission_required
from app.reports import bp
from app import db
from app.models import *
from sqlalchemy import func
from datetime import datetime, timedelta

@bp.route('/')
@login_required
@permission_required('reports.view')
def index():
    """Reports dashboard"""
    return render_template('reports/index.html')

@bp.route('/sales')
@login_required
@permission_required('reports.sales')
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

    # Get currency settings
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/sales.html',
                         invoices=invoices,
                         total_sales=total_sales,
                         total_tax=total_tax,
                         start_date=start_date,
                         end_date=end_date,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)

@bp.route('/purchases')
@login_required
@permission_required('reports.purchases')
def purchases_report():
    """Purchases report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = PurchaseInvoice.query.filter(PurchaseInvoice.status != 'cancelled')

    if start_date:
        query = query.filter(PurchaseInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(PurchaseInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    invoices = query.all()

    total_purchases = sum(inv.total_amount for inv in invoices)
    total_tax = sum(inv.tax_amount for inv in invoices)

    # Get currency settings
    currency_code = current_app.config.get('CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    # Debug
    print(f"DEBUG: invoices count = {len(invoices)}")
    print(f"DEBUG: total_purchases = {total_purchases}")
    print(f"DEBUG: total_tax = {total_tax}")
    print(f"DEBUG: currency_name = {currency_name}")

    return render_template('reports/purchases.html',
                         invoices=invoices,
                         total_purchases=total_purchases,
                         total_tax=total_tax,
                         start_date=start_date,
                         end_date=end_date,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)

@bp.route('/inventory')
@login_required
@permission_required('reports.inventory')
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

    # Get company settings for currency
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('reports/inventory.html',
                         inventory_data=inventory_data,
                         total_value=total_value,
                         currency_code=currency_code,
                         currency_symbol=currency_symbol)

@bp.route('/profit-loss')
@login_required
@permission_required('reports.financial')
def profit_loss():
    """Profit and Loss statement"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Calculate revenue
    revenue_query = db.session.query(func.sum(SalesInvoice.total_amount)).filter(SalesInvoice.status != 'cancelled')
    if start_date:
        revenue_query = revenue_query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        revenue_query = revenue_query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    total_revenue = revenue_query.scalar() or 0

    # Calculate cost of goods sold (COGS) - from sales invoice items
    sales_query = SalesInvoice.query.filter(SalesInvoice.status != 'cancelled')
    if start_date:
        sales_query = sales_query.filter(SalesInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        sales_query = sales_query.filter(SalesInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    sales_invoices = sales_query.all()

    total_cogs = 0
    for invoice in sales_invoices:
        for item in invoice.items:
            total_cogs += item.product.cost_price * item.quantity

    gross_profit = total_revenue - total_cogs

    # Get currency settings
    currency_code = current_app.config.get('CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/profit_loss.html',
                         total_revenue=total_revenue,
                         total_cogs=total_cogs,
                         gross_profit=gross_profit,
                         start_date=start_date,
                         end_date=end_date,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)

@bp.route('/low-stock')
@login_required
@permission_required('reports.inventory')
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
@permission_required('reports.inventory')
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
@permission_required('reports.sales')
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
@permission_required('reports.sales')
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

@bp.route('/purchases-by-product')
@login_required
@permission_required('reports.purchases')
def purchases_by_product():
    """Purchases report by product"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    product_id = request.args.get('product_id', type=int)

    # Base query for purchase invoice items
    query = db.session.query(
        Product.id,
        Product.name,
        Product.code,
        func.sum(PurchaseInvoiceItem.quantity).label('total_quantity'),
        func.sum(PurchaseInvoiceItem.total).label('total_amount'),
        func.count(func.distinct(PurchaseInvoiceItem.invoice_id)).label('invoice_count')
    ).join(
        PurchaseInvoiceItem, Product.id == PurchaseInvoiceItem.product_id
    ).join(
        PurchaseInvoice, PurchaseInvoiceItem.invoice_id == PurchaseInvoice.id
    ).filter(
        PurchaseInvoice.status != 'cancelled'
    )

    # Apply filters
    if start_date:
        query = query.filter(PurchaseInvoice.invoice_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(PurchaseInvoice.invoice_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    if product_id:
        query = query.filter(Product.id == product_id)

    # Group by product
    query = query.group_by(Product.id, Product.name, Product.code)

    # Order by total amount descending
    query = query.order_by(func.sum(PurchaseInvoiceItem.total).desc())

    products_data = query.all()

    # Calculate totals
    total_quantity = sum(p.total_quantity or 0 for p in products_data)
    total_amount = sum(p.total_amount or 0 for p in products_data)
    total_invoices = sum(p.invoice_count or 0 for p in products_data)

    # Get all products for filter dropdown
    all_products = Product.query.filter_by(is_active=True, is_purchasable=True).order_by(Product.name).all()

    # Get currency info
    currencies = current_app.config.get('CURRENCIES', {})
    default_currency = current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_info = currencies.get(default_currency, {})
    currency_code = default_currency
    currency_name = currency_info.get('name', 'Euro')
    currency_symbol = currency_info.get('symbol', '€')

    return render_template('reports/purchases_by_product.html',
                         products_data=products_data,
                         total_quantity=total_quantity,
                         total_amount=total_amount,
                         total_invoices=total_invoices,
                         all_products=all_products,
                         start_date=start_date,
                         end_date=end_date,
                         selected_product_id=product_id,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)

@bp.route('/purchases-monthly')
@login_required
@permission_required('reports.purchases')
def purchases_monthly():
    """Monthly purchases report"""
    year = request.args.get('year', type=int)
    if not year:
        year = datetime.now().year

    # Get all invoices for the year
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()

    invoices = PurchaseInvoice.query.filter(
        PurchaseInvoice.status != 'cancelled',
        PurchaseInvoice.invoice_date >= start_date,
        PurchaseInvoice.invoice_date <= end_date
    ).all()

    # Group by month
    monthly_dict = {}
    for invoice in invoices:
        month_num = invoice.invoice_date.month
        if month_num not in monthly_dict:
            monthly_dict[month_num] = {
                'invoice_count': 0,
                'total_amount': 0,
                'total_tax': 0
            }
        monthly_dict[month_num]['invoice_count'] += 1
        monthly_dict[month_num]['total_amount'] += invoice.total_amount
        monthly_dict[month_num]['total_tax'] += invoice.tax_amount

    # Create complete 12-month data
    months_data = []
    month_names = [
        'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
        'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
    ]

    for month_num in range(1, 13):
        if month_num in monthly_dict:
            data = monthly_dict[month_num]
            months_data.append({
                'month_num': month_num,
                'month_name': month_names[month_num - 1],
                'invoice_count': data['invoice_count'],
                'total_amount': data['total_amount'],
                'total_tax': data['total_tax']
            })
        else:
            months_data.append({
                'month_num': month_num,
                'month_name': month_names[month_num - 1],
                'invoice_count': 0,
                'total_amount': 0,
                'total_tax': 0
            })

    # Calculate totals
    total_invoices = sum(m['invoice_count'] for m in months_data)
    total_purchases = sum(m['total_amount'] for m in months_data)
    total_tax = sum(m['total_tax'] for m in months_data)

    # Get currency settings
    currency_code = current_app.config.get('CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    # Get available years
    all_invoices = PurchaseInvoice.query.filter(
        PurchaseInvoice.status != 'cancelled'
    ).all()

    years_set = set()
    for inv in all_invoices:
        if inv.invoice_date:
            years_set.add(inv.invoice_date.year)

    available_years = sorted(list(years_set), reverse=True)
    if not available_years:
        available_years = [datetime.now().year]

    return render_template('reports/purchases_monthly.html',
                         months_data=months_data,
                         total_invoices=total_invoices,
                         total_purchases=total_purchases,
                         total_tax=total_tax,
                         year=year,
                         available_years=available_years,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)


# ==================== Supplier Reports ====================

@bp.route('/suppliers')
@login_required
@permission_required('reports.purchases')
def suppliers_list():
    """Suppliers list report"""
    suppliers = Supplier.query.filter_by(is_active=True).all()

    # Calculate totals
    total_suppliers = len(suppliers)
    total_balance = sum(s.current_balance or 0 for s in suppliers)

    # Count suppliers with purchases
    suppliers_with_purchases = 0
    for supplier in suppliers:
        if supplier.invoices:
            suppliers_with_purchases += 1

    # Get currency settings
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/suppliers.html',
                         suppliers=suppliers,
                         total_suppliers=total_suppliers,
                         total_balance=total_balance,
                         suppliers_with_purchases=suppliers_with_purchases,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)


@bp.route('/suppliers/top')
@login_required
@permission_required('reports.purchases')
def suppliers_top():
    """Best suppliers report - ranked by purchase volume"""
    # Get all suppliers with their purchase totals
    suppliers_data = []

    suppliers = Supplier.query.filter_by(is_active=True).all()

    for supplier in suppliers:
        # Calculate total purchases for this supplier
        total_purchases = db.session.query(func.sum(PurchaseInvoice.total_amount))\
            .filter(PurchaseInvoice.supplier_id == supplier.id)\
            .filter(PurchaseInvoice.status == 'confirmed')\
            .scalar() or 0

        # Count invoices
        invoice_count = PurchaseInvoice.query.filter_by(
            supplier_id=supplier.id,
            status='confirmed'
        ).count()

        if total_purchases > 0:
            suppliers_data.append({
                'supplier': supplier,
                'total_purchases': total_purchases,
                'invoice_count': invoice_count,
                'average_purchase': total_purchases / invoice_count if invoice_count > 0 else 0
            })

    # Sort by total purchases (descending)
    suppliers_data.sort(key=lambda x: x['total_purchases'], reverse=True)

    # Calculate totals
    total_purchases = sum(s['total_purchases'] for s in suppliers_data)
    total_invoices = sum(s['invoice_count'] for s in suppliers_data)

    # Get currency settings
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/suppliers_top.html',
                         suppliers_data=suppliers_data,
                         total_purchases=total_purchases,
                         total_invoices=total_invoices,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)


@bp.route('/suppliers/balances')
@login_required
@permission_required('reports.purchases')
def suppliers_balances():
    """Supplier balances report"""
    suppliers = Supplier.query.filter_by(is_active=True).all()

    # Calculate totals
    total_debit = sum(s.current_balance for s in suppliers if s.current_balance > 0)
    total_credit = abs(sum(s.current_balance for s in suppliers if s.current_balance < 0))
    net_balance = sum(s.current_balance or 0 for s in suppliers)

    # Get currency settings
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/suppliers_balances.html',
                         suppliers=suppliers,
                         total_debit=total_debit,
                         total_credit=total_credit,
                         net_balance=net_balance,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)


@bp.route('/suppliers/history/<int:supplier_id>')
@login_required
@permission_required('reports.purchases')
def suppliers_history(supplier_id):
    """Supplier history report - shows all transactions for a specific supplier"""
    supplier = Supplier.query.get_or_404(supplier_id)

    # Get all purchase invoices for this supplier
    invoices = PurchaseInvoice.query.filter_by(supplier_id=supplier_id)\
        .order_by(PurchaseInvoice.invoice_date.desc()).all()

    # Calculate totals
    total_invoices = len(invoices)
    total_purchases = sum(inv.total_amount for inv in invoices if inv.status == 'confirmed')
    total_paid = sum(inv.paid_amount or 0 for inv in invoices)
    total_remaining = sum(inv.remaining_amount or 0 for inv in invoices)

    # Get currency settings
    from app.models import Company
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'EUR')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'Euro')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', '€')

    return render_template('reports/suppliers_history.html',
                         supplier=supplier,
                         invoices=invoices,
                         total_invoices=total_invoices,
                         total_purchases=total_purchases,
                         total_paid=total_paid,
                         total_remaining=total_remaining,
                         currency_code=currency_code,
                         currency_name=currency_name,
                         currency_symbol=currency_symbol)


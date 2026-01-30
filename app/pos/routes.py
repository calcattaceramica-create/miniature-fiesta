from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.pos import bp
from app import db
from app.models import POSSession, POSOrder, POSOrderItem, Product, Customer, Warehouse, Company
from app.models import SalesInvoice, SalesInvoiceItem, Stock, StockMovement
from app.auth.decorators import permission_required, any_permission_required
from datetime import datetime

def _generate_invoice_number():
    """Generate unique invoice number for POS sales"""
    today = datetime.utcnow()
    prefix = f'INV{today.year}{today.month:02d}'
    last_invoice = SalesInvoice.query.filter(
        SalesInvoice.invoice_number.like(f'{prefix}%')
    ).order_by(SalesInvoice.id.desc()).first()

    if last_invoice:
        last_num = int(last_invoice.invoice_number[-4:])
        invoice_number = f'{prefix}{(last_num + 1):04d}'
    else:
        invoice_number = f'{prefix}0001'

    return invoice_number

def _get_or_create_default_customer():
    """Get or create default walk-in customer"""
    # Try to find existing default customer
    default_customer = Customer.query.filter_by(code='WALK-IN').first()

    if not default_customer:
        # Create default walk-in customer
        default_customer = Customer(
            code='WALK-IN',
            name='عميل افتراضي',
            name_en='Walk-in Customer',
            phone='0000000000',
            email='walkin@default.com',
            is_active=True
        )
        db.session.add(default_customer)
        db.session.commit()

    return default_customer.id

@bp.route('/')
@login_required
@permission_required('pos.access')
def index():
    """POS Main Interface"""
    # Check if user has an open session
    open_session = POSSession.query.filter_by(
        cashier_id=current_user.id,
        status='open'
    ).first()
    
    if not open_session:
        return redirect(url_for('pos.open_session'))

    products = Product.query.filter_by(is_active=True, is_sellable=True).all()
    customers = Customer.query.filter_by(is_active=True).all()

    # Get company settings for currency and tax
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')
    tax_rate = company.tax_rate if company else 15.0

    return render_template('pos/index.html',
                         pos_session=open_session,
                         products=products,
                         customers=customers,
                         company=company,
                         currency_code=currency_code,
                         currency_symbol=currency_symbol,
                         tax_rate=tax_rate)

@bp.route('/open-session', methods=['GET', 'POST'])
@login_required
@permission_required('pos.session.manage')
def open_session():
    """Open new POS session"""
    if request.method == 'POST':
        # Generate session number
        today = datetime.utcnow()
        prefix = f'POS{today.year}{today.month:02d}{today.day:02d}'
        last_session = POSSession.query.filter(
            POSSession.session_number.like(f'{prefix}%')
        ).order_by(POSSession.id.desc()).first()
        
        if last_session:
            last_num = int(last_session.session_number[-3:])
            session_number = f'{prefix}{(last_num + 1):03d}'
        else:
            session_number = f'{prefix}001'
        
        session = POSSession(
            session_number=session_number,
            cashier_id=current_user.id,
            warehouse_id=request.form.get('warehouse_id', type=int),
            opening_balance=request.form.get('opening_balance', 0, type=float),
            status='open'
        )
        
        db.session.add(session)
        db.session.commit()
        
        flash('تم فتح الوردية بنجاح', 'success')
        return redirect(url_for('pos.index'))
    
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return render_template('pos/open_session.html', warehouses=warehouses)

@bp.route('/close-session/<int:id>', methods=['POST'])
@login_required
@permission_required('pos.session.manage')
def close_session(id):
    """Close POS session"""
    session = POSSession.query.get_or_404(id)
    
    if session.cashier_id != current_user.id:
        flash('غير مصرح لك بإغلاق هذه الوردية', 'danger')
        return redirect(url_for('pos.index'))
    
    session.closing_time = datetime.utcnow()
    session.closing_balance = request.form.get('closing_balance', 0, type=float)
    session.status = 'closed'
    
    # Calculate totals
    orders = POSOrder.query.filter_by(session_id=session.id, status='completed').all()
    session.total_sales = sum(order.total_amount for order in orders)
    session.total_cash = sum(order.cash_amount for order in orders)
    session.total_card = sum(order.card_amount for order in orders)
    
    db.session.commit()
    
    flash('تم إغلاق الوردية بنجاح', 'success')
    return redirect(url_for('pos.sessions'))

@bp.route('/sessions')
@login_required
@permission_required('pos.access')
def sessions():
    """List POS sessions"""
    page = request.args.get('page', 1, type=int)
    sessions = POSSession.query.order_by(POSSession.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Get company settings for currency
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('pos/sessions.html', sessions=sessions, currency_symbol=currency_symbol)

@bp.route('/session/<int:id>')
@login_required
@permission_required('pos.access')
def session_details(id):
    """View session details"""
    pos_session = POSSession.query.get_or_404(id)

    # Get company settings for currency
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('pos/session_details.html',
                         pos_session=pos_session,
                         currency_symbol=currency_symbol)

@bp.route('/delete-session/<int:id>', methods=['POST'])
@login_required
@permission_required('pos.session.manage')
def delete_session(id):
    """Delete POS session"""
    session = POSSession.query.get_or_404(id)

    # Check if session has orders
    if session.orders:
        flash(_('Cannot delete session with orders. Please delete orders first.'), 'danger')
        return redirect(url_for('pos.sessions'))

    # Check if session is open
    if session.status == 'open':
        flash(_('Cannot delete an open session. Please close it first.'), 'danger')
        return redirect(url_for('pos.sessions'))

    try:
        session_number = session.session_number
        db.session.delete(session)
        db.session.commit()
        flash(_('Session %(number)s deleted successfully', number=session_number), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('Error deleting session: %(error)s', error=str(e)), 'danger')

    return redirect(url_for('pos.sessions'))

@bp.route('/create-order', methods=['POST'])
@login_required
@permission_required('pos.sell')
def create_order():
    """Create new POS order"""
    try:
        data = request.get_json()

        # Generate order number
        today = datetime.utcnow()
        prefix = f'ORD{today.year}{today.month:02d}{today.day:02d}'
        last_order = POSOrder.query.filter(
            POSOrder.order_number.like(f'{prefix}%')
        ).order_by(POSOrder.id.desc()).first()

        if last_order:
            last_num = int(last_order.order_number[-4:])
            order_number = f'{prefix}{(last_num + 1):04d}'
        else:
            order_number = f'{prefix}0001'

        # Create order
        order = POSOrder(
            order_number=order_number,
            session_id=data['session_id'],
            customer_id=data.get('customer_id'),
            subtotal=data['subtotal'],
            discount_amount=data['discount_amount'],
            tax_amount=data['tax_amount'],
            total_amount=data['total_amount'],
            payment_method=data['payment_method'],
            cash_amount=data['cash_amount'],
            card_amount=data['card_amount'],
            change_amount=max(0, data['cash_amount'] - data['total_amount']) if data['payment_method'] == 'cash' else 0,
            status='completed'
        )

        db.session.add(order)
        db.session.flush()

        # Add order items
        session = POSSession.query.get(data['session_id'])

        for item_data in data['items']:
            item = POSOrderItem(
                order_id=order.id,
                product_id=item_data['productId'],
                quantity=item_data['quantity'],
                unit_price=item_data['price'],
                total=item_data['price'] * item_data['quantity']
            )
            db.session.add(item)

            # Update stock
            stock = Stock.query.filter_by(
                product_id=item_data['productId'],
                warehouse_id=session.warehouse_id
            ).first()

            if stock:
                stock.quantity -= item_data['quantity']

                # Create stock movement
                movement = StockMovement(
                    product_id=item_data['productId'],
                    warehouse_id=session.warehouse_id,
                    movement_type='out',
                    quantity=item_data['quantity'],
                    reference_type='pos_order',
                    reference_id=order.id,
                    notes=f'بيع من نقطة البيع - طلب {order_number}'
                )
                db.session.add(movement)

        # ✅ Create Sales Invoice automatically
        invoice_number = _generate_invoice_number()

        # Get customer_id or use default walk-in customer
        customer_id = data.get('customer_id')
        if not customer_id:
            customer_id = _get_or_create_default_customer()

        invoice = SalesInvoice(
            invoice_number=invoice_number,
            invoice_date=datetime.utcnow().date(),
            customer_id=customer_id,
            warehouse_id=session.warehouse_id,
            subtotal=data['subtotal'],
            discount_amount=data['discount_amount'],
            tax_amount=data['tax_amount'],
            total_amount=data['total_amount'],
            paid_amount=data['total_amount'],  # Fully paid in POS
            remaining_amount=0.0,  # No remaining amount
            notes=f'فاتورة من نقطة البيع - طلب {order_number}',
            pos_order_id=order.id,
            user_id=current_user.id,
            status='paid'  # Automatically mark as paid
        )

        db.session.add(invoice)
        db.session.flush()

        # Add invoice items from POS order items
        for item_data in data['items']:
            product = Product.query.get(item_data['productId'])
            item_total = item_data['price'] * item_data['quantity']

            # Calculate tax for this item
            tax_rate = product.tax_rate if product else 15.0
            item_tax = item_total * (tax_rate / 100)

            invoice_item = SalesInvoiceItem(
                invoice_id=invoice.id,
                product_id=item_data['productId'],
                description=product.name if product else '',
                quantity=item_data['quantity'],
                unit_price=item_data['price'],
                discount_percentage=0.0,
                discount_amount=0.0,
                tax_rate=tax_rate,
                tax_amount=item_tax,
                total=item_total
            )
            db.session.add(invoice_item)

        db.session.commit()

        return jsonify({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number,
            'invoice_id': invoice.id,
            'invoice_number': invoice_number
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@bp.route('/print-receipt/<int:order_id>')
@login_required
@permission_required('pos.access')
def print_receipt(order_id):
    """Print order receipt"""
    order = POSOrder.query.get_or_404(order_id)

    # Get company settings
    company = Company.query.first()

    # Get currency settings
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('pos/receipt.html',
                         order=order,
                         company=company,
                         currency_symbol=currency_symbol,
                         currency_code=currency_code)

@bp.route('/print-session-report/<int:id>')
@login_required
@permission_required('pos.access')
def print_session_report(id):
    """Print session report"""
    session = POSSession.query.get_or_404(id)
    return render_template('pos/session_report.html', session=session)

@bp.route('/create-quotation', methods=['POST'])
@login_required
@permission_required('pos.quotation.create')
def create_quotation():
    """Create quotation from POS cart"""
    try:
        data = request.get_json()

        # Import Quotation model
        from app.models import Quotation, QuotationItem

        # Generate quotation number
        today = datetime.utcnow()
        prefix = f'QUO{today.year}{today.month:02d}'
        last_quotation = Quotation.query.filter(
            Quotation.quotation_number.like(f'{prefix}%')
        ).order_by(Quotation.id.desc()).first()

        if last_quotation:
            last_num = int(last_quotation.quotation_number[-4:])
            quotation_number = f'{prefix}{(last_num + 1):04d}'
        else:
            quotation_number = f'{prefix}0001'

        # Get customer_id or use default walk-in customer
        customer_id = data.get('customer_id')
        if not customer_id:
            customer_id = _get_or_create_default_customer()

        # Create quotation
        quotation = Quotation(
            quotation_number=quotation_number,
            quotation_date=datetime.utcnow().date(),
            customer_id=customer_id,
            subtotal=data['subtotal'],
            discount_amount=data['discount_amount'],
            tax_amount=data['tax_amount'],
            total_amount=data['total_amount'],
            notes=f'عرض سعر من نقطة البيع',
            user_id=current_user.id,
            status='pending'
        )

        db.session.add(quotation)
        db.session.flush()

        # Add quotation items
        for item_data in data['items']:
            product = Product.query.get(item_data['productId'])
            item_total = item_data['price'] * item_data['quantity']

            # Calculate tax for this item
            tax_rate = product.tax_rate if product else 15.0
            item_tax = item_total * (tax_rate / 100)

            quotation_item = QuotationItem(
                quotation_id=quotation.id,
                product_id=item_data['productId'],
                description=product.name if product else '',
                quantity=item_data['quantity'],
                unit_price=item_data['price'],
                tax_rate=tax_rate,
                total=item_total + item_tax
            )
            db.session.add(quotation_item)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم إنشاء عرض السعر بنجاح',
            'quotation_id': quotation.id,
            'quotation_number': quotation_number
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@bp.route('/print-quotation/<int:quotation_id>')
@login_required
@permission_required('pos.access')
def print_quotation(quotation_id):
    """Print quotation"""
    from app.models import Quotation
    quotation = Quotation.query.get_or_404(quotation_id)

    # Get company settings for currency
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('pos/quotation.html',
                         quotation=quotation,
                         company=company,
                         currency_symbol=currency_symbol)


from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.pos import bp
from app import db
from app.models import POSSession, POSOrder, POSOrderItem, Product, Customer, Warehouse
from datetime import datetime

@bp.route('/')
@login_required
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
    
    return render_template('pos/index.html',
                         session=open_session,
                         products=products,
                         customers=customers)

@bp.route('/open-session', methods=['GET', 'POST'])
@login_required
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
def sessions():
    """List POS sessions"""
    page = request.args.get('page', 1, type=int)
    sessions = POSSession.query.order_by(POSSession.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('pos/sessions.html', sessions=sessions)

@bp.route('/session/<int:id>')
@login_required
def session_details(id):
    """View session details"""
    session = POSSession.query.get_or_404(id)
    return render_template('pos/session_details.html', session=session)

@bp.route('/create-order', methods=['POST'])
@login_required
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
        from app.models import Stock, StockMovement
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

        db.session.commit()

        return jsonify({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@bp.route('/print-receipt/<int:order_id>')
@login_required
def print_receipt(order_id):
    """Print order receipt"""
    order = POSOrder.query.get_or_404(order_id)
    return render_template('pos/receipt.html', order=order)

@bp.route('/print-session-report/<int:id>')
@login_required
def print_session_report(id):
    """Print session report"""
    session = POSSession.query.get_or_404(id)
    return render_template('pos/session_report.html', session=session)


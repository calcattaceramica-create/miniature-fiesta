from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.sales import bp
from app import db
from app.models import Customer, SalesInvoice, SalesInvoiceItem, Product, Warehouse, Stock, StockMovement
from app.models_sales import Quotation, QuotationItem
from app.utils.accounting_helper import create_sales_invoice_journal_entry
from datetime import datetime, timedelta

@bp.route('/customers')
@login_required
def customers():
    """List all customers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Customer.query
    
    if search:
        query = query.filter(
            (Customer.name.contains(search)) |
            (Customer.code.contains(search)) |
            (Customer.phone.contains(search))
        )
    
    customers = query.order_by(Customer.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('sales/customers.html',
                         customers=customers,
                         search=search)

@bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    """Add new customer"""
    if request.method == 'POST':
        # Generate customer code
        last_customer = Customer.query.order_by(Customer.id.desc()).first()
        code = f'CUS{(last_customer.id + 1):05d}' if last_customer else 'CUS00001'
        
        customer = Customer(
            code=code,
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            mobile=request.form.get('mobile'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            country=request.form.get('country'),
            tax_number=request.form.get('tax_number'),
            customer_type=request.form.get('customer_type', 'individual'),
            credit_limit=request.form.get('credit_limit', 0, type=float),
            payment_terms=request.form.get('payment_terms', 0, type=int),
            category=request.form.get('category'),
            is_active=True
        )
        
        db.session.add(customer)
        db.session.commit()
        
        flash('تم إضافة العميل بنجاح', 'success')
        return redirect(url_for('sales.customers'))
    
    return render_template('sales/add_customer.html')

@bp.route('/invoices')
@login_required
def invoices():
    """List all sales invoices"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = SalesInvoice.query
    
    if search:
        query = query.filter(SalesInvoice.invoice_number.contains(search))
    
    if status:
        query = query.filter_by(status=status)
    
    invoices = query.order_by(SalesInvoice.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('sales/invoices.html',
                         invoices=invoices,
                         search=search,
                         status=status)

@bp.route('/invoices/add', methods=['GET', 'POST'])
@login_required
def add_invoice():
    """Add new sales invoice"""
    if request.method == 'POST':
        # Generate invoice number
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
        
        invoice = SalesInvoice(
            invoice_number=invoice_number,
            invoice_date=datetime.strptime(request.form.get('invoice_date'), '%Y-%m-%d').date(),
            customer_id=request.form.get('customer_id', type=int),
            warehouse_id=request.form.get('warehouse_id', type=int),
            notes=request.form.get('notes'),
            user_id=current_user.id,
            status='draft'
        )
        
        db.session.add(invoice)
        db.session.flush()  # Get invoice ID
        
        # Add invoice items
        items_data = request.form.getlist('items')
        subtotal = 0
        total_tax = 0
        
        for item_json in items_data:
            import json
            item = json.loads(item_json)
            
            product = Product.query.get(item['product_id'])
            quantity = float(item['quantity'])
            unit_price = float(item['unit_price'])
            discount_percentage = float(item.get('discount_percentage', 0))
            
            line_total = quantity * unit_price
            discount_amount = line_total * (discount_percentage / 100)
            line_total -= discount_amount
            
            tax_amount = line_total * (product.tax_rate / 100)
            line_total += tax_amount
            
            invoice_item = SalesInvoiceItem(
                invoice_id=invoice.id,
                product_id=item['product_id'],
                description=product.name,
                quantity=quantity,
                unit_price=unit_price,
                discount_percentage=discount_percentage,
                discount_amount=discount_amount,
                tax_rate=product.tax_rate,
                tax_amount=tax_amount,
                total=line_total
            )
            
            db.session.add(invoice_item)
            subtotal += (quantity * unit_price - discount_amount)
            total_tax += tax_amount
        
        # Update invoice totals
        invoice.subtotal = subtotal
        invoice.tax_amount = total_tax
        invoice.total_amount = subtotal + total_tax
        invoice.remaining_amount = invoice.total_amount
        
        db.session.commit()
        
        flash('تم إضافة الفاتورة بنجاح', 'success')
        return redirect(url_for('sales.invoices'))
    
    customers = Customer.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True, is_sellable=True).all()
    
    # Get today's date for default value
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')

    return render_template('sales/add_invoice.html',
                         customers=customers,
                         warehouses=warehouses,
                         products=products,
                         today=today)

@bp.route('/invoices/<int:id>')
@login_required
def invoice_details(id):
    """View invoice details"""
    invoice = SalesInvoice.query.get_or_404(id)
    return render_template('sales/invoice_details.html', invoice=invoice)

@bp.route('/invoices/<int:id>/confirm', methods=['POST', 'GET'])
@login_required
def confirm_invoice(id):
    """Confirm sales invoice and update stock"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status != 'draft':
        flash('لا يمكن تأكيد هذه الفاتورة', 'error')
        return redirect(url_for('sales.invoice_details', id=id))

    try:
        # Update invoice status
        invoice.status = 'confirmed'

        # Update stock for each item
        for item in invoice.items:
            # Get stock for this product in the warehouse
            stock = Stock.query.filter_by(
                product_id=item.product_id,
                warehouse_id=invoice.warehouse_id
            ).first()

            if not stock:
                flash(f'المنتج {item.product.name} غير موجود في المستودع', 'error')
                db.session.rollback()
                return redirect(url_for('sales.invoice_details', id=id))

            # Check if enough quantity available
            if stock.quantity < item.quantity:
                flash(f'الكمية المتاحة من {item.product.name} غير كافية. المتاح: {stock.quantity}', 'error')
                db.session.rollback()
                return redirect(url_for('sales.invoice_details', id=id))

            # Reduce stock quantity
            stock.quantity -= item.quantity

            # Create stock movement record
            movement = StockMovement(
                product_id=item.product_id,
                warehouse_id=invoice.warehouse_id,
                movement_type='out',
                quantity=item.quantity,
                reference_type='sales_invoice',
                reference_id=invoice.id,
                notes=f'بيع - فاتورة رقم {invoice.invoice_number}',
                user_id=current_user.id
            )
            db.session.add(movement)

        # Update customer balance
        invoice.customer.current_balance += invoice.total_amount

        # Create accounting journal entry
        try:
            journal_entry = create_sales_invoice_journal_entry(invoice)
            if journal_entry:
                flash(f'تم إنشاء القيد المحاسبي رقم {journal_entry.entry_number}', 'info')
        except Exception as je:
            # Log the error but don't fail the invoice confirmation
            flash(f'تحذير: لم يتم إنشاء القيد المحاسبي: {str(je)}', 'warning')

        db.session.commit()
        flash('تم تأكيد الفاتورة بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تأكيد الفاتورة: {str(e)}', 'error')

    return redirect(url_for('sales.invoice_details', id=id))

@bp.route('/invoices/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete_invoice(id):
    """Delete sales invoice"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status != 'draft':
        flash('لا يمكن حذف فاتورة مؤكدة', 'error')
        return redirect(url_for('sales.invoice_details', id=id))

    try:
        db.session.delete(invoice)
        db.session.commit()
        flash('تم حذف الفاتورة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف الفاتورة: {str(e)}', 'error')

    return redirect(url_for('sales.invoices'))

@bp.route('/invoices/<int:id>/cancel', methods=['POST', 'GET'])
@login_required
def cancel_invoice(id):
    """Cancel sales invoice and restore stock"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status not in ['confirmed', 'draft']:
        flash('لا يمكن إلغاء هذه الفاتورة', 'error')
        return redirect(url_for('sales.invoice_details', id=id))

    try:
        # If invoice was confirmed, restore stock
        if invoice.status == 'confirmed':
            for item in invoice.items:
                stock = Stock.query.filter_by(
                    product_id=item.product_id,
                    warehouse_id=invoice.warehouse_id
                ).first()

                if stock:
                    stock.quantity += item.quantity

                    # Create stock movement record
                    movement = StockMovement(
                        product_id=item.product_id,
                        warehouse_id=invoice.warehouse_id,
                        movement_type='in',
                        quantity=item.quantity,
                        reference_type='sales_invoice_cancel',
                        reference_id=invoice.id,
                        notes=f'إلغاء بيع - فاتورة رقم {invoice.invoice_number}',
                        user_id=current_user.id
                    )
                    db.session.add(movement)

            # Update customer balance
            invoice.customer.current_balance -= invoice.total_amount

        # Update invoice status
        invoice.status = 'cancelled'
        invoice.payment_status = 'unpaid'

        db.session.commit()
        flash('تم إلغاء الفاتورة بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء إلغاء الفاتورة: {str(e)}', 'error')

    return redirect(url_for('sales.invoice_details', id=id))

# ==================== Quotations Routes ====================

@bp.route('/quotations')
@login_required
def quotations():
    """List all quotations"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = Quotation.query

    if search:
        query = query.filter(Quotation.quotation_number.contains(search))

    if status:
        query = query.filter_by(status=status)

    quotations = query.order_by(Quotation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    warehouses = Warehouse.query.filter_by(is_active=True).all()

    from datetime import date
    today = date.today()

    return render_template('sales/quotations.html',
                         quotations=quotations,
                         warehouses=warehouses,
                         today=today,
                         search=search,
                         status=status)

@bp.route('/quotations/add', methods=['GET', 'POST'])
@login_required
def add_quotation():
    """Add new quotation"""
    if request.method == 'POST':
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

        # Parse dates
        quotation_date = datetime.strptime(request.form.get('quotation_date'), '%Y-%m-%d').date()
        valid_days = int(request.form.get('valid_days', 30))
        valid_until = quotation_date + timedelta(days=valid_days)

        quotation = Quotation(
            quotation_number=quotation_number,
            quotation_date=quotation_date,
            valid_until=valid_until,
            customer_id=request.form.get('customer_id', type=int),
            notes=request.form.get('notes'),
            user_id=current_user.id,
            status='draft'
        )

        db.session.add(quotation)
        db.session.flush()  # Get quotation ID

        # Add quotation items
        items_data = request.form.getlist('items')
        subtotal = 0
        total_tax = 0

        for item_json in items_data:
            import json
            item = json.loads(item_json)

            product = Product.query.get(item['product_id'])
            quantity = float(item['quantity'])
            unit_price = float(item['unit_price'])
            discount_percentage = float(item.get('discount_percentage', 0))

            line_total = quantity * unit_price
            discount_amount = line_total * (discount_percentage / 100)
            line_total -= discount_amount

            tax_amount = line_total * (product.tax_rate / 100)
            line_total += tax_amount

            quotation_item = QuotationItem(
                quotation_id=quotation.id,
                product_id=item['product_id'],
                description=product.name,
                quantity=quantity,
                unit_price=unit_price,
                discount_percentage=discount_percentage,
                tax_rate=product.tax_rate,
                total=line_total
            )

            db.session.add(quotation_item)
            subtotal += (quantity * unit_price - discount_amount)
            total_tax += tax_amount

        # Update quotation totals
        quotation.subtotal = subtotal
        quotation.tax_amount = total_tax
        quotation.total_amount = subtotal + total_tax

        db.session.commit()

        flash('تم إضافة عرض السعر بنجاح', 'success')
        return redirect(url_for('sales.quotations'))

    customers = Customer.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True, is_sellable=True).all()

    # Get today's date for default value
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')

    return render_template('sales/add_quotation.html',
                         customers=customers,
                         products=products,
                         today=today)

@bp.route('/quotations/<int:id>')
@login_required
def quotation_details(id):
    """View quotation details"""
    quotation = Quotation.query.get_or_404(id)
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    from datetime import date
    today = date.today()

    return render_template('sales/quotation_details.html',
                         quotation=quotation,
                         warehouses=warehouses,
                         today=today)

@bp.route('/quotations/<int:id>/convert', methods=['POST'])
@login_required
def convert_quotation_to_invoice(id):
    """Convert quotation to sales invoice"""
    quotation = Quotation.query.get_or_404(id)

    if quotation.status not in ['draft', 'sent', 'accepted']:
        flash('لا يمكن تحويل هذا العرض إلى فاتورة', 'error')
        return redirect(url_for('sales.quotation_details', id=id))

    try:
        # Generate invoice number
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

        # Create invoice from quotation
        invoice = SalesInvoice(
            invoice_number=invoice_number,
            invoice_date=datetime.utcnow().date(),
            customer_id=quotation.customer_id,
            warehouse_id=request.form.get('warehouse_id', type=int),
            subtotal=quotation.subtotal,
            tax_amount=quotation.tax_amount,
            total_amount=quotation.total_amount,
            remaining_amount=quotation.total_amount,
            notes=quotation.notes,
            quotation_id=quotation.id,
            user_id=current_user.id,
            status='draft'
        )

        db.session.add(invoice)
        db.session.flush()

        # Copy items from quotation to invoice
        for q_item in quotation.items:
            invoice_item = SalesInvoiceItem(
                invoice_id=invoice.id,
                product_id=q_item.product_id,
                description=q_item.description,
                quantity=q_item.quantity,
                unit_price=q_item.unit_price,
                discount_percentage=q_item.discount_percentage,
                discount_amount=(q_item.quantity * q_item.unit_price) * (q_item.discount_percentage / 100),
                tax_rate=q_item.tax_rate,
                tax_amount=(q_item.quantity * q_item.unit_price - (q_item.quantity * q_item.unit_price) * (q_item.discount_percentage / 100)) * (q_item.tax_rate / 100),
                total=q_item.total
            )
            db.session.add(invoice_item)

        # Update quotation status
        quotation.status = 'accepted'

        db.session.commit()
        flash('تم تحويل عرض السعر إلى فاتورة بنجاح', 'success')
        return redirect(url_for('sales.invoice_details', id=invoice.id))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تحويل عرض السعر: {str(e)}', 'error')
        return redirect(url_for('sales.quotation_details', id=id))

@bp.route('/quotations/<int:id>/update_status', methods=['POST'])
@login_required
def update_quotation_status(id):
    """Update quotation status"""
    quotation = Quotation.query.get_or_404(id)
    new_status = request.form.get('status')

    if new_status in ['draft', 'sent', 'accepted', 'rejected', 'expired']:
        quotation.status = new_status
        db.session.commit()
        flash('تم تحديث حالة عرض السعر بنجاح', 'success')
    else:
        flash('حالة غير صالحة', 'error')

    return redirect(url_for('sales.quotation_details', id=id))

@bp.route('/quotations/<int:id>/delete', methods=['POST'])
@login_required
def delete_quotation(id):
    """Delete quotation"""
    quotation = Quotation.query.get_or_404(id)

    if quotation.status == 'accepted':
        flash('لا يمكن حذف عرض سعر مقبول', 'error')
        return redirect(url_for('sales.quotation_details', id=id))

    try:
        db.session.delete(quotation)
        db.session.commit()
        flash('تم حذف عرض السعر بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف عرض السعر: {str(e)}', 'error')

    return redirect(url_for('sales.quotations'))

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.sales import bp
from app import db
from app.models import Customer, SalesInvoice, SalesInvoiceItem, Product, Warehouse, Stock, StockMovement
from app.models_sales import Quotation, QuotationItem
from app.utils.accounting_helper import create_sales_invoice_journal_entry
from app.auth.decorators import permission_required, any_permission_required
from datetime import datetime, timedelta

@bp.route('/customers')
@login_required
@permission_required('customers.view')
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
@permission_required('customers.create')
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
        
        flash(_('Customer added successfully'), 'success')
        return redirect(url_for('sales.customers'))
    
    return render_template('sales/add_customer.html')

@bp.route('/customers/add_ajax', methods=['POST'])
@login_required
@permission_required('customers.create')
def add_customer_ajax():
    """Add new customer via AJAX (for use in invoice forms)"""
    try:
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

        return jsonify({
            'success': True,
            'message': _('Customer added successfully'),
            'customer': {
                'id': customer.id,
                'code': customer.code,
                'name': customer.name
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@bp.route('/invoices')
@login_required
@permission_required('sales.view')
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
@permission_required('sales.create')
def add_invoice():
    """Add new sales invoice"""
    if request.method == 'POST':
        try:
            print("=== Starting invoice creation ===")
            print("Form data:", request.form)

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

            print(f"Generated invoice number: {invoice_number}")

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

            print(f"Invoice created with ID: {invoice.id}")

            # Add invoice items
            items_data = request.form.getlist('items')
            print(f"Items data received: {len(items_data)} items")

            subtotal = 0
            total_tax = 0

            for item_json in items_data:
                import json
                item = json.loads(item_json)
                print(f"Processing item: {item}")

                product = Product.query.get(item['product_id'])
                if not product:
                    raise Exception(f"Product with ID {item['product_id']} not found")

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

            print(f"Invoice totals - Subtotal: {subtotal}, Tax: {total_tax}, Total: {invoice.total_amount}")

            db.session.commit()

            print("=== Invoice saved successfully ===")

            # Check if user wants to complete the sale immediately
            action = request.form.get('action', 'save_draft')

            if action == 'complete_sale':
                # Redirect to complete_sale route
                flash(_('Invoice created successfully. Completing sale...'), 'info')
                return redirect(url_for('sales.complete_sale', id=invoice.id))
            else:
                flash(_('Invoice added successfully'), 'success')
                return redirect(url_for('sales.invoices'))

        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(_('Error adding invoice: %(error)s', error=str(e)), 'error')
            # Don't redirect, stay on the same page to show the error
    
    customers = Customer.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    products_query = Product.query.filter_by(is_active=True, is_sellable=True).all()

    # Convert products to dictionary for JSON serialization
    products = [{
        'id': p.id,
        'name': p.name,
        'code': p.code,
        'selling_price': float(p.selling_price) if p.selling_price else 0,
        'tax_rate': float(p.tax_rate) if p.tax_rate else 15
    } for p in products_query]

    # Get today's date for default value
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')

    # Get company settings for currency
    from app.models import Company
    from flask import current_app
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('sales/add_invoice.html',
                         customers=customers,
                         warehouses=warehouses,
                         products=products,
                         today=today,
                         currency_code=currency_code,
                         currency_symbol=currency_symbol)

@bp.route('/invoices/<int:id>')
@login_required
@permission_required('sales.view')
def invoice_details(id):
    """View invoice details"""
    invoice = SalesInvoice.query.get_or_404(id)
    return render_template('sales/invoice_details.html', invoice=invoice)

@bp.route('/invoices/<int:id>/customer-receipt')
@login_required
@permission_required('sales.view')
def customer_receipt(id):
    """Print customer receipt"""
    invoice = SalesInvoice.query.get_or_404(id)
    return render_template('sales/customer_receipt.html', invoice=invoice)

@bp.route('/invoices/<int:id>/warehouse-paper')
@login_required
@permission_required('sales.view')
def warehouse_paper(id):
    """Print warehouse paper"""
    invoice = SalesInvoice.query.get_or_404(id)
    return render_template('sales/warehouse_paper.html', invoice=invoice)

@bp.route('/invoices/<int:id>/confirm', methods=['POST', 'GET'])
@login_required
@permission_required('sales.edit')
def confirm_invoice(id):
    """Confirm sales invoice and update stock"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status != 'draft':
        flash(_('Cannot confirm this invoice'), 'error')
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
                flash(_('Product %(name)s not found in warehouse', name=item.product.name), 'error')
                db.session.rollback()
                return redirect(url_for('sales.invoice_details', id=id))

            # Check if enough quantity available
            if stock.quantity < item.quantity:
                flash(_('Insufficient quantity of %(name)s available. Available: %(qty)s', name=item.product.name, qty=stock.quantity), 'error')
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
                flash(_('Journal entry number %(number)s created', number=journal_entry.entry_number), 'info')
        except Exception as je:
            # Log the error but don't fail the invoice confirmation
            flash(_('Warning: Journal entry was not created: %(error)s', error=str(je)), 'warning')

        db.session.commit()
        flash(_('Invoice confirmed successfully'), 'success')

    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while confirming the invoice: %(error)s', error=str(e)), 'error')

    return redirect(url_for('sales.invoice_details', id=id))

@bp.route('/invoices/<int:id>/complete_sale', methods=['POST', 'GET'])
@login_required
@permission_required('sales.complete')
def complete_sale(id):
    """Complete sale: Confirm invoice and mark as paid"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status != 'draft':
        flash(_('Cannot complete this sale. Invoice is already %(status)s', status=invoice.status), 'error')
        return redirect(url_for('sales.invoice_details', id=id))

    try:
        print(f"=== Completing sale for invoice {invoice.invoice_number} ===")

        # Update invoice status to confirmed
        invoice.status = 'confirmed'
        invoice.payment_status = 'paid'
        invoice.paid_amount = invoice.total_amount
        invoice.remaining_amount = 0

        # Update stock for each item
        for item in invoice.items:
            print(f"Processing item: {item.product.name}, Quantity: {item.quantity}")

            # Get stock for this product in the warehouse
            stock = Stock.query.filter_by(
                product_id=item.product_id,
                warehouse_id=invoice.warehouse_id
            ).first()

            if not stock:
                flash(_('Product %(name)s not found in warehouse', name=item.product.name), 'error')
                db.session.rollback()
                return redirect(url_for('sales.invoice_details', id=id))

            # Check if enough quantity available
            if stock.quantity < item.quantity:
                flash(_('Insufficient quantity of %(name)s available. Available: %(qty)s',
                       name=item.product.name, qty=stock.quantity), 'error')
                db.session.rollback()
                return redirect(url_for('sales.invoice_details', id=id))

            # Reduce stock quantity
            old_quantity = stock.quantity
            stock.quantity -= item.quantity
            print(f"Stock updated: {item.product.name} - Old: {old_quantity}, New: {stock.quantity}")

            # Create stock movement record
            movement = StockMovement(
                product_id=item.product_id,
                warehouse_id=invoice.warehouse_id,
                movement_type='out',
                quantity=item.quantity,
                reference_type='sales_invoice',
                reference_id=invoice.id,
                notes=f'بيع مكتمل - فاتورة رقم {invoice.invoice_number}',
                user_id=current_user.id
            )
            db.session.add(movement)

        # Update customer balance (no balance since it's paid)
        # Customer balance remains unchanged for cash sales

        # Create accounting journal entry
        try:
            journal_entry = create_sales_invoice_journal_entry(invoice)
            if journal_entry:
                flash(_('Journal entry number %(number)s created', number=journal_entry.entry_number), 'info')
        except Exception as je:
            # Log the error but don't fail the sale completion
            print(f"Journal entry error: {str(je)}")
            flash(_('Warning: Journal entry was not created: %(error)s', error=str(je)), 'warning')

        db.session.commit()
        print(f"=== Sale completed successfully for invoice {invoice.invoice_number} ===")
        flash(_('Sale completed successfully! Invoice confirmed and marked as paid.'), 'success')

    except Exception as e:
        db.session.rollback()
        print(f"ERROR completing sale: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(_('An error occurred while completing the sale: %(error)s', error=str(e)), 'error')

    return redirect(url_for('sales.invoice_details', id=id))

@bp.route('/invoices/<int:id>/delete', methods=['POST', 'GET'])
@login_required
@permission_required('sales.delete')
def delete_invoice(id):
    """Delete sales invoice"""
    invoice = SalesInvoice.query.get_or_404(id)

    try:
        # If invoice was confirmed or paid, restore stock and update customer balance
        if invoice.status in ['confirmed', 'paid']:
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
                        reference_type='sales_invoice_delete',
                        reference_id=invoice.id,
                        notes=f'حذف فاتورة مبيعات رقم {invoice.invoice_number}',
                        user_id=current_user.id
                    )
                    db.session.add(movement)

            # Update customer balance
            invoice.customer.current_balance -= invoice.total_amount

        # Delete invoice
        db.session.delete(invoice)
        db.session.commit()
        flash(_('Invoice deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while deleting the invoice: %(error)s', error=str(e)), 'error')

    return redirect(url_for('sales.invoices'))

@bp.route('/invoices/<int:id>/cancel', methods=['POST', 'GET'])
@login_required
@permission_required('sales.cancel')
def cancel_invoice(id):
    """Cancel sales invoice and restore stock"""
    invoice = SalesInvoice.query.get_or_404(id)

    if invoice.status not in ['confirmed', 'draft']:
        flash(_('Cannot cancel this invoice'), 'error')
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
        flash(_('Invoice cancelled successfully'), 'success')

    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while cancelling the invoice: %(error)s', error=str(e)), 'error')

    return redirect(url_for('sales.invoice_details', id=id))

# ==================== Quotations Routes ====================

@bp.route('/quotations')
@login_required
@permission_required('sales.quotations')
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
@permission_required('sales.quotations')
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

        flash(_('Quotation added successfully'), 'success')
        return redirect(url_for('sales.quotations'))

    customers = Customer.query.filter_by(is_active=True).all()
    products_query = Product.query.filter_by(is_active=True, is_sellable=True).all()

    # Convert products to dictionary for JSON serialization
    products = [{
        'id': p.id,
        'name': p.name,
        'code': p.code,
        'selling_price': float(p.selling_price) if p.selling_price else 0,
        'tax_rate': float(p.tax_rate) if p.tax_rate else 15
    } for p in products_query]

    # Get today's date for default value
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')

    # Get company settings for currency
    from app.models import Company
    from flask import current_app
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('sales/add_quotation.html',
                         customers=customers,
                         products=products,
                         today=today,
                         currency_code=currency_code,
                         currency_symbol=currency_symbol)

@bp.route('/quotations/<int:id>')
@login_required
@permission_required('sales.quotations')
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
@permission_required('sales.quotations')
def convert_quotation_to_invoice(id):
    """Convert quotation to sales invoice"""
    quotation = Quotation.query.get_or_404(id)

    if quotation.status not in ['draft', 'sent', 'accepted']:
        flash(_('Cannot convert this quotation to invoice'), 'error')
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
        flash(_('Quotation converted to invoice successfully'), 'success')
        return redirect(url_for('sales.invoice_details', id=invoice.id))

    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while converting quotation: %(error)s', error=str(e)), 'error')
        return redirect(url_for('sales.quotation_details', id=id))

@bp.route('/quotations/<int:id>/update_status', methods=['POST'])
@login_required
@permission_required('sales.quotations')
def update_quotation_status(id):
    """Update quotation status"""
    quotation = Quotation.query.get_or_404(id)
    new_status = request.form.get('status')

    if new_status in ['draft', 'sent', 'accepted', 'rejected', 'expired']:
        quotation.status = new_status
        db.session.commit()
        flash(_('Quotation status updated successfully'), 'success')
    else:
        flash(_('Invalid status'), 'error')

    return redirect(url_for('sales.quotation_details', id=id))

@bp.route('/quotations/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('sales.quotations')
def delete_quotation(id):
    """Delete quotation"""
    quotation = Quotation.query.get_or_404(id)

    if quotation.status == 'accepted':
        flash(_('Cannot delete an accepted quotation'), 'error')
        return redirect(url_for('sales.quotation_details', id=id))

    try:
        db.session.delete(quotation)
        db.session.commit()
        flash(_('Quotation deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while deleting quotation: %(error)s', error=str(e)), 'error')

    return redirect(url_for('sales.quotations'))

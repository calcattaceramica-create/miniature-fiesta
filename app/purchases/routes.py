from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.purchases import bp
from app import db
from app.models import Supplier, PurchaseInvoice, PurchaseInvoiceItem, Product, Warehouse, Stock, StockMovement
from app.utils.accounting_helper import create_purchase_invoice_journal_entry
from app.auth.decorators import permission_required, any_permission_required
from datetime import datetime

@bp.route('/suppliers')
@login_required
@permission_required('suppliers.view')
def suppliers():
    """List all suppliers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Supplier.query
    
    if search:
        query = query.filter(
            (Supplier.name.contains(search)) |
            (Supplier.code.contains(search)) |
            (Supplier.phone.contains(search))
        )
    
    suppliers = query.order_by(Supplier.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('purchases/suppliers.html',
                         suppliers=suppliers,
                         search=search)

@bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
@permission_required('suppliers.create')
def add_supplier():
    """Add new supplier"""
    if request.method == 'POST':
        # Generate supplier code
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        code = f'SUP{(last_supplier.id + 1):05d}' if last_supplier else 'SUP00001'
        
        supplier = Supplier(
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
            credit_limit=request.form.get('credit_limit', 0, type=float),
            payment_terms=request.form.get('payment_terms', 0, type=int),
            category=request.form.get('category'),
            is_active=True
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        flash(_('Supplier added successfully'), 'success')
        return redirect(url_for('purchases.suppliers'))
    
    return render_template('purchases/add_supplier.html')

@bp.route('/suppliers/<int:id>')
@login_required
@permission_required('suppliers.view')
def supplier_details(id):
    """View supplier details"""
    supplier = Supplier.query.get_or_404(id)
    return render_template('purchases/supplier_details.html', supplier=supplier)

@bp.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('suppliers.edit')
def edit_supplier(id):
    """Edit supplier"""
    supplier = Supplier.query.get_or_404(id)

    if request.method == 'POST':
        try:
            supplier.name = request.form.get('name')
            supplier.name_en = request.form.get('name_en')
            supplier.email = request.form.get('email')
            supplier.phone = request.form.get('phone')
            supplier.mobile = request.form.get('mobile')
            supplier.address = request.form.get('address')
            supplier.city = request.form.get('city')
            supplier.country = request.form.get('country')
            supplier.tax_number = request.form.get('tax_number')
            supplier.credit_limit = request.form.get('credit_limit', 0, type=float)
            supplier.payment_terms = request.form.get('payment_terms', 0, type=int)
            supplier.category = request.form.get('category')

            db.session.commit()
            flash(_('Supplier updated successfully'), 'success')
            return redirect(url_for('purchases.suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')

    return render_template('purchases/edit_supplier.html', supplier=supplier)

@bp.route('/invoices')
@login_required
@permission_required('purchases.view')
def invoices():
    """List all purchase invoices"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = PurchaseInvoice.query
    
    if search:
        query = query.filter(PurchaseInvoice.invoice_number.contains(search))
    
    if status:
        query = query.filter_by(status=status)
    
    invoices = query.order_by(PurchaseInvoice.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('purchases/invoices.html',
                         invoices=invoices,
                         search=search,
                         status=status)

@bp.route('/invoices/add', methods=['GET', 'POST'])
@login_required
@permission_required('purchases.create')
def add_invoice():
    """Add new purchase invoice"""
    if request.method == 'POST':
        # Generate invoice number
        today = datetime.utcnow()
        prefix = f'PINV{today.year}{today.month:02d}'
        last_invoice = PurchaseInvoice.query.filter(
            PurchaseInvoice.invoice_number.like(f'{prefix}%')
        ).order_by(PurchaseInvoice.id.desc()).first()
        
        if last_invoice:
            last_num = int(last_invoice.invoice_number[-4:])
            invoice_number = f'{prefix}{(last_num + 1):04d}'
        else:
            invoice_number = f'{prefix}0001'
        
        invoice = PurchaseInvoice(
            invoice_number=invoice_number,
            invoice_date=datetime.strptime(request.form.get('invoice_date'), '%Y-%m-%d').date(),
            supplier_id=request.form.get('supplier_id', type=int),
            warehouse_id=request.form.get('warehouse_id', type=int),
            supplier_invoice_number=request.form.get('supplier_invoice_number'),
            notes=request.form.get('notes'),
            user_id=current_user.id,
            status='draft'
        )

        db.session.add(invoice)
        db.session.flush()  # Get invoice ID before adding items

        # Add invoice items
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')
        discount_percents = request.form.getlist('discount_percent[]')
        tax_percents = request.form.getlist('tax_percent[]')

        # Initialize invoice totals
        invoice_subtotal = 0
        invoice_discount = 0
        invoice_tax = 0

        for i in range(len(product_ids)):
            if product_ids[i]:  # Skip empty rows
                quantity = float(quantities[i])
                unit_price = float(unit_prices[i])
                discount_percentage = float(discount_percents[i]) if discount_percents[i] else 0
                tax_rate = float(tax_percents[i]) if tax_percents[i] else 0

                # Calculate item totals
                item_subtotal = quantity * unit_price
                item_discount = item_subtotal * (discount_percentage / 100)
                taxable_amount = item_subtotal - item_discount
                item_tax = taxable_amount * (tax_rate / 100)
                item_total = taxable_amount + item_tax

                # Add to invoice totals
                invoice_subtotal += item_subtotal
                invoice_discount += item_discount
                invoice_tax += item_tax

                item = PurchaseInvoiceItem(
                    invoice_id=invoice.id,
                    product_id=int(product_ids[i]),
                    quantity=quantity,
                    unit_price=unit_price,
                    discount_percentage=discount_percentage,
                    tax_rate=tax_rate,
                    total=item_total
                )
                db.session.add(item)

        # Update invoice totals
        invoice.subtotal = invoice_subtotal
        invoice.discount_amount = invoice_discount
        invoice.tax_amount = invoice_tax
        invoice.total_amount = invoice_subtotal - invoice_discount + invoice_tax
        invoice.paid_amount = 0
        invoice.remaining_amount = invoice.total_amount

        db.session.commit()

        flash(_('Purchase invoice added successfully'), 'success')
        return redirect(url_for('purchases.invoices'))
    
    suppliers = Supplier.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True, is_purchasable=True).all()

    # Get company settings for currency
    from app.models import Company
    from flask import current_app
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('purchases/add_invoice.html',
                         suppliers=suppliers,
                         warehouses=warehouses,
                         products=products,
                         currency_code=currency_code,
                         currency_symbol=currency_symbol)

@bp.route('/invoices/<int:id>')
@login_required
@permission_required('purchases.view')
def invoice_details(id):
    """View purchase invoice details"""
    invoice = PurchaseInvoice.query.get_or_404(id)
    return render_template('purchases/invoice_details.html', invoice=invoice)

@bp.route('/invoices/<int:id>/confirm', methods=['GET', 'POST'])
@login_required
@permission_required('purchases.edit')
def confirm_invoice(id):
    """Confirm purchase invoice and add stock"""
    invoice = PurchaseInvoice.query.get_or_404(id)

    if invoice.status != 'draft':
        flash(_('Cannot confirm this invoice'), 'error')
        return redirect(url_for('purchases.invoice_details', id=id))

    if request.method == 'POST':
        try:
            # Update invoice status and mark as paid
            invoice.status = 'confirmed'
            invoice.payment_status = 'paid'
            invoice.paid_amount = invoice.total_amount
            invoice.remaining_amount = 0

            # Add stock for each item
            for item in invoice.items:
                # Get or create stock record
                stock = Stock.query.filter_by(
                    product_id=item.product_id,
                    warehouse_id=invoice.warehouse_id
                ).first()

                if not stock:
                    stock = Stock(
                        product_id=item.product_id,
                        warehouse_id=invoice.warehouse_id,
                        quantity=0
                    )
                    db.session.add(stock)

                # Add quantity
                stock.quantity += item.quantity

                # Create stock movement record
                movement = StockMovement(
                    product_id=item.product_id,
                    warehouse_id=invoice.warehouse_id,
                    movement_type='in',
                    quantity=item.quantity,
                    reference_type='purchase_invoice',
                    reference_id=invoice.id,
                    notes=f'فاتورة شراء رقم {invoice.invoice_number}',
                    user_id=current_user.id
                )
                db.session.add(movement)

            # Update supplier balance
            invoice.supplier.current_balance += invoice.total_amount

            # Create accounting journal entry
            try:
                journal_entry = create_purchase_invoice_journal_entry(invoice)
                if journal_entry:
                    flash(_('Journal entry number %(number)s created', number=journal_entry.entry_number), 'info')
            except Exception as je:
                # Log the error but don't fail the invoice confirmation
                flash(_('Warning: Journal entry was not created: %(error)s', error=str(je)), 'warning')

            db.session.commit()
            flash(_('Purchase invoice confirmed successfully'), 'success')
            return redirect(url_for('purchases.invoice_details', id=id))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')
            return redirect(url_for('purchases.invoice_details', id=id))

    # Get company settings for currency
    from app.models import Company
    from flask import current_app
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

    return render_template('purchases/confirm_invoice.html',
                         invoice=invoice,
                         currency_symbol=currency_symbol,
                         currency_code=currency_code)

@bp.route('/invoices/<int:id>/cancel', methods=['GET', 'POST'])
@login_required
@permission_required('purchases.cancel')
def cancel_invoice(id):
    """Cancel purchase invoice and remove stock"""
    invoice = PurchaseInvoice.query.get_or_404(id)

    if invoice.status != 'confirmed':
        flash(_('Cannot cancel this invoice'), 'error')
        return redirect(url_for('purchases.invoice_details', id=id))

    if request.method == 'POST':
        try:
            # Update invoice status
            invoice.status = 'cancelled'

            # Remove stock for each item
            for item in invoice.items:
                stock = Stock.query.filter_by(
                    product_id=item.product_id,
                    warehouse_id=invoice.warehouse_id
                ).first()

                if stock:
                    stock.quantity -= item.quantity

                    # Create stock movement record
                    movement = StockMovement(
                        product_id=item.product_id,
                        warehouse_id=invoice.warehouse_id,
                        movement_type='out',
                        quantity=item.quantity,
                        reference_type='purchase_invoice_cancel',
                        reference_id=invoice.id,
                        notes=f'إلغاء فاتورة شراء رقم {invoice.invoice_number}',
                        user_id=current_user.id
                    )
                    db.session.add(movement)

            # Update supplier balance
            invoice.supplier.current_balance -= invoice.total_amount

            db.session.commit()
            flash(_('Purchase invoice cancelled successfully'), 'success')
            return redirect(url_for('purchases.invoice_details', id=id))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')
            return redirect(url_for('purchases.invoice_details', id=id))

    return render_template('purchases/cancel_invoice.html', invoice=invoice)

@bp.route('/invoices/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@permission_required('purchases.delete')
def delete_invoice(id):
    """Delete purchase invoice"""
    invoice = PurchaseInvoice.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # If invoice was confirmed, remove stock and update supplier balance
            if invoice.status == 'confirmed':
                for item in invoice.items:
                    stock = Stock.query.filter_by(
                        product_id=item.product_id,
                        warehouse_id=invoice.warehouse_id
                    ).first()

                    if stock:
                        stock.quantity -= item.quantity

                        # Create stock movement record
                        movement = StockMovement(
                            product_id=item.product_id,
                            warehouse_id=invoice.warehouse_id,
                            movement_type='out',
                            quantity=item.quantity,
                            reference_type='purchase_invoice_delete',
                            reference_id=invoice.id,
                            notes=f'حذف فاتورة مشتريات رقم {invoice.invoice_number}',
                            user_id=current_user.id
                        )
                        db.session.add(movement)

                # Update supplier balance
                invoice.supplier.current_balance -= invoice.total_amount

            # Delete invoice
            db.session.delete(invoice)
            db.session.commit()
            flash(_('Purchase invoice deleted successfully'), 'success')
            return redirect(url_for('purchases.invoices'))
        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')
            return redirect(url_for('purchases.invoice_details', id=id))

    return render_template('purchases/delete_invoice.html', invoice=invoice)

@bp.route('/suppliers/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('suppliers.delete')
def delete_supplier(id):
    """Delete supplier"""
    try:
        supplier = Supplier.query.get_or_404(id)

        # Check if supplier has purchase invoices
        if supplier.purchase_invoices:
            flash(_('Cannot delete supplier because it has purchase invoices'), 'error')
            # Check referer to redirect to correct page
            referer = request.referrer
            if referer and 'reports/suppliers' in referer:
                return redirect(url_for('reports.suppliers_list'))
            return redirect(url_for('purchases.suppliers'))

        # Delete supplier
        db.session.delete(supplier)
        db.session.commit()
        flash(_('Supplier deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'error')

    # Check referer to redirect to correct page
    referer = request.referrer
    if referer and 'reports/suppliers' in referer:
        return redirect(url_for('reports.suppliers_list'))
    return redirect(url_for('purchases.suppliers'))

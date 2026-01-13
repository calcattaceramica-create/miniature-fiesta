from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.inventory import bp
from app import db
from app.models import Product, Category, Unit, Warehouse, Stock, StockMovement, Branch, User
from app.models_sales import SalesInvoiceItem, QuotationItem
from app.models_purchases import PurchaseInvoiceItem, PurchaseOrderItem, PurchaseReturnItem
from app.models_pos import POSOrderItem
from datetime import datetime

@bp.route('/products')
@login_required
def products():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    
    query = Product.query
    
    if search:
        query = query.filter(
            (Product.name.contains(search)) |
            (Product.code.contains(search)) |
            (Product.barcode.contains(search))
        )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('inventory/products.html',
                         products=products,
                         categories=categories,
                         search=search,
                         category_id=category_id)

@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add new product"""
    if request.method == 'POST':
        try:
            # Get code, barcode and SKU, set to None if empty
            code = request.form.get('code')
            barcode = request.form.get('barcode') or None
            sku = request.form.get('sku') or None

            # Check if code already exists (required field)
            if code:
                existing_code = Product.query.filter_by(code=code).first()
                if existing_code:
                    flash(f'كود المنتج {code} موجود مسبقاً للمنتج: {existing_code.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    warehouses = Warehouse.query.filter_by(is_active=True).all()
                    return render_template('inventory/add_product.html',
                                         categories=categories,
                                         units=units,
                                         warehouses=warehouses)

            # Check if barcode already exists (if provided)
            if barcode:
                existing_barcode = Product.query.filter_by(barcode=barcode).first()
                if existing_barcode:
                    flash(f'الباركود {barcode} موجود مسبقاً للمنتج: {existing_barcode.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    warehouses = Warehouse.query.filter_by(is_active=True).all()
                    return render_template('inventory/add_product.html',
                                         categories=categories,
                                         units=units,
                                         warehouses=warehouses)

            # Check if SKU already exists (if provided)
            if sku:
                existing_sku = Product.query.filter_by(sku=sku).first()
                if existing_sku:
                    flash(f'SKU {sku} موجود مسبقاً للمنتج: {existing_sku.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    warehouses = Warehouse.query.filter_by(is_active=True).all()
                    return render_template('inventory/add_product.html',
                                         categories=categories,
                                         units=units,
                                         warehouses=warehouses)

            product = Product(
                name=request.form.get('name'),
                name_en=request.form.get('name_en'),
                code=request.form.get('code'),
                barcode=barcode,
                sku=sku,
                category_id=request.form.get('category_id', type=int),
                unit_id=request.form.get('unit_id', type=int),
                description=request.form.get('description'),
                cost_price=request.form.get('cost_price', 0, type=float),
                selling_price=request.form.get('selling_price', 0, type=float),
                min_price=request.form.get('min_price', 0, type=float),
                min_stock=request.form.get('min_stock', 0, type=float),
                max_stock=request.form.get('max_stock', 0, type=float),
                reorder_level=request.form.get('reorder_level', 0, type=float),
                tax_rate=request.form.get('tax_rate', 15.0, type=float),
                is_active=request.form.get('is_active') == 'on',
                is_sellable=request.form.get('is_sellable') == 'on',
                is_purchasable=request.form.get('is_purchasable') == 'on',
                track_inventory=request.form.get('track_inventory') == 'on',
            )

            db.session.add(product)
            db.session.flush()  # Get product ID before adding stock

            # Add initial stock for each warehouse
            stock_added = False
            for key in request.form.keys():
                if key.startswith('warehouse_'):
                    warehouse_id = int(key.split('_')[1])
                    quantity = request.form.get(key, 0, type=float)

                    if quantity > 0:
                        stock = Stock(
                            product_id=product.id,
                            warehouse_id=warehouse_id,
                            quantity=quantity,
                            available_quantity=quantity
                        )
                        db.session.add(stock)

                        # Create stock movement record
                        movement = StockMovement(
                            product_id=product.id,
                            warehouse_id=warehouse_id,
                            movement_type='in',
                            quantity=quantity,
                            reference_type='initial_stock',
                            reference_id=product.id,
                            notes='رصيد افتتاحي عند إضافة المنتج',
                            user_id=current_user.id
                        )
                        db.session.add(movement)
                        stock_added = True

            db.session.commit()

            if stock_added:
                flash('تم إضافة المنتج والمخزون بنجاح', 'success')
            else:
                flash('تم إضافة المنتج بنجاح', 'success')

            return redirect(url_for('inventory.products'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'error')

    categories = Category.query.filter_by(is_active=True).all()
    units = Unit.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    return render_template('inventory/add_product.html',
                         categories=categories,
                         units=units,
                         warehouses=warehouses)

@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Get code, barcode and SKU, set to None if empty
            code = request.form.get('code')
            barcode = request.form.get('barcode') or None
            sku = request.form.get('sku') or None

            # Check if code already exists for another product (if changed)
            if code and code != product.code:
                existing_code = Product.query.filter_by(code=code).first()
                if existing_code and existing_code.id != product.id:
                    flash(f'كود المنتج {code} موجود مسبقاً للمنتج: {existing_code.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    return render_template('inventory/edit_product.html',
                                         product=product,
                                         categories=categories,
                                         units=units)

            # Check if barcode already exists for another product (if provided)
            if barcode and barcode != product.barcode:
                existing_barcode = Product.query.filter_by(barcode=barcode).first()
                if existing_barcode and existing_barcode.id != product.id:
                    flash(f'الباركود {barcode} موجود مسبقاً للمنتج: {existing_barcode.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    return render_template('inventory/edit_product.html',
                                         product=product,
                                         categories=categories,
                                         units=units)

            # Check if SKU already exists for another product (if provided)
            if sku and sku != product.sku:
                existing_sku = Product.query.filter_by(sku=sku).first()
                if existing_sku and existing_sku.id != product.id:
                    flash(f'SKU {sku} موجود مسبقاً للمنتج: {existing_sku.name}', 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    return render_template('inventory/edit_product.html',
                                         product=product,
                                         categories=categories,
                                         units=units)

            product.name = request.form.get('name')
            product.name_en = request.form.get('name_en')
            product.code = request.form.get('code')
            product.barcode = barcode
            product.sku = sku
            product.category_id = request.form.get('category_id', type=int)
            product.unit_id = request.form.get('unit_id', type=int)
            product.description = request.form.get('description')
            product.cost_price = request.form.get('cost_price', 0, type=float)
            product.selling_price = request.form.get('selling_price', 0, type=float)
            product.min_price = request.form.get('min_price', 0, type=float)
            product.min_stock = request.form.get('min_stock', 0, type=float)
            product.max_stock = request.form.get('max_stock', 0, type=float)
            product.reorder_level = request.form.get('reorder_level', 0, type=float)
            product.tax_rate = request.form.get('tax_rate', 15.0, type=float)
            product.is_active = request.form.get('is_active') == 'on'
            product.is_sellable = request.form.get('is_sellable') == 'on'
            product.is_purchasable = request.form.get('is_purchasable') == 'on'
            product.track_inventory = request.form.get('track_inventory') == 'on'
            product.updated_at = datetime.utcnow()

            db.session.commit()

            flash('تم تحديث المنتج بنجاح', 'success')
            return redirect(url_for('inventory.products'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'error')
    
    categories = Category.query.filter_by(is_active=True).all()
    units = Unit.query.filter_by(is_active=True).all()
    
    return render_template('inventory/edit_product.html',
                         product=product,
                         categories=categories,
                         units=units)

@bp.route('/products/<int:id>/delete', methods=['POST', 'DELETE'])
@login_required
def delete_product(id):
    """Delete product (soft delete by default, hard delete if force=true)"""
    product = Product.query.get_or_404(id)
    force_delete = request.form.get('force') == 'true' or request.args.get('force') == 'true'

    try:
        # Check for related records
        relations = []

        # Check sales invoice items
        sales_items = SalesInvoiceItem.query.filter_by(product_id=id).count()
        if sales_items > 0:
            relations.append(f'فواتير مبيعات ({sales_items})')

        # Check quotation items
        quotation_items = QuotationItem.query.filter_by(product_id=id).count()
        if quotation_items > 0:
            relations.append(f'عروض أسعار ({quotation_items})')

        # Check purchase invoice items
        purchase_items = PurchaseInvoiceItem.query.filter_by(product_id=id).count()
        if purchase_items > 0:
            relations.append(f'فواتير مشتريات ({purchase_items})')

        # Check purchase order items
        purchase_order_items = PurchaseOrderItem.query.filter_by(product_id=id).count()
        if purchase_order_items > 0:
            relations.append(f'طلبات شراء ({purchase_order_items})')

        # Check purchase return items
        purchase_return_items = PurchaseReturnItem.query.filter_by(product_id=id).count()
        if purchase_return_items > 0:
            relations.append(f'مرتجعات مشتريات ({purchase_return_items})')

        # Check POS order items
        pos_items = POSOrderItem.query.filter_by(product_id=id).count()
        if pos_items > 0:
            relations.append(f'طلبات نقاط البيع ({pos_items})')

        # Check stock records
        stock_records = Stock.query.filter_by(product_id=id).count()
        if stock_records > 0:
            relations.append(f'سجلات مخزون ({stock_records})')

        # Check stock movements
        stock_movements = StockMovement.query.filter_by(product_id=id).count()
        if stock_movements > 0:
            relations.append(f'حركات مخزون ({stock_movements})')

        # If there are relations and not forcing delete
        if relations and not force_delete:
            relations_text = '، '.join(relations)
            flash(f'لا يمكن حذف المنتج "{product.name}" لأنه مرتبط بـ: {relations_text}. سيتم تعطيل المنتج بدلاً من حذفه.', 'warning')
            product.is_active = False
            db.session.commit()
            return redirect(url_for('inventory.products'))

        # If forcing delete or no relations, perform hard delete
        if force_delete and relations:
            # Delete all related records first
            SalesInvoiceItem.query.filter_by(product_id=id).delete()
            QuotationItem.query.filter_by(product_id=id).delete()
            PurchaseInvoiceItem.query.filter_by(product_id=id).delete()
            PurchaseOrderItem.query.filter_by(product_id=id).delete()
            PurchaseReturnItem.query.filter_by(product_id=id).delete()
            POSOrderItem.query.filter_by(product_id=id).delete()
            Stock.query.filter_by(product_id=id).delete()
            StockMovement.query.filter_by(product_id=id).delete()
            flash(f'تم حذف المنتج "{product.name}" وجميع السجلات المرتبطة به نهائياً', 'success')

        # Delete the product
        db.session.delete(product)
        db.session.commit()

        if not force_delete:
            flash(f'تم حذف المنتج "{product.name}" بنجاح', 'success')

        return redirect(url_for('inventory.products'))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف المنتج: {str(e)}', 'error')
        return redirect(url_for('inventory.products'))

@bp.route('/categories')
@login_required
def categories():
    """List all categories"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return render_template('inventory/categories.html', categories=categories)
    except Exception as e:
        flash(f'خطأ في تحميل الصفحة: {str(e)}', 'error')
        return redirect(url_for('inventory.products'))

@bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    """Add new category"""
    try:
        category = Category(
            name=request.form.get('name'),
            description=request.form.get('description'),
            is_active=bool(request.form.get('is_active'))
        )
        db.session.add(category)
        db.session.commit()
        flash('تم إضافة التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/edit_category/<int:id>', methods=['POST'])
@login_required
def edit_category(id):
    """Edit category"""
    try:
        category = Category.query.get_or_404(id)
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        category.is_active = bool(request.form.get('is_active'))
        db.session.commit()
        flash('تم تحديث التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/delete_category/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    """Delete category"""
    try:
        category = Category.query.get_or_404(id)
        # Check if category has products
        if category.products:
            flash('لا يمكن حذف التصنيف لأنه يحتوي على منتجات', 'error')
        else:
            db.session.delete(category)
            db.session.commit()
            flash('تم حذف التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/stock')
@login_required
def stock():
    """View stock levels"""
    page = request.args.get('page', 1, type=int)
    warehouse_id = request.args.get('warehouse', type=int)
    
    query = Stock.query.join(Product).join(Warehouse)
    
    if warehouse_id:
        query = query.filter(Stock.warehouse_id == warehouse_id)
    
    stocks = query.order_by(Product.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    
    return render_template('inventory/stock.html',
                         stocks=stocks,
                         warehouses=warehouses,
                         warehouse_id=warehouse_id)

@bp.route('/warehouses')
@login_required
def warehouses():
    """List all warehouses"""
    warehouses = Warehouse.query.order_by(Warehouse.created_at.desc()).all()
    branches = Branch.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()
    return render_template('inventory/warehouses.html',
                         warehouses=warehouses,
                         branches=branches,
                         users=users)

@bp.route('/warehouses/add', methods=['POST'])
@login_required
def add_warehouse():
    """Add new warehouse"""
    try:
        warehouse = Warehouse(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            code=request.form.get('code'),
            branch_id=request.form.get('branch_id') or None,
            address=request.form.get('address'),
            manager_id=request.form.get('manager_id') or None,
            is_active=bool(request.form.get('is_active'))
        )

        db.session.add(warehouse)
        db.session.commit()

        flash('تم إضافة المستودع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>/edit', methods=['POST'])
@login_required
def edit_warehouse(id):
    """Edit warehouse"""
    warehouse = Warehouse.query.get_or_404(id)

    try:
        warehouse.name = request.form.get('name')
        warehouse.name_en = request.form.get('name_en')
        warehouse.code = request.form.get('code')
        warehouse.branch_id = request.form.get('branch_id') or None
        warehouse.address = request.form.get('address')
        warehouse.manager_id = request.form.get('manager_id') or None
        warehouse.is_active = bool(request.form.get('is_active'))

        db.session.commit()
        flash('تم تحديث المستودع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>/delete', methods=['POST'])
@login_required
def delete_warehouse(id):
    """Delete warehouse"""
    warehouse = Warehouse.query.get_or_404(id)

    # Check if warehouse has stock
    if warehouse.stocks:
        flash('لا يمكن حذف المستودع لأنه يحتوي على مخزون', 'danger')
        return redirect(url_for('inventory.warehouses'))

    try:
        db.session.delete(warehouse)
        db.session.commit()
        flash('تم حذف المستودع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>')
@login_required
def warehouse_details(id):
    """View warehouse details"""
    warehouse = Warehouse.query.get_or_404(id)

    # Get stock in this warehouse
    stocks = Stock.query.filter_by(warehouse_id=id).join(Product).order_by(Product.name).all()

    # Calculate statistics
    total_products = len(stocks)
    total_value = sum(stock.quantity * stock.product.cost_price for stock in stocks)
    low_stock_count = sum(1 for stock in stocks if stock.quantity <= stock.product.min_stock_level)

    return render_template('inventory/warehouse_details.html',
                         warehouse=warehouse,
                         stocks=stocks,
                         total_products=total_products,
                         total_value=total_value,
                         low_stock_count=low_stock_count)

@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def stock_transfer():
    """Transfer stock between warehouses"""
    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id')
            from_warehouse_id = request.form.get('from_warehouse_id')
            to_warehouse_id = request.form.get('to_warehouse_id')
            quantity = float(request.form.get('quantity'))
            notes = request.form.get('notes')

            # Validate
            if from_warehouse_id == to_warehouse_id:
                flash('لا يمكن النقل إلى نفس المستودع', 'danger')
                return redirect(url_for('inventory.stock_transfer'))

            # Get source stock
            from_stock = Stock.query.filter_by(
                product_id=product_id,
                warehouse_id=from_warehouse_id
            ).first()

            if not from_stock or from_stock.available_quantity < quantity:
                flash('الكمية المتاحة غير كافية', 'danger')
                return redirect(url_for('inventory.stock_transfer'))

            # Get or create destination stock
            to_stock = Stock.query.filter_by(
                product_id=product_id,
                warehouse_id=to_warehouse_id
            ).first()

            if not to_stock:
                to_stock = Stock(
                    product_id=product_id,
                    warehouse_id=to_warehouse_id,
                    quantity=0,
                    reserved_quantity=0,
                    available_quantity=0
                )
                db.session.add(to_stock)

            # Update stocks
            from_stock.quantity -= quantity
            from_stock.available_quantity -= quantity
            to_stock.quantity += quantity
            to_stock.available_quantity += quantity

            # Create stock movements
            out_movement = StockMovement(
                product_id=product_id,
                warehouse_id=from_warehouse_id,
                movement_type='out',
                quantity=quantity,
                reference_type='transfer',
                notes=f'نقل إلى مستودع {to_stock.warehouse.name}. {notes or ""}',
                created_by=current_user.id
            )

            in_movement = StockMovement(
                product_id=product_id,
                warehouse_id=to_warehouse_id,
                movement_type='in',
                quantity=quantity,
                reference_type='transfer',
                notes=f'نقل من مستودع {from_stock.warehouse.name}. {notes or ""}',
                created_by=current_user.id
            )

            db.session.add(out_movement)
            db.session.add(in_movement)
            db.session.commit()

            flash('تم نقل المخزون بنجاح', 'success')
            return redirect(url_for('inventory.stock_transfer'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    products = Product.query.filter_by(is_active=True, track_inventory=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    return render_template('inventory/stock_transfer.html',
                         products=products,
                         warehouses=warehouses)

@bp.route('/api/product-stock/<int:product_id>')
@login_required
def get_product_stock(product_id):
    """Get product stock by warehouse (API endpoint)"""
    stocks = Stock.query.filter_by(product_id=product_id).all()

    stock_data = {}
    for stock in stocks:
        stock_data[stock.warehouse_id] = {
            'quantity': stock.quantity,
            'available': stock.available_quantity,
            'reserved': stock.reserved_quantity,
            'warehouse_name': stock.warehouse.name
        }

    return jsonify(stock_data)


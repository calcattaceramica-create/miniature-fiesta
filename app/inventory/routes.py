from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.inventory import bp
from app import db
from app.models import Product, Category, Unit, Warehouse, Stock, StockMovement, Branch, User, DamagedInventory
from app.models_sales import SalesInvoiceItem, QuotationItem
from app.models_purchases import PurchaseInvoiceItem, PurchaseOrderItem, PurchaseReturnItem
from app.models_pos import POSOrderItem
from app.auth.decorators import permission_required, any_permission_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_product_image(file):
    """Save product image and return filename"""
    if file and allowed_file(file.filename):
        # Create uploads directory if it doesn't exist
        upload_folder = current_app.config['UPLOAD_FOLDER']
        products_folder = os.path.join(upload_folder, 'products')
        os.makedirs(products_folder, exist_ok=True)

        # Generate unique filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}{ext}"

        # Save file
        filepath = os.path.join(products_folder, unique_filename)
        file.save(filepath)

        # Return relative path for database
        return f"products/{unique_filename}"
    return None

@bp.route('/products')
@login_required
@permission_required('inventory.products.view')
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

    # Get company settings for currency
    from app.models import Company
    from flask import current_app
    company = Company.query.first()
    currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
    currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')
    currency_name = current_app.config['CURRENCIES'].get(currency_code, {}).get('name', 'ريال سعودي')

    return render_template('inventory/products.html',
                         products=products,
                         categories=categories,
                         search=search,
                         category_id=category_id,
                         currency_symbol=currency_symbol,
                         currency_name=currency_name,
                         currency_code=currency_code)

@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.products.create')
def add_product():
    """Add new product"""
    if request.method == 'POST':
        try:
            # Get barcode, set to None if empty
            barcode = request.form.get('barcode') or None

            # Auto-generate Product Code if not provided
            code = request.form.get('code')
            if not code or code.strip() == '':
                # Generate code: PRD-YYYYMM-XXXX
                from datetime import datetime
                today = datetime.utcnow()
                prefix = f'PRD-{today.year}{today.month:02d}'

                # Find last product with this prefix
                last_product = Product.query.filter(
                    Product.code.like(f'{prefix}-%')
                ).order_by(Product.id.desc()).first()

                if last_product:
                    try:
                        last_num = int(last_product.code.split('-')[-1])
                        code = f'{prefix}-{(last_num + 1):04d}'
                    except:
                        code = f'{prefix}-0001'
                else:
                    code = f'{prefix}-0001'
            else:
                # Check if manually entered code already exists
                existing_code = Product.query.filter_by(code=code).first()
                if existing_code:
                    flash(_('Product code %(code)s already exists for product: %(name)s', code=code, name=existing_code.name), 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    warehouses = Warehouse.query.filter_by(is_active=True).all()
                    return render_template('inventory/add_product.html',
                                         categories=categories,
                                         units=units,
                                         warehouses=warehouses)

            # Auto-generate SKU if not provided
            sku = request.form.get('sku')
            if not sku or sku.strip() == '':
                # Generate SKU: SKU-XXXX
                last_product = Product.query.filter(
                    Product.sku.like('SKU-%')
                ).order_by(Product.id.desc()).first()

                if last_product and last_product.sku:
                    try:
                        last_num = int(last_product.sku.split('-')[-1])
                        sku = f'SKU-{(last_num + 1):04d}'
                    except:
                        sku = f'SKU-0001'
                else:
                    sku = f'SKU-0001'
            else:
                # Check if manually entered SKU already exists
                existing_sku = Product.query.filter_by(sku=sku).first()
                if existing_sku:
                    flash(_('SKU %(sku)s already exists for product: %(name)s', sku=sku, name=existing_sku.name), 'error')
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
                    flash(_('Barcode %(barcode)s already exists for product: %(name)s', barcode=barcode, name=existing_barcode.name), 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    warehouses = Warehouse.query.filter_by(is_active=True).all()
                    return render_template('inventory/add_product.html',
                                         categories=categories,
                                         units=units,
                                         warehouses=warehouses)

            # Handle image upload
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    image_filename = save_product_image(file)
                    if not image_filename:
                        flash(_('Invalid image file. Allowed formats: PNG, JPG, JPEG, GIF'), 'error')

            product = Product(
                name=request.form.get('name'),
                name_en=request.form.get('name_en'),
                code=code,
                barcode=barcode,
                sku=sku,
                category_id=request.form.get('category_id', type=int),
                unit_id=request.form.get('unit_id', type=int),
                description=request.form.get('description'),
                image=image_filename,
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
                flash(_('Product and stock added successfully'), 'success')
            else:
                flash(_('Product added successfully'), 'success')

            return redirect(url_for('inventory.products'))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')

    categories = Category.query.filter_by(is_active=True).all()
    units = Unit.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    return render_template('inventory/add_product.html',
                         categories=categories,
                         units=units,
                         warehouses=warehouses)

@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.products.edit')
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
                    flash(_('Product code %(code)s already exists for product: %(name)s', code=code, name=existing_code.name), 'error')
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
                    flash(_('Barcode %(barcode)s already exists for product: %(name)s', barcode=barcode, name=existing_barcode.name), 'error')
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
                    flash(_('SKU %(sku)s already exists for product: %(name)s', sku=sku, name=existing_sku.name), 'error')
                    categories = Category.query.filter_by(is_active=True).all()
                    units = Unit.query.filter_by(is_active=True).all()
                    return render_template('inventory/edit_product.html',
                                         product=product,
                                         categories=categories,
                                         units=units)

            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    # Delete old image if exists
                    if product.image:
                        old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image)
                        if os.path.exists(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except:
                                pass

                    # Save new image
                    image_filename = save_product_image(file)
                    if image_filename:
                        product.image = image_filename
                    else:
                        flash(_('Invalid image file. Allowed formats: PNG, JPG, JPEG, GIF'), 'error')

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

            flash(_('Product updated successfully'), 'success')
            return redirect(url_for('inventory.products'))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')
    
    categories = Category.query.filter_by(is_active=True).all()
    units = Unit.query.filter_by(is_active=True).all()
    
    return render_template('inventory/edit_product.html',
                         product=product,
                         categories=categories,
                         units=units)

@bp.route('/products/<int:id>/delete', methods=['POST', 'DELETE'])
@login_required
@permission_required('inventory.products.delete')
def delete_product(id):
    """Delete product permanently (hard delete)"""
    product = Product.query.get_or_404(id)

    try:
        # Delete all related records first
        SalesInvoiceItem.query.filter_by(product_id=id).delete()
        QuotationItem.query.filter_by(product_id=id).delete()
        PurchaseInvoiceItem.query.filter_by(product_id=id).delete()
        PurchaseOrderItem.query.filter_by(product_id=id).delete()
        PurchaseReturnItem.query.filter_by(product_id=id).delete()
        POSOrderItem.query.filter_by(product_id=id).delete()
        Stock.query.filter_by(product_id=id).delete()
        StockMovement.query.filter_by(product_id=id).delete()

        # Delete the product
        product_name = product.name
        db.session.delete(product)
        db.session.commit()

        flash(_('Product "%(name)s" and all related records have been permanently deleted', name=product_name), 'success')
        return redirect(url_for('inventory.products'))

    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred while deleting the product: %(error)s', error=str(e)), 'error')
        return redirect(url_for('inventory.products'))

@bp.route('/categories')
@login_required
@permission_required('inventory.categories.manage')
def categories():
    """List all categories"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return render_template('inventory/categories.html', categories=categories)
    except Exception as e:
        flash(_('Error loading page: %(error)s', error=str(e)), 'error')
        return redirect(url_for('inventory.products'))

@bp.route('/add_category', methods=['POST'])
@login_required
@permission_required('inventory.categories.manage')
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
        flash(_('Category added successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/edit_category/<int:id>', methods=['POST'])
@login_required
@permission_required('inventory.categories.manage')
def edit_category(id):
    """Edit category"""
    try:
        category = Category.query.get_or_404(id)
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        category.is_active = bool(request.form.get('is_active'))
        db.session.commit()
        flash(_('Category updated successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/delete_category/<int:id>', methods=['POST'])
@login_required
@permission_required('inventory.categories.manage')
def delete_category(id):
    """Delete category"""
    try:
        category = Category.query.get_or_404(id)
        # Check if category has products
        if category.products:
            flash(_('Cannot delete category because it contains products'), 'error')
        else:
            db.session.delete(category)
            db.session.commit()
            flash(_('Category deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'error')
    return redirect(url_for('inventory.categories'))

@bp.route('/stock')
@login_required
@permission_required('inventory.stock.view')
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
@permission_required('inventory.warehouses.view')
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
@permission_required('inventory.warehouses.manage')
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

        flash(_('Warehouse added successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>/edit', methods=['POST'])
@login_required
@permission_required('inventory.warehouses.manage')
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
        flash(_('Warehouse updated successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('inventory.warehouses.manage')
def delete_warehouse(id):
    """Delete warehouse"""
    warehouse = Warehouse.query.get_or_404(id)

    # Check if warehouse has stock
    if warehouse.stocks:
        flash(_('Cannot delete warehouse because it contains stock'), 'danger')
        return redirect(url_for('inventory.warehouses'))

    try:
        db.session.delete(warehouse)
        db.session.commit()
        flash(_('Warehouse deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'danger')

    return redirect(url_for('inventory.warehouses'))

@bp.route('/warehouses/<int:id>')
@login_required
@permission_required('inventory.warehouses.view')
def warehouse_details(id):
    """View warehouse details"""
    warehouse = Warehouse.query.get_or_404(id)

    # Get stock in this warehouse
    stocks = Stock.query.filter_by(warehouse_id=id).join(Product).order_by(Product.name).all()

    # Calculate statistics
    total_products = len(stocks)
    total_value = sum(stock.quantity * stock.product.cost_price for stock in stocks)
    low_stock_count = sum(1 for stock in stocks if stock.product.min_stock and stock.quantity <= stock.product.min_stock)

    return render_template('inventory/warehouse_details.html',
                         warehouse=warehouse,
                         stocks=stocks,
                         total_products=total_products,
                         total_value=total_value,
                         low_stock_count=low_stock_count)

@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.stock.transfer')
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
                flash(_('Cannot transfer to the same warehouse'), 'danger')
                return redirect(url_for('inventory.stock_transfer'))

            # Get source stock
            from_stock = Stock.query.filter_by(
                product_id=product_id,
                warehouse_id=from_warehouse_id
            ).first()

            if not from_stock or from_stock.available_quantity < quantity:
                flash(_('Insufficient quantity available'), 'danger')
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

            flash(_('Stock transferred successfully'), 'success')
            return redirect(url_for('inventory.stock_transfer'))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'danger')

    products = Product.query.filter_by(is_active=True, track_inventory=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    from datetime import datetime
    now = datetime.now()

    return render_template('inventory/stock_transfer.html',
                         products=products,
                         warehouses=warehouses,
                         now=now)

@bp.route('/api/product-stock/<int:product_id>')
@login_required
@permission_required('inventory.stock.view')
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

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/api/product-stock/<int:product_id>')
@login_required
@permission_required('inventory.stock.view')
def api_product_stock(product_id):
    """Get product stock information by warehouse"""
    stocks = Stock.query.filter_by(product_id=product_id).all()

    stock_data = {}
    for stock in stocks:
        stock_data[str(stock.warehouse_id)] = {
            'quantity': float(stock.quantity or 0),
            'reserved': float(stock.reserved_quantity or 0),
            'damaged': float(stock.damaged_quantity or 0),
            'available': float(stock.available_quantity or 0)
        }

    return jsonify(stock_data)

@bp.route('/damaged-inventory')
@login_required
@permission_required('inventory.stock.view')
def damaged_inventory():
    """View damaged inventory"""
    page = request.args.get('page', 1, type=int)
    warehouse_id = request.args.get('warehouse', type=int)

    query = DamagedInventory.query.join(Product).join(Warehouse)

    if warehouse_id:
        query = query.filter(DamagedInventory.warehouse_id == warehouse_id)

    damaged_items = query.order_by(DamagedInventory.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    warehouses = Warehouse.query.filter_by(is_active=True).all()

    # Calculate total damaged value
    total_damaged_value = db.session.query(db.func.sum(DamagedInventory.cost_value)).scalar() or 0

    return render_template('inventory/damaged_inventory.html',
                         damaged_items=damaged_items,
                         warehouses=warehouses,
                         warehouse_id=warehouse_id,
                         total_damaged_value=total_damaged_value)

@bp.route('/damaged-inventory/add', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.stock.edit')
def add_damaged_inventory():
    """Add damaged inventory record"""
    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id', type=int)
            warehouse_id = request.form.get('warehouse_id', type=int)
            quantity = request.form.get('quantity', type=float)
            reason = request.form.get('reason')
            damage_type = request.form.get('damage_type')
            notes = request.form.get('notes')

            # Get product and stock
            product = Product.query.get_or_404(product_id)
            stock = Stock.query.filter_by(
                product_id=product_id,
                warehouse_id=warehouse_id
            ).first()

            if not stock or stock.quantity < quantity:
                flash(_('Insufficient quantity in stock'), 'error')
                return redirect(url_for('inventory.add_damaged_inventory'))

            # Calculate cost value
            cost_value = quantity * product.cost_price

            # Create damaged inventory record
            damaged = DamagedInventory(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity=quantity,
                reason=reason,
                damage_type=damage_type,
                cost_value=cost_value,
                notes=notes,
                user_id=current_user.id
            )
            db.session.add(damaged)
            db.session.flush()  # Get the ID without committing

            # Update stock
            stock.quantity -= quantity
            stock.damaged_quantity = (stock.damaged_quantity or 0) + quantity
            stock.available_quantity = stock.quantity - stock.reserved_quantity - stock.damaged_quantity

            # Create stock movement
            movement = StockMovement(
                product_id=product_id,
                warehouse_id=warehouse_id,
                movement_type='damaged',
                quantity=-quantity,  # Negative for outgoing
                reference_type='damaged',
                reference_id=damaged.id,
                notes=f'{_("Damaged inventory")}: {reason}',
                user_id=current_user.id
            )
            db.session.add(movement)

            db.session.commit()

            flash(_('Damaged inventory recorded successfully'), 'success')
            return redirect(url_for('inventory.damaged_inventory'))

        except Exception as e:
            db.session.rollback()
            flash(_('An error occurred: %(error)s', error=str(e)), 'error')

    products = Product.query.filter_by(is_active=True, track_inventory=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    return render_template('inventory/add_damaged_inventory.html',
                         products=products,
                         warehouses=warehouses)

@bp.route('/damaged-inventory/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.stock.delete')
def delete_damaged_inventory(id):
    """Delete damaged inventory record"""
    damaged = DamagedInventory.query.get_or_404(id)

    try:
        # Get stock
        stock = Stock.query.filter_by(
            product_id=damaged.product_id,
            warehouse_id=damaged.warehouse_id
        ).first()

        if stock:
            # Restore stock
            stock.quantity += damaged.quantity
            stock.damaged_quantity = max(0, (stock.damaged_quantity or 0) - damaged.quantity)
            stock.available_quantity = stock.quantity - stock.reserved_quantity - stock.damaged_quantity

        # Delete damaged record
        db.session.delete(damaged)
        db.session.commit()

        flash(_('Damaged inventory record deleted successfully'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(_('An error occurred: %(error)s', error=str(e)), 'error')

    return redirect(url_for('inventory.damaged_inventory'))


from datetime import datetime
from app import db

# Supplier and Purchase Models
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False, index=True)
    name_en = db.Column(db.String(128))
    
    # Contact Info
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    
    # Business Info
    tax_number = db.Column(db.String(64))
    commercial_register = db.Column(db.String(64))
    
    # Financial
    credit_limit = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    payment_terms = db.Column(db.Integer, default=0)  # Days
    
    # Classification
    category = db.Column(db.String(64))
    rating = db.Column(db.Integer, default=0)  # 1-5 stars
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    order_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    expected_delivery = db.Column(db.Date)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, sent, confirmed, received, cancelled
    
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = db.relationship('Supplier', backref='purchase_orders')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PurchaseOrder {self.order_number}>'

class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    description = db.Column(db.String(256))
    quantity = db.Column(db.Float, nullable=False)
    received_quantity = db.Column(db.Float, default=0.0)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<PurchaseOrderItem {self.product_id}>'

class PurchaseInvoice(db.Model):
    __tablename__ = 'purchase_invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    invoice_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    supplier_invoice_number = db.Column(db.String(64))  # Supplier's invoice number
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    remaining_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, paid, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, partial, paid
    
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = db.relationship('Supplier', backref='invoices')
    warehouse = db.relationship('Warehouse')
    purchase_order = db.relationship('PurchaseOrder')
    user = db.relationship('User')
    items = db.relationship('PurchaseInvoiceItem', backref='invoice', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PurchaseInvoice {self.invoice_number}>'

class PurchaseInvoiceItem(db.Model):
    __tablename__ = 'purchase_invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('purchase_invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    description = db.Column(db.String(256))
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<PurchaseInvoiceItem {self.product_id}>'

class PurchaseReturn(db.Model):
    __tablename__ = 'purchase_returns'
    
    id = db.Column(db.Integer, primary_key=True)
    return_number = db.Column(db.String(64), unique=True, nullable=False)
    return_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    purchase_invoice_id = db.Column(db.Integer, db.ForeignKey('purchase_invoices.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    total_amount = db.Column(db.Float, default=0.0)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, refunded
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    supplier = db.relationship('Supplier', backref='returns')
    purchase_invoice = db.relationship('PurchaseInvoice')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')
    items = db.relationship('PurchaseReturnItem', backref='return', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PurchaseReturn {self.return_number}>'

class PurchaseReturnItem(db.Model):
    __tablename__ = 'purchase_return_items'
    
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey('purchase_returns.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')


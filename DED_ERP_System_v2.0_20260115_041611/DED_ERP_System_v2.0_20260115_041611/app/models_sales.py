from datetime import datetime
from app import db

# Customer and Sales Models
class Customer(db.Model):
    __tablename__ = 'customers'
    
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
    customer_type = db.Column(db.String(20), default='individual')  # individual, company
    
    # Financial
    credit_limit = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    payment_terms = db.Column(db.Integer, default=0)  # Days
    
    # Classification
    category = db.Column(db.String(64))  # VIP, Regular, Wholesale, etc.
    rating = db.Column(db.Integer, default=0)  # 1-5 stars
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class SalesInvoice(db.Model):
    __tablename__ = 'sales_invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    invoice_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    discount_percentage = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    remaining_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, paid, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, partial, paid
    
    # Additional Info
    notes = db.Column(db.Text)
    terms_conditions = db.Column(db.Text)
    
    # References
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'))
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))
    pos_order_id = db.Column(db.Integer, db.ForeignKey('pos_orders.id'))  # Link to POS order

    # Tracking
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer', backref='invoices')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')
    items = db.relationship('SalesInvoiceItem', backref='invoice', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SalesInvoice {self.invoice_number}>'

class SalesInvoiceItem(db.Model):
    __tablename__ = 'sales_invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    description = db.Column(db.String(256))
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<SalesInvoiceItem {self.product_id}>'

class Quotation(db.Model):
    __tablename__ = 'quotations'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_number = db.Column(db.String(64), unique=True, nullable=False)
    quotation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    valid_until = db.Column(db.Date)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='draft')  # draft, sent, accepted, rejected, expired
    notes = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='quotations')
    user = db.relationship('User')
    items = db.relationship('QuotationItem', backref='quotation', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quotation {self.quotation_number}>'

class QuotationItem(db.Model):
    __tablename__ = 'quotation_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    description = db.Column(db.String(256))
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')

class SalesOrder(db.Model):
    __tablename__ = 'sales_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False)
    order_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    delivery_date = db.Column(db.Date)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    total_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, delivered, cancelled
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='orders')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')


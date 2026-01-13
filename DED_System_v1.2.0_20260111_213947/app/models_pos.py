from datetime import datetime
from app import db

# POS Models
class POSSession(db.Model):
    __tablename__ = 'pos_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_number = db.Column(db.String(64), unique=True, nullable=False)
    
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    opening_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    closing_time = db.Column(db.DateTime)
    
    opening_balance = db.Column(db.Float, default=0.0)
    closing_balance = db.Column(db.Float, default=0.0)
    
    total_sales = db.Column(db.Float, default=0.0)
    total_cash = db.Column(db.Float, default=0.0)
    total_card = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='open')  # open, closed
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    cashier = db.relationship('User')
    warehouse = db.relationship('Warehouse')
    
    def __repr__(self):
        return f'<POSSession {self.session_number}>'

class POSOrder(db.Model):
    __tablename__ = 'pos_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    session_id = db.Column(db.Integer, db.ForeignKey('pos_sessions.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Payment
    payment_method = db.Column(db.String(20), default='cash')  # cash, card, mixed
    cash_amount = db.Column(db.Float, default=0.0)
    card_amount = db.Column(db.Float, default=0.0)
    change_amount = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='completed')  # completed, cancelled, refunded
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    session = db.relationship('POSSession', backref='orders')
    customer = db.relationship('Customer')
    items = db.relationship('POSOrderItem', backref='order', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<POSOrder {self.order_number}>'

class POSOrderItem(db.Model):
    __tablename__ = 'pos_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('pos_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<POSOrderItem {self.product_id}>'


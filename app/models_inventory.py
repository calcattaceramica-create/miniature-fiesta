from datetime import datetime
from app import db

# Inventory Models
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    code = db.Column(db.String(20), unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for parent/child categories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Unit(db.Model):
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(64))
    symbol = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Unit {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True)
    name_en = db.Column(db.String(256))
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    barcode = db.Column(db.String(128), index=True)  # Removed unique constraint
    sku = db.Column(db.String(64))
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    
    description = db.Column(db.Text)
    image = db.Column(db.String(256))
    
    # Pricing
    cost_price = db.Column(db.Float, default=0.0)
    selling_price = db.Column(db.Float, default=0.0)
    min_price = db.Column(db.Float, default=0.0)
    
    # Stock
    min_stock = db.Column(db.Float, default=0.0)
    max_stock = db.Column(db.Float, default=0.0)
    reorder_level = db.Column(db.Float, default=0.0)
    
    # Flags
    is_active = db.Column(db.Boolean, default=True)
    is_sellable = db.Column(db.Boolean, default=True)
    is_purchasable = db.Column(db.Boolean, default=True)
    track_inventory = db.Column(db.Boolean, default=True)
    has_expiry = db.Column(db.Boolean, default=False)
    has_serial = db.Column(db.Boolean, default=False)
    
    # Tax
    tax_rate = db.Column(db.Float, default=15.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', backref='products')
    unit = db.relationship('Unit', backref='products')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_stock(self, warehouse_id=None):
        """Get current stock quantity"""
        query = Stock.query.filter_by(product_id=self.id)
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        stocks = query.all()
        return sum(s.quantity for s in stocks)

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    code = db.Column(db.String(20), unique=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    address = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    branch = db.relationship('Branch', backref='warehouses')
    
    def __repr__(self):
        return f'<Warehouse {self.name}>'

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Float, default=0.0)
    reserved_quantity = db.Column(db.Float, default=0.0)  # Reserved for orders
    damaged_quantity = db.Column(db.Float, default=0.0)  # Damaged/defective items
    available_quantity = db.Column(db.Float, default=0.0)  # quantity - reserved - damaged
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship('Product', backref='stocks')
    warehouse = db.relationship('Warehouse', backref='stocks')

    __table_args__ = (
        db.UniqueConstraint('product_id', 'warehouse_id', name='unique_product_warehouse'),
    )

    def __repr__(self):
        return f'<Stock Product:{self.product_id} Warehouse:{self.warehouse_id} Qty:{self.quantity}>'

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)

    movement_type = db.Column(db.String(20))  # in, out, transfer, adjustment, damaged
    quantity = db.Column(db.Float, nullable=False)
    reference_type = db.Column(db.String(50))  # purchase, sale, transfer, adjustment, damaged
    reference_id = db.Column(db.Integer)

    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')

    def __repr__(self):
        return f'<StockMovement {self.movement_type} {self.quantity}>'

class DamagedInventory(db.Model):
    __tablename__ = 'damaged_inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(200))  # Reason for damage
    damage_type = db.Column(db.String(50))  # expired, broken, defective, etc.
    cost_value = db.Column(db.Float, default=0.0)  # Cost value of damaged items
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')

    def __repr__(self):
        return f'<DamagedInventory Product:{self.product_id} Qty:{self.quantity}>'


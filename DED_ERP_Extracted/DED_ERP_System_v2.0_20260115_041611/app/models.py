from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

# User and Authentication Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    full_name = db.Column(db.String(128))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(5), default='ar')
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'))  # NEW: Link to license
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Security fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    last_failed_login = db.Column(db.DateTime)
    password_changed_at = db.Column(db.DateTime)
    must_change_password = db.Column(db.Boolean, default=False)
    last_ip_address = db.Column(db.String(45))  # IPv6 support

    # Relationships
    branch = db.relationship('Branch', foreign_keys=[branch_id], backref='users')
    role = db.relationship('Role', backref='users', lazy='joined')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        """Check if user has a specific permission"""
        if self.is_admin:
            return True
        if not self.role:
            return False
        try:
            return any(p.name == permission_name for p in self.role.permissions)
        except Exception as e:
            # Log the error and return False
            print(f"Error checking permission: {e}")
            return False

    def has_any_permission(self, *permission_names):
        """Check if user has any of the specified permissions"""
        if self.is_admin:
            return True
        return any(self.has_permission(p) for p in permission_names)

    def has_all_permissions(self, *permission_names):
        """Check if user has all of the specified permissions"""
        if self.is_admin:
            return True
        return all(self.has_permission(p) for p in permission_names)

    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until is None:
            return False
        return datetime.utcnow() < self.account_locked_until

    def lock_account(self, minutes=30):
        """Lock account for specified minutes"""
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        db.session.commit()

    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        db.session.commit()

    def record_failed_login(self):
        """Record a failed login attempt"""
        self.failed_login_attempts += 1
        self.last_failed_login = datetime.utcnow()

        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.lock_account(30)  # Lock for 30 minutes

        db.session.commit()

    def record_successful_login(self, ip_address=None):
        """Record a successful login"""
        self.last_login = datetime.utcnow()
        self.failed_login_attempts = 0
        self.account_locked_until = None
        if ip_address:
            self.last_ip_address = ip_address
        db.session.commit()

    def has_valid_license(self):
        """Check if user has a valid license"""
        if self.is_admin:
            return True  # Admin always has access
        if not self.license_id:
            return False
        return self.license.is_valid()

    def get_license_status(self):
        """Get license status message"""
        if self.is_admin:
            return 'admin'
        if not self.license_id:
            return 'no_license'
        if not self.license.is_valid():
            if self.license.status == 'suspended':
                return 'suspended'
            elif self.license.status == 'expired':
                return 'expired'
            else:
                return 'inactive'
        return 'active'

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    name_ar = db.Column(db.String(64))
    description = db.Column(db.String(256))
    permissions = db.relationship('Permission', secondary='role_permissions', backref='roles', lazy='joined')

    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    name_ar = db.Column(db.String(64))
    module = db.Column(db.String(64))  # inventory, sales, purchases, etc.
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))

# Security Models
class SecurityLog(db.Model):
    """Log security-related events"""
    __tablename__ = 'security_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_type = db.Column(db.String(50), nullable=False)  # login, logout, failed_login, password_change, etc.
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))
    details = db.Column(db.Text)
    severity = db.Column(db.String(20), default='info')  # info, warning, critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = db.relationship('User', backref='security_logs')

    def __repr__(self):
        return f'<SecurityLog {self.event_type} - {self.created_at}>'

class IPWhitelist(db.Model):
    """Whitelist of allowed IP addresses"""
    __tablename__ = 'ip_whitelist'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<IPWhitelist {self.ip_address}>'

class SessionLog(db.Model):
    """Track active user sessions"""
    __tablename__ = 'session_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_id = db.Column(db.String(256), unique=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))
    login_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    logout_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship('User', backref='sessions')

    def __repr__(self):
        return f'<SessionLog {self.user_id} - {self.session_id}>'

# Company and Branch Models
class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    tax_number = db.Column(db.String(64))
    commercial_register = db.Column(db.String(64))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(128))
    logo = db.Column(db.String(256))
    currency = db.Column(db.String(3), default='SAR')
    tax_rate = db.Column(db.Float, default=15.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Company {self.name}>'

class Branch(db.Model):
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    code = db.Column(db.String(20), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref='branches')
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_branches')

    def __repr__(self):
        return f'<Branch {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import all models
from app.models_inventory import Category, Unit, Product, Warehouse, Stock, StockMovement
from app.models_sales import Customer, SalesInvoice, SalesInvoiceItem, Quotation, QuotationItem, SalesOrder
from app.models_purchases import Supplier, PurchaseOrder, PurchaseOrderItem, PurchaseInvoice, PurchaseInvoiceItem, PurchaseReturn, PurchaseReturnItem
from app.models_accounting import Account, JournalEntry, JournalEntryItem, Payment, BankAccount, CostCenter
from app.models_hr import Employee, Department, Position, Attendance, Leave, LeaveType, Payroll
from app.models_pos import POSSession, POSOrder, POSOrderItem
from app.models_settings import SystemSettings, AccountingSettings
from app.models_crm import Lead, Interaction, Opportunity, Task, Campaign, Contact


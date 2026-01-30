"""
License Management Models
نماذج إدارة التراخيص
"""
from datetime import datetime, timedelta
from app import db
import secrets
import hashlib

class License(db.Model):
    """License model for application access control"""
    __tablename__ = 'licenses'
    
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    license_hash = db.Column(db.String(128), nullable=False)  # SHA-256 hash for verification
    
    # Client Information
    client_name = db.Column(db.String(128), nullable=False)
    client_email = db.Column(db.String(120))
    client_phone = db.Column(db.String(20))
    client_company = db.Column(db.String(128))
    
    # License Details
    license_type = db.Column(db.String(20), default='trial')  # trial, monthly, yearly, lifetime
    max_users = db.Column(db.Integer, default=1)
    max_branches = db.Column(db.Integer, default=1)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_suspended = db.Column(db.Boolean, default=False)  # للتعليق المؤقت
    suspension_reason = db.Column(db.Text)
    
    # Dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    activated_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    last_check = db.Column(db.DateTime)  # آخر مرة تم التحقق من الترخيص
    
    # Machine binding (optional - لربط الترخيص بجهاز معين)
    machine_id = db.Column(db.String(128))  # Hardware ID
    ip_address = db.Column(db.String(45))
    
    # Admin user for this license
    admin_username = db.Column(db.String(64))
    admin_password_hash = db.Column(db.String(256))
    
    # Notes
    notes = db.Column(db.Text)
    
    @staticmethod
    def generate_license_key():
        """Generate a unique license key"""
        # Format: XXXX-XXXX-XXXX-XXXX
        key = secrets.token_hex(8).upper()
        formatted_key = f"{key[0:4]}-{key[4:8]}-{key[8:12]}-{key[12:16]}"
        return formatted_key
    
    @staticmethod
    def hash_license_key(key):
        """Create SHA-256 hash of license key"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def verify_license_key(self, key):
        """Verify license key against stored hash"""
        return self.license_hash == self.hash_license_key(key)
    
    def is_valid(self):
        """Check if license is valid"""
        if not self.is_active:
            return False, "الترخيص غير مفعّل"
        
        if self.is_suspended:
            return False, f"الترخيص معلق: {self.suspension_reason}"
        
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False, "الترخيص منتهي الصلاحية"
        
        return True, "الترخيص صالح"
    
    def can_add_user(self):
        """Check if more users can be added to this license"""
        from app.models import User
        current_users = User.query.filter_by(license_id=self.id).count()
        return current_users < self.max_users
    
    def days_remaining(self):
        """Get remaining days until expiration"""
        if not self.expires_at:
            return None  # Lifetime license
        
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)
    
    def extend_license(self, days):
        """Extend license expiration"""
        if self.expires_at:
            self.expires_at += timedelta(days=days)
        else:
            self.expires_at = datetime.utcnow() + timedelta(days=days)
    
    def suspend(self, reason=""):
        """Suspend license"""
        self.is_suspended = True
        self.suspension_reason = reason
    
    def unsuspend(self):
        """Unsuspend license"""
        self.is_suspended = False
        self.suspension_reason = None
    
    def __repr__(self):
        return f'<License {self.license_key} - {self.client_name}>'


class LicenseCheck(db.Model):
    """License check history"""
    __tablename__ = 'license_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False)
    
    check_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_valid = db.Column(db.Boolean)
    check_result = db.Column(db.String(256))
    
    # System info at check time
    ip_address = db.Column(db.String(45))
    machine_id = db.Column(db.String(128))
    
    license = db.relationship('License', backref='checks')
    
    def __repr__(self):
        return f'<LicenseCheck {self.check_time} - Valid: {self.is_valid}>'


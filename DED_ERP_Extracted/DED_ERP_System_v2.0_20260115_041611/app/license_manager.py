"""
License Manager
مدير التراخيص - للتحكم في صلاحية التطبيق
"""
from datetime import datetime, timedelta
from app import db
from app.models_license import License, LicenseCheck
from werkzeug.security import generate_password_hash
import platform
import uuid
import socket

class LicenseManager:
    """License management system"""
    
    @staticmethod
    def get_machine_id():
        """Get unique machine identifier"""
        # Combine multiple hardware identifiers
        machine_info = f"{platform.node()}-{uuid.getnode()}"
        return machine_info
    
    @staticmethod
    def get_ip_address():
        """Get current IP address"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except:
            return "Unknown"
    
    @staticmethod
    def create_license(client_name, admin_username, admin_password, 
                      license_type='trial', duration_days=30,
                      max_users=1, max_branches=1,
                      client_email=None, client_phone=None, 
                      client_company=None, notes=None):
        """
        Create a new license
        
        Args:
            client_name: اسم العميل
            admin_username: اسم المستخدم للمدير
            admin_password: كلمة المرور للمدير
            license_type: نوع الترخيص (trial, monthly, yearly, lifetime)
            duration_days: مدة الترخيص بالأيام (None للترخيص الدائم)
            max_users: الحد الأقصى للمستخدمين
            max_branches: الحد الأقصى للفروع
        
        Returns:
            License object with license_key
        """
        # Generate unique license key
        license_key = License.generate_license_key()
        license_hash = License.hash_license_key(license_key)
        
        # Calculate expiration date
        expires_at = None
        if duration_days:
            expires_at = datetime.utcnow() + timedelta(days=duration_days)
        
        # Create license
        license = License(
            license_key=license_key,
            license_hash=license_hash,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            client_company=client_company,
            license_type=license_type,
            max_users=max_users,
            max_branches=max_branches,
            is_active=True,
            activated_at=datetime.utcnow(),
            expires_at=expires_at,
            admin_username=admin_username,
            admin_password_hash=generate_password_hash(admin_password),
            notes=notes
        )
        
        db.session.add(license)
        db.session.commit()
        
        return license
    
    @staticmethod
    def verify_license(license_key=None):
        """
        Verify if application license is valid
        
        Returns:
            (is_valid, message, license)
        """
        # Get active license
        if license_key:
            license = License.query.filter_by(license_key=license_key).first()
        else:
            # Get the first active license
            license = License.query.filter_by(is_active=True).first()
        
        if not license:
            return False, "لا يوجد ترخيص مفعّل", None
        
        # Check license validity
        is_valid, message = license.is_valid()
        
        # Update last check time
        license.last_check = datetime.utcnow()
        
        # Log the check
        check = LicenseCheck(
            license_id=license.id,
            is_valid=is_valid,
            check_result=message,
            ip_address=LicenseManager.get_ip_address(),
            machine_id=LicenseManager.get_machine_id()
        )
        db.session.add(check)
        db.session.commit()
        
        return is_valid, message, license
    
    @staticmethod
    def suspend_license(license_id, reason=""):
        """Suspend a license (للتعليق المؤقت)"""
        license = License.query.get(license_id)
        if license:
            license.suspend(reason)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def unsuspend_license(license_id):
        """Unsuspend a license (إلغاء التعليق)"""
        license = License.query.get(license_id)
        if license:
            license.unsuspend()
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def deactivate_license(license_id):
        """Deactivate a license permanently (إلغاء التفعيل نهائياً)"""
        license = License.query.get(license_id)
        if license:
            license.is_active = False
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def extend_license(license_id, days):
        """Extend license duration"""
        license = License.query.get(license_id)
        if license:
            license.extend_license(days)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_all_licenses():
        """Get all licenses"""
        return License.query.order_by(License.created_at.desc()).all()
    
    @staticmethod
    def get_license_info(license_id):
        """Get detailed license information"""
        license = License.query.get(license_id)
        if not license:
            return None
        
        is_valid, message = license.is_valid()
        days_remaining = license.days_remaining()
        
        return {
            'license': license,
            'is_valid': is_valid,
            'message': message,
            'days_remaining': days_remaining,
            'checks_count': len(license.checks)
        }


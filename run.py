import os
from app import create_app, db
from app.models import *

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'Company': Company,
        'Branch': Branch,
        'Category': Category,
        'Unit': Unit,
        'Product': Product,
        'Warehouse': Warehouse,
        'Stock': Stock,
        'Customer': Customer,
        'Supplier': Supplier,
        'SalesInvoice': SalesInvoice,
        'PurchaseInvoice': PurchaseInvoice,
        'Account': Account,
        'JournalEntry': JournalEntry,
        'Employee': Employee,
        'Department': Department,
    }

@app.cli.command()
def create_license():
    """Create default license for production"""
    from app.models_license import License
    from datetime import datetime
    import hashlib

    try:
        # Check if license already exists
        existing_license = License.query.filter_by(license_key='9813-26D0-F98D-741C').first()

        if existing_license:
            print('✅ License already exists')
            return

        # Create the license hash
        license_key = '9813-26D0-F98D-741C'
        license_hash = hashlib.sha256(license_key.encode()).hexdigest()

        # Create the license
        new_license = License(
            license_key=license_key,
            license_hash=license_hash,
            client_name='DED Company',
            client_company='DED ERP System',
            license_type='lifetime',
            max_users=10,
            max_branches=5,
            expires_at=None,  # Lifetime license
            is_active=True,
            activated_at=datetime.utcnow(),
            notes='Auto-created for production deployment'
        )
        db.session.add(new_license)
        db.session.commit()
        print('✅ License created successfully!')
        print(f'🔑 License Key: {license_key}')

    except Exception as e:
        print(f'❌ Error creating license: {e}')
        db.session.rollback()

@app.cli.command()
def init_db():
    """Initialize the database with default data"""
    db.create_all()
    
    # Create default company
    if not Company.query.first():
        company = Company(
            name='شركة نموذجية',
            name_en='Sample Company',
            tax_number='123456789',
            city='الرياض',
            country='السعودية',
            currency='SAR',
            tax_rate=15.0
        )
        db.session.add(company)
    
    # Create default branch
    if not Branch.query.first():
        branch = Branch(
            name='الفرع الرئيسي',
            name_en='Main Branch',
            code='BR001',
            company_id=1,
            city='الرياض',
            is_active=True
        )
        db.session.add(branch)
    
    # Create default roles
    if not Role.query.first():
        admin_role = Role(name='admin', name_ar='مدير النظام', description='Full system access')
        manager_role = Role(name='manager', name_ar='مدير', description='Manager access')
        user_role = Role(name='user', name_ar='مستخدم', description='Basic user access')
        db.session.add_all([admin_role, manager_role, user_role])
    
    # Create default admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            full_name='مدير النظام',
            is_active=True,
            is_admin=True,
            language='ar',
            branch_id=1,
            role_id=1
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create default units
    if not Unit.query.first():
        units = [
            Unit(name='قطعة', name_en='Piece', symbol='قطعة'),
            Unit(name='كيلوجرام', name_en='Kilogram', symbol='كجم'),
            Unit(name='متر', name_en='Meter', symbol='م'),
            Unit(name='لتر', name_en='Liter', symbol='لتر'),
            Unit(name='صندوق', name_en='Box', symbol='صندوق'),
        ]
        db.session.add_all(units)
    
    # Create default warehouse
    if not Warehouse.query.first():
        warehouse = Warehouse(
            name='المستودع الرئيسي',
            name_en='Main Warehouse',
            code='WH001',
            branch_id=1,
            is_active=True
        )
        db.session.add(warehouse)
    
    # Create default chart of accounts
    if not Account.query.first():
        accounts = [
            Account(code='1000', name='الأصول', name_en='Assets', account_type='asset', is_system=True),
            Account(code='2000', name='الخصوم', name_en='Liabilities', account_type='liability', is_system=True),
            Account(code='3000', name='حقوق الملكية', name_en='Equity', account_type='equity', is_system=True),
            Account(code='4000', name='الإيرادات', name_en='Revenue', account_type='revenue', is_system=True),
            Account(code='5000', name='المصروفات', name_en='Expenses', account_type='expense', is_system=True),
        ]
        db.session.add_all(accounts)
    
    db.session.commit()
    print('Database initialized successfully!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


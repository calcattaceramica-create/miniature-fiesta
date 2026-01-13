"""
Database initialization script
Creates all tables and populates with initial data
"""
from app import create_app, db
from app.models import User, Role, Permission, RolePermission, Company, Branch
from app.models_inventory import Category, Unit, Product, Warehouse
from app.models_accounting import Account
from datetime import datetime

def init_database():
    """Initialize database with tables and default data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables (be careful in production!)
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        
        # Create default roles
        print("Creating default roles...")
        admin_role = Role(
            name='admin',
            name_ar='مدير النظام',
            description='Full system access'
        )
        manager_role = Role(
            name='manager',
            name_ar='مدير',
            description='Manager access'
        )
        user_role = Role(
            name='user',
            name_ar='مستخدم',
            description='Basic user access'
        )
        
        db.session.add_all([admin_role, manager_role, user_role])
        db.session.commit()

        # Create default permissions
        print("Creating default permissions...")
        permissions_data = [
            # Inventory permissions
            {'name': 'inventory.view', 'name_ar': 'عرض المخزون', 'module': 'inventory'},
            {'name': 'inventory.create', 'name_ar': 'إضافة منتجات', 'module': 'inventory'},
            {'name': 'inventory.edit', 'name_ar': 'تعديل منتجات', 'module': 'inventory'},
            {'name': 'inventory.delete', 'name_ar': 'حذف منتجات', 'module': 'inventory'},

            # Sales permissions
            {'name': 'sales.view', 'name_ar': 'عرض المبيعات', 'module': 'sales'},
            {'name': 'sales.create', 'name_ar': 'إنشاء فواتير بيع', 'module': 'sales'},
            {'name': 'sales.edit', 'name_ar': 'تعديل فواتير بيع', 'module': 'sales'},
            {'name': 'sales.delete', 'name_ar': 'حذف فواتير بيع', 'module': 'sales'},

            # Purchases permissions
            {'name': 'purchases.view', 'name_ar': 'عرض المشتريات', 'module': 'purchases'},
            {'name': 'purchases.create', 'name_ar': 'إنشاء فواتير شراء', 'module': 'purchases'},
            {'name': 'purchases.edit', 'name_ar': 'تعديل فواتير شراء', 'module': 'purchases'},
            {'name': 'purchases.delete', 'name_ar': 'حذف فواتير شراء', 'module': 'purchases'},

            # Accounting permissions
            {'name': 'accounting.view', 'name_ar': 'عرض الحسابات', 'module': 'accounting'},
            {'name': 'accounting.create', 'name_ar': 'إنشاء قيود', 'module': 'accounting'},
            {'name': 'accounting.edit', 'name_ar': 'تعديل قيود', 'module': 'accounting'},
            {'name': 'accounting.delete', 'name_ar': 'حذف قيود', 'module': 'accounting'},

            # HR permissions
            {'name': 'hr.view', 'name_ar': 'عرض الموظفين', 'module': 'hr'},
            {'name': 'hr.create', 'name_ar': 'إضافة موظفين', 'module': 'hr'},
            {'name': 'hr.edit', 'name_ar': 'تعديل موظفين', 'module': 'hr'},
            {'name': 'hr.delete', 'name_ar': 'حذف موظفين', 'module': 'hr'},

            # POS permissions
            {'name': 'pos.view', 'name_ar': 'عرض نقاط البيع', 'module': 'pos'},
            {'name': 'pos.create', 'name_ar': 'إنشاء طلبات POS', 'module': 'pos'},

            # Reports permissions
            {'name': 'reports.view', 'name_ar': 'عرض التقارير', 'module': 'reports'},
            {'name': 'reports.export', 'name_ar': 'تصدير التقارير', 'module': 'reports'},

            # Settings permissions
            {'name': 'settings.view', 'name_ar': 'عرض الإعدادات', 'module': 'settings'},
            {'name': 'settings.edit', 'name_ar': 'تعديل الإعدادات', 'module': 'settings'},
            {'name': 'settings.users', 'name_ar': 'إدارة المستخدمين', 'module': 'settings'},
            {'name': 'settings.roles', 'name_ar': 'إدارة الأدوار', 'module': 'settings'},
        ]

        permissions = []
        for perm_data in permissions_data:
            perm = Permission(**perm_data)
            permissions.append(perm)
            db.session.add(perm)

        db.session.commit()

        # Assign all permissions to admin role
        print("Assigning permissions to admin role...")
        for permission in permissions:
            role_perm = RolePermission(
                role_id=admin_role.id,
                permission_id=permission.id
            )
            db.session.add(role_perm)

        db.session.commit()

        # Assign basic permissions to manager role
        print("Assigning permissions to manager role...")
        manager_permissions = [
            'inventory.view', 'inventory.create', 'inventory.edit',
            'sales.view', 'sales.create', 'sales.edit',
            'purchases.view', 'purchases.create', 'purchases.edit',
            'accounting.view',
            'hr.view',
            'pos.view', 'pos.create',
            'reports.view', 'reports.export',
            'settings.view'
        ]

        for perm_name in manager_permissions:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm:
                role_perm = RolePermission(
                    role_id=manager_role.id,
                    permission_id=perm.id
                )
                db.session.add(role_perm)

        db.session.commit()

        # Assign basic permissions to user role
        print("Assigning permissions to user role...")
        user_permissions = [
            'inventory.view',
            'sales.view', 'sales.create',
            'purchases.view',
            'pos.view', 'pos.create',
            'reports.view'
        ]

        for perm_name in user_permissions:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm:
                role_perm = RolePermission(
                    role_id=user_role.id,
                    permission_id=perm.id
                )
                db.session.add(role_perm)

        db.session.commit()

        # Create default company
        print("Creating default company...")
        company = Company(
            name='شركة تجريبية',
            name_en='Demo Company',
            tax_number='123456789',
            commercial_register='1234567890',
            phone='+966 12 345 6789',
            email='info@company.com',
            address='الرياض، المملكة العربية السعودية',
            city='الرياض',
            country='المملكة العربية السعودية'
        )
        db.session.add(company)
        db.session.commit()
        
        # Create default branch
        print("Creating default branch...")
        branch = Branch(
            company_id=company.id,
            name='الفرع الرئيسي',
            name_en='Main Branch',
            code='MAIN',
            phone='+966 12 345 6789',
            address='الرياض، المملكة العربية السعودية',
            city='الرياض',
            is_active=True
        )
        db.session.add(branch)
        db.session.commit()
        
        # Create default admin user
        print("Creating default admin user...")
        admin_user = User(
            username='admin',
            email='admin@company.com',
            full_name='مدير النظام',
            is_active=True,
            is_admin=True,
            branch_id=branch.id,
            role_id=admin_role.id
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()

        # Create default units
        print("Creating default units...")
        units = [
            Unit(name='قطعة', name_en='Piece', symbol='قطعة'),
            Unit(name='كيلوجرام', name_en='Kilogram', symbol='كجم'),
            Unit(name='متر', name_en='Meter', symbol='م'),
            Unit(name='لتر', name_en='Liter', symbol='لتر'),
            Unit(name='صندوق', name_en='Box', symbol='صندوق'),
            Unit(name='كرتون', name_en='Carton', symbol='كرتون'),
        ]
        db.session.add_all(units)
        db.session.commit()
        
        # Create default categories
        print("Creating default categories...")
        categories = [
            Category(name='إلكترونيات', name_en='Electronics', code='ELEC'),
            Category(name='ملابس', name_en='Clothing', code='CLTH'),
            Category(name='أغذية', name_en='Food', code='FOOD'),
            Category(name='مشروبات', name_en='Beverages', code='BEV'),
            Category(name='أدوات منزلية', name_en='Home Appliances', code='HOME'),
        ]
        db.session.add_all(categories)
        db.session.commit()
        
        # Create default warehouse
        print("Creating default warehouse...")
        warehouse = Warehouse(
            name='المستودع الرئيسي',
            name_en='Main Warehouse',
            code='WH-MAIN',
            branch_id=branch.id,
            address='الرياض، المملكة العربية السعودية',
            is_active=True
        )
        db.session.add(warehouse)
        db.session.commit()
        
        # Create chart of accounts
        print("Creating chart of accounts...")
        accounts = [
            # Assets
            Account(code='1000', name='الأصول', name_en='Assets', account_type='asset', is_system=True),
            Account(code='1100', name='الأصول المتداولة', name_en='Current Assets', account_type='asset', is_system=True),
            Account(code='1110', name='النقدية', name_en='Cash', account_type='asset', is_system=True),
            Account(code='1120', name='البنوك', name_en='Banks', account_type='asset', is_system=True),
            Account(code='1130', name='العملاء', name_en='Accounts Receivable', account_type='asset', is_system=True),
            Account(code='1140', name='المخزون', name_en='Inventory', account_type='asset', is_system=True),
            
            # Liabilities
            Account(code='2000', name='الخصوم', name_en='Liabilities', account_type='liability', is_system=True),
            Account(code='2100', name='الخصوم المتداولة', name_en='Current Liabilities', account_type='liability', is_system=True),
            Account(code='2110', name='الموردين', name_en='Accounts Payable', account_type='liability', is_system=True),
            Account(code='2120', name='الضرائب المستحقة', name_en='Taxes Payable', account_type='liability', is_system=True),
            
            # Equity
            Account(code='3000', name='حقوق الملكية', name_en='Equity', account_type='equity', is_system=True),
            Account(code='3100', name='رأس المال', name_en='Capital', account_type='equity', is_system=True),
            Account(code='3200', name='الأرباح المحتجزة', name_en='Retained Earnings', account_type='equity', is_system=True),
            
            # Revenue
            Account(code='4000', name='الإيرادات', name_en='Revenue', account_type='revenue', is_system=True),
            Account(code='4100', name='إيرادات المبيعات', name_en='Sales Revenue', account_type='revenue', is_system=True),
            
            # Expenses
            Account(code='5000', name='المصروفات', name_en='Expenses', account_type='expense', is_system=True),
            Account(code='5100', name='تكلفة البضاعة المباعة', name_en='Cost of Goods Sold', account_type='expense', is_system=True),
            Account(code='5200', name='مصروفات إدارية', name_en='Administrative Expenses', account_type='expense', is_system=True),
            Account(code='5300', name='مصروفات تسويقية', name_en='Marketing Expenses', account_type='expense', is_system=True),
        ]
        db.session.add_all(accounts)
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ Database initialized successfully!")
        print("="*50)
        print("\nDefault credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\n⚠️  Please change the default password after first login!")
        print("="*50)

if __name__ == '__main__':
    init_database()


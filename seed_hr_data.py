"""
Script to seed HR system with sample data
"""
from app import create_app, db
from app.models_hr import Department, Position, Employee, LeaveType, Attendance, Leave, Payroll
from datetime import datetime, timedelta
import random

def seed_hr_data():
    """Seed HR system with sample data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 بدء إضافة البيانات التجريبية لنظام الموارد البشرية...")
        
        # 1. إضافة الأقسام
        print("\n📁 إضافة الأقسام...")
        departments_data = [
            {'name': 'تقنية المعلومات', 'name_en': 'IT Department', 'description': 'قسم تقنية المعلومات'},
            {'name': 'الموارد البشرية', 'name_en': 'HR Department', 'description': 'قسم الموارد البشرية'},
            {'name': 'المحاسبة', 'name_en': 'Accounting', 'description': 'قسم المحاسبة'},
            {'name': 'المبيعات', 'name_en': 'Sales', 'description': 'قسم المبيعات'},
            {'name': 'المشتريات', 'name_en': 'Purchases', 'description': 'قسم المشتريات'},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept = Department.query.filter_by(name=dept_data['name']).first()
            if not dept:
                dept = Department(**dept_data)
                db.session.add(dept)
                departments.append(dept)
                print(f"  ✅ تم إضافة قسم: {dept_data['name']}")
            else:
                departments.append(dept)
                print(f"  ⏭️  القسم موجود: {dept_data['name']}")
        
        db.session.commit()
        
        # 2. إضافة المناصب
        print("\n👔 إضافة المناصب...")
        positions_data = [
            {'name': 'مدير', 'name_en': 'Manager', 'description': 'مدير القسم'},
            {'name': 'مطور برمجيات', 'name_en': 'Software Developer', 'description': 'مطور برمجيات'},
            {'name': 'محاسب', 'name_en': 'Accountant', 'description': 'محاسب'},
            {'name': 'مندوب مبيعات', 'name_en': 'Sales Representative', 'description': 'مندوب مبيعات'},
            {'name': 'موظف مشتريات', 'name_en': 'Purchasing Officer', 'description': 'موظف مشتريات'},
        ]
        
        positions = []
        for pos_data in positions_data:
            pos = Position.query.filter_by(name=pos_data['name']).first()
            if not pos:
                pos = Position(**pos_data)
                db.session.add(pos)
                positions.append(pos)
                print(f"  ✅ تم إضافة منصب: {pos_data['name']}")
            else:
                positions.append(pos)
                print(f"  ⏭️  المنصب موجود: {pos_data['name']}")
        
        db.session.commit()
        
        # 3. إضافة أنواع الإجازات
        print("\n📅 إضافة أنواع الإجازات...")
        leave_types_data = [
            {'name': 'إجازة سنوية', 'name_en': 'Annual Leave', 'days_per_year': 30, 'is_paid': True},
            {'name': 'إجازة مرضية', 'name_en': 'Sick Leave', 'days_per_year': 15, 'is_paid': True},
            {'name': 'إجازة طارئة', 'name_en': 'Emergency Leave', 'days_per_year': 5, 'is_paid': True},
            {'name': 'إجازة بدون راتب', 'name_en': 'Unpaid Leave', 'days_per_year': 0, 'is_paid': False},
        ]
        
        leave_types = []
        for lt_data in leave_types_data:
            lt = LeaveType.query.filter_by(name=lt_data['name']).first()
            if not lt:
                lt = LeaveType(**lt_data)
                db.session.add(lt)
                leave_types.append(lt)
                print(f"  ✅ تم إضافة نوع إجازة: {lt_data['name']}")
            else:
                leave_types.append(lt)
                print(f"  ⏭️  نوع الإجازة موجود: {lt_data['name']}")
        
        db.session.commit()
        
        # 4. إضافة الموظفين
        print("\n👥 إضافة الموظفين...")
        employees_data = [
            {
                'employee_number': 'EMP001',
                'first_name': 'محمد',
                'last_name': 'أحمد',
                'email': 'mohamed@example.com',
                'phone': '0501234567',
                'hire_date': datetime.now() - timedelta(days=365),
                'basic_salary': 10000,
                'department_id': departments[0].id,
                'position_id': positions[1].id,
            },
            {
                'employee_number': 'EMP002',
                'first_name': 'فاطمة',
                'last_name': 'علي',
                'email': 'fatima@example.com',
                'phone': '0507654321',
                'hire_date': datetime.now() - timedelta(days=730),
                'basic_salary': 12000,
                'department_id': departments[1].id,
                'position_id': positions[0].id,
            },
            {
                'employee_number': 'EMP003',
                'first_name': 'أحمد',
                'last_name': 'محمود',
                'email': 'ahmed@example.com',
                'phone': '0509876543',
                'hire_date': datetime.now() - timedelta(days=180),
                'basic_salary': 8000,
                'department_id': departments[2].id,
                'position_id': positions[2].id,
            },
        ]
        
        employees = []
        for emp_data in employees_data:
            emp = Employee.query.filter_by(employee_number=emp_data['employee_number']).first()
            if not emp:
                emp = Employee(**emp_data)
                db.session.add(emp)
                employees.append(emp)
                print(f"  ✅ تم إضافة موظف: {emp_data['first_name']} {emp_data['last_name']}")
            else:
                employees.append(emp)
                print(f"  ⏭️  الموظف موجود: {emp_data['first_name']} {emp_data['last_name']}")
        
        db.session.commit()
        
        print("\n✅ تم إضافة جميع البيانات التجريبية بنجاح!")
        print(f"\n📊 الإحصائيات:")
        print(f"  - الأقسام: {Department.query.count()}")
        print(f"  - المناصب: {Position.query.count()}")
        print(f"  - أنواع الإجازات: {LeaveType.query.count()}")
        print(f"  - الموظفين: {Employee.query.count()}")

if __name__ == '__main__':
    seed_hr_data()


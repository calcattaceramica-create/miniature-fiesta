from datetime import datetime
from app import db

# HR Models
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Personal Info
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    first_name_en = db.Column(db.String(64))
    last_name_en = db.Column(db.String(64))
    
    national_id = db.Column(db.String(20), unique=True)
    passport_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(20))
    nationality = db.Column(db.String(64))
    
    # Contact
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    
    # Employment
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    
    hire_date = db.Column(db.Date)
    contract_type = db.Column(db.String(20))  # permanent, temporary, contract
    employment_status = db.Column(db.String(20), default='active')  # active, resigned, terminated
    
    # Salary
    basic_salary = db.Column(db.Float, default=0.0)
    
    # Documents
    photo = db.Column(db.String(256))
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='employee')
    department = db.relationship('Department', foreign_keys=[department_id], backref='employees')
    position = db.relationship('Position', backref='employees')
    branch = db.relationship('Branch')
    
    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    code = db.Column(db.String(20), unique=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    children = db.relationship('Department', backref=db.backref('parent', remote_side=[id]))
    manager = db.relationship('Employee', foreign_keys=[manager_id], backref='managed_departments')

    def __repr__(self):
        return f'<Department {self.name}>'

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_en = db.Column(db.String(128))
    code = db.Column(db.String(20), unique=True)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    department = db.relationship('Department')
    
    def __repr__(self):
        return f'<Position {self.name}>'

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    
    status = db.Column(db.String(20), default='present')  # present, absent, late, half_day, leave
    working_hours = db.Column(db.Float, default=0.0)
    overtime_hours = db.Column(db.Float, default=0.0)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='attendance_records')
    
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'attendance_date', name='unique_employee_date'),
    )
    
    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.attendance_date}>'

class Leave(db.Model):
    __tablename__ = 'leaves'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_count = db.Column(db.Integer, nullable=False)
    
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, cancelled
    
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='leaves')
    leave_type = db.relationship('LeaveType')
    
    def __repr__(self):
        return f'<Leave {self.employee_id} - {self.start_date}>'

class LeaveType(db.Model):
    __tablename__ = 'leave_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(64))
    
    days_per_year = db.Column(db.Integer, default=0)
    is_paid = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<LeaveType {self.name}>'

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    basic_salary = db.Column(db.Float, default=0.0)
    allowances = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    overtime = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='draft')  # draft, approved, paid
    payment_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='payrolls')
    
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'month', 'year', name='unique_employee_month_year'),
    )
    
    def __repr__(self):
        return f'<Payroll {self.employee_id} - {self.month}/{self.year}>'


from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.auth.decorators import permission_required
from app.hr import bp
from app import db
from app.models import Employee, Department, Position, Attendance, Leave, LeaveType, Payroll, Branch
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract

# ==================== Dashboard ====================
@bp.route('/')
@bp.route('/dashboard')
@login_required
@permission_required('hr.view')
def dashboard():
    """HR Dashboard"""
    # Statistics
    stats = {
        'total_employees': Employee.query.filter_by(is_active=True).count(),
        'total_departments': Department.query.filter_by(is_active=True).count(),
        'total_positions': Position.query.filter_by(is_active=True).count(),
        'pending_leaves': Leave.query.filter_by(status='pending').count(),
    }

    # Today's attendance
    today = date.today()
    today_attendance = Attendance.query.filter_by(attendance_date=today).all()
    stats['present_today'] = len([a for a in today_attendance if a.status == 'present'])
    stats['absent_today'] = stats['total_employees'] - stats['present_today']

    # Recent employees
    recent_employees = Employee.query.filter_by(is_active=True).order_by(Employee.created_at.desc()).limit(5).all()

    # Pending leave requests
    pending_leaves = Leave.query.filter_by(status='pending').order_by(Leave.created_at.desc()).limit(5).all()

    return render_template('hr/dashboard.html',
                         stats=stats,
                         recent_employees=recent_employees,
                         pending_leaves=pending_leaves)

# ==================== Employees ====================
@bp.route('/employees')
@login_required
@permission_required('hr.employees.view')
def employees():
    """List all employees"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    department_id = request.args.get('department_id', type=int)

    query = Employee.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            (Employee.first_name.contains(search)) |
            (Employee.last_name.contains(search)) |
            (Employee.employee_number.contains(search))
        )

    if department_id:
        query = query.filter_by(department_id=department_id)

    employees = query.order_by(Employee.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    departments = Department.query.filter_by(is_active=True).all()

    return render_template('hr/employees.html',
                         employees=employees,
                         departments=departments,
                         search=search,
                         department_id=department_id)

@bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
@permission_required('hr.employees.manage')
def add_employee():
    """Add new employee"""
    if request.method == 'POST':
        try:
            # Generate employee number
            last_employee = Employee.query.order_by(Employee.id.desc()).first()
            if last_employee and last_employee.employee_number:
                last_num = int(last_employee.employee_number.replace('EMP', ''))
                employee_number = f'EMP{last_num + 1:05d}'
            else:
                employee_number = 'EMP00001'

            employee = Employee(
                employee_number=employee_number,
                first_name=request.form.get('first_name'),
                last_name=request.form.get('last_name'),
                first_name_en=request.form.get('first_name_en'),
                last_name_en=request.form.get('last_name_en'),
                national_id=request.form.get('national_id'),
                passport_number=request.form.get('passport_number'),
                date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date() if request.form.get('date_of_birth') else None,
                gender=request.form.get('gender'),
                marital_status=request.form.get('marital_status'),
                nationality=request.form.get('nationality'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                mobile=request.form.get('mobile'),
                address=request.form.get('address'),
                city=request.form.get('city'),
                department_id=request.form.get('department_id', type=int),
                position_id=request.form.get('position_id', type=int),
                branch_id=request.form.get('branch_id', type=int),
                hire_date=datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date() if request.form.get('hire_date') else None,
                contract_type=request.form.get('contract_type'),
                employment_status=request.form.get('employment_status', 'active'),
                basic_salary=float(request.form.get('basic_salary', 0)),
                is_active=True
            )

            db.session.add(employee)
            db.session.commit()
            flash('تم إضافة الموظف بنجاح', 'success')
            return redirect(url_for('hr.employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    departments = Department.query.filter_by(is_active=True).all()
    positions = Position.query.filter_by(is_active=True).all()
    branches = Branch.query.filter_by(is_active=True).all()

    return render_template('hr/add_employee.html',
                         departments=departments,
                         positions=positions,
                         branches=branches)

@bp.route('/employees/<int:id>')
@login_required
@permission_required('hr.employees.view')
def employee_details(id):
    """Employee details"""
    employee = Employee.query.get_or_404(id)

    # Get attendance summary
    attendance_summary = db.session.query(
        func.count(Attendance.id).label('total_days'),
        func.sum(Attendance.working_hours).label('total_hours')
    ).filter_by(employee_id=id).first()

    # Get recent attendance
    recent_attendance = Attendance.query.filter_by(employee_id=id).order_by(Attendance.attendance_date.desc()).limit(10).all()

    # Get leaves
    leaves = Leave.query.filter_by(employee_id=id).order_by(Leave.created_at.desc()).limit(10).all()

    # Get payrolls
    payrolls = Payroll.query.filter_by(employee_id=id).order_by(Payroll.year.desc(), Payroll.month.desc()).limit(6).all()

    return render_template('hr/employee_details.html',
                         employee=employee,
                         attendance_summary=attendance_summary,
                         recent_attendance=recent_attendance,
                         leaves=leaves,
                         payrolls=payrolls)

@bp.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('hr.employees.manage')
def edit_employee(id):
    """Edit employee"""
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        try:
            employee.first_name = request.form.get('first_name')
            employee.last_name = request.form.get('last_name')
            employee.first_name_en = request.form.get('first_name_en')
            employee.last_name_en = request.form.get('last_name_en')
            employee.national_id = request.form.get('national_id')
            employee.passport_number = request.form.get('passport_number')
            employee.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date() if request.form.get('date_of_birth') else None
            employee.gender = request.form.get('gender')
            employee.marital_status = request.form.get('marital_status')
            employee.nationality = request.form.get('nationality')
            employee.email = request.form.get('email')
            employee.phone = request.form.get('phone')
            employee.mobile = request.form.get('mobile')
            employee.address = request.form.get('address')
            employee.city = request.form.get('city')
            employee.department_id = request.form.get('department_id', type=int)
            employee.position_id = request.form.get('position_id', type=int)
            employee.branch_id = request.form.get('branch_id', type=int)
            employee.hire_date = datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date() if request.form.get('hire_date') else None
            employee.contract_type = request.form.get('contract_type')
            employee.employment_status = request.form.get('employment_status')
            employee.basic_salary = float(request.form.get('basic_salary', 0))
            employee.updated_at = datetime.utcnow()

            db.session.commit()
            flash('تم تحديث بيانات الموظف بنجاح', 'success')
            return redirect(url_for('hr.employee_details', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    departments = Department.query.filter_by(is_active=True).all()
    positions = Position.query.filter_by(is_active=True).all()
    branches = Branch.query.filter_by(is_active=True).all()

    return render_template('hr/edit_employee.html',
                         employee=employee,
                         departments=departments,
                         positions=positions,
                         branches=branches)

@bp.route('/employees/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def delete_employee(id):
    """Delete employee (soft delete)"""
    try:
        employee = Employee.query.get_or_404(id)
        employee.is_active = False
        employee.employment_status = 'terminated'
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        flash('تم حذف الموظف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.employees'))

# ==================== Departments ====================
@bp.route('/departments')
@login_required
@permission_required('hr.view')
def departments():
    """List all departments"""
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('hr/departments.html', departments=departments)

@bp.route('/departments/add', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def add_department():
    """Add new department"""
    try:
        # Generate code
        last_dept = Department.query.order_by(Department.id.desc()).first()
        if last_dept and last_dept.code:
            last_num = int(last_dept.code.replace('DEPT', ''))
            code = f'DEPT{last_num + 1:03d}'
        else:
            code = 'DEPT001'

        department = Department(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            code=code,
            parent_id=request.form.get('parent_id', type=int),
            manager_id=request.form.get('manager_id', type=int),
            description=request.form.get('description'),
            is_active=True
        )

        db.session.add(department)
        db.session.commit()
        flash('تم إضافة القسم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.departments'))

@bp.route('/departments/<int:id>/edit', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def edit_department(id):
    """Edit department"""
    try:
        department = Department.query.get_or_404(id)
        department.name = request.form.get('name')
        department.name_en = request.form.get('name_en')
        department.parent_id = request.form.get('parent_id', type=int)
        department.manager_id = request.form.get('manager_id', type=int)
        department.description = request.form.get('description')

        db.session.commit()
        flash('تم تحديث القسم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.departments'))

@bp.route('/departments/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def delete_department(id):
    """Delete department"""
    try:
        department = Department.query.get_or_404(id)
        department.is_active = False
        db.session.commit()
        flash('تم حذف القسم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.departments'))

# ==================== Positions ====================
@bp.route('/positions')
@login_required
@permission_required('hr.view')
def positions():
    """List all positions"""
    positions = Position.query.filter_by(is_active=True).all()
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('hr/positions.html', positions=positions, departments=departments)

@bp.route('/positions/add', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def add_position():
    """Add new position"""
    try:
        # Generate code
        last_pos = Position.query.order_by(Position.id.desc()).first()
        if last_pos and last_pos.code:
            last_num = int(last_pos.code.replace('POS', ''))
            code = f'POS{last_num + 1:03d}'
        else:
            code = 'POS001'

        position = Position(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            code=code,
            department_id=request.form.get('department_id', type=int),
            description=request.form.get('description'),
            is_active=True
        )

        db.session.add(position)
        db.session.commit()
        flash('تم إضافة المنصب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.positions'))

@bp.route('/positions/<int:id>/edit', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def edit_position(id):
    """Edit position"""
    try:
        position = Position.query.get_or_404(id)
        position.name = request.form.get('name')
        position.name_en = request.form.get('name_en')
        position.department_id = request.form.get('department_id', type=int)
        position.description = request.form.get('description')

        db.session.commit()
        flash('تم تحديث المنصب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.positions'))

@bp.route('/positions/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def delete_position(id):
    """Delete position"""
    try:
        position = Position.query.get_or_404(id)
        position.is_active = False
        db.session.commit()
        flash('تم حذف المنصب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.positions'))

# ==================== Attendance ====================
@bp.route('/attendance')
@login_required
@permission_required('hr.attendance.view')
def attendance():
    """Attendance records"""
    page = request.args.get('page', 1, type=int)
    employee_id = request.args.get('employee_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Attendance.query

    if employee_id:
        query = query.filter_by(employee_id=employee_id)

    if start_date:
        query = query.filter(Attendance.attendance_date >= datetime.strptime(start_date, '%Y-%m-%d').date())

    if end_date:
        query = query.filter(Attendance.attendance_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    records = query.order_by(Attendance.attendance_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    employees = Employee.query.filter_by(is_active=True).all()

    return render_template('hr/attendance.html',
                         records=records,
                         employees=employees,
                         employee_id=employee_id,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/attendance/add', methods=['GET', 'POST'])
@login_required
@permission_required('hr.attendance.manage')
def add_attendance():
    """Add attendance record"""
    if request.method == 'POST':
        try:
            attendance_date = datetime.strptime(request.form.get('attendance_date'), '%Y-%m-%d').date()
            check_in = datetime.strptime(f"{request.form.get('attendance_date')} {request.form.get('check_in')}", '%Y-%m-%d %H:%M') if request.form.get('check_in') else None
            check_out = datetime.strptime(f"{request.form.get('attendance_date')} {request.form.get('check_out')}", '%Y-%m-%d %H:%M') if request.form.get('check_out') else None

            # Calculate working hours
            working_hours = 0
            if check_in and check_out:
                working_hours = (check_out - check_in).total_seconds() / 3600

            attendance = Attendance(
                employee_id=request.form.get('employee_id', type=int),
                attendance_date=attendance_date,
                check_in=check_in,
                check_out=check_out,
                status=request.form.get('status', 'present'),
                working_hours=working_hours,
                overtime_hours=float(request.form.get('overtime_hours', 0)),
                notes=request.form.get('notes')
            )

            db.session.add(attendance)
            db.session.commit()
            flash('تم إضافة سجل الحضور بنجاح', 'success')
            return redirect(url_for('hr.attendance'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    employees = Employee.query.filter_by(is_active=True).all()
    return render_template('hr/add_attendance.html', employees=employees)

# ==================== Leaves ====================
@bp.route('/leaves')
@login_required
@permission_required('hr.view')
def leaves():
    """Leave requests"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    employee_id = request.args.get('employee_id', type=int)

    query = Leave.query

    if status:
        query = query.filter_by(status=status)

    if employee_id:
        query = query.filter_by(employee_id=employee_id)

    leaves = query.order_by(Leave.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    employees = Employee.query.filter_by(is_active=True).all()

    return render_template('hr/leaves.html',
                         leaves=leaves,
                         employees=employees,
                         status=status,
                         employee_id=employee_id)

@bp.route('/leaves/add', methods=['GET', 'POST'])
@login_required
@permission_required('hr.employees.manage')
def add_leave():
    """Add leave request"""
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            days_count = (end_date - start_date).days + 1

            leave = Leave(
                employee_id=request.form.get('employee_id', type=int),
                leave_type_id=request.form.get('leave_type_id', type=int),
                start_date=start_date,
                end_date=end_date,
                days_count=days_count,
                reason=request.form.get('reason'),
                status='pending'
            )

            db.session.add(leave)
            db.session.commit()
            flash('تم إضافة طلب الإجازة بنجاح', 'success')
            return redirect(url_for('hr.leaves'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    employees = Employee.query.filter_by(is_active=True).all()
    leave_types = LeaveType.query.filter_by(is_active=True).all()
    return render_template('hr/add_leave.html', employees=employees, leave_types=leave_types)

@bp.route('/leaves/<int:id>/approve', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def approve_leave(id):
    """Approve leave request"""
    try:
        leave = Leave.query.get_or_404(id)
        leave.status = 'approved'
        leave.approved_by = current_user.id
        leave.approved_at = datetime.utcnow()
        db.session.commit()
        flash('تم الموافقة على طلب الإجازة', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.leaves'))

@bp.route('/leaves/<int:id>/reject', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def reject_leave(id):
    """Reject leave request"""
    try:
        leave = Leave.query.get_or_404(id)
        leave.status = 'rejected'
        leave.approved_by = current_user.id
        leave.approved_at = datetime.utcnow()
        db.session.commit()
        flash('تم رفض طلب الإجازة', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.leaves'))

# ==================== Leave Types ====================
@bp.route('/leave-types')
@login_required
@permission_required('hr.view')
def leave_types():
    """Leave types"""
    leave_types = LeaveType.query.filter_by(is_active=True).all()
    return render_template('hr/leave_types.html', leave_types=leave_types)

@bp.route('/leave-types/add', methods=['POST'])
@login_required
@permission_required('hr.employees.manage')
def add_leave_type():
    """Add leave type"""
    try:
        leave_type = LeaveType(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            days_per_year=int(request.form.get('days_per_year', 0)),
            is_paid=request.form.get('is_paid') == 'on',
            is_active=True
        )

        db.session.add(leave_type)
        db.session.commit()
        flash('تم إضافة نوع الإجازة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.leave_types'))

# ==================== Payroll ====================
@bp.route('/payroll')
@login_required
@permission_required('hr.payroll.view')
def payroll():
    """Payroll management"""
    page = request.args.get('page', 1, type=int)
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    employee_id = request.args.get('employee_id', type=int)

    query = Payroll.query

    if month:
        query = query.filter_by(month=month)

    if year:
        query = query.filter_by(year=year)

    if employee_id:
        query = query.filter_by(employee_id=employee_id)

    payrolls = query.order_by(Payroll.year.desc(), Payroll.month.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    employees = Employee.query.filter_by(is_active=True).all()

    return render_template('hr/payroll.html',
                         payrolls=payrolls,
                         employees=employees,
                         month=month,
                         year=year,
                         employee_id=employee_id)

@bp.route('/payroll/generate', methods=['GET', 'POST'])
@login_required
@permission_required('hr.payroll.manage')
def generate_payroll():
    """Generate payroll for a month"""
    if request.method == 'POST':
        try:
            month = int(request.form.get('month'))
            year = int(request.form.get('year'))

            # Check if payroll already exists
            existing = Payroll.query.filter_by(month=month, year=year).first()
            if existing:
                flash('كشف الرواتب لهذا الشهر موجود بالفعل', 'warning')
                return redirect(url_for('hr.payroll'))

            # Get all active employees
            employees = Employee.query.filter_by(is_active=True).all()

            for employee in employees:
                # Calculate overtime
                overtime_hours = db.session.query(func.sum(Attendance.overtime_hours)).filter(
                    Attendance.employee_id == employee.id,
                    extract('month', Attendance.attendance_date) == month,
                    extract('year', Attendance.attendance_date) == year
                ).scalar() or 0

                overtime_amount = overtime_hours * (employee.basic_salary / 240)  # Assuming 240 working hours per month

                # Calculate net salary
                basic_salary = employee.basic_salary
                allowances = 0  # Can be customized
                deductions = 0  # Can be customized
                net_salary = basic_salary + allowances + overtime_amount - deductions

                payroll = Payroll(
                    employee_id=employee.id,
                    month=month,
                    year=year,
                    basic_salary=basic_salary,
                    allowances=allowances,
                    deductions=deductions,
                    overtime=overtime_amount,
                    net_salary=net_salary,
                    status='draft'
                )

                db.session.add(payroll)

            db.session.commit()
            flash(f'تم إنشاء كشف الرواتب لشهر {month}/{year} بنجاح', 'success')
            return redirect(url_for('hr.payroll'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    return render_template('hr/generate_payroll.html')

@bp.route('/payroll/<int:id>/approve', methods=['POST'])
@login_required
@permission_required('hr.payroll.manage')
def approve_payroll(id):
    """Approve payroll"""
    try:
        payroll = Payroll.query.get_or_404(id)
        payroll.status = 'approved'
        db.session.commit()
        flash('تم اعتماد الراتب', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.payroll'))

@bp.route('/payroll/<int:id>/pay', methods=['POST'])
@login_required
@permission_required('hr.payroll.manage')
def pay_payroll(id):
    """Mark payroll as paid"""
    try:
        payroll = Payroll.query.get_or_404(id)
        payroll.status = 'paid'
        payroll.payment_date = date.today()
        db.session.commit()
        flash('تم تسجيل دفع الراتب', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('hr.payroll'))

@bp.route('/payroll/<int:id>/details')
@login_required
@permission_required('hr.payroll.view')
def payroll_details(id):
    """Payroll details"""
    payroll = Payroll.query.get_or_404(id)
    return render_template('hr/payroll_details.html', payroll=payroll)

# ==================== Reports ====================
@bp.route('/reports')
@login_required
@permission_required('hr.view')
def reports():
    """HR Reports"""
    return render_template('hr/reports.html')

@bp.route('/reports/attendance-summary')
@login_required
@permission_required('hr.view')
def attendance_summary_report():
    """Attendance summary report"""
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    if not month or not year:
        # Default to current month
        today = date.today()
        month = today.month
        year = today.year

    # Get all employees
    employees = Employee.query.filter_by(is_active=True).all()

    # Get attendance for the month
    attendance_data = []
    for employee in employees:
        records = Attendance.query.filter(
            Attendance.employee_id == employee.id,
            extract('month', Attendance.attendance_date) == month,
            extract('year', Attendance.attendance_date) == year
        ).all()

        present_days = len([r for r in records if r.status == 'present'])
        absent_days = len([r for r in records if r.status == 'absent'])
        late_days = len([r for r in records if r.status == 'late'])
        total_hours = sum([r.working_hours for r in records])
        overtime_hours = sum([r.overtime_hours for r in records])

        attendance_data.append({
            'employee': employee,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'total_hours': total_hours,
            'overtime_hours': overtime_hours
        })

    return render_template('hr/attendance_summary_report.html',
                         attendance_data=attendance_data,
                         month=month,
                         year=year)


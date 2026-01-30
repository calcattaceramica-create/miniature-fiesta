from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.auth.decorators import permission_required
from app.accounting import bp
from app import db
from app.models_accounting import Account, JournalEntry, JournalEntryItem, Payment, BankAccount, CostCenter
from app.models import Customer, Supplier
from app.utils.accounting_helper import create_payment_journal_entry
from datetime import datetime, date

# ==================== دليل الحسابات ====================

@bp.route('/accounts')
@login_required
@permission_required('accounting.view')
def accounts():
    """Chart of accounts - دليل الحسابات"""
    accounts = Account.query.order_by(Account.code).all()

    # تنظيم الحسابات حسب النوع
    accounts_by_type = {
        'asset': [],
        'liability': [],
        'equity': [],
        'revenue': [],
        'expense': []
    }

    for account in accounts:
        if account.account_type in accounts_by_type:
            accounts_by_type[account.account_type].append(account)

    return render_template('accounting/accounts.html',
                         accounts=accounts,
                         accounts_by_type=accounts_by_type)

@bp.route('/accounts/add', methods=['GET', 'POST'])
@login_required
@permission_required('accounting.accounts.manage')
def add_account():
    """Add new account - إضافة حساب جديد"""
    if request.method == 'POST':
        try:
            account = Account(
                code=request.form.get('code'),
                name=request.form.get('name'),
                name_en=request.form.get('name_en'),
                account_type=request.form.get('account_type'),
                parent_id=request.form.get('parent_id', type=int) if request.form.get('parent_id') else None,
                description=request.form.get('description'),
                is_active=True
            )

            db.session.add(account)
            db.session.commit()

            flash('تم إضافة الحساب بنجاح', 'success')
            return redirect(url_for('accounting.accounts'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    # Get parent accounts for dropdown
    parent_accounts = Account.query.filter_by(is_active=True).order_by(Account.code).all()

    return render_template('accounting/add_account.html', parent_accounts=parent_accounts)

@bp.route('/accounts/<int:id>')
@login_required
@permission_required('accounting.view')
def account_details(id):
    """Account details - تفاصيل الحساب"""
    account = Account.query.get_or_404(id)

    # Get account transactions
    transactions = JournalEntryItem.query.filter_by(account_id=id)\
        .join(JournalEntry)\
        .filter(JournalEntry.status == 'posted')\
        .order_by(JournalEntry.entry_date.desc())\
        .limit(50).all()

    return render_template('accounting/account_details.html',
                         account=account,
                         transactions=transactions)

# ==================== القيود اليومية ====================

@bp.route('/journal-entries')
@login_required
@permission_required('accounting.transactions.view')
def journal_entries():
    """List journal entries - قائمة القيود اليومية"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')

    query = JournalEntry.query

    if status != 'all':
        query = query.filter_by(status=status)

    entries = query.order_by(JournalEntry.entry_date.desc(), JournalEntry.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('accounting/journal_entries.html',
                         entries=entries,
                         current_status=status)

@bp.route('/journal-entries/add', methods=['GET', 'POST'])
@login_required
@permission_required('accounting.transactions.create')
def add_journal_entry():
    """Add new journal entry - إضافة قيد يومي جديد"""
    if request.method == 'POST':
        try:
            # Generate entry number
            today = datetime.utcnow()
            prefix = f'JE{today.year}{today.month:02d}{today.day:02d}'

            last_entry = JournalEntry.query.filter(
                JournalEntry.entry_number.like(f'{prefix}%')
            ).order_by(JournalEntry.id.desc()).first()

            if last_entry:
                last_num = int(last_entry.entry_number[-4:])
                entry_number = f'{prefix}{(last_num + 1):04d}'
            else:
                entry_number = f'{prefix}0001'

            # Create journal entry
            entry = JournalEntry(
                entry_number=entry_number,
                entry_date=datetime.strptime(request.form.get('entry_date'), '%Y-%m-%d').date(),
                entry_type='manual',
                description=request.form.get('description'),
                user_id=current_user.id,
                status='draft'
            )

            db.session.add(entry)
            db.session.flush()

            # Add journal entry items
            accounts = request.form.getlist('account_id[]')
            descriptions = request.form.getlist('item_description[]')
            debits = request.form.getlist('debit[]')
            credits = request.form.getlist('credit[]')

            total_debit = 0
            total_credit = 0

            for i in range(len(accounts)):
                if accounts[i]:
                    debit = float(debits[i]) if debits[i] else 0
                    credit = float(credits[i]) if credits[i] else 0

                    item = JournalEntryItem(
                        journal_entry_id=entry.id,
                        account_id=int(accounts[i]),
                        description=descriptions[i],
                        debit=debit,
                        credit=credit
                    )

                    db.session.add(item)
                    total_debit += debit
                    total_credit += credit

            # Update totals
            entry.total_debit = total_debit
            entry.total_credit = total_credit

            # Validate balanced entry
            if abs(total_debit - total_credit) > 0.01:
                raise ValueError('القيد غير متوازن! يجب أن يتساوى المدين والدائن')

            db.session.commit()

            flash('تم إضافة القيد بنجاح', 'success')
            return redirect(url_for('accounting.journal_entry_details', id=entry.id))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    # Get accounts for dropdown
    accounts = Account.query.filter_by(is_active=True).order_by(Account.code).all()

    return render_template('accounting/add_journal_entry.html', accounts=accounts)

@bp.route('/journal-entries/<int:id>')
@login_required
@permission_required('accounting.transactions.view')
def journal_entry_details(id):
    """Journal entry details - تفاصيل القيد"""
    entry = JournalEntry.query.get_or_404(id)
    return render_template('accounting/journal_entry_details.html', entry=entry)

@bp.route('/journal-entries/<int:id>/post', methods=['POST'])
@login_required
@permission_required('accounting.transactions.create')
def post_journal_entry(id):
    """Post journal entry - ترحيل القيد"""
    try:
        entry = JournalEntry.query.get_or_404(id)

        if entry.status != 'draft':
            flash('هذا القيد تم ترحيله مسبقاً', 'warning')
            return redirect(url_for('accounting.journal_entry_details', id=id))

        # Update account balances
        for item in entry.items:
            account = Account.query.get(item.account_id)
            account.debit_balance += item.debit
            account.credit_balance += item.credit

            # Calculate current balance based on account type
            if account.account_type in ['asset', 'expense']:
                account.current_balance = account.debit_balance - account.credit_balance
            else:  # liability, equity, revenue
                account.current_balance = account.credit_balance - account.debit_balance

        # Update entry status
        entry.status = 'posted'
        entry.posted_by = current_user.id
        entry.posted_at = datetime.utcnow()

        db.session.commit()

        flash('تم ترحيل القيد بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('accounting.journal_entry_details', id=id))

@bp.route('/journal-entries/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('accounting.transactions.create')
def delete_journal_entry(id):
    """Delete journal entry - حذف القيد"""
    try:
        entry = JournalEntry.query.get_or_404(id)

        if entry.status == 'posted':
            flash('لا يمكن حذف قيد تم ترحيله', 'danger')
            return redirect(url_for('accounting.journal_entry_details', id=id))

        db.session.delete(entry)
        db.session.commit()

        flash('تم حذف القيد بنجاح', 'success')
        return redirect(url_for('accounting.journal_entries'))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('accounting.journal_entry_details', id=id))

# ==================== المدفوعات ====================

@bp.route('/payments')
@login_required
@permission_required('accounting.payments.view')
def payments():
    """List payments - قائمة المدفوعات"""
    page = request.args.get('page', 1, type=int)
    payment_type = request.args.get('type', 'all')

    query = Payment.query

    if payment_type != 'all':
        query = query.filter_by(payment_type=payment_type)

    payments = query.order_by(Payment.payment_date.desc(), Payment.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('accounting/payments.html',
                         payments=payments,
                         current_type=payment_type)

@bp.route('/payments/add', methods=['GET', 'POST'])
@login_required
@permission_required('accounting.payments.create')
def add_payment():
    """Add new payment - إضافة مدفوعة جديدة"""
    if request.method == 'POST':
        try:
            # Generate payment number
            today = datetime.utcnow()
            payment_type = request.form.get('payment_type')
            prefix = f'PAY{today.year}{today.month:02d}{today.day:02d}' if payment_type == 'payment' else f'REC{today.year}{today.month:02d}{today.day:02d}'

            last_payment = Payment.query.filter(
                Payment.payment_number.like(f'{prefix}%')
            ).order_by(Payment.id.desc()).first()

            if last_payment:
                last_num = int(last_payment.payment_number[-4:])
                payment_number = f'{prefix}{(last_num + 1):04d}'
            else:
                payment_number = f'{prefix}0001'

            # Create payment
            payment = Payment(
                payment_number=payment_number,
                payment_date=datetime.strptime(request.form.get('payment_date'), '%Y-%m-%d').date(),
                payment_type=payment_type,
                party_type=request.form.get('party_type'),
                party_id=request.form.get('party_id', type=int) if request.form.get('party_id') else None,
                amount=float(request.form.get('amount')),
                payment_method=request.form.get('payment_method'),
                bank_account_id=request.form.get('bank_account_id', type=int) if request.form.get('bank_account_id') else None,
                check_number=request.form.get('check_number'),
                check_date=datetime.strptime(request.form.get('check_date'), '%Y-%m-%d').date() if request.form.get('check_date') else None,
                reference_number=request.form.get('reference_number'),
                notes=request.form.get('notes'),
                user_id=current_user.id,
                status='draft'
            )

            db.session.add(payment)
            db.session.flush()

            # Create accounting journal entry
            try:
                journal_entry = create_payment_journal_entry(payment)
                if journal_entry:
                    flash(f'تم إنشاء القيد المحاسبي رقم {journal_entry.entry_number}', 'info')
            except Exception as je:
                # Log the error but don't fail the payment creation
                flash(f'تحذير: لم يتم إنشاء القيد المحاسبي: {str(je)}', 'warning')

            db.session.commit()

            flash('تم إضافة المدفوعة بنجاح', 'success')
            return redirect(url_for('accounting.payment_details', id=payment.id))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    # Get data for dropdowns
    customers = Customer.query.filter_by(is_active=True).all()
    suppliers = Supplier.query.filter_by(is_active=True).all()
    bank_accounts = BankAccount.query.filter_by(is_active=True).all()

    return render_template('accounting/add_payment.html',
                         customers=customers,
                         suppliers=suppliers,
                         bank_accounts=bank_accounts)

@bp.route('/payments/<int:id>')
@login_required
@permission_required('accounting.payments.view')
def payment_details(id):
    """Payment details - تفاصيل المدفوعة"""
    payment = Payment.query.get_or_404(id)

    # Get party name
    party_name = None
    if payment.party_type == 'customer' and payment.party_id:
        customer = Customer.query.get(payment.party_id)
        party_name = customer.name if customer else None
    elif payment.party_type == 'supplier' and payment.party_id:
        supplier = Supplier.query.get(payment.party_id)
        party_name = supplier.name if supplier else None

    return render_template('accounting/payment_details.html',
                         payment=payment,
                         party_name=party_name)

# ==================== الحسابات البنكية ====================

@bp.route('/bank-accounts')
@login_required
@permission_required('accounting.view')
def bank_accounts():
    """List bank accounts - قائمة الحسابات البنكية"""
    accounts = BankAccount.query.filter_by(is_active=True).all()

    # Calculate total balance
    total_balance = sum(acc.current_balance for acc in accounts)

    return render_template('accounting/bank_accounts.html',
                         accounts=accounts,
                         total_balance=total_balance)

@bp.route('/bank-accounts/add', methods=['GET', 'POST'])
@login_required
@permission_required('accounting.accounts.manage')
def add_bank_account():
    """Add new bank account - إضافة حساب بنكي جديد"""
    if request.method == 'POST':
        try:
            account = BankAccount(
                account_name=request.form.get('account_name'),
                account_number=request.form.get('account_number'),
                bank_name=request.form.get('bank_name'),
                branch=request.form.get('branch'),
                iban=request.form.get('iban'),
                swift_code=request.form.get('swift_code'),
                currency=request.form.get('currency', 'SAR'),
                current_balance=float(request.form.get('current_balance', 0)),
                account_id=request.form.get('account_id', type=int) if request.form.get('account_id') else None,
                is_active=True
            )

            db.session.add(account)
            db.session.commit()

            flash('تم إضافة الحساب البنكي بنجاح', 'success')
            return redirect(url_for('accounting.bank_accounts'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    # Get accounts for linking
    accounts = Account.query.filter_by(account_type='asset', is_active=True).order_by(Account.code).all()

    return render_template('accounting/add_bank_account.html', accounts=accounts)

# ==================== مراكز التكلفة ====================

@bp.route('/cost-centers')
@login_required
@permission_required('accounting.accounts.manage')
def cost_centers():
    """List cost centers - قائمة مراكز التكلفة"""
    centers = CostCenter.query.filter_by(is_active=True).order_by(CostCenter.code).all()
    return render_template('accounting/cost_centers.html', centers=centers)

@bp.route('/cost-centers/add', methods=['GET', 'POST'])
@login_required
@permission_required('accounting.accounts.manage')
def add_cost_center():
    """Add new cost center - إضافة مركز تكلفة جديد"""
    if request.method == 'POST':
        try:
            center = CostCenter(
                code=request.form.get('code'),
                name=request.form.get('name'),
                name_en=request.form.get('name_en'),
                parent_id=request.form.get('parent_id', type=int) if request.form.get('parent_id') else None,
                description=request.form.get('description'),
                is_active=True
            )

            db.session.add(center)
            db.session.commit()

            flash('تم إضافة مركز التكلفة بنجاح', 'success')
            return redirect(url_for('accounting.cost_centers'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')

    # Get parent cost centers
    parent_centers = CostCenter.query.filter_by(is_active=True).order_by(CostCenter.code).all()

    return render_template('accounting/add_cost_center.html', parent_centers=parent_centers)

# ==================== التقارير ====================

@bp.route('/reports/trial-balance')
@login_required
@permission_required('reports.financial')
def trial_balance():
    """Trial balance report - ميزان المراجعة"""
    accounts = Account.query.filter_by(is_active=True).order_by(Account.code).all()

    total_debit = sum(acc.debit_balance for acc in accounts)
    total_credit = sum(acc.credit_balance for acc in accounts)

    return render_template('accounting/trial_balance.html',
                         accounts=accounts,
                         total_debit=total_debit,
                         total_credit=total_credit)

@bp.route('/reports/balance-sheet')
@login_required
@permission_required('reports.financial')
def balance_sheet():
    """Balance sheet report - الميزانية العمومية"""
    # Assets
    assets = Account.query.filter_by(account_type='asset', is_active=True).order_by(Account.code).all()
    total_assets = sum(acc.current_balance for acc in assets)

    # Liabilities
    liabilities = Account.query.filter_by(account_type='liability', is_active=True).order_by(Account.code).all()
    total_liabilities = sum(acc.current_balance for acc in liabilities)

    # Equity
    equity = Account.query.filter_by(account_type='equity', is_active=True).order_by(Account.code).all()
    total_equity = sum(acc.current_balance for acc in equity)

    return render_template('accounting/balance_sheet.html',
                         assets=assets,
                         liabilities=liabilities,
                         equity=equity,
                         total_assets=total_assets,
                         total_liabilities=total_liabilities,
                         total_equity=total_equity)

@bp.route('/reports/income-statement')
@login_required
@permission_required('reports.financial')
def income_statement():
    """Income statement report - قائمة الدخل"""
    # Get date range from request or use current month
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    # Revenue accounts
    revenue_accounts = Account.query.filter_by(account_type='revenue', is_active=True).order_by(Account.code).all()
    total_revenue = sum(acc.credit_balance for acc in revenue_accounts)

    # COGS accounts (تكلفة البضاعة المباعة)
    cogs_accounts = Account.query.filter(
        Account.account_type == 'expense',
        Account.code.like('5%'),  # Assuming COGS accounts start with 5
        Account.is_active == True
    ).order_by(Account.code).all()
    total_cogs = sum(acc.debit_balance for acc in cogs_accounts)

    # Operating expense accounts
    expense_accounts = Account.query.filter(
        Account.account_type == 'expense',
        ~Account.code.like('5%'),  # Exclude COGS
        Account.is_active == True
    ).order_by(Account.code).all()
    total_expenses = sum(acc.debit_balance for acc in expense_accounts)

    # Calculations
    gross_profit = total_revenue - total_cogs
    net_profit = gross_profit - total_expenses

    return render_template('accounting/income_statement.html',
                         revenue_accounts=revenue_accounts,
                         cogs_accounts=cogs_accounts,
                         expense_accounts=expense_accounts,
                         total_revenue=total_revenue,
                         total_cogs=total_cogs,
                         total_expenses=total_expenses,
                         gross_profit=gross_profit,
                         net_profit=net_profit,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/reports/cash-flow')
@login_required
@permission_required('reports.financial')
def cash_flow():
    """Cash flow statement - قائمة التدفقات النقدية"""
    # Get date range
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    # Simplified cash flow data (should be calculated from actual transactions)
    net_profit = 0
    depreciation = 0
    inventory_change = 0
    receivables_change = 0
    payables_change = 0

    operating_cash_flow = net_profit + depreciation + inventory_change - receivables_change + payables_change

    # Investing activities
    fixed_assets_purchase = 0
    fixed_assets_sale = 0
    investing_cash_flow = fixed_assets_sale - fixed_assets_purchase

    # Financing activities
    new_loans = 0
    loan_repayment = 0
    capital_increase = 0
    dividends = 0
    financing_cash_flow = new_loans - loan_repayment + capital_increase - dividends

    # Net change
    net_cash_change = operating_cash_flow + investing_cash_flow + financing_cash_flow

    # Opening and closing cash
    opening_cash = 0
    closing_cash = opening_cash + net_cash_change

    return render_template('accounting/cash_flow.html',
                         start_date=start_date,
                         end_date=end_date,
                         net_profit=net_profit,
                         depreciation=depreciation,
                         inventory_change=inventory_change,
                         receivables_change=receivables_change,
                         payables_change=payables_change,
                         operating_cash_flow=operating_cash_flow,
                         fixed_assets_purchase=fixed_assets_purchase,
                         fixed_assets_sale=fixed_assets_sale,
                         investing_cash_flow=investing_cash_flow,
                         new_loans=new_loans,
                         loan_repayment=loan_repayment,
                         capital_increase=capital_increase,
                         dividends=dividends,
                         financing_cash_flow=financing_cash_flow,
                         net_cash_change=net_cash_change,
                         opening_cash=opening_cash,
                         closing_cash=closing_cash)

@bp.route('/reports/account-statement')
@login_required
@permission_required('reports.financial')
def account_statement():
    """Account statement - كشف حساب"""
    # Get all accounts for dropdown
    all_accounts = Account.query.filter_by(is_active=True).order_by(Account.code).all()

    # Get selected account
    account_id = request.args.get('account_id', type=int)
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    if not account_id:
        return render_template('accounting/account_statement.html',
                             all_accounts=all_accounts,
                             account=None,
                             entries=[],
                             opening_balance=0,
                             total_debit=0,
                             total_credit=0,
                             closing_balance=0,
                             start_date=start_date,
                             end_date=end_date,
                             selected_account_id=None)

    account = Account.query.get_or_404(account_id)

    # Get entries for this account
    entries = JournalEntryItem.query.join(JournalEntry).filter(
        JournalEntryItem.account_id == account_id,
        JournalEntry.status == 'posted'
    ).order_by(JournalEntry.entry_date).all()

    # Calculate balances
    opening_balance = 0  # Should be calculated from previous period
    total_debit = sum(entry.debit for entry in entries)
    total_credit = sum(entry.credit for entry in entries)
    closing_balance = opening_balance + total_debit - total_credit

    return render_template('accounting/account_statement.html',
                         all_accounts=all_accounts,
                         account=account,
                         entries=entries,
                         opening_balance=opening_balance,
                         total_debit=total_debit,
                         total_credit=total_credit,
                         closing_balance=closing_balance,
                         start_date=start_date,
                         end_date=end_date,
                         selected_account_id=account_id)

@bp.route('/reports/aging')
@login_required
@permission_required('reports.financial')
def aging_report():
    """Aging report - تقرير الأعمار"""
    report_type = request.args.get('type', 'receivables')
    report_date = date.today().strftime('%Y-%m-%d')

    # Simplified aging data (should be calculated from actual invoices)
    aging_data = []
    totals = {
        'total': 0,
        'current': 0,
        'days_31_60': 0,
        'days_61_90': 0,
        'days_91_120': 0,
        'over_120': 0
    }

    if report_type == 'receivables':
        # Get customers with outstanding balances
        customers = Customer.query.all()
        for customer in customers:
            # This should be calculated from actual invoices
            aging_data.append({
                'name': customer.name,
                'total': 0,
                'current': 0,
                'days_31_60': 0,
                'days_61_90': 0,
                'days_91_120': 0,
                'over_120': 0
            })
    else:
        # Get suppliers with outstanding balances
        suppliers = Supplier.query.all()
        for supplier in suppliers:
            aging_data.append({
                'name': supplier.name,
                'total': 0,
                'current': 0,
                'days_31_60': 0,
                'days_61_90': 0,
                'days_91_120': 0,
                'over_120': 0
            })

    return render_template('accounting/aging_report.html',
                         report_type=report_type,
                         report_date=report_date,
                         aging_data=aging_data,
                         totals=totals)

@bp.route('/reports/cost-center')
@login_required
@permission_required('reports.financial')
def cost_center_report():
    """Cost center report - تقرير مراكز التكلفة"""
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    # Get all cost centers
    centers = CostCenter.query.filter_by(is_active=True).order_by(CostCenter.code).all()

    # Calculate revenue and expenses for each cost center
    cost_centers = []
    total_revenue = 0
    total_expenses = 0
    total_net_profit = 0

    for center in centers:
        # This should be calculated from actual transactions
        revenue = 0
        expenses = 0
        net_profit = revenue - expenses

        cost_centers.append({
            'code': center.code,
            'name': center.name,
            'revenue': revenue,
            'expenses': expenses,
            'net_profit': net_profit
        })

        total_revenue += revenue
        total_expenses += expenses
        total_net_profit += net_profit

    return render_template('accounting/cost_center_report.html',
                         cost_centers=cost_centers,
                         total_revenue=total_revenue,
                         total_expenses=total_expenses,
                         total_net_profit=total_net_profit,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/reports')
@login_required
@permission_required('reports.view')
def reports():
    """Reports main page - صفحة التقارير الرئيسية"""
    # Get summary data
    total_assets = sum(acc.debit_balance for acc in Account.query.filter_by(account_type='asset', is_active=True).all())
    total_revenue = sum(acc.credit_balance for acc in Account.query.filter_by(account_type='revenue', is_active=True).all())
    total_expenses = sum(acc.debit_balance for acc in Account.query.filter_by(account_type='expense', is_active=True).all())
    net_profit = total_revenue - total_expenses

    return render_template('accounting/reports.html',
                         total_assets=total_assets,
                         total_revenue=total_revenue,
                         total_expenses=total_expenses,
                         net_profit=net_profit)

@bp.route('/dashboard')
@login_required
@permission_required('accounting.view')
def dashboard():
    """Accounting dashboard - لوحة التحكم المحاسبية"""
    # Summary data
    total_assets = sum(acc.debit_balance for acc in Account.query.filter_by(account_type='asset', is_active=True).all())

    # Monthly data (simplified - should be calculated from actual transactions)
    monthly_revenue = 0
    monthly_expenses = 0
    monthly_profit = monthly_revenue - monthly_expenses

    # Financial indicators
    current_assets = sum(acc.debit_balance for acc in Account.query.filter(
        Account.account_type == 'asset',
        Account.code.like('1%'),
        Account.is_active == True
    ).all())

    current_liabilities = sum(acc.credit_balance for acc in Account.query.filter(
        Account.account_type == 'liability',
        Account.code.like('2%'),
        Account.is_active == True
    ).all())

    current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
    profit_margin = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0

    total_liabilities = sum(acc.credit_balance for acc in Account.query.filter_by(account_type='liability', is_active=True).all())
    debt_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 else 0
    roa = (monthly_profit / total_assets * 100) if total_assets > 0 else 0

    # Cash and bank balances
    cash_balance = 0
    bank_balance = sum(acc.current_balance for acc in BankAccount.query.filter_by(is_active=True).all())

    # Recent entries
    recent_entries = JournalEntry.query.order_by(JournalEntry.entry_date.desc()).limit(5).all()

    # Alerts
    overdue_receivables_count = 0
    overdue_payables_count = 0
    pending_entries_count = JournalEntry.query.filter_by(status='draft').count()

    # Chart data (last 6 months)
    chart_labels = []
    revenue_data = []
    expense_data = []

    # Expense distribution
    expense_categories = []
    expense_values = []

    return render_template('accounting/dashboard.html',
                         total_assets=total_assets,
                         monthly_revenue=monthly_revenue,
                         monthly_expenses=monthly_expenses,
                         monthly_profit=monthly_profit,
                         current_ratio=current_ratio,
                         profit_margin=profit_margin,
                         debt_ratio=debt_ratio,
                         roa=roa,
                         cash_balance=cash_balance,
                         bank_balance=bank_balance,
                         recent_entries=recent_entries,
                         overdue_receivables_count=overdue_receivables_count,
                         overdue_payables_count=overdue_payables_count,
                         pending_entries_count=pending_entries_count,
                         chart_labels=chart_labels,
                         revenue_data=revenue_data,
                         expense_data=expense_data,
                         expense_categories=expense_categories,
                         expense_values=expense_values)


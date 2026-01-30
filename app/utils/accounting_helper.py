"""
Accounting Helper Functions
Functions to automatically create journal entries for various transactions
"""

from app import db
from app.models_accounting import JournalEntry, JournalEntryItem
from app.models_settings import AccountingSettings
from datetime import datetime

def create_sales_invoice_journal_entry(invoice):
    """
    Create journal entry for sales invoice
    
    Debit: Accounts Receivable (Customer)
    Credit: Sales Revenue
    Credit: Sales Tax Payable
    """
    settings = AccountingSettings.query.first()
    
    if not settings or not settings.auto_create_journal_entries:
        return None
    
    # Check required accounts
    if not settings.accounts_receivable_account_id or not settings.sales_revenue_account_id:
        raise ValueError('إعدادات الحسابات المحاسبية غير مكتملة')
    
    # Generate entry number
    today = datetime.utcnow()
    prefix = f'JE{today.year}{today.month:02d}'
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
        entry_date=invoice.invoice_date,
        entry_type='auto',
        reference_type='sales_invoice',
        reference_id=invoice.id,
        description=f'قيد تلقائي - فاتورة مبيعات رقم {invoice.invoice_number}',
        total_debit=invoice.total_amount,
        total_credit=invoice.total_amount,
        status='posted' if settings.auto_post_journal_entries else 'draft'
    )
    
    db.session.add(entry)
    db.session.flush()
    
    # Debit: Accounts Receivable
    debit_item = JournalEntryItem(
        journal_entry_id=entry.id,
        account_id=settings.accounts_receivable_account_id,
        description=f'مبيعات للعميل: {invoice.customer.name}',
        debit=invoice.total_amount,
        credit=0
    )
    db.session.add(debit_item)

    # Credit: Sales Revenue
    credit_revenue = JournalEntryItem(
        journal_entry_id=entry.id,
        account_id=settings.sales_revenue_account_id,
        description=f'إيرادات مبيعات - فاتورة {invoice.invoice_number}',
        debit=0,
        credit=invoice.subtotal
    )
    db.session.add(credit_revenue)

    # Credit: Sales Tax (if applicable)
    if invoice.tax_amount > 0 and settings.sales_tax_account_id:
        credit_tax = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=settings.sales_tax_account_id,
            description=f'ضريبة مبيعات - فاتورة {invoice.invoice_number}',
            debit=0,
            credit=invoice.tax_amount
        )
        db.session.add(credit_tax)
    
    # Update account balances if posted
    if entry.status == 'posted':
        update_account_balances(entry)
    
    return entry

def create_purchase_invoice_journal_entry(invoice):
    """
    Create journal entry for purchase invoice
    
    Debit: Purchase Expense / Inventory
    Debit: Purchase Tax (if applicable)
    Credit: Accounts Payable (Supplier)
    """
    settings = AccountingSettings.query.first()
    
    if not settings or not settings.auto_create_journal_entries:
        return None
    
    # Check required accounts
    if not settings.accounts_payable_account_id or not settings.purchase_expense_account_id:
        raise ValueError('إعدادات الحسابات المحاسبية غير مكتملة')
    
    # Generate entry number
    today = datetime.utcnow()
    prefix = f'JE{today.year}{today.month:02d}'
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
        entry_date=invoice.invoice_date,
        entry_type='auto',
        reference_type='purchase_invoice',
        reference_id=invoice.id,
        description=f'قيد تلقائي - فاتورة مشتريات رقم {invoice.invoice_number}',
        total_debit=invoice.total_amount,
        total_credit=invoice.total_amount,
        status='posted' if settings.auto_post_journal_entries else 'draft'
    )
    
    db.session.add(entry)
    db.session.flush()
    
    # Debit: Purchase Expense
    debit_expense = JournalEntryItem(
        journal_entry_id=entry.id,
        account_id=settings.purchase_expense_account_id,
        description=f'مشتريات من المورد: {invoice.supplier.name}',
        debit=invoice.subtotal,
        credit=0
    )
    db.session.add(debit_expense)

    # Debit: Purchase Tax (if applicable)
    if invoice.tax_amount > 0 and settings.purchase_tax_account_id:
        debit_tax = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=settings.purchase_tax_account_id,
            description=f'ضريبة مشتريات - فاتورة {invoice.invoice_number}',
            debit=invoice.tax_amount,
            credit=0
        )
        db.session.add(debit_tax)

    # Credit: Accounts Payable
    credit_payable = JournalEntryItem(
        journal_entry_id=entry.id,
        account_id=settings.accounts_payable_account_id,
        description=f'مستحق للمورد: {invoice.supplier.name}',
        debit=0,
        credit=invoice.total_amount
    )
    db.session.add(credit_payable)

    # Update account balances if posted
    if entry.status == 'posted':
        update_account_balances(entry)

    return entry

def create_payment_journal_entry(payment):
    """
    Create journal entry for payment/receipt

    For Payment (to supplier):
    Debit: Accounts Payable
    Credit: Cash/Bank

    For Receipt (from customer):
    Debit: Cash/Bank
    Credit: Accounts Receivable
    """
    settings = AccountingSettings.query.first()

    if not settings or not settings.auto_create_journal_entries:
        return None

    # Generate entry number
    today = datetime.utcnow()
    prefix = f'JE{today.year}{today.month:02d}'
    last_entry = JournalEntry.query.filter(
        JournalEntry.entry_number.like(f'{prefix}%')
    ).order_by(JournalEntry.id.desc()).first()

    if last_entry:
        last_num = int(last_entry.entry_number[-4:])
        entry_number = f'{prefix}{(last_num + 1):04d}'
    else:
        entry_number = f'{prefix}0001'

    # Determine cash/bank account
    cash_account_id = payment.bank_account.account_id if payment.bank_account else settings.cash_account_id

    # Create journal entry
    entry = JournalEntry(
        entry_number=entry_number,
        entry_date=payment.payment_date,
        entry_type='auto',
        reference_type='payment',
        reference_id=payment.id,
        description=f'قيد تلقائي - {payment.payment_type} رقم {payment.payment_number}',
        total_debit=payment.amount,
        total_credit=payment.amount,
        status='posted' if settings.auto_post_journal_entries else 'draft'
    )

    db.session.add(entry)
    db.session.flush()

    if payment.payment_type == 'receipt':
        # Receipt from customer
        # Debit: Cash/Bank
        debit_cash = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=cash_account_id,
            description=f'تحصيل من العميل',
            debit=payment.amount,
            credit=0
        )
        db.session.add(debit_cash)

        # Credit: Accounts Receivable
        credit_receivable = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=settings.accounts_receivable_account_id,
            description=f'تحصيل من العميل',
            debit=0,
            credit=payment.amount
        )
        db.session.add(credit_receivable)

    else:
        # Payment to supplier
        # Debit: Accounts Payable
        debit_payable = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=settings.accounts_payable_account_id,
            description=f'دفع للمورد',
            debit=payment.amount,
            credit=0
        )
        db.session.add(debit_payable)

        # Credit: Cash/Bank
        credit_cash = JournalEntryItem(
            journal_entry_id=entry.id,
            account_id=cash_account_id,
            description=f'دفع للمورد',
            debit=0,
            credit=payment.amount
        )
        db.session.add(credit_cash)

    # Update account balances if posted
    if entry.status == 'posted':
        update_account_balances(entry)

    return entry

def update_account_balances(entry):
    """Update account balances after posting journal entry"""
    from app.models_accounting import Account

    for item in entry.items:
        account = Account.query.get(item.account_id)
        if account:
            account.debit_balance += item.debit
            account.credit_balance += item.credit

            # Calculate current balance based on account type
            if account.account_type in ['asset', 'expense']:
                account.current_balance = account.debit_balance - account.credit_balance
            else:  # liability, equity, revenue
                account.current_balance = account.credit_balance - account.debit_balance



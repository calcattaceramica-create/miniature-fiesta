from app import db
from datetime import datetime

# Settings Models
class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(64), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(20), default='string')  # string, integer, float, boolean, json
    description = db.Column(db.Text)
    module = db.Column(db.String(50))  # sales, purchases, accounting, inventory, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemSettings {self.setting_key}>'

class AccountingSettings(db.Model):
    __tablename__ = 'accounting_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Sales Accounts
    sales_revenue_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    sales_tax_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    sales_discount_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    accounts_receivable_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    sales_cost_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Purchase Accounts
    purchase_expense_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    purchase_tax_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    purchase_discount_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    accounts_payable_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Inventory Accounts
    inventory_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    inventory_adjustment_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Cash & Bank Accounts
    cash_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'))
    
    # POS Accounts
    pos_cash_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    pos_card_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Settings
    auto_create_journal_entries = db.Column(db.Boolean, default=True)
    auto_post_journal_entries = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales_revenue_account = db.relationship('Account', foreign_keys=[sales_revenue_account_id])
    sales_tax_account = db.relationship('Account', foreign_keys=[sales_tax_account_id])
    sales_discount_account = db.relationship('Account', foreign_keys=[sales_discount_account_id])
    accounts_receivable_account = db.relationship('Account', foreign_keys=[accounts_receivable_account_id])
    sales_cost_account = db.relationship('Account', foreign_keys=[sales_cost_account_id])
    
    purchase_expense_account = db.relationship('Account', foreign_keys=[purchase_expense_account_id])
    purchase_tax_account = db.relationship('Account', foreign_keys=[purchase_tax_account_id])
    purchase_discount_account = db.relationship('Account', foreign_keys=[purchase_discount_account_id])
    accounts_payable_account = db.relationship('Account', foreign_keys=[accounts_payable_account_id])
    
    inventory_account = db.relationship('Account', foreign_keys=[inventory_account_id])
    inventory_adjustment_account = db.relationship('Account', foreign_keys=[inventory_adjustment_account_id])
    
    cash_account = db.relationship('Account', foreign_keys=[cash_account_id])
    
    pos_cash_account = db.relationship('Account', foreign_keys=[pos_cash_account_id])
    pos_card_account = db.relationship('Account', foreign_keys=[pos_card_account_id])
    
    def __repr__(self):
        return f'<AccountingSettings {self.id}>'


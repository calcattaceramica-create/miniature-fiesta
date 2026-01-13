# 🗄️ Database & Models - README

## Quick Reference

### Files Structure

```
app/
├── __init__.py              # Database initialization
├── models.py                # Core models (User, Role, Company, etc.)
├── models_inventory.py      # Inventory models
├── models_sales.py         # Sales models
├── models_purchases.py     # Purchase models
├── models_accounting.py    # Accounting models
├── models_hr.py            # HR models
└── models_pos.py           # POS models
```

---

## Models Overview

### Core Models (models.py)
- `User` - System users
- `Role` - User roles
- `Permission` - System permissions
- `Company` - Company information
- `Branch` - Company branches
- `Currency` - Currencies

### Inventory Models (models_inventory.py)
- `Category` - Product categories
- `Unit` - Units of measurement
- `Product` - Products
- `Warehouse` - Warehouses
- `Stock` - Stock levels
- `StockMovement` - Stock movements

### Sales Models (models_sales.py)
- `Customer` - Customers
- `SalesInvoice` - Sales invoices
- `SalesInvoiceItem` - Invoice line items
- `Quotation` - Quotations
- `SalesOrder` - Sales orders
- `SalesReturn` - Sales returns

### Purchase Models (models_purchases.py)
- `Supplier` - Suppliers
- `PurchaseOrder` - Purchase orders
- `PurchaseInvoice` - Purchase invoices
- `PurchaseInvoiceItem` - Invoice line items
- `PurchaseReturn` - Purchase returns

### Accounting Models (models_accounting.py)
- `Account` - Chart of accounts
- `JournalEntry` - Journal entries
- `JournalEntryItem` - Entry line items
- `Payment` - Payments
- `BankAccount` - Bank accounts
- `CostCenter` - Cost centers

### HR Models (models_hr.py)
- `Employee` - Employees
- `Department` - Departments
- `Position` - Job positions
- `Attendance` - Attendance records
- `Leave` - Leave requests
- `Payroll` - Payroll records

### POS Models (models_pos.py)
- `POSSession` - POS sessions
- `POSOrder` - POS orders
- `POSOrderItem` - Order line items

---

## Common Operations

### Creating Records

```python
from app import db
from app.models import User

# Create a new user
user = User(username='john', email='john@example.com')
user.set_password('password')
db.session.add(user)
db.session.commit()
```

### Querying Records

```python
# Get by ID
user = User.query.get(1)

# Get by filter
user = User.query.filter_by(username='john').first()

# Get all
users = User.query.all()

# Get with conditions
active_users = User.query.filter_by(is_active=True).all()
```

### Updating Records

```python
user = User.query.get(1)
user.full_name = 'John Doe'
db.session.commit()
```

### Deleting Records

```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

---

## Relationships

### One-to-Many

```python
# Company has many branches
company = Company.query.get(1)
branches = company.branches

# Branch has many users
branch = Branch.query.get(1)
users = branch.users
```

### Many-to-Many

```python
# Role has many permissions
role = Role.query.get(1)
permissions = role.permissions
```

### Self-Referential

```python
# Category has parent and children
category = Category.query.get(1)
parent = category.parent
children = category.children
```

---

## Best Practices

1. **Always use transactions**
```python
try:
    db.session.add(obj)
    db.session.commit()
except:
    db.session.rollback()
    raise
```

2. **Use relationships instead of manual joins**
```python
# Good
product.category.name

# Bad
category = Category.query.get(product.category_id)
category.name
```

3. **Check for existence before operations**
```python
user = User.query.filter_by(username='john').first()
if not user:
    # Handle not found
    pass
```

4. **Use bulk operations for multiple records**
```python
db.session.bulk_insert_mappings(Product, products_data)
db.session.commit()
```

---

## Database Initialization

### First Time Setup

```bash
# Initialize database
python init_db.py

# Add sample data
python seed_data.py
```

### Using Migrations

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

---

## Troubleshooting

### "No such table" error
```bash
python init_db.py
```

### "Connection refused" error
- Check database server is running
- Verify connection string in `.env`

### "Access denied" error
- Check username and password
- Verify user has proper permissions

---

## References

- [DATABASE.md](../DATABASE.md) - Full database documentation
- [MODELS.md](../MODELS.md) - Models documentation
- [MIGRATION.md](../MIGRATION.md) - Migration guide

---

**Last Updated:** 2026-01-10


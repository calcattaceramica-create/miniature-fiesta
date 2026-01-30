# Multi-Tenancy Implementation Plan
# خطة تنفيذ نظام Multi-Tenancy

## 📋 Overview - نظرة عامة

كل ترخيص = عميل مستقل مع بيانات منفصلة تماماً

## 🎯 Models That Need license_id

### ✅ Already Has license_id:
1. **User** - المستخدمون (already has license_id)

### 🔧 Needs license_id:

#### Core Master Data (البيانات الأساسية):
2. **Company** - الشركات
3. **Branch** - الفروع
4. **Currency** - العملات

#### Inventory (المخزون):
5. **Category** - التصنيفات
6. **Unit** - وحدات القياس
7. **Product** - المنتجات
8. **Warehouse** - المستودعات
9. **Stock** - المخزون
10. **StockMovement** - حركات المخزون

#### Sales (المبيعات):
11. **Customer** - العملاء
12. **SalesInvoice** - فواتير البيع
13. **SalesInvoiceItem** - تفاصيل فواتير البيع
14. **Quotation** - عروض الأسعار
15. **QuotationItem** - تفاصيل عروض الأسعار
16. **SalesOrder** - طلبات البيع

#### Purchases (المشتريات):
17. **Supplier** - الموردين
18. **PurchaseOrder** - طلبات الشراء
19. **PurchaseOrderItem** - تفاصيل طلبات الشراء
20. **PurchaseInvoice** - فواتير الشراء
21. **PurchaseInvoiceItem** - تفاصيل فواتير الشراء
22. **PurchaseReturn** - مرتجعات الشراء
23. **PurchaseReturnItem** - تفاصيل مرتجعات الشراء

#### Accounting (المحاسبة):
24. **Account** - الحسابات
25. **JournalEntry** - القيود اليومية
26. **JournalEntryItem** - تفاصيل القيود
27. **Payment** - المدفوعات
28. **BankAccount** - الحسابات البنكية
29. **CostCenter** - مراكز التكلفة

#### HR (الموارد البشرية):
30. **Employee** - الموظفين
31. **Department** - الأقسام
32. **Position** - الوظائف
33. **Attendance** - الحضور
34. **Leave** - الإجازات
35. **LeaveType** - أنواع الإجازات
36. **Payroll** - الرواتب

#### POS (نقاط البيع):
37. **POSSession** - جلسات نقاط البيع
38. **POSOrder** - طلبات نقاط البيع
39. **POSOrderItem** - تفاصيل طلبات نقاط البيع

#### CRM (إدارة علاقات العملاء):
40. **Lead** - العملاء المحتملين
41. **Opportunity** - الفرص
42. **Activity** - الأنشطة

#### Settings (الإعدادات):
43. **SystemSettings** - إعدادات النظام
44. **AccountingSettings** - إعدادات المحاسبة

### ❌ Does NOT Need license_id (Shared Globally):
- **Role** - الأدوار (shared across all licenses)
- **Permission** - الصلاحيات (shared across all licenses)
- **License** - التراخيص (obviously!)
- **SecurityLog** - سجل الأمان (for admin monitoring)

## 📝 Implementation Steps

### Step 1: Add license_id Column to Models
- Add `license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False, index=True)`
- Add relationship: `license = db.relationship('License', backref='...')`

### Step 2: Create Migration Script
- Script to add license_id column to all tables
- Update existing data with default license_id

### Step 3: Create Query Filter Mixin
- Create a base mixin that automatically filters by license_id
- Override query property to add license_id filter

### Step 4: Update All Models
- Inherit from the mixin
- Add license_id to all relevant models

### Step 5: Create Middleware
- Before each request, set current license_id from current_user
- Automatically inject license_id when creating new records

### Step 6: Update Routes
- Ensure all queries use current_user.license_id
- Add license_id when creating new records

### Step 7: Testing
- Create second test license
- Verify data isolation
- Test cross-license access prevention

## 🔒 Security Considerations

1. **Automatic Filtering**: All queries must automatically filter by license_id
2. **Creation**: All new records must have license_id set
3. **Updates**: Cannot update records from other licenses
4. **Deletes**: Cannot delete records from other licenses
5. **API Access**: API must respect license_id boundaries

## 📊 Database Changes

```sql
-- Example for products table
ALTER TABLE products ADD COLUMN license_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX idx_products_license_id ON products(license_id);
ALTER TABLE products ADD FOREIGN KEY (license_id) REFERENCES licenses(id);
```

## ✅ Success Criteria

- ✅ Each license sees only its own data
- ✅ Cannot access other license's data
- ✅ New records automatically get license_id
- ✅ Queries automatically filtered by license_id
- ✅ Admin can see all licenses (optional)
- ✅ Easy to create new license with clean data

## 🎯 Next Steps

1. ✅ Create this plan
2. ⏳ Add license_id to all model files
3. ⏳ Create migration script
4. ⏳ Create query filter mixin
5. ⏳ Update routes
6. ⏳ Test with second license

---

**Total Models to Update: ~44 models**
**Estimated Time: 2-3 hours**


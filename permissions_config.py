#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Permissions Configuration
تعريف جميع الصلاحيات والأدوار في النظام
"""

# تعريف الصلاحيات حسب الوحدات
PERMISSIONS = {
    # صلاحيات المبيعات
    'sales': [
        {'name': 'sales.view', 'name_ar': 'عرض المبيعات', 'module': 'sales'},
        {'name': 'sales.create', 'name_ar': 'إنشاء فاتورة مبيعات', 'module': 'sales'},
        {'name': 'sales.edit', 'name_ar': 'تعديل فاتورة مبيعات', 'module': 'sales'},
        {'name': 'sales.delete', 'name_ar': 'حذف فاتورة مبيعات', 'module': 'sales'},
        {'name': 'sales.complete', 'name_ar': 'إتمام عملية البيع', 'module': 'sales'},
        {'name': 'sales.cancel', 'name_ar': 'إلغاء فاتورة مبيعات', 'module': 'sales'},
        {'name': 'sales.print', 'name_ar': 'طباعة فاتورة مبيعات', 'module': 'sales'},
        {'name': 'sales.quotations', 'name_ar': 'إدارة عروض الأسعار', 'module': 'sales'},
        {'name': 'sales.returns', 'name_ar': 'إدارة مرتجعات المبيعات', 'module': 'sales'},
    ],
    
    # صلاحيات المشتريات
    'purchases': [
        {'name': 'purchases.view', 'name_ar': 'عرض المشتريات', 'module': 'purchases'},
        {'name': 'purchases.create', 'name_ar': 'إنشاء فاتورة مشتريات', 'module': 'purchases'},
        {'name': 'purchases.edit', 'name_ar': 'تعديل فاتورة مشتريات', 'module': 'purchases'},
        {'name': 'purchases.delete', 'name_ar': 'حذف فاتورة مشتريات', 'module': 'purchases'},
        {'name': 'purchases.complete', 'name_ar': 'إتمام عملية الشراء', 'module': 'purchases'},
        {'name': 'purchases.cancel', 'name_ar': 'إلغاء فاتورة مشتريات', 'module': 'purchases'},
        {'name': 'purchases.print', 'name_ar': 'طباعة فاتورة مشتريات', 'module': 'purchases'},
        {'name': 'purchases.orders', 'name_ar': 'إدارة طلبات الشراء', 'module': 'purchases'},
        {'name': 'purchases.returns', 'name_ar': 'إدارة مرتجعات المشتريات', 'module': 'purchases'},
    ],
    
    # صلاحيات المخزون
    'inventory': [
        {'name': 'inventory.view', 'name_ar': 'عرض المخزون', 'module': 'inventory'},
        {'name': 'inventory.products.view', 'name_ar': 'عرض المنتجات', 'module': 'inventory'},
        {'name': 'inventory.products.create', 'name_ar': 'إضافة منتج', 'module': 'inventory'},
        {'name': 'inventory.products.edit', 'name_ar': 'تعديل منتج', 'module': 'inventory'},
        {'name': 'inventory.products.delete', 'name_ar': 'حذف منتج', 'module': 'inventory'},
        {'name': 'inventory.categories.manage', 'name_ar': 'إدارة التصنيفات', 'module': 'inventory'},
        {'name': 'inventory.units.manage', 'name_ar': 'إدارة الوحدات', 'module': 'inventory'},
        {'name': 'inventory.warehouses.view', 'name_ar': 'عرض المستودعات', 'module': 'inventory'},
        {'name': 'inventory.warehouses.manage', 'name_ar': 'إدارة المستودعات', 'module': 'inventory'},
        {'name': 'inventory.stock.view', 'name_ar': 'عرض المخزون', 'module': 'inventory'},
        {'name': 'inventory.stock.adjust', 'name_ar': 'تعديل المخزون', 'module': 'inventory'},
        {'name': 'inventory.stock.transfer', 'name_ar': 'نقل المخزون', 'module': 'inventory'},
    ],
    
    # صلاحيات العملاء
    'customers': [
        {'name': 'customers.view', 'name_ar': 'عرض العملاء', 'module': 'customers'},
        {'name': 'customers.create', 'name_ar': 'إضافة عميل', 'module': 'customers'},
        {'name': 'customers.edit', 'name_ar': 'تعديل عميل', 'module': 'customers'},
        {'name': 'customers.delete', 'name_ar': 'حذف عميل', 'module': 'customers'},
    ],
    
    # صلاحيات الموردين
    'suppliers': [
        {'name': 'suppliers.view', 'name_ar': 'عرض الموردين', 'module': 'suppliers'},
        {'name': 'suppliers.create', 'name_ar': 'إضافة مورد', 'module': 'suppliers'},
        {'name': 'suppliers.edit', 'name_ar': 'تعديل مورد', 'module': 'suppliers'},
        {'name': 'suppliers.delete', 'name_ar': 'حذف مورد', 'module': 'suppliers'},
    ],
    
    # صلاحيات المحاسبة
    'accounting': [
        {'name': 'accounting.view', 'name_ar': 'عرض المحاسبة', 'module': 'accounting'},
        {'name': 'accounting.accounts.manage', 'name_ar': 'إدارة الحسابات', 'module': 'accounting'},
        {'name': 'accounting.transactions.view', 'name_ar': 'عرض المعاملات', 'module': 'accounting'},
        {'name': 'accounting.transactions.create', 'name_ar': 'إنشاء معاملة', 'module': 'accounting'},
        {'name': 'accounting.payments.view', 'name_ar': 'عرض المدفوعات', 'module': 'accounting'},
        {'name': 'accounting.payments.create', 'name_ar': 'إنشاء مدفوعة', 'module': 'accounting'},
    ],
    
    # صلاحيات نقاط البيع
    'pos': [
        {'name': 'pos.access', 'name_ar': 'الوصول إلى نقاط البيع', 'module': 'pos'},
        {'name': 'pos.sell', 'name_ar': 'إجراء عملية بيع', 'module': 'pos'},
        {'name': 'pos.refund', 'name_ar': 'إجراء استرجاع', 'module': 'pos'},
        {'name': 'pos.discount', 'name_ar': 'منح خصم', 'module': 'pos'},
        {'name': 'pos.close_shift', 'name_ar': 'إغلاق الوردية', 'module': 'pos'},
    ],
    
    # صلاحيات الموارد البشرية
    'hr': [
        {'name': 'hr.view', 'name_ar': 'عرض الموارد البشرية', 'module': 'hr'},
        {'name': 'hr.employees.view', 'name_ar': 'عرض الموظفين', 'module': 'hr'},
        {'name': 'hr.employees.manage', 'name_ar': 'إدارة الموظفين', 'module': 'hr'},
        {'name': 'hr.attendance.view', 'name_ar': 'عرض الحضور', 'module': 'hr'},
        {'name': 'hr.attendance.manage', 'name_ar': 'إدارة الحضور', 'module': 'hr'},
        {'name': 'hr.payroll.view', 'name_ar': 'عرض الرواتب', 'module': 'hr'},
        {'name': 'hr.payroll.manage', 'name_ar': 'إدارة الرواتب', 'module': 'hr'},
    ],
    
    # صلاحيات التقارير
    'reports': [
        {'name': 'reports.view', 'name_ar': 'عرض التقارير', 'module': 'reports'},
        {'name': 'reports.sales', 'name_ar': 'تقارير المبيعات', 'module': 'reports'},
        {'name': 'reports.purchases', 'name_ar': 'تقارير المشتريات', 'module': 'reports'},
        {'name': 'reports.inventory', 'name_ar': 'تقارير المخزون', 'module': 'reports'},
        {'name': 'reports.financial', 'name_ar': 'التقارير المالية', 'module': 'reports'},
        {'name': 'reports.export', 'name_ar': 'تصدير التقارير', 'module': 'reports'},
    ],
    
    # صلاحيات الإعدادات
    'settings': [
        {'name': 'settings.view', 'name_ar': 'عرض الإعدادات', 'module': 'settings'},
        {'name': 'settings.company', 'name_ar': 'إعدادات الشركة', 'module': 'settings'},
        {'name': 'settings.users.view', 'name_ar': 'عرض المستخدمين', 'module': 'settings'},
        {'name': 'settings.users.manage', 'name_ar': 'إدارة المستخدمين', 'module': 'settings'},
        {'name': 'settings.roles.view', 'name_ar': 'عرض الأدوار', 'module': 'settings'},
        {'name': 'settings.roles.manage', 'name_ar': 'إدارة الأدوار', 'module': 'settings'},
        {'name': 'settings.permissions.view', 'name_ar': 'عرض الصلاحيات', 'module': 'settings'},
        {'name': 'settings.permissions.manage', 'name_ar': 'إدارة الصلاحيات', 'module': 'settings'},
        {'name': 'settings.branches.manage', 'name_ar': 'إدارة الفروع', 'module': 'settings'},
    ],
}

# تعريف الأدوار الافتراضية
DEFAULT_ROLES = [
    {
        'name': 'admin',
        'name_ar': 'مدير النظام',
        'description': 'صلاحيات كاملة على جميع أجزاء النظام',
        'permissions': 'all'  # جميع الصلاحيات
    },
    {
        'name': 'manager',
        'name_ar': 'مدير',
        'description': 'صلاحيات إدارية على معظم أجزاء النظام',
        'permissions': [
            # المبيعات
            'sales.view', 'sales.create', 'sales.edit', 'sales.complete', 'sales.print',
            'sales.quotations', 'sales.returns',
            # المشتريات
            'purchases.view', 'purchases.create', 'purchases.edit', 'purchases.complete',
            'purchases.print', 'purchases.orders', 'purchases.returns',
            # المخزون
            'inventory.view', 'inventory.products.view', 'inventory.products.create',
            'inventory.products.edit', 'inventory.categories.manage', 'inventory.units.manage',
            'inventory.warehouses.view', 'inventory.stock.view', 'inventory.stock.adjust',
            'inventory.stock.transfer',
            # العملاء والموردين
            'customers.view', 'customers.create', 'customers.edit',
            'suppliers.view', 'suppliers.create', 'suppliers.edit',
            # المحاسبة
            'accounting.view', 'accounting.transactions.view', 'accounting.payments.view',
            'accounting.payments.create',
            # نقاط البيع
            'pos.access', 'pos.sell', 'pos.refund', 'pos.discount', 'pos.close_shift',
            # الموارد البشرية
            'hr.view', 'hr.employees.view', 'hr.attendance.view', 'hr.attendance.manage',
            # التقارير
            'reports.view', 'reports.sales', 'reports.purchases', 'reports.inventory',
            'reports.financial', 'reports.export',
            # الإعدادات (محدودة)
            'settings.view', 'settings.company',
        ]
    },
    {
        'name': 'sales_manager',
        'name_ar': 'مدير مبيعات',
        'description': 'صلاحيات إدارة المبيعات والعملاء',
        'permissions': [
            # المبيعات
            'sales.view', 'sales.create', 'sales.edit', 'sales.complete', 'sales.cancel',
            'sales.print', 'sales.quotations', 'sales.returns',
            # العملاء
            'customers.view', 'customers.create', 'customers.edit',
            # المخزون (عرض فقط)
            'inventory.view', 'inventory.products.view', 'inventory.stock.view',
            # نقاط البيع
            'pos.access', 'pos.sell', 'pos.refund', 'pos.discount', 'pos.close_shift',
            # التقارير
            'reports.view', 'reports.sales',
        ]
    },
    {
        'name': 'sales_employee',
        'name_ar': 'موظف مبيعات',
        'description': 'صلاحيات إجراء عمليات البيع',
        'permissions': [
            # المبيعات
            'sales.view', 'sales.create', 'sales.complete', 'sales.print',
            # العملاء (عرض فقط)
            'customers.view',
            # المخزون (عرض فقط)
            'inventory.view', 'inventory.products.view', 'inventory.stock.view',
            # نقاط البيع
            'pos.access', 'pos.sell', 'pos.refund',
        ]
    },
    {
        'name': 'purchases_manager',
        'name_ar': 'مدير مشتريات',
        'description': 'صلاحيات إدارة المشتريات والموردين',
        'permissions': [
            # المشتريات
            'purchases.view', 'purchases.create', 'purchases.edit', 'purchases.complete',
            'purchases.cancel', 'purchases.print', 'purchases.orders', 'purchases.returns',
            # الموردين
            'suppliers.view', 'suppliers.create', 'suppliers.edit',
            # المخزون
            'inventory.view', 'inventory.products.view', 'inventory.stock.view',
            'inventory.stock.adjust',
            # التقارير
            'reports.view', 'reports.purchases', 'reports.inventory',
        ]
    },
    {
        'name': 'inventory_manager',
        'name_ar': 'مدير مخزون',
        'description': 'صلاحيات إدارة المخزون والمنتجات',
        'permissions': [
            # المخزون
            'inventory.view', 'inventory.products.view', 'inventory.products.create',
            'inventory.products.edit', 'inventory.categories.manage', 'inventory.units.manage',
            'inventory.warehouses.view', 'inventory.warehouses.manage', 'inventory.stock.view',
            'inventory.stock.adjust', 'inventory.stock.transfer',
            # المشتريات (عرض فقط)
            'purchases.view',
            # التقارير
            'reports.view', 'reports.inventory',
        ]
    },
    {
        'name': 'accountant',
        'name_ar': 'محاسب',
        'description': 'صلاحيات المحاسبة والتقارير المالية',
        'permissions': [
            # المحاسبة
            'accounting.view', 'accounting.accounts.manage', 'accounting.transactions.view',
            'accounting.transactions.create', 'accounting.payments.view', 'accounting.payments.create',
            # المبيعات والمشتريات (عرض فقط)
            'sales.view', 'purchases.view',
            # العملاء والموردين (عرض فقط)
            'customers.view', 'suppliers.view',
            # التقارير
            'reports.view', 'reports.sales', 'reports.purchases', 'reports.financial',
            'reports.export',
        ]
    },
    {
        'name': 'cashier',
        'name_ar': 'أمين صندوق',
        'description': 'صلاحيات نقاط البيع والمدفوعات',
        'permissions': [
            # نقاط البيع
            'pos.access', 'pos.sell', 'pos.refund',
            # المبيعات
            'sales.view', 'sales.create', 'sales.complete', 'sales.print',
            # العملاء (عرض فقط)
            'customers.view',
            # المخزون (عرض فقط)
            'inventory.view', 'inventory.products.view', 'inventory.stock.view',
            # المحاسبة (محدودة)
            'accounting.payments.view', 'accounting.payments.create',
        ]
    },
    {
        'name': 'hr_manager',
        'name_ar': 'مدير موارد بشرية',
        'description': 'صلاحيات إدارة الموارد البشرية',
        'permissions': [
            # الموارد البشرية
            'hr.view', 'hr.employees.view', 'hr.employees.manage', 'hr.attendance.view',
            'hr.attendance.manage', 'hr.payroll.view', 'hr.payroll.manage',
            # التقارير
            'reports.view',
        ]
    },
    {
        'name': 'viewer',
        'name_ar': 'مشاهد',
        'description': 'صلاحيات العرض فقط',
        'permissions': [
            # عرض فقط
            'sales.view', 'purchases.view', 'inventory.view', 'inventory.products.view',
            'inventory.stock.view', 'customers.view', 'suppliers.view',
            'reports.view', 'reports.sales', 'reports.purchases', 'reports.inventory',
        ]
    },
]


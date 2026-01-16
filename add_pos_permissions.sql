-- إضافة صلاحيات نقطة البيع (POS Permissions)
-- يجب تشغيل هذا السكريبت لإضافة الصلاحيات الجديدة

-- 1. صلاحية الوصول إلى نقطة البيع
INSERT OR IGNORE INTO permissions (name, name_ar, module) 
VALUES ('pos.access', 'الوصول إلى نقطة البيع', 'pos');

-- 2. صلاحية إدارة الجلسات (فتح/إغلاق الوردية)
INSERT OR IGNORE INTO permissions (name, name_ar, module) 
VALUES ('pos.session.manage', 'إدارة جلسات نقطة البيع', 'pos');

-- 3. صلاحية البيع
INSERT OR IGNORE INTO permissions (name, name_ar, module) 
VALUES ('pos.sell', 'البيع من نقطة البيع', 'pos');

-- 4. صلاحية إنشاء عروض الأسعار
INSERT OR IGNORE INTO permissions (name, name_ar, module) 
VALUES ('pos.quotation.create', 'إنشاء عروض أسعار من نقطة البيع', 'pos');

-- 5. صلاحية عرض تقارير الجلسات
INSERT OR IGNORE INTO permissions (name, name_ar, module) 
VALUES ('pos.reports.view', 'عرض تقارير نقطة البيع', 'pos');

-- ============================================================
-- إضافة الصلاحيات لدور المدير (Admin Role)
-- ============================================================

-- الحصول على ID دور المدير
-- افترض أن ID دور المدير هو 1، إذا كان مختلفاً، قم بتعديله

-- إضافة جميع صلاحيات POS لدور المدير
INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT 1, id FROM permissions WHERE module = 'pos';

-- ============================================================
-- إضافة الصلاحيات لدور الكاشير (Cashier Role) - إذا كان موجوداً
-- ============================================================

-- إنشاء دور الكاشير إذا لم يكن موجوداً
INSERT OR IGNORE INTO roles (name, name_ar, description)
VALUES ('cashier', 'كاشير', 'موظف نقطة البيع - صلاحيات محدودة');

-- إضافة صلاحيات محددة لدور الكاشير
INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id 
FROM roles r, permissions p
WHERE r.name = 'cashier' 
AND p.name IN (
    'pos.access',           -- الوصول إلى نقطة البيع
    'pos.session.manage',   -- إدارة الجلسات
    'pos.sell',             -- البيع
    'pos.quotation.create'  -- إنشاء عروض أسعار
);

-- ============================================================
-- التحقق من الصلاحيات المضافة
-- ============================================================

-- عرض جميع صلاحيات POS
SELECT * FROM permissions WHERE module = 'pos';

-- عرض صلاحيات دور المدير
SELECT r.name as role_name, p.name as permission_name, p.name_ar
FROM roles r
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
WHERE r.name = 'admin' AND p.module = 'pos';

-- عرض صلاحيات دور الكاشير
SELECT r.name as role_name, p.name as permission_name, p.name_ar
FROM roles r
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
WHERE r.name = 'cashier' AND p.module = 'pos';


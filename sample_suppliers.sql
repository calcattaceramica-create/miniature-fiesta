-- بيانات تجريبية للموردين
-- يمكن استخدام هذا الملف لإضافة موردين تجريبيين للنظام

-- مورد 1: شركة الأمل للتجارة
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile, 
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-001',
    'شركة الأمل للتجارة',
    'Al-Amal Trading Company',
    'محلي',
    'info@alamal.com',
    '0112345678',
    '0501234567',
    'شارع الملك فهد، حي العليا',
    'الرياض',
    'السعودية',
    '300123456789012',
    '1010123456',
    50000.00,
    30,
    0.00,
    1,
    'مورد رئيسي للمواد الغذائية'
);

-- مورد 2: مؤسسة النجاح
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile,
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-002',
    'مؤسسة النجاح',
    'Al-Najah Establishment',
    'جملة',
    'sales@alnajah.com',
    '0126789012',
    '0559876543',
    'طريق الملك عبدالعزيز',
    'جدة',
    'السعودية',
    '300987654321098',
    '2020987654',
    75000.00,
    45,
    0.00,
    1,
    'مورد معتمد للأدوات المكتبية'
);

-- مورد 3: شركة الخليج الدولية
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile,
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-003',
    'شركة الخليج الدولية',
    'Gulf International Company',
    'دولي',
    'contact@gulf-intl.com',
    '0138765432',
    '0545678901',
    'الكورنيش الشرقي',
    'الدمام',
    'السعودية',
    '300456789012345',
    '3030456789',
    100000.00,
    60,
    0.00,
    1,
    'مورد للإلكترونيات والأجهزة'
);

-- مورد 4: مؤسسة الفجر
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile,
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-004',
    'مؤسسة الفجر',
    'Al-Fajr Establishment',
    'تجزئة',
    'info@alfajr.sa',
    '0114567890',
    '0512345678',
    'حي الملز',
    'الرياض',
    'السعودية',
    '300234567890123',
    '1010234567',
    25000.00,
    15,
    0.00,
    1,
    'مورد للمنظفات ومواد التنظيف'
);

-- مورد 5: شركة الصحراء
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile,
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-005',
    'شركة الصحراء',
    'Al-Sahra Company',
    'محلي',
    'sales@alsahra.com',
    '0123456789',
    '0567890123',
    'شارع الأمير سلطان',
    'مكة المكرمة',
    'السعودية',
    '300345678901234',
    '4040345678',
    40000.00,
    30,
    0.00,
    1,
    'مورد للمواد الاستهلاكية'
);

-- مورد غير نشط (للاختبار)
INSERT INTO supplier (
    code, name, name_en, category, email, phone, mobile,
    address, city, country, tax_number, commercial_register,
    credit_limit, payment_terms, current_balance, is_active, notes
) VALUES (
    'SUP-006',
    'مؤسسة القديمة',
    'Old Establishment',
    'محلي',
    'old@example.com',
    '0111111111',
    '0500000000',
    'عنوان قديم',
    'الرياض',
    'السعودية',
    '300111111111111',
    '1010111111',
    0.00,
    0,
    0.00,
    0,
    'مورد غير نشط - للاختبار فقط'
);

-- ملاحظات:
-- 1. تأكد من وجود جدول supplier في قاعدة البيانات
-- 2. قد تحتاج لتعديل الأكواد حسب نظام الترقيم لديك
-- 3. الأرقام الضريبية والسجلات التجارية هي أمثلة فقط
-- 4. يمكنك تعديل البيانات حسب احتياجاتك


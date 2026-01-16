"""Add invoice_template field to companies table"""
from app import create_app, db
from sqlalchemy import text
import traceback

app = create_app()

with app.app_context():
    try:
        # Add the column
        with db.engine.begin() as conn:
            conn.execute(text("ALTER TABLE companies ADD COLUMN invoice_template VARCHAR(50) DEFAULT 'modern'"))
        print("✅ تم إضافة حقل invoice_template بنجاح!")
    except Exception as e:
        error_str = str(e).lower()
        if "duplicate column" in error_str or "already exists" in error_str:
            print("⚠️ الحقل موجود بالفعل")
        else:
            print(f"❌ خطأ: {e}")
            traceback.print_exc()


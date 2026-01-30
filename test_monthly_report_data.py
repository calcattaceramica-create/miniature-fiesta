"""Test Monthly Purchases Report Data"""
import sys
from datetime import datetime
from app import create_app, db
from app.models import PurchaseInvoice

print("=" * 70)
print("🧪 Testing Monthly Purchases Report Data")
print("=" * 70)

app = create_app()

with app.app_context():
    # Get current year
    year = datetime.now().year
    print(f"\n📅 Testing for year: {year}")
    
    # Get all invoices for the year
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()
    
    print(f"📆 Date range: {start_date} to {end_date}")
    
    invoices = PurchaseInvoice.query.filter(
        PurchaseInvoice.status != 'cancelled',
        PurchaseInvoice.invoice_date >= start_date,
        PurchaseInvoice.invoice_date <= end_date
    ).all()
    
    print(f"\n📊 Found {len(invoices)} invoices in {year}")
    
    if invoices:
        print("\n📋 Invoice Details:")
        print("-" * 70)
        total_amount = 0
        total_tax = 0
        
        for inv in invoices[:10]:  # Show first 10
            print(f"  • Invoice #{inv.invoice_number}")
            print(f"    Date: {inv.invoice_date}")
            print(f"    Total: {inv.total_amount:.2f}")
            print(f"    Tax: {inv.tax_amount:.2f}")
            print(f"    Status: {inv.status}")
            print()
            total_amount += inv.total_amount
            total_tax += inv.tax_amount
        
        if len(invoices) > 10:
            print(f"  ... and {len(invoices) - 10} more invoices")
        
        print("\n" + "=" * 70)
        print("📊 Summary:")
        print("=" * 70)
        print(f"  Total Invoices: {len(invoices)}")
        print(f"  Total Amount: {total_amount:,.2f} €")
        print(f"  Total Tax: {total_tax:,.2f} €")
        print("=" * 70)
    else:
        print("\n⚠️  No invoices found for this year!")
        print("\n🔍 Checking all invoices in database...")
        
        all_invoices = PurchaseInvoice.query.filter(
            PurchaseInvoice.status != 'cancelled'
        ).all()
        
        print(f"\n📊 Total invoices in database: {len(all_invoices)}")
        
        if all_invoices:
            print("\n📋 Sample invoices:")
            print("-" * 70)
            for inv in all_invoices[:5]:
                print(f"  • Invoice #{inv.invoice_number}")
                print(f"    Date: {inv.invoice_date}")
                print(f"    Year: {inv.invoice_date.year if inv.invoice_date else 'N/A'}")
                print(f"    Total: {inv.total_amount:.2f}")
                print(f"    Status: {inv.status}")
                print()
            
            # Get years
            years_set = set()
            for inv in all_invoices:
                if inv.invoice_date:
                    years_set.add(inv.invoice_date.year)
            
            print(f"\n📅 Available years: {sorted(list(years_set), reverse=True)}")
        else:
            print("\n❌ No invoices found in database at all!")

print("\n" + "=" * 70)
print("✅ Test Complete!")
print("=" * 70)


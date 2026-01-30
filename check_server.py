"""Check if Flask server is running"""
import socket
import time

def check_port(host='localhost', port=5000, timeout=2):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

print("="*70)
print("🔍 Checking Flask Server Status")
print("="*70)

# Check multiple times
for i in range(5):
    if check_port():
        print(f"✅ Server is RUNNING on http://localhost:5000")
        print("\n📋 Next steps:")
        print("1. The browser should have opened automatically")
        print("2. If not, open: http://localhost:5000/reports/inventory?v=999")
        print("3. You should see THREE colored cards at the top!")
        print("\n🎨 Expected cards:")
        print("   1. Purple card - Total Inventory Value (إجمالي قيمة المخزون)")
        print("   2. Green card - Total Products (إجمالي المنتجات)")
        print("   3. Blue card - Average Value (متوسط القيمة)")
        break
    else:
        print(f"⏳ Waiting for server to start... ({i+1}/5)")
        time.sleep(2)
else:
    print("❌ Server is NOT running!")
    print("\n📋 To start the server manually:")
    print("   python run.py")

print("="*70)


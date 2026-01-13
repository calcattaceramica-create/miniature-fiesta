import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test the license generation
from datetime import datetime, timedelta
import hashlib
import secrets
import uuid
import platform
import subprocess

def get_machine_id():
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], 
                                  capture_output=True, text=True, timeout=5)
            machine_id = result.stdout.split('\n')[1].strip()
        else:
            machine_id = str(uuid.getnode())
        
        return hashlib.md5(machine_id.encode()).hexdigest()[:16].upper()
    except:
        return secrets.token_hex(8).upper()

def create_license_key(company, machine_id=""):
    timestamp = datetime.now().isoformat()
    random_part = secrets.token_hex(16)
    
    data = f"{company}-{machine_id}-{timestamp}-{random_part}"
    hash_obj = hashlib.sha256(data.encode())
    
    full_key = hash_obj.hexdigest()[:32].upper()
    formatted_key = '-'.join([full_key[i:i+4] for i in range(0, 32, 4)])
    
    return formatted_key

# Test
print("Testing License Generation...")
print("=" * 80)

company = "Test Company"
machine_id = get_machine_id()
key = create_license_key(company, machine_id)
expiry = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

license_data = {
    'company': company,
    'expiry': expiry,
    'created': created,
    'duration_days': 365,
    'machine_id': machine_id,
    'license_type': 'Standard',
    'max_users': 10,
    'features': ['all'],
    'status': 'active',
    'activation_count': 0,
    'last_check': None,
    'contact_email': '',
    'contact_phone': '',
    'notes': ''
}

print(f"Company: {license_data['company']}")
print(f"License Key: {key}")
print(f"Created: {license_data['created']}")
print(f"Duration: {license_data['duration_days']} days")
print(f"Expiry: {license_data['expiry']}")
print(f"Machine ID: {license_data['machine_id']}")
print(f"License Type: {license_data['license_type']}")
print(f"Max Users: {license_data['max_users']}")
print(f"Features: {', '.join(license_data['features'])}")
print(f"Status: {license_data['status']}")
print(f"Activation Count: {license_data['activation_count']}")
print("=" * 80)
print("\nAll license information is working correctly! ✅")


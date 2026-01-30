"""List all Flask routes"""
import os
import sys

# Set the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

print("All registered routes:")
print("=" * 80)

for rule in app.url_map.iter_rules():
    if 'reports' in rule.endpoint:
        print(f"{rule.endpoint:50s} {rule.rule}")

print("=" * 80)


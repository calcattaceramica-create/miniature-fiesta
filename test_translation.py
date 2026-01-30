#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()

with app.test_request_context():
    from flask import session
    from flask_babel import gettext as _

    # Set language to Arabic
    session['language'] = 'ar'

    print("Testing Roles and Permissions Page Translations:")
    print("=" * 70)
    print(f"Roles Management: {_('Roles Management')}")
    print(f"Roles and Permissions Management: {_('Roles and Permissions Management')}")
    print(f"Add New Role: {_('Add New Role')}")
    print(f"Permissions:: {_('Permissions:')}")
    print(f"Save Permissions: {_('Save Permissions')}")
    print(f"Number of Users:: {_('Number of Users:')}")
    print(f"Role Name (English): {_('Role Name (English)')}")
    print(f"Example: sales_manager: {_('Example: sales_manager')}")
    print(f"Role Name (Arabic): {_('Role Name (Arabic)')}")
    print(f"Description: {_('Description')}")
    print(f"Cancel: {_('Cancel')}")
    print(f"Save: {_('Save')}")
    print(f"Edit Role: {_('Edit Role')}")
    print(f"Save Changes: {_('Save Changes')}")
    print(f"Confirm Deletion: {_('Confirm Deletion')}")
    print(f"Are you sure you want to delete the role: {_('Are you sure you want to delete the role')}")
    print(f"This action cannot be undone!: {_('This action cannot be undone!')}")
    print(f"Delete: {_('Delete')}")
    print("=" * 70)


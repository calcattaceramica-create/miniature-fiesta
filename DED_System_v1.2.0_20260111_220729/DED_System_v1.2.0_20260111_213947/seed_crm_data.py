#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to seed CRM data for testing
"""

from app import create_app, db
from app.models import (
    User, Customer, Lead, Opportunity, Interaction, 
    Task, Campaign
)
from datetime import datetime, timedelta
import random

def seed_crm_data():
    """Seed CRM data"""
    app = create_app()

    with app.app_context():
        print("Starting CRM data seeding...")

        # Delete existing CRM data
        print("\nDeleting existing CRM data...")
        Task.query.delete()
        Interaction.query.delete()
        Opportunity.query.delete()
        Campaign.query.delete()
        Lead.query.delete()
        db.session.commit()
        print("  Existing data deleted")

        # Get existing users
        users = User.query.all()
        if not users:
            print("No users found. Please create users first.")
            return

        # Get existing customers
        customers = Customer.query.all()
        if not customers:
            print("No customers found. Please create customers first.")
            return
        
        # Create Leads
        print("\nCreating Leads...")
        leads_data = [
            {
                'name': 'أحمد محمد',
                'company': 'شركة التقنية المتقدمة',
                'title': 'مدير تقنية المعلومات',
                'email': 'ahmed@tech-advanced.com',
                'phone': '0112345678',
                'mobile': '0501234567',
                'source': 'website',
                'status': 'new',
                'rating': 4,
                'expected_revenue': 50000,
                'probability': 60,
            },
            {
                'name': 'فاطمة علي',
                'company': 'مؤسسة الابتكار',
                'title': 'مديرة المشتريات',
                'email': 'fatima@innovation.com',
                'phone': '0112345679',
                'mobile': '0501234568',
                'source': 'referral',
                'status': 'contacted',
                'rating': 5,
                'expected_revenue': 75000,
                'probability': 70,
            },
            {
                'name': 'خالد سعيد',
                'company': 'شركة النجاح',
                'title': 'المدير التنفيذي',
                'email': 'khaled@success.com',
                'phone': '0112345680',
                'mobile': '0501234569',
                'source': 'cold_call',
                'status': 'qualified',
                'rating': 3,
                'expected_revenue': 30000,
                'probability': 50,
            },
            {
                'name': 'نورة عبدالله',
                'company': 'مجموعة الرؤية',
                'title': 'مديرة التسويق',
                'email': 'noura@vision-group.com',
                'phone': '0112345681',
                'mobile': '0501234570',
                'source': 'social_media',
                'status': 'new',
                'rating': 4,
                'expected_revenue': 60000,
                'probability': 65,
            },
            {
                'name': 'سعود محمد',
                'company': 'شركة الأفق',
                'title': 'مدير العمليات',
                'email': 'saud@horizon.com',
                'phone': '0112345682',
                'mobile': '0501234571',
                'source': 'event',
                'status': 'contacted',
                'rating': 5,
                'expected_revenue': 90000,
                'probability': 80,
            }
        ]
        
        leads = []
        for i, lead_data in enumerate(leads_data):
            lead = Lead(
                code=f'LEAD-{datetime.now().year}-{str(i+1).zfill(3)}',
                assigned_to=random.choice(users).id,
                expected_close_date=datetime.now() + timedelta(days=random.randint(30, 90)),
                **lead_data
            )
            db.session.add(lead)
            leads.append(lead)
            print(f"  Created lead: {lead.name}")
        
        db.session.commit()
        
        # Create Opportunities
        print("\nCreating Opportunities...")
        opportunities_data = [
            {
                'name': 'نظام إدارة المخزون',
                'amount': 120000,
                'probability': 75,
                'stage': 'proposal',
            },
            {
                'name': 'تطوير موقع إلكتروني',
                'amount': 80000,
                'probability': 60,
                'stage': 'qualification',
            },
            {
                'name': 'نظام نقاط البيع',
                'amount': 150000,
                'probability': 85,
                'stage': 'negotiation',
            },
            {
                'name': 'تجديد الاشتراك السنوي',
                'amount': 50000,
                'probability': 90,
                'stage': 'proposal',
            }
        ]

        opportunities = []
        for i, opp_data in enumerate(opportunities_data):
            opp = Opportunity(
                code=f'OPP-{datetime.now().year}-{str(i+1).zfill(3)}',
                customer_id=random.choice(customers).id,
                lead_id=random.choice(leads).id if random.random() > 0.5 else None,
                assigned_to=random.choice(users).id,
                expected_close_date=datetime.now() + timedelta(days=random.randint(30, 120)),
                **opp_data
            )
            db.session.add(opp)
            opportunities.append(opp)
            print(f"  Created opportunity: {opp.name}")

        db.session.commit()
        
        # Create Interactions
        print("\nCreating Interactions...")
        interaction_types = ['call', 'email', 'meeting', 'note']
        outcomes = ['successful', 'unsuccessful', 'follow_up_required', 'no_answer']
        
        for i in range(15):
            interaction = Interaction(
                interaction_type=random.choice(interaction_types),
                subject=f'تفاعل رقم {i+1}',
                description=f'وصف التفاعل رقم {i+1}',
                interaction_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                duration=random.randint(10, 60),
                outcome=random.choice(outcomes),
                lead_id=random.choice(leads).id if random.random() > 0.5 else None,
                customer_id=random.choice(customers).id if random.random() > 0.5 else None,
                opportunity_id=random.choice(opportunities).id if random.random() > 0.5 else None,
                created_by=random.choice(users).id
            )
            db.session.add(interaction)
        
        print(f"  Created 15 interactions")
        db.session.commit()

        # Create Tasks
        print("\nCreating Tasks...")
        task_types = ['call', 'email', 'meeting', 'follow_up', 'other']
        priorities = ['low', 'normal', 'high', 'urgent']
        statuses = ['pending', 'in_progress', 'completed', 'cancelled']

        for i in range(20):
            task = Task(
                title=f'مهمة رقم {i+1}',
                description=f'وصف المهمة رقم {i+1}',
                task_type=random.choice(task_types),
                priority=random.choice(priorities),
                status=random.choice(statuses),
                due_date=datetime.now() + timedelta(days=random.randint(1, 30)),
                assigned_to=random.choice(users).id,
                lead_id=random.choice(leads).id if random.random() > 0.5 else None,
                customer_id=random.choice(customers).id if random.random() > 0.5 else None,
                opportunity_id=random.choice(opportunities).id if random.random() > 0.5 else None,
                created_by=random.choice(users).id
            )
            db.session.add(task)

        print(f"  Created 20 tasks")
        db.session.commit()

        # Create Campaigns
        print("\nCreating Campaigns...")
        campaigns_data = [
            {
                'name': 'حملة التسويق الرقمي 2024',
                'code': 'CAMP-2024-001',
                'campaign_type': 'social_media',
                'status': 'active',
                'budget': 100000,
                'actual_cost': 75000,
                'expected_revenue': 500000,
                'actual_revenue': 350000,
                'target_audience': 100,
                'leads_generated': 75,
                'conversions': 25,
            },
            {
                'name': 'حملة البريد الإلكتروني - الربع الأول',
                'code': 'CAMP-2024-002',
                'campaign_type': 'email',
                'status': 'completed',
                'budget': 50000,
                'actual_cost': 45000,
                'expected_revenue': 200000,
                'actual_revenue': 180000,
                'target_audience': 50,
                'leads_generated': 45,
                'conversions': 15,
            },
            {
                'name': 'معرض التقنية 2024',
                'code': 'CAMP-2024-003',
                'campaign_type': 'event',
                'status': 'planning',
                'budget': 200000,
                'actual_cost': 0,
                'expected_revenue': 800000,
                'actual_revenue': 0,
                'target_audience': 150,
                'leads_generated': 0,
                'conversions': 0,
            }
        ]

        for campaign_data in campaigns_data:
            campaign = Campaign(
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=30),
                **campaign_data
            )
            db.session.add(campaign)
            print(f"  Created campaign: {campaign.name}")

        db.session.commit()

        print("\n✅ CRM data seeding completed successfully!")
        print(f"  - {len(leads)} Leads")
        print(f"  - {len(opportunities)} Opportunities")
        print(f"  - 15 Interactions")
        print(f"  - 20 Tasks")
        print(f"  - 3 Campaigns")

if __name__ == '__main__':
    seed_crm_data()


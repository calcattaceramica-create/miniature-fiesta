from datetime import datetime
from app import db

# Lead - العملاء المحتملون
class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    # Basic Info
    name = db.Column(db.String(128), nullable=False, index=True)
    company = db.Column(db.String(128))
    title = db.Column(db.String(64))  # Job title
    
    # Contact Info
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Address
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    
    # Lead Info
    source = db.Column(db.String(64))  # Website, Referral, Cold Call, etc.
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    rating = db.Column(db.Integer, default=0)  # 1-5 stars
    
    # Sales Info
    expected_revenue = db.Column(db.Float, default=0.0)
    probability = db.Column(db.Integer, default=0)  # 0-100%
    expected_close_date = db.Column(db.Date)
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Conversion
    converted_to_customer = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    converted_date = db.Column(db.DateTime)
    
    # Notes
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    interactions = db.relationship('Interaction', backref='lead', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='lead', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lead {self.name}>'


# Interaction - التفاعلات مع العملاء
class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Type
    interaction_type = db.Column(db.String(20), nullable=False)  # call, email, meeting, note
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Related To
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    
    # Details
    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # Minutes
    outcome = db.Column(db.String(200))
    
    # Assignment
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Interaction {self.subject}>'


# Opportunity - الفرص التجارية
class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    # Basic Info
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Related
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    
    # Sales Info
    amount = db.Column(db.Float, default=0.0)
    probability = db.Column(db.Integer, default=0)  # 0-100%
    stage = db.Column(db.String(20), default='prospecting')  # prospecting, qualification, proposal, negotiation, closed_won, closed_lost
    
    # Dates
    expected_close_date = db.Column(db.Date)
    actual_close_date = db.Column(db.Date)
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    interactions = db.relationship('Interaction', backref='opportunity', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='opportunity', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Opportunity {self.name}>'


# Task - المهام
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Type & Priority
    task_type = db.Column(db.String(20), default='general')  # call, email, meeting, follow_up, general
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent

    # Related To
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))

    # Dates
    due_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled

    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Task {self.title}>'


# Campaign - الحملات التسويقية
class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)

    # Basic Info
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)

    # Campaign Info
    campaign_type = db.Column(db.String(20))  # email, social, event, webinar, etc.
    status = db.Column(db.String(20), default='planning')  # planning, active, completed, cancelled

    # Dates
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Budget & Results
    budget = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float, default=0.0)
    expected_revenue = db.Column(db.Float, default=0.0)
    actual_revenue = db.Column(db.Float, default=0.0)

    # Metrics
    target_audience = db.Column(db.Integer, default=0)
    leads_generated = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)

    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Status
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Campaign {self.name}>'


# Contact - جهات الاتصال
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64))  # Job title

    # Related
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # Contact Info
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))

    # Social
    linkedin = db.Column(db.String(200))
    twitter = db.Column(db.String(200))

    # Status
    is_primary = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Notes
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Contact {self.full_name}>'


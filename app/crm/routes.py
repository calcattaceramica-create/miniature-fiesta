from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.crm import bp
from app import db
from app.models_crm import Lead, Interaction, Opportunity, Task, Campaign, Contact
from app.models_sales import Customer
from app.models import User
from app.auth.decorators import permission_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_

# ==================== Dashboard ====================
@bp.route('/')
@bp.route('/dashboard')
@login_required
@permission_required('crm.view')
def index():
    """CRM Dashboard"""
    # Statistics
    stats = {
        'total_leads': Lead.query.filter_by(converted_to_customer=False).count(),
        'total_opportunities': Opportunity.query.filter_by(is_active=True).count(),
        'total_tasks': Task.query.filter_by(status='pending').count(),
        'total_campaigns': Campaign.query.filter_by(is_active=True).count(),
    }

    # Lead Status Distribution
    lead_status = db.session.query(
        Lead.status,
        func.count(Lead.id)
    ).filter_by(converted_to_customer=False).group_by(Lead.status).all()

    # Opportunity Stage Distribution
    opp_stages = db.session.query(
        Opportunity.stage,
        func.count(Opportunity.id)
    ).filter_by(is_active=True).group_by(Opportunity.stage).all()

    # Recent Leads
    recent_leads = Lead.query.filter_by(converted_to_customer=False).order_by(Lead.created_at.desc()).limit(5).all()

    # Recent Opportunities
    recent_opportunities = Opportunity.query.filter_by(is_active=True).order_by(Opportunity.created_at.desc()).limit(5).all()

    # Upcoming Tasks
    upcoming_tasks = Task.query.filter(
        Task.status.in_(['pending', 'in_progress']),
        Task.due_date.isnot(None)
    ).order_by(Task.due_date).limit(5).all()

    # Recent Interactions
    recent_interactions = Interaction.query.order_by(Interaction.created_at.desc()).limit(5).all()

    return render_template('crm/dashboard.html',
                         stats=stats,
                         lead_status=lead_status,
                         opp_stages=opp_stages,
                         recent_leads=recent_leads,
                         recent_opportunities=recent_opportunities,
                         upcoming_tasks=upcoming_tasks,
                         recent_interactions=recent_interactions)


# ==================== Leads ====================
@bp.route('/leads')
@login_required
@permission_required('crm.view')
def leads():
    """List all leads"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = Lead.query.filter_by(converted_to_customer=False)

    if search:
        query = query.filter(
            or_(
                Lead.name.contains(search),
                Lead.company.contains(search),
                Lead.email.contains(search),
                Lead.phone.contains(search)
            )
        )

    if status:
        query = query.filter_by(status=status)

    leads = query.order_by(Lead.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('crm/leads.html',
                         leads=leads,
                         search=search,
                         status=status)


@bp.route('/leads/add', methods=['GET', 'POST'])
@login_required
@permission_required('crm.leads.manage')
def add_lead():
    """Add new lead"""
    if request.method == 'POST':
        # Generate code
        last_lead = Lead.query.order_by(Lead.id.desc()).first()
        code = f"LEAD-{(last_lead.id + 1) if last_lead else 1:05d}"

        lead = Lead(
            code=code,
            name=request.form.get('name'),
            company=request.form.get('company'),
            title=request.form.get('title'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            mobile=request.form.get('mobile'),
            website=request.form.get('website'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            country=request.form.get('country'),
            source=request.form.get('source'),
            status=request.form.get('status', 'new'),
            rating=request.form.get('rating', 0, type=int),
            expected_revenue=request.form.get('expected_revenue', 0, type=float),
            probability=request.form.get('probability', 0, type=int),
            description=request.form.get('description'),
            assigned_to=request.form.get('assigned_to', type=int),
            created_by=current_user.id
        )

        # Expected close date
        close_date = request.form.get('expected_close_date')
        if close_date:
            lead.expected_close_date = datetime.strptime(close_date, '%Y-%m-%d').date()

        db.session.add(lead)
        db.session.commit()

        flash('تم إضافة العميل المحتمل بنجاح', 'success')
        return redirect(url_for('crm.leads'))

    users = User.query.filter_by(is_active=True).all()
    return render_template('crm/add_lead.html', users=users)


@bp.route('/leads/<int:id>')
@login_required
@permission_required('crm.view')
def lead_details(id):
    """View lead details"""
    lead = Lead.query.get_or_404(id)
    interactions = lead.interactions.order_by(Interaction.created_at.desc()).all()
    tasks = lead.tasks.order_by(Task.due_date).all()

    return render_template('crm/lead_details.html',
                         lead=lead,
                         interactions=interactions,
                         tasks=tasks)


@bp.route('/leads/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('crm.leads.manage')
def edit_lead(id):
    """Edit lead"""
    lead = Lead.query.get_or_404(id)

    if request.method == 'POST':
        lead.name = request.form.get('name')
        lead.company = request.form.get('company')
        lead.title = request.form.get('title')
        lead.email = request.form.get('email')
        lead.phone = request.form.get('phone')
        lead.mobile = request.form.get('mobile')
        lead.website = request.form.get('website')
        lead.address = request.form.get('address')
        lead.city = request.form.get('city')
        lead.country = request.form.get('country')
        lead.source = request.form.get('source')
        lead.status = request.form.get('status')
        lead.rating = request.form.get('rating', 0, type=int)
        lead.expected_revenue = request.form.get('expected_revenue', 0, type=float)
        lead.probability = request.form.get('probability', 0, type=int)
        lead.description = request.form.get('description')
        lead.assigned_to = request.form.get('assigned_to', type=int)

        # Expected close date
        close_date = request.form.get('expected_close_date')
        if close_date:
            lead.expected_close_date = datetime.strptime(close_date, '%Y-%m-%d').date()

        db.session.commit()

        flash('تم تحديث العميل المحتمل بنجاح', 'success')
        return redirect(url_for('crm.lead_details', id=lead.id))

    users = User.query.filter_by(is_active=True).all()
    return render_template('crm/edit_lead.html', lead=lead, users=users)


@bp.route('/leads/<int:id>/convert', methods=['POST'])
@login_required
@permission_required('crm.leads.manage')
def convert_lead(id):
    """Convert lead to customer"""
    lead = Lead.query.get_or_404(id)

    # Generate customer code
    last_customer = Customer.query.order_by(Customer.id.desc()).first()
    code = f"CUST-{(last_customer.id + 1) if last_customer else 1:05d}"

    # Create customer
    customer = Customer(
        code=code,
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        mobile=lead.mobile,
        address=lead.address,
        city=lead.city,
        country=lead.country,
        customer_type='company' if lead.company else 'individual',
        is_active=True
    )

    db.session.add(customer)
    db.session.flush()

    # Update lead
    lead.converted_to_customer = True
    lead.customer_id = customer.id
    lead.converted_date = datetime.utcnow()
    lead.status = 'converted'

    db.session.commit()

    flash('تم تحويل العميل المحتمل إلى عميل بنجاح', 'success')
    return redirect(url_for('sales.customers'))


# ==================== Opportunities ====================
@bp.route('/opportunities')
@login_required
@permission_required('crm.view')
def opportunities():
    """List all opportunities"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    stage = request.args.get('stage', '')

    query = Opportunity.query.filter_by(is_active=True)

    if search:
        query = query.filter(Opportunity.name.contains(search))

    if stage:
        query = query.filter_by(stage=stage)

    opportunities = query.order_by(Opportunity.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('crm/opportunities.html',
                         opportunities=opportunities,
                         search=search,
                         stage=stage)


@bp.route('/opportunities/add', methods=['GET', 'POST'])
@login_required
@permission_required('crm.opportunities.manage')
def add_opportunity():
    """Add new opportunity"""
    if request.method == 'POST':
        # Generate code
        last_opp = Opportunity.query.order_by(Opportunity.id.desc()).first()
        code = f"OPP-{(last_opp.id + 1) if last_opp else 1:05d}"

        opportunity = Opportunity(
            code=code,
            name=request.form.get('name'),
            description=request.form.get('description'),
            customer_id=request.form.get('customer_id', type=int),
            lead_id=request.form.get('lead_id', type=int),
            amount=request.form.get('amount', 0, type=float),
            probability=request.form.get('probability', 0, type=int),
            stage=request.form.get('stage', 'prospecting'),
            assigned_to=request.form.get('assigned_to', type=int),
            created_by=current_user.id
        )

        # Expected close date
        close_date = request.form.get('expected_close_date')
        if close_date:
            opportunity.expected_close_date = datetime.strptime(close_date, '%Y-%m-%d').date()

        db.session.add(opportunity)
        db.session.commit()

        flash('تم إضافة الفرصة التجارية بنجاح', 'success')
        return redirect(url_for('crm.opportunities'))

    customers = Customer.query.filter_by(is_active=True).all()
    leads = Lead.query.filter_by(converted_to_customer=False).all()
    users = User.query.filter_by(is_active=True).all()

    return render_template('crm/add_opportunity.html',
                         customers=customers,
                         leads=leads,
                         users=users)


@bp.route('/opportunities/<int:id>')
@login_required
@permission_required('crm.view')
def opportunity_details(id):
    """View opportunity details"""
    opportunity = Opportunity.query.get_or_404(id)
    interactions = opportunity.interactions.order_by(Interaction.created_at.desc()).all()
    tasks = opportunity.tasks.order_by(Task.due_date).all()

    return render_template('crm/opportunity_details.html',
                         opportunity=opportunity,
                         interactions=interactions,
                         tasks=tasks)


@bp.route('/opportunities/<int:id>/update_stage', methods=['POST'])
@login_required
@permission_required('crm.opportunities.manage')
def update_opportunity_stage(id):
    """Update opportunity stage"""
    opportunity = Opportunity.query.get_or_404(id)

    opportunity.stage = request.form.get('stage')

    # If closed won or lost, set actual close date
    if opportunity.stage in ['closed_won', 'closed_lost']:
        opportunity.actual_close_date = date.today()
        if opportunity.stage == 'closed_lost':
            opportunity.is_active = False

    db.session.commit()

    flash('تم تحديث مرحلة الفرصة بنجاح', 'success')
    return redirect(url_for('crm.opportunity_details', id=opportunity.id))


# ==================== Interactions ====================
@bp.route('/interactions')
@login_required
@permission_required('crm.view')
def interactions():
    """List all interactions"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    interaction_type = request.args.get('interaction_type', '')

    query = Interaction.query

    if search:
        query = query.filter(Interaction.subject.contains(search))

    if interaction_type:
        query = query.filter_by(interaction_type=interaction_type)

    interactions = query.order_by(Interaction.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('crm/interactions.html',
                         interactions=interactions,
                         search=search,
                         interaction_type=interaction_type)


@bp.route('/interactions/add', methods=['GET', 'POST'])
@login_required
@permission_required('crm.interactions.manage')
def add_interaction():
    """Add new interaction"""
    if request.method == 'POST':
        interaction = Interaction(
            interaction_type=request.form.get('interaction_type'),
            subject=request.form.get('subject'),
            description=request.form.get('description'),
            lead_id=request.form.get('lead_id', type=int),
            customer_id=request.form.get('customer_id', type=int),
            opportunity_id=request.form.get('opportunity_id', type=int),
            duration=request.form.get('duration', type=int),
            outcome=request.form.get('outcome'),
            created_by=current_user.id
        )

        # Interaction date
        interaction_date = request.form.get('interaction_date')
        if interaction_date:
            interaction.interaction_date = datetime.strptime(interaction_date, '%Y-%m-%dT%H:%M')

        db.session.add(interaction)
        db.session.commit()

        flash('تم إضافة التفاعل بنجاح', 'success')
        return redirect(url_for('crm.interactions'))

    leads = Lead.query.filter_by(converted_to_customer=False).all()
    customers = Customer.query.filter_by(is_active=True).all()
    opportunities = Opportunity.query.filter_by(is_active=True).all()

    return render_template('crm/add_interaction.html',
                         leads=leads,
                         customers=customers,
                         opportunities=opportunities)


# ==================== Tasks ====================
@bp.route('/tasks')
@login_required
@permission_required('crm.view')
def tasks():
    """List all tasks"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')

    query = Task.query

    if status:
        query = query.filter_by(status=status)

    if priority:
        query = query.filter_by(priority=priority)

    tasks = query.order_by(Task.due_date).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('crm/tasks.html',
                         tasks=tasks,
                         status=status,
                         priority=priority)


@bp.route('/tasks/add', methods=['GET', 'POST'])
@login_required
@permission_required('crm.tasks.manage')
def add_task():
    """Add new task"""
    if request.method == 'POST':
        task = Task(
            title=request.form.get('title'),
            description=request.form.get('description'),
            task_type=request.form.get('task_type', 'general'),
            priority=request.form.get('priority', 'medium'),
            lead_id=request.form.get('lead_id', type=int),
            customer_id=request.form.get('customer_id', type=int),
            opportunity_id=request.form.get('opportunity_id', type=int),
            assigned_to=request.form.get('assigned_to', type=int),
            status='pending',
            created_by=current_user.id
        )

        # Due date
        due_date = request.form.get('due_date')
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')

        db.session.add(task)
        db.session.commit()

        flash('تم إضافة المهمة بنجاح', 'success')
        return redirect(url_for('crm.tasks'))

    leads = Lead.query.filter_by(converted_to_customer=False).all()
    customers = Customer.query.filter_by(is_active=True).all()
    opportunities = Opportunity.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()

    return render_template('crm/add_task.html',
                         leads=leads,
                         customers=customers,
                         opportunities=opportunities,
                         users=users)


@bp.route('/tasks/<int:id>/complete', methods=['POST'])
@login_required
@permission_required('crm.tasks.manage')
def complete_task(id):
    """Mark task as completed"""
    task = Task.query.get_or_404(id)

    task.status = 'completed'
    task.completed_date = datetime.utcnow()

    db.session.commit()

    flash('تم إكمال المهمة بنجاح', 'success')
    return redirect(url_for('crm.tasks'))


# ==================== Campaigns ====================
@bp.route('/campaigns')
@login_required
@permission_required('crm.view')
def campaigns():
    """List all campaigns"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = Campaign.query.filter_by(is_active=True)

    if status:
        query = query.filter_by(status=status)

    campaigns = query.order_by(Campaign.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Calculate statistics
    all_campaigns = Campaign.query.filter_by(is_active=True).all()
    total_campaigns = len(all_campaigns)
    active_campaigns = Campaign.query.filter_by(is_active=True, status='active').count()
    total_budget = sum([c.budget for c in all_campaigns])
    total_leads_generated = sum([c.leads_generated for c in all_campaigns])

    return render_template('crm/campaigns.html',
                         campaigns=campaigns,
                         status=status,
                         total_campaigns=total_campaigns,
                         active_campaigns=active_campaigns,
                         total_budget=total_budget,
                         total_leads_generated=total_leads_generated)


@bp.route('/campaigns/add', methods=['GET', 'POST'])
@login_required
@permission_required('crm.campaigns.manage')
def add_campaign():
    """Add new campaign"""
    if request.method == 'POST':
        # Generate code
        last_campaign = Campaign.query.order_by(Campaign.id.desc()).first()
        code = f"CAMP-{(last_campaign.id + 1) if last_campaign else 1:05d}"

        campaign = Campaign(
            code=code,
            name=request.form.get('name'),
            description=request.form.get('description'),
            campaign_type=request.form.get('campaign_type'),
            status=request.form.get('status', 'planning'),
            budget=request.form.get('budget', 0, type=float),
            expected_revenue=request.form.get('expected_revenue', 0, type=float),
            target_audience=request.form.get('target_audience', 0, type=int),
            assigned_to=request.form.get('assigned_to', type=int),
            created_by=current_user.id
        )

        # Dates
        start_date = request.form.get('start_date')
        if start_date:
            campaign.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        end_date = request.form.get('end_date')
        if end_date:
            campaign.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        db.session.add(campaign)
        db.session.commit()

        flash('تم إضافة الحملة التسويقية بنجاح', 'success')
        return redirect(url_for('crm.campaigns'))

    users = User.query.filter_by(is_active=True).all()
    return render_template('crm/add_campaign.html', users=users)


@bp.route('/campaigns/<int:id>')
@login_required
@permission_required('crm.view')
def campaign_details(id):
    """View campaign details"""
    campaign = Campaign.query.get_or_404(id)

    # Calculate ROI
    roi = 0
    if campaign.actual_cost > 0:
        roi = ((campaign.actual_revenue - campaign.actual_cost) / campaign.actual_cost) * 100

    return render_template('crm/campaign_details.html',
                         campaign=campaign,
                         roi=roi)


# ==================== Delete Routes ====================
@bp.route('/leads/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('crm.leads.manage')
def delete_lead(id):
    """Delete lead"""
    lead = Lead.query.get_or_404(id)

    # Delete related interactions and tasks
    Interaction.query.filter_by(lead_id=id).delete()
    Task.query.filter_by(lead_id=id).delete()

    db.session.delete(lead)
    db.session.commit()

    flash('تم حذف العميل المحتمل بنجاح', 'success')
    return redirect(url_for('crm.leads'))


@bp.route('/opportunities/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('crm.opportunities.manage')
def delete_opportunity(id):
    """Delete opportunity"""
    opportunity = Opportunity.query.get_or_404(id)

    # Delete related interactions and tasks
    Interaction.query.filter_by(opportunity_id=id).delete()
    Task.query.filter_by(opportunity_id=id).delete()

    db.session.delete(opportunity)
    db.session.commit()

    flash('تم حذف الفرصة التجارية بنجاح', 'success')
    return redirect(url_for('crm.opportunities'))


@bp.route('/interactions/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('crm.interactions.manage')
def delete_interaction(id):
    """Delete interaction"""
    interaction = Interaction.query.get_or_404(id)

    db.session.delete(interaction)
    db.session.commit()

    flash('تم حذف التفاعل بنجاح', 'success')
    return redirect(url_for('crm.interactions'))


@bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('crm.tasks.manage')
def delete_task(id):
    """Delete task"""
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    flash('تم حذف المهمة بنجاح', 'success')
    return redirect(url_for('crm.tasks'))


@bp.route('/campaigns/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('crm.campaigns.manage')
def delete_campaign(id):
    """Delete campaign"""
    campaign = Campaign.query.get_or_404(id)

    db.session.delete(campaign)
    db.session.commit()

    flash('تم حذف الحملة التسويقية بنجاح', 'success')
    return redirect(url_for('crm.campaigns'))

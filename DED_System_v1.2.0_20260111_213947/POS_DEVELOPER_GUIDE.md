# 🔧 نظام نقاط البيع - دليل المطور

## 📋 نظرة عامة تقنية

نظام نقاط البيع (POS) مبني باستخدام:
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLAlchemy ORM
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

---

## 🏗️ البنية المعمارية

### 1. هيكل المشروع

```
app/
├── pos/
│   ├── __init__.py          # Blueprint initialization
│   └── routes.py            # Route handlers
├── models_pos.py            # Database models
└── templates/
    └── pos/
        ├── open_session.html
        ├── index.html
        ├── sessions.html
        ├── session_details.html
        ├── receipt.html
        └── session_report.html
```

### 2. النماذج (Models)

#### POSSession
```python
class POSSession(db.Model):
    __tablename__ = 'pos_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_number = db.Column(db.String(64), unique=True, nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    opening_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    closing_time = db.Column(db.DateTime)
    opening_balance = db.Column(db.Float, default=0.0)
    closing_balance = db.Column(db.Float, default=0.0)
    total_sales = db.Column(db.Float, default=0.0)
    total_cash = db.Column(db.Float, default=0.0)
    total_card = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='open')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cashier = db.relationship('User')
    warehouse = db.relationship('Warehouse')
    orders = db.relationship('POSOrder', backref='session')
```

#### POSOrder
```python
class POSOrder(db.Model):
    __tablename__ = 'pos_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    session_id = db.Column(db.Integer, db.ForeignKey('pos_sessions.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Payment
    payment_method = db.Column(db.String(20), default='cash')
    cash_amount = db.Column(db.Float, default=0.0)
    card_amount = db.Column(db.Float, default=0.0)
    change_amount = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='completed')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer')
    items = db.relationship('POSOrderItem', backref='order', cascade='all, delete-orphan')
```

#### POSOrderItem
```python
class POSOrderItem(db.Model):
    __tablename__ = 'pos_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('pos_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    # Relationships
    product = db.relationship('Product')
```

---

## 🛣️ المسارات (Routes)

### 1. GET /pos/
**الوصف**: واجهة البيع الرئيسية  
**المصادقة**: مطلوبة  
**المعاملات**: لا يوجد

**الوظيفة**:
```python
@bp.route('/')
@login_required
def index():
    # Check for open session
    open_session = POSSession.query.filter_by(
        cashier_id=current_user.id,
        status='open'
    ).first()
    
    if not open_session:
        return redirect(url_for('pos.open_session'))
    
    products = Product.query.filter_by(is_active=True, is_sellable=True).all()
    customers = Customer.query.filter_by(is_active=True).all()
    
    return render_template('pos/index.html',
                         session=open_session,
                         products=products,
                         customers=customers)
```

### 2. GET/POST /pos/open-session
**الوصف**: فتح وردية جديدة  
**المصادقة**: مطلوبة  
**المعاملات** (POST):
- `warehouse_id` (int): معرف المستودع
- `opening_balance` (float): الرصيد الافتتاحي

**الوظيفة**:
```python
@bp.route('/open-session', methods=['GET', 'POST'])
@login_required
def open_session():
    if request.method == 'POST':
        # Generate session number
        today = datetime.utcnow()
        prefix = f'POS{today.year}{today.month:02d}{today.day:02d}'
        
        # Get last session number
        last_session = POSSession.query.filter(
            POSSession.session_number.like(f'{prefix}%')
        ).order_by(POSSession.id.desc()).first()
        
        # Generate new number
        if last_session:
            last_num = int(last_session.session_number[-3:])
            session_number = f'{prefix}{(last_num + 1):03d}'
        else:
            session_number = f'{prefix}001'
        
        # Create session
        session = POSSession(
            session_number=session_number,
            cashier_id=current_user.id,
            warehouse_id=request.form.get('warehouse_id', type=int),
            opening_balance=request.form.get('opening_balance', 0, type=float),
            status='open'
        )
        
        db.session.add(session)
        db.session.commit()
        
        flash('تم فتح الوردية بنجاح', 'success')
        return redirect(url_for('pos.index'))
    
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return render_template('pos/open_session.html', warehouses=warehouses)
```

### 3. POST /pos/close-session/<id>
**الوصف**: إغلاق وردية  
**المصادقة**: مطلوبة  
**المعاملات**:
- `id` (int): معرف الوردية
- `closing_balance` (float): الرصيد الختامي

**الوظيفة**:
```python
@bp.route('/close-session/<int:id>', methods=['POST'])
@login_required
def close_session(id):
    session = POSSession.query.get_or_404(id)
    
    # Check authorization
    if session.cashier_id != current_user.id:
        flash('غير مصرح لك بإغلاق هذه الوردية', 'danger')
        return redirect(url_for('pos.index'))
    
    # Update session
    session.closing_time = datetime.utcnow()
    session.closing_balance = request.form.get('closing_balance', 0, type=float)
    session.status = 'closed'
    
    # Calculate totals
    orders = POSOrder.query.filter_by(session_id=session.id, status='completed').all()
    session.total_sales = sum(order.total_amount for order in orders)
    session.total_cash = sum(order.cash_amount for order in orders)
    session.total_card = sum(order.card_amount for order in orders)
    
    db.session.commit()
    
    flash('تم إغلاق الوردية بنجاح', 'success')
    return redirect(url_for('pos.sessions'))
```

### 4. POST /pos/create-order (API)
**الوصف**: إنشاء طلب جديد  
**المصادقة**: مطلوبة  
**Content-Type**: application/json

**Request Body**:
```json
{
  "session_id": 1,
  "customer_id": 5,
  "items": [
    {
      "productId": 10,
      "productName": "منتج أ",
      "price": 100.00,
      "quantity": 2
    }
  ],
  "subtotal": 200.00,
  "discount_amount": 20.00,
  "tax_amount": 27.00,
  "total_amount": 207.00,
  "payment_method": "cash",
  "cash_amount": 207.00,
  "card_amount": 0.00
}
```

**Response**:
```json
{
  "success": true,
  "order_id": 123,
  "order_number": "ORD202601100001"
}
```

---

## 💻 JavaScript API

### متغيرات عامة
```javascript
let cart = [];                    // سلة المشتريات
const TAX_RATE = 0.15;           // معدل الضريبة
const SESSION_ID = {{ session.id }};  // معرف الوردية
```

### الدوال الرئيسية

#### addToCart()
```javascript
function addToCart(productId, productName, price) {
    const existingItem = cart.find(item => item.productId === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            productId: productId,
            productName: productName,
            price: price,
            quantity: 1
        });
    }
    
    renderCart();
    updateTotals();
}
```

#### updateTotals()
```javascript
function updateTotals() {
    const subtotal = cart.reduce((sum, item) => 
        sum + (item.price * item.quantity), 0);
    
    const discountPercent = parseFloat(
        document.getElementById('discount-percent').value) || 0;
    
    const discountAmount = subtotal * (discountPercent / 100);
    const afterDiscount = subtotal - discountAmount;
    const taxAmount = afterDiscount * TAX_RATE;
    const total = afterDiscount + taxAmount;
    
    document.getElementById('subtotal').textContent = subtotal.toFixed(2);
    document.getElementById('discount-amount').textContent = discountAmount.toFixed(2);
    document.getElementById('tax-amount').textContent = taxAmount.toFixed(2);
    document.getElementById('total').textContent = total.toFixed(2);
}
```

#### processPayment()
```javascript
async function processPayment() {
    // Validation
    if (cart.length === 0) {
        alert('السلة فارغة!');
        return;
    }
    
    // Prepare data
    const orderData = {
        session_id: SESSION_ID,
        customer_id: customerId,
        items: cart,
        subtotal: subtotal,
        discount_amount: discountAmount,
        tax_amount: taxAmount,
        total_amount: total,
        payment_method: paymentMethod,
        cash_amount: cashAmount,
        card_amount: cardAmount
    };
    
    // Send request
    try {
        const response = await fetch('/pos/create-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('تم إتمام البيع بنجاح!\nرقم الطلب: ' + result.order_number);
            clearCart();
            
            // Print receipt
            if (confirm('هل تريد طباعة الفاتورة؟')) {
                window.open('/pos/print-receipt/' + result.order_id, '_blank');
            }
        } else {
            alert('خطأ: ' + result.message);
        }
    } catch (error) {
        alert('حدث خطأ في الاتصال بالخادم');
        console.error(error);
    }
}
```

---

## 🔄 سير العمل التقني

### 1. فتح وردية
```
User → POST /pos/open-session
  ↓
Generate session_number (POS20260110001)
  ↓
Create POSSession record
  ↓
Redirect to /pos/
```

### 2. إتمام بيع
```
User adds products → JavaScript cart[]
  ↓
User clicks "إتمام البيع"
  ↓
processPayment() → POST /pos/create-order (JSON)
  ↓
Generate order_number (ORD202601100001)
  ↓
Create POSOrder record
  ↓
Create POSOrderItem records
  ↓
Update Stock (quantity -= sold)
  ↓
Create StockMovement records
  ↓
Return {success, order_id, order_number}
  ↓
Clear cart
  ↓
Optional: Print receipt
```

### 3. إغلاق وردية
```
User → POST /pos/close-session/<id>
  ↓
Validate cashier_id
  ↓
Set closing_time, closing_balance
  ↓
Calculate totals from orders
  ↓
Set status = 'closed'
  ↓
Redirect to /pos/sessions
```

---

## 🎨 تخصيص الواجهة

### الألوان
```css
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
}
```

### الأنماط المخصصة
```css
.product-card {
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid transparent;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    border-color: #0d6efd;
}
```

---

## 🧪 الاختبار

### اختبار فتح وردية
```python
def test_open_session():
    with app.test_client() as client:
        # Login
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin'
        })
        
        # Open session
        response = client.post('/pos/open-session', data={
            'warehouse_id': 1,
            'opening_balance': 1000.00
        })
        
        assert response.status_code == 302
        assert POSSession.query.filter_by(status='open').count() == 1
```

### اختبار إنشاء طلب
```python
def test_create_order():
    with app.test_client() as client:
        # Login and open session
        # ...
        
        # Create order
        response = client.post('/pos/create-order',
            json={
                'session_id': 1,
                'items': [
                    {'productId': 1, 'price': 100, 'quantity': 2}
                ],
                'subtotal': 200,
                'discount_amount': 0,
                'tax_amount': 30,
                'total_amount': 230,
                'payment_method': 'cash',
                'cash_amount': 230,
                'card_amount': 0
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'order_number' in data
```

---

## 🔐 الأمان

### 1. المصادقة
```python
@bp.route('/pos/')
@login_required  # Requires authentication
def index():
    # ...
```

### 2. التفويض
```python
# Only cashier can close their own session
if session.cashier_id != current_user.id:
    flash('غير مصرح لك بإغلاق هذه الوردية', 'danger')
    return redirect(url_for('pos.index'))
```

### 3. التحقق من البيانات
```python
# Validate payment amount
if payment_method == 'mixed':
    if cash_amount + card_amount < total:
        return jsonify({
            'success': False,
            'message': 'المبلغ المدفوع أقل من الإجمالي'
        }), 400
```

---

## 📊 قاعدة البيانات

### الجداول
```sql
-- pos_sessions
CREATE TABLE pos_sessions (
    id INTEGER PRIMARY KEY,
    session_number VARCHAR(64) UNIQUE NOT NULL,
    cashier_id INTEGER NOT NULL,
    warehouse_id INTEGER,
    opening_time DATETIME NOT NULL,
    closing_time DATETIME,
    opening_balance FLOAT DEFAULT 0.0,
    closing_balance FLOAT DEFAULT 0.0,
    total_sales FLOAT DEFAULT 0.0,
    total_cash FLOAT DEFAULT 0.0,
    total_card FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'open',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cashier_id) REFERENCES users(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- pos_orders
CREATE TABLE pos_orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(64) UNIQUE NOT NULL,
    order_date DATETIME NOT NULL,
    session_id INTEGER NOT NULL,
    customer_id INTEGER,
    subtotal FLOAT DEFAULT 0.0,
    discount_amount FLOAT DEFAULT 0.0,
    tax_amount FLOAT DEFAULT 0.0,
    total_amount FLOAT DEFAULT 0.0,
    payment_method VARCHAR(20) DEFAULT 'cash',
    cash_amount FLOAT DEFAULT 0.0,
    card_amount FLOAT DEFAULT 0.0,
    change_amount FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'completed',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES pos_sessions(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- pos_order_items
CREATE TABLE pos_order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity FLOAT NOT NULL,
    unit_price FLOAT NOT NULL,
    discount_percentage FLOAT DEFAULT 0.0,
    discount_amount FLOAT DEFAULT 0.0,
    tax_rate FLOAT DEFAULT 15.0,
    tax_amount FLOAT DEFAULT 0.0,
    total FLOAT DEFAULT 0.0,
    FOREIGN KEY (order_id) REFERENCES pos_orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## 🚀 التحسينات المستقبلية

### قصيرة المدى
- [ ] WebSocket للتحديثات الفورية
- [ ] تكامل مع قارئ الباركود
- [ ] طباعة تلقائية
- [ ] مرتجعات المبيعات

### متوسطة المدى
- [ ] تطبيق موبايل (React Native)
- [ ] تحليلات متقدمة
- [ ] تقارير مخصصة
- [ ] API RESTful كامل

### طويلة المدى
- [ ] Machine Learning للتوصيات
- [ ] تكامل مع أنظمة خارجية
- [ ] نظام الطلبات عبر الإنترنت
- [ ] Multi-tenant support

---

**تم بحمد الله**  
**التاريخ**: 2026-01-10  
**الإصدار**: 1.0


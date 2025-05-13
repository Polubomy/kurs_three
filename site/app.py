from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__, template_folder='site')
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/sitedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

class Manager(db.Model):
    __tablename__ = 'managers'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    manager_code = db.Column(db.String(10), db.ForeignKey('managers.code'))
    status = db.Column(db.String(50), nullable=False)
    contract_price = db.Column(db.Numeric(12,2))
    total_amount = db.Column(db.Numeric(12,2))
    order_type = db.Column(db.String(100))
    items_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    full_payment_date = db.Column(db.DateTime(timezone=True))
    payment_status = db.Column(db.String(50))

    client = db.relationship('Client')
    manager = db.relationship('Manager')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', backref='items')

# Декоратор для защиты маршрута
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Замените на свою систему проверки
        if email == 'admin@example.com' and password == '123':
            session['user'] = email
            return redirect(url_for('prod'))
        return render_template('login.html', error="Неверный логин или пароль")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/prod')
@login_required
def prod():

    orders = (Order.query
              .join(Client)
              .outerjoin(Manager)
              .order_by(Order.created_at.desc())
              .all())
    return render_template('prod.html', orders=orders)

@app.route('/new_order', methods=['GET', 'POST'])
@login_required
def new_order():
    clients = Client.query.all()
    managers = Manager.query.all()
    products = db.session.query(OrderItem.product_name).distinct().all()
    products = [p[0] for p in products if p[0]]  # получаем список названий

    if request.method == 'POST':
        order_number = request.form['order_number']
        client_id = request.form['client_id']
        manager_code = request.form['manager_code']
        status = request.form['status']
        contract_price = request.form['contract_price']
        total_amount = request.form['total_amount']
        order_type = request.form['order_type']
        items_description = request.form['items_description']
        payment_status = request.form['payment_status']
        full_payment_date = request.form['full_payment_date'] or None

        # Создаём заказ
        new_order = Order(
            order_number=order_number,
            client_id=client_id,
            manager_code=manager_code,
            status=status,
            contract_price=contract_price,
            total_amount=total_amount,
            order_type=order_type,
            items_description=items_description,
            payment_status=payment_status,
            full_payment_date=full_payment_date
        )
        db.session.add(new_order)
        db.session.commit()

        # Добавляем товары заказа
        product_names = request.form.getlist('product_name')
        quantities = request.form.getlist('quantity')
        for name, qty in zip(product_names, quantities):
            if name.strip() and qty.strip():
                item = OrderItem(order_id=new_order.id, product_name=name, quantity=int(qty))
                db.session.add(item)

        db.session.commit()
        return redirect(url_for('prod'))

    return render_template('new_order.html', clients=clients, managers=managers, products=products)


if __name__ == '__main__':
    # with app.app_context():
    #     db.session.execute(text("DROP TABLE IF EXISTS order_items CASCADE;"))
    #     db.session.execute(text("DROP TABLE IF EXISTS orders CASCADE;"))
    #     db.session.execute(text("DROP TABLE IF EXISTS clients CASCADE;"))
    #     db.session.execute(text("DROP TABLE IF EXISTS managers CASCADE;"))
    #     db.session.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
    #     db.session.commit()
    #     db.create_all()
    app.run(debug=True)

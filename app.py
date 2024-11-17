from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nammakadai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cash_balance = db.Column(db.Float, default=1000.0)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, default=0)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()
    if not Company.query.first():
        default_company = Company(name='Default Company', cash_balance=1000.0)
        db.session.add(default_company)
        db.session.commit()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        item = Item(name=data['item_name'], rate=data['price'], qty=data['quantity'])
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item added successfully!"}), 201
    items = Item.query.all()
    return jsonify([{"item_id": item.id, "item_name": item.name, "quantity": item.qty, "price": item.rate} for item in items])

@app.route('/purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    item = db.session.get(Item, data['item_id'])  # Updated from Item.query.get()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    purchase_amount = data['rate'] * data['qty']
    item.qty += data['qty']
    company = Company.query.first()
    company.cash_balance -= purchase_amount
    purchase = Purchase(item_id=item.id, rate=data['rate'], qty=data['qty'], amount=purchase_amount)
    db.session.add(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase recorded successfully!"}), 201

@app.route('/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    item = db.session.get(Item, data['item_id'])  # Updated from Item.query.get()
    if not item or item.qty < data['qty']:
        return jsonify({"error": "Insufficient quantity"}), 400
    sales_amount = data['rate'] * data['qty']
    item.qty -= data['qty']
    company = Company.query.first()
    company.cash_balance += sales_amount
    sale = Sale(item_id=item.id, rate=data['rate'], qty=data['qty'], amount=sales_amount)
    db.session.add(sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded successfully!"}), 201


@app.route('/report', methods=['GET'])
def view_report():
    company = Company.query.first()
    total_items = Item.query.count()
    total_purchases = Purchase.query.count()
    report_data = [
        {"description": "Total Items", "value": total_items},
        {"description": "Total Purchases", "value": total_purchases},
        {"description": "Current Cash Balance", "value": company.cash_balance}
    ]
    return jsonify(report_data)

if __name__ == '__main__':
    app.run(debug=True)

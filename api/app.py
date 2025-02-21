from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'brand': product.brand,
        'stock': product.stock
    } for product in products])

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'brand': product.brand,
        'stock': product.stock
    })

@app.route('/api/products/health', methods=['GET'])
def health_check():
    return "API Is Healthy!"

if __name__ == '__main__':
    app.run(debug=True)
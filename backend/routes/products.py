from flask import Blueprint, request, jsonify
from models import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        product = Product(
            name        = data['name'],
            sku         = data['sku'],
            unit_price  = data['unit_price'],
            stock_level = data.get('stock_level', 0),
            category    = data.get('category', '')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        product.name        = data.get('name',        product.name)
        product.sku         = data.get('sku',         product.sku)
        product.unit_price  = data.get('unit_price',  product.unit_price)
        product.stock_level = data.get('stock_level', product.stock_level)
        product.category    = data.get('category',    product.category)
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
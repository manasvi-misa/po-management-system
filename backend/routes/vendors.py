from flask import Blueprint, request, jsonify
from models import db, Vendor

vendors_bp = Blueprint('vendors', __name__)

@vendors_bp.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        vendors = Vendor.query.all()
        return jsonify([v.to_dict() for v in vendors]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vendors_bp.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    try:
        vendor = Vendor.query.get_or_404(id)
        return jsonify(vendor.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vendors_bp.route('/vendors', methods=['POST'])
def create_vendor():
    try:
        data = request.get_json()
        vendor = Vendor(
            name=data['name'],
            contact=data['contact'],
            rating=data.get('rating', 0)
        )
        db.session.add(vendor)
        db.session.commit()
        return jsonify(vendor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@vendors_bp.route('/vendors/<int:id>', methods=['PUT'])
def update_vendor(id):
    try:
        vendor = Vendor.query.get_or_404(id)
        data = request.get_json()
        vendor.name    = data.get('name',    vendor.name)
        vendor.contact = data.get('contact', vendor.contact)
        vendor.rating  = data.get('rating',  vendor.rating)
        db.session.commit()
        return jsonify(vendor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@vendors_bp.route('/vendors/<int:id>', methods=['DELETE'])
def delete_vendor(id):
    try:
        vendor = Vendor.query.get_or_404(id)
        db.session.delete(vendor)
        db.session.commit()
        return jsonify({"message": "Vendor deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
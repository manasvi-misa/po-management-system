from flask import Blueprint, request, jsonify
from models import db, PurchaseOrder, POItem, Product, Vendor
import requests as http_requests

orders_bp = Blueprint('orders', __name__)

TAX_RATE = 0.05
NOTIFY_URL = 'http://localhost:4000/notify'

def calculate_total(items_data):
    subtotal = sum(i['quantity'] * i['unit_price'] for i in items_data)
    return round(subtotal * (1 + TAX_RATE), 2)

def send_notification(reference_no, status, vendor_name):
    try:
        http_requests.post(NOTIFY_URL, json={
            'reference_no': reference_no,
            'status':       status,
            'vendor':       vendor_name
        }, timeout=2)
    except Exception:
        pass 

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = PurchaseOrder.query.all()
        return jsonify([o.to_dict() for o in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    try:
        order = PurchaseOrder.query.get_or_404(id)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data       = request.get_json()
        items_data = data.get('items', [])
        total      = calculate_total(items_data)

        order = PurchaseOrder(
            reference_no = data['reference_no'],
            vendor_id    = data['vendor_id'],
            total_amount = total,
            status       = 'Draft'
        )
        db.session.add(order)
        db.session.flush()

        for item in items_data:
            po_item = POItem(
                po_id      = order.id,
                product_id = item['product_id'],
                quantity   = item['quantity'],
                unit_price = item['unit_price'],
                subtotal   = item['quantity'] * item['unit_price']
            )
            db.session.add(po_item)

        db.session.commit()

        vendor = Vendor.query.get(data['vendor_id'])
        vendor_name = vendor.name if vendor else ''
        send_notification(order.reference_no, 'Draft', vendor_name)

        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/orders/<int:id>/status', methods=['PUT'])
def update_status(id):
    try:
        order  = PurchaseOrder.query.get_or_404(id)
        data   = request.get_json()
        order.status = data['status']
        db.session.commit()

        vendor = Vendor.query.get(order.vendor_id)
        vendor_name = vendor.name if vendor else ''
        send_notification(order.reference_no, data['status'], vendor_name)

        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = PurchaseOrder.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
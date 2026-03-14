from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    contact    = db.Column(db.String(100), nullable=False)
    rating     = db.Column(db.Numeric(2,1))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "contact":    self.contact,
            "rating":     float(self.rating) if self.rating else None,
            "created_at": str(self.created_at)
        }

class Product(db.Model):
    __tablename__ = 'products'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    sku         = db.Column(db.String(50),  unique=True, nullable=False)
    unit_price  = db.Column(db.Numeric(10,2), nullable=False)
    stock_level = db.Column(db.Integer, default=0)
    category    = db.Column(db.String(50))
    created_at  = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "sku":         self.sku,
            "unit_price":  float(self.unit_price),
            "stock_level": self.stock_level,
            "category":    self.category,
            "created_at":  str(self.created_at)
        }

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id           = db.Column(db.Integer, primary_key=True)
    reference_no = db.Column(db.String(50), unique=True, nullable=False)
    vendor_id    = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    total_amount = db.Column(db.Numeric(10,2), default=0)
    status       = db.Column(db.String(20), default='Draft')
    created_at   = db.Column(db.DateTime, server_default=db.func.now())
    items        = db.relationship('POItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            "id":           self.id,
            "reference_no": self.reference_no,
            "vendor_id":    self.vendor_id,
            "total_amount": float(self.total_amount),
            "status":       self.status,
            "created_at":   str(self.created_at),
            "items":        [i.to_dict() for i in self.items]
        }

class POItem(db.Model):
    __tablename__ = 'po_items'
    id         = db.Column(db.Integer, primary_key=True)
    po_id      = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    subtotal   = db.Column(db.Numeric(10,2), nullable=False)

    def to_dict(self):
        return {
            "id":         self.id,
            "po_id":      self.po_id,
            "product_id": self.product_id,
            "quantity":   self.quantity,
            "unit_price": float(self.unit_price),
            "subtotal":   float(self.subtotal)
        }
class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id":       self.id,
            "username": self.username,
            "email":    self.email
        }    
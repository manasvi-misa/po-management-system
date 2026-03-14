from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.vendors import vendors_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.ai import ai_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, origins=["*"])
    JWTManager(app)

    app.register_blueprint(vendors_bp,  url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(orders_bp,   url_prefix='/api')
    app.register_blueprint(ai_bp,       url_prefix='/api')
    app.register_blueprint(auth_bp,     url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
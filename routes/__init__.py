from .dashboard_routes import dashboard_bp
from .auth_routes import auth_bp
from .owner_routes import owner_bp
from .petugas_routes import petugas_bp
from .transaksi_routes import transaksi_bp
from .handler_routes import handler_bp
from .users_routes import users_bp
from .parking_routes import parking_bp



def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(owner_bp)
    app.register_blueprint(petugas_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(handler_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(parking_bp)

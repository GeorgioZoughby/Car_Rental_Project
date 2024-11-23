from .backend.category_routes import category_bp
from .backend.admins_routes import admins_bp
from .html_routes import html_bp
#from .clients_routes import client_bp

def init_blueprints(app):
    app.register_blueprint(category_bp)
    app.register_blueprint(html_bp)
    app.register_blueprint(admins_bp)
    #app.register_blueprint(client_bp)


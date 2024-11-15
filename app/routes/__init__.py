from .category_routes import category_bp
from .html_routes import html_bp

def init_blueprints(app):
    app.register_blueprint(category_bp)
    app.register_blueprint(html_bp)


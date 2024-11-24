from .backend.admins_routes import admins_bp
from .backend.bookings_routes import bookings_bp
from .backend.brand_routes import brand_bp
from .backend.category_routes import category_bp
from .backend.cars_categories_routes import cars_categories_bp
from .backend.cars_details_routes import cars_details_bp
from .backend.cars_routes import cars_bp
from .backend.clients_routes import clients_bp
from .backend.countries_routes import countries_bp
from .backend.cars_maintenance_routes import cars_maintenance_bp
from .backend.cars_image_routes import cars_images_bp
from .backend.invoices_routes import invoices_bp
from .html_routes import html_bp

def init_blueprints(app):
    app.register_blueprint(category_bp)
    app.register_blueprint(html_bp)
    app.register_blueprint(admins_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(brand_bp)
    app.register_blueprint(cars_categories_bp)
    app.register_blueprint(cars_details_bp)
    app.register_blueprint(cars_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cars_maintenance_bp)
    app.register_blueprint(cars_images_bp)
    app.register_blueprint(invoices_bp)


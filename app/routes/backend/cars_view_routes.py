from flask import Blueprint, request, jsonify
import connection as db_con

cars_view_bp = Blueprint('cars_view', __name__)

@cars_view_bp.route('/api/carsV', methods=['GET'])
def get_cars():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_V;")
    cars = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars)


@cars_view_bp.route('/api/carsV/<int:id>', methods=['GET'])
def get_cars_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_V WHERE car_id = %s;", (id,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404


@cars_view_bp.route('/api/cars/<int:brand_id>', methods=['GET'])
def get_cars_by_brand(brand_id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE brand_id = %s;", (brand_id,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404





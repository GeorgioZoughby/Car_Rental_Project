from flask import Blueprint, request, jsonify
import connection as db_con

cars_bp = Blueprint('cars', __name__)

@cars_bp.route('/api/cars', methods=['GET'])
def get_cars():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars;")
    cars = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars)

@cars_bp.route('/api/cars', methods=['POST'])
def create_cars():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415
    
    vin_number = data.get('vin_number')

    purchase_date = data.get('purchase_date')

    brand_id = data.get('brand_id')

    model = data.get('model')

    make = data.get('make')

    rental_price = data.get('rental_price')

    insurance_price = data.get('insurance_price')


    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO cars (vin_number, purchase_date, brand_id, model, make_year, rental_price, insurance_price) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING car_id;",
            (vin_number, purchase_date, brand_id, model, make, rental_price, insurance_price)
        )
        conn.commit()
        car_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': car_id, 'message': 'cars created successfully'}), 201

@cars_bp.route('/api/cars/<int:id>', methods=['GET'])
def get_cars_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE car_id = %s;", (id,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404

@cars_bp.route('/api/cars/price_range', methods=['GET'])
def get_cars_by_price_range():
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is None or max_price is None:
        return jsonify({'error': 'Please provide both min_price and max_price parameters'}), 400
    if min_price > max_price:
        return jsonify({'error': 'min_price should be less than or equal to max_price'}), 400
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE rental_price BETWEEN %s AND %s;", (min_price, max_price))
    cars = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'Error':'No cars found'})

@cars_bp.route('/api/cars/<int:brand_id>', methods=['GET'])
def get_cars_by_brand(brand_id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE brand_id = %s;", (brand_id,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404


@cars_bp.route('/api/cars/<int:available>', methods=['GET'])
def get_cars_by_availability(available):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_availability_V WHERE available = %s;", (available,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404


@cars_bp.route('/api/cars/<int:available>', methods=['GET'])
def get_cars_by_pri(available):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_availability_V WHERE available = %s;", (available,))
    cars = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(cars) if cars else jsonify({'error': 'cars not found'}), 404



@cars_bp.route('/api/cars/<int:id>', methods=['PUT'])
def update_cars(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cars SET vin_number = %s, purchase_date = %s, brand_id = %s, model = %s, make = %s, rental_price = %s, insurance_price = %s WHERE id = %s;",
        ( data['vin_number'], data['purchase_date'], data['brand_id'], data['model'], data['make'], data['insurance_price'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'cars updated successfully'})

@cars_bp.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_cars(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars WHERE car_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'cars deleted successfully'})


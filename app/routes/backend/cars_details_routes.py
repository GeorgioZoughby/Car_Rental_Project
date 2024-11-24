from flask import Blueprint, request, jsonify
import connection as db_con

cars_details_bp = Blueprint('cars_details', __name__)

@cars_details_bp.route('/api/cars_details', methods=['GET'])
def get_cars_details():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_details;")
    cars_details = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_details)

@cars_details_bp.route('/api/cars_details', methods=['POST'])
def create_cars_details():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    car_id = data.get('car_id')
    if not car_id:
        return jsonify({'error': 'Car id is required'}), 400
    
    transmission = data.get('transmission')
    if not transmission:
        return jsonify({'error': 'Transmission is required'}), 400
    
    fuel_type = data.get('car_id')
    if not fuel_type:
        return jsonify({'error': 'Fuel type is required'}), 400
    
    engine_size = data.get('engine_size')
    if not engine_size:
        return jsonify({'error':'Engine size is required'})

    horsepower = data.get('horsepower')
    if not horsepower:
        return jsonify({'error':'Horsepower required'})
    
    mileage = data.get('mileage')
    if not mileage:
        return jsonify({'error': 'Mileage is required'}), 400
    
    seating_capacity = data.get('seating_capacity')
    if not seating_capacity:
        return jsonify({'error': 'Seating Capacity is required'}), 400
    
    color = data.get('color')
    if not color:
        return jsonify({'error': 'Color is required'}), 400
    
    options = data.get('options')
    if not color:
        return jsonify({'error': 'Options is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO cars_details (transmission, fuel_type, engine_size, horsepower, mileage, seating_capacity, color, options) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING car_id;",
            (transmission,fuel_type,engine_size,horsepower, mileage, seating_capacity, color, options )
        )
        conn.commit()
        car_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': car_id, 'message': 'Car details created successfully'}), 201

@cars_details_bp.route('/api/cars_details/<int:id>', methods=['GET'])
def get_car_details(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_details WHERE car_id = %s;", (id,))
    car = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(car) if car else jsonify({'error': 'Car details not found'}), 404

@cars_details_bp.route('/api/cars_details/<int:id>', methods=['PUT'])
def update_car_details(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cars_details SET transmission = %s, fuel_type = %s, engine_size = %s, horsepower = %s, mileage = %s, seating_capacity = %s, color = %s, options = %s WHERE car_id = %s;",
        (data['transmission'], data['fuel_type'],data['engine_size'], data['horsepower'], data['mileage'], data['seating_capacity'], data['color'], data['options'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Category updated successfully'})

@cars_details_bp.route('/api/cars_details/<int:id>', methods=['DELETE'])
def delete_car_details(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars_details WHERE car_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Car details deleted successfully'})


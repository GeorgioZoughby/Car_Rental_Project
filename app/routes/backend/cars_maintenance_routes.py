from flask import Blueprint, request, jsonify
import connection as db_con
from  datetime import datetime, timedelta

cars_maintenance_bp = Blueprint('cars_maintenance', __name__)

@cars_maintenance_bp.route('/api/cars_maintenance', methods=['GET'])
def get_cars_maintenance():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_full_details_V;")
    cars_maintenance = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_maintenance)

@cars_maintenance_bp.route('/api/cars_maintenance/<int:car_id>', methods=['POST'])
def create_cars_maintenance(car_id):
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    last_service_date = data.get('last_service_date')

    service_due_date = data.get('service_due_date')

    registration_expiration_date = data.get('registration_expiration_date')

    accident_history = data.get('accident_history')

    comments = data.get('comments')
    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO cars_maintenance (car_id, last_service_date, service_due_date, registration_expiration_date, accident_history, comments) VALUES (%s, %s,%s,%s,%s,%s);",
            (car_id, last_service_date, service_due_date, registration_expiration_date, accident_history, comments)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)})
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'cars_maintenance created successfully'}), 201

@cars_maintenance_bp.route('/api/cars_maintenance/<int:id>', methods=['GET'])
def get_cars_maintenance_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT car_id, CONCAT_WS(' ', brand, model, make_year) as car_name, registration_expiration_date, last_service_date, service_due_date, accident_history  FROM cars_full_details_V WHERE car_id = %s;", (id,))
    cars_maintenance = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_maintenance),200

@cars_maintenance_bp.route('/api/cars_maintenance/past_due', methods=['GET'])
def get_past_maintenance():
    conn = db_con.connect()
    cur = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    cur.execute("SELECT * FROM cars_full_details_V WHERE service_due_date < %s;", (today,))
    cars_maintenance = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_maintenance) if cars_maintenance else jsonify({'error': 'cars maintenance not found'}), 404

@cars_maintenance_bp.route('/api/cars_maintenance/need_service_soon', methods=['GET'])
def get_soon_past_maintenance():
    conn = db_con.connect()
    cur = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    one_month_today = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    cur.execute("SELECT * FROM cars_full_details_V WHERE service_due_date BETWEEN %s AND %s;", (today,one_month_today))
    cars_maintenance = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_maintenance), 200

@cars_maintenance_bp.route('/api/cars_maintenance/registration_expiry', methods=['GET'])
def get_registration_expiry_maintenance():
    conn = db_con.connect()
    cur = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    three_months_today = (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d')
    cur.execute("SELECT * FROM cars_full_details_V WHERE registration_expiration_date BETWEEN %s AND %s;", (today,three_months_today))
    cars_maintenance = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_maintenance)




@cars_maintenance_bp.route('/api/cars_maintenance/<int:id>', methods=['PUT'])
def update_cars_maintenance(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cars_maintenance SET last_service_date = %s, service_due_date = %s, registration_expiration_date = %s, accident_history = %s, comments = %s  WHERE car_id = %s;",
        (data['last_service_date'], data['service_due_date'], data['registration_expiration_date'], data['accident_history'], data['comments'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Car record updated successfully'}), 200

@cars_maintenance_bp.route('/api/cars_maintenance/<int:id>', methods=['DELETE'])
def delete_cars_maintenance(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars_maintenance WHERE car_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'cars_maintenance deleted successfully'})


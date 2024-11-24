from flask import Blueprint, request, jsonify
import connection as db_con
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/api/bookings', methods=['GET'])
def get_bookings():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings;")
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(bookings)

@bookings_bp.route('/api/bookings', methods=['POST'])
def create_bookings():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    client_id = data.get('client_id')
    if not client_id:
        return jsonify({'error': 'Client id is required'}), 400

    car_id = data.get('car_id')
    if not car_id:
        return jsonify({'error': 'Car id is required'}), 400

    start_date = data.get('start_date')
    if not start_date:
        return jsonify({'error': 'Start Date is required'}), 400

    end_date = data.get('end_date')
    if not end_date:
        return jsonify({'error': 'End Date is required'}), 400


    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO bookings (booking_date, client_id, car_id, start_date, end_date) VALUES (CURRENT_DATE,%s,%s,%s,%s) RETURNING booking_id;",
            (client_id, car_id, start_date, end_date)
        )
        conn.commit()
        bookings_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': bookings_id, 'message': 'bookings created successfully'}), 201

@bookings_bp.route('/api/bookings/<int:id>', methods=['GET'])
def get_bookings_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE booking_id = %s;", (id,))
    bookings = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(bookings) if bookings else jsonify({'error': 'bookings not found'}), 404

@bookings_bp.route('/api/bookings/<int:id>', methods=['PUT'])
def update_bookings(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET booking_date = %s, client_id = %s car_id = %s, start_date = %s, end_date = %s WHERE booking_id = %s;",
        (data['booking_date'], data['client_id'],data['car_id'],data['start_date'], data['end_date'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Bookings updated successfully'})

@bookings_bp.route('/api/bookings/<int:id>', methods=['DELETE'])
def delete_bookings(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings WHERE booking_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Bookings deleted successfully'})


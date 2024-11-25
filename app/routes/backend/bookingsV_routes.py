from flask import Blueprint, request, jsonify
import connection as db_con

bookings_view_bp = Blueprint('bookingsV', __name__)

@bookings_view_bp.route('/api/bookingsV', methods=['GET'])
def get_bookings():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings_V;")
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(bookings)


@bookings_view_bp.route('/api/bookingsV/<int:id>', methods=['GET'])
def get_bookings_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings_V WHERE booking_id = %s;", (id,))
    bookings = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(bookings) if bookings else jsonify({'error': 'bookings not found'}), 404



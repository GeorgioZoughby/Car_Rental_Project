from flask import Blueprint, request, jsonify
import connection as db_con

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('/api/invoices', methods=['GET'])
def get_invoices():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices;")
    invoices = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(invoices)

@invoices_bp.route('/api/invoices', methods=['POST'])
def create_invoices():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    invoice_id = data.get('invoice_id')
    if not invoice_id:
        return jsonify({'error': 'Invoice ID is required'}), 400

    booking_id = data.get('booking_id')
    if not booking_id:
        return jsonify({'error': 'Booking ID is required'}), 400

    total_price_paid = data.get('total_price_paid')
    if not total_price_paid:
        return jsonify({'error': 'Total price paid is required'}), 400

    insurance_price = data.get('insurance_price')
    if not insurance_price:
        return jsonify({'error': 'insurance price is required'}), 400

    insurance_deducted = data.get('insurance_deducted')
    if not insurance_deducted:
        return jsonify({'error': 'insurance deducted is required'}), 400

    invoice_date = data.get('invoice_date')
    if not invoice_date:
        return jsonify({'error': 'invoice edate is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO invoices (invoice_id, booking_id, total_price_paid, insurance_price, insurance_deducted, invoice_date) VALUES (%s,%s,%s,%s,%s,%s) RETURNING invoice_id;",
            (invoice_id, booking_id, total_price_paid, insurance_price, insurance_deducted, invoice_date)
        )
        conn.commit()
        invoices_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': invoices_id, 'message': 'invoices created successfully'}), 201

@invoices_bp.route('/api/invoices/<int:id>', methods=['GET'])
def get_invoices(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE invoice_id = %s;", (id,))
    invoices = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(invoices) if invoices else jsonify({'error': 'invoices not found'}), 404

@invoices_bp.route('/api/invoices/<int:id>', methods=['PUT'])
def update_invoices(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE invoices SET booking_id = %s, total_price_paid = %s, insurance_price= %s, insurance_deducted = %s, invoice_date = %s WHERE invoice_id = %s;",
        (data['booking_id'], data['total_price_paid'], data['insurance_price'], data['insurance_deducted'], data['invoice_date'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'invoices updated successfully'})

@invoices_bp.route('/api/invoices/<int:id>', methods=['DELETE'])
def delete_invoices(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM invoices WHERE invoice_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'invoices deleted successfully'})


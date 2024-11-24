from flask import Blueprint, request, jsonify
import connection as db_con
import os

brand_bp = Blueprint('brand', __name__)

@brand_bp.route('/api/brands', methods=['GET'])
def get_brand():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM brands;")
    brand = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(brand)

@brand_bp.route('/api/brands', methods=['POST'])
def create_brand():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    brand = data.get('brand')
    if not brand:
        return jsonify({'error': 'Brand is required'}), 400
    brand_country = data.get('brand_country')
    if not brand_country:
        return jsonify({'error': 'Brand Country is required'}), 400
    logo_url = data.get('logo_url')
    if not logo_url:
        return jsonify({'error': 'Logo is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        file = request.files['logo_url']
        if file.filename == '':
            return "No selected file", 400
        if file:
            filename = file.filename
            #filepath = os.path.join(config['UPLOAD_FOLDER'], filename)
            #file.save(filepath)
        cur.execute(
            "INSERT INTO brands (brand, brand_country, logo_url) VALUES (%s) RETURNING brand_id;",
            (brand, brand_country, logo_url)
        )
        conn.commit()
        brand_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': brand_id, 'message': 'brand created successfully'}), 201

@brand_bp.route('/api/brands/<int:id>', methods=['GET'])
def get_brand_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM brands WHERE brand_id = %s;", (id,))
    brand = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(brand) if brand else jsonify({'error': 'brand not found'}), 404

@brand_bp.route('/api/brand/<int:id>', methods=['PUT'])
def update_brand(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE brands SET brand = %s, brand_country = %s, logo_url = %s WHERE brand_id = %s;",
        (data['brand'], data['brand_country'], data['logo_url'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Brand updated successfully'})

@brand_bp.route('/api/brand/<int:id>', methods=['DELETE'])
def delete_brand(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM brands WHERE brand_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Brand deleted successfully'})
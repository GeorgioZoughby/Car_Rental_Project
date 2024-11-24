from flask import Blueprint, request, jsonify
import connection as db_con

countries_bp = Blueprint('country', __name__)

@countries_bp.route('/api/countries', methods=['GET'])
def get_countries():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries;")
    countries = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(countries)

@countries_bp.route('/api/countries', methods=['POST'])
def create_country():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    country = data.get('country')
    if not country:
        return jsonify({'error': 'country is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO countries (country) VALUES (%s) RETURNING country_id;",
            (country,)
        )
        conn.commit()
        country_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': country_id, 'message': 'country created successfully'}), 201

@countries_bp.route('/api/countries/<int:id>', methods=['GET'])
def get_country(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries WHERE country_id = %s;", (id,))
    country = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(country) if country else jsonify({'error': 'country not found'}), 404

@countries_bp.route('/api/countries/<int:id>', methods=['PUT'])
def update_country(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE countries SET country_id = %s, country = %s WHERE id = %s;",
        (data['country_id'], data['country'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'country updated successfully'})

@countries_bp.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM countries WHERE country_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'country deleted successfully'})


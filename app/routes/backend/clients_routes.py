from flask import Blueprint, request, jsonify
import connection as db_con

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/api/clients', methods=['GET'])
def get_clients():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("""SELECT 
                client_id,
                creation_date::text AS creation_date,
                username,
                encode(password, 'base64') AS password,
                title,
                first_name,
                last_name,
                birth_date::text AS birth_date, 
                gender,
                email,
                phone_number,
                country_id,
                address
            FROM clients;""")
    clients = cur.fetchall()
    cur.close()
    conn.close()
    print(clients)
    return jsonify(clients)

@clients_bp.route('/api/clients', methods=['POST'])
def create_clients():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    client_id = data.get('client_id')
    if not client_id:
        return jsonify({'error': 'client ID is required'}), 400

    creation_date = data.get('creation_date')
    if not creation_date:
        return jsonify({'error': 'client ID is required'}), 400

    username = data.get('username')
    if not username:
        return jsonify({'error': 'client ID is required'}), 400

    password = data.get('password')
    if not password:
        return jsonify({'error': 'client ID is required'}), 400

    title = data.get('title')
    if not title:
        return jsonify({'error': 'client ID is required'}), 400

    first_name = data.get('first_name')
    if not first_name:
        return jsonify({'error': 'client ID is required'}), 400

    last_name = data.get('last_name')
    if not last_name:
        return jsonify({'error': 'client ID is required'}), 400

    birth_date = data.get('birth_date')
    if not birth_date:
        return jsonify({'error': 'client ID is required'}), 400

    gender = data.get('gender')
    if not gender:
        return jsonify({'error': 'client ID is required'}), 400

    email = data.get('email')
    if not email:
        return jsonify({'error': 'client ID is required'}), 400

    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({'error': 'client ID is required'}), 400

    country_id = data.get('country_id')
    if not country_id:
        return jsonify({'error': 'client ID is required'}), 400
    
    address = data.get('address')
    if not address:
        return jsonify({'error': 'client ID is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO clients (client_id, creation_date, username, password, title, first_name, last_name, birth_date, gender, email, phone_number, country_id, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING client_id;",
            (client_id, creation_date, username, password, title, first_name, last_name, birth_date, gender, email, phone_number, country_id, address)
        )
        conn.commit()
        client_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': client_id, 'message': 'clients created successfully'}), 201

@clients_bp.route('/api/clients/<int:id>', methods=['GET'])
def get_clients_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE client_id = %s;", (id,))
    clients = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(clients) if clients else jsonify({'error': 'clients not found'}), 404

@clients_bp.route('/api/clients/<int:id>', methods=['PUT'])
def update_clients(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE clients SET client_id = %s, creation_date = %s, username = %s, password = %s, title = %s, first_name = %s, last_name = %s, birth_date = %s, gender = %s, email = %s, phone_number = %s, country_id = %s, address = %s WHERE client_id = %s;",
        (data['client_id'], data['creation_date'], data['username'], data['password'], data['title'], data['first_name'], data['last_name'], data['birth_date'], data['gender'], data['email'], data['phone_number'], data['country_id'], data['address'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'clients updated successfully'})

@clients_bp.route('/api/clients/<int:id>', methods=['DELETE'])
def delete_clients(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE client_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'clients deleted successfully'})


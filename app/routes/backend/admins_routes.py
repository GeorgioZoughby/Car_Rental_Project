from flask import Blueprint, request, jsonify
import connection as db_con
import functions.passwords as password_func

 


admins_bp = Blueprint('admins', __name__)

@admins_bp.route('/api/admins', methods=['GET'])
def get_admins():
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT admin_id, username FROM admins;")
    admins = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(admins)

@admins_bp.route('/api/admins', methods=['POST'])
def create_admin():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    username = data.get('username')
    password = data.get('password')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    hashed_password = password_func.hash_password(password)

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO admins(username, password) VALUES (%s, %s);",
            (username, hashed_password)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Admin created successfully'}), 201

@admins_bp.route('/api/admins/<string:username>/<string:password>', methods=['GET'])
def get_username(username, password):
    conn = db_con.connect()
    cur = conn.cursor()

    cur.execute("SELECT password FROM admins WHERE username = %s;", (username,))
    result = cur.fetchone()

    if not result:
        return jsonify({'message': 'Invalid username or password'}), 401

    stored_password = result[0]  

    if password_func.verify_password(password, stored_password):
        return jsonify({'message': 'Successful login'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401



@admins_bp.route('/api/admins/<int:id>', methods=['PUT'])
def update_admins(id):
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    conn = db_con.connect()
    cur = conn.cursor()

    if 'password' in data and data['password']:
        hashed_password = password_func.hash_password(data['password'])
        cur.execute("UPDATE admins SET password = %s WHERE admin_id = %s;",
                    (hashed_password, id))

    if 'username' in data and data['username']:
        cur.execute("UPDATE admins SET username = %s WHERE admin_id = %s;",
                    (data['username'], id))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Updated successfully'})


@admins_bp.route('/api/admins/<int:id>', methods=['DELETE'])
def delete_admin(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM admins WHERE admin_id = %s;",
                (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message':'Successful delete'})
from flask import Blueprint, request, jsonify
import connection as db_con

cars_categories_bp = Blueprint('category', __name__)

@cars_categories_bp.route('/api/cars_categories', methods=['GET'])
def get_cars_categories():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_categories;")
    cars_categories = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_categories)

@cars_categories_bp.route('/api/cars_categories', methods=['POST'])
def create_category():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    car_id = data.get('car_id')
    if not car_id:
        return jsonify({'error': 'Car id is required'}), 400

    category_id = data.get('category_id')
    if not category_id:
        return jsonify({'error': 'Category id is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO cars_categories (car_id, category_id) VALUES (%s, %s) RETURNING category_id;",
            (car_id, category_id)
        )
        conn.commit()
        category_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': category_id, 'message': 'Car Category created successfully'}), 201

@cars_categories_bp.route('/api/cars_categories/<int:id>', methods=['GET'])
def get_category(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_categories WHERE car_id = %s;", (id,))
    category = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(category) if category else jsonify({'error': 'Car Category not found'}), 404

@cars_categories_bp.route('/api/cars_categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cars_categories SET category_id = %s WHERE car_id = %s;",
        (data['category_id'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Category updated successfully'})

@cars_categories_bp.route('/api/cars_categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars_categories WHERE car_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Category deleted successfully'})
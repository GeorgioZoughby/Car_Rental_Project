from flask import Blueprint, request, jsonify
import connection as db_con

category_bp = Blueprint('category', __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories;")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(categories)

@category_bp.route('/api/categories', methods=['POST'])
def create_category():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    category = data.get('category')
    if not category:
        return jsonify({'error': 'Category is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO categories (category) VALUES (%s) RETURNING category_id;",
            (category,)
        )
        conn.commit()
        category_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': category_id, 'message': 'Category created successfully'}), 201

@category_bp.route('/api/categories/<int:id>', methods=['GET'])
def get_category(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories WHERE category_id = %s;", (id,))
    category = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(category) if category else jsonify({'error': 'Category not found'}), 404

@category_bp.route('/api/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE categories SET name = %s, description = %s WHERE id = %s;",
        (data['name'], data['description'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Category updated successfully'})

@category_bp.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE category_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Category deleted successfully'})


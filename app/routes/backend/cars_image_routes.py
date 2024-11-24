from flask import Blueprint, request, jsonify
import connection as db_con
import os

cars_images_bp = Blueprint('car_images', __name__)

@cars_images_bp.route('/api/cars_images', methods=['GET'])
def get_cars_images():
    conn = db_con.connect() 
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_images;")
    cars_images = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cars_images)

@cars_images_bp.route('/api/cars_images/<int:car_id>', methods=['POST'])
def create_cars_images():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    cars_images = data.get('car_id')
    image_url = data.get('image_url')
    if not cars_images:
        return jsonify({'error': 'Car Image is required'}), 400

    conn = db_con.connect()
    cur = conn.cursor()

    try:
        if 'images' not in request.files:
            return "No file part in the request", 400

        files = request.files.getlist('images')
        uploaded_files = []

        for file in files:
            if file:
                filename = file.filename
                #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                #file.save(filepath)
                uploaded_files.append(filename)
        cur.execute(
            "INSERT INTO cars_images (car_id, image_url) VALUES (%s,%s) RETURNING car_id;",
            (car_id, image_url)
        )
        conn.commit()
        car_id = cur.fetchone()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': car_id, 'message': 'Car image created successfully'}), 201

@cars_images_bp.route('/api/cars_images/<int:id>', methods=['GET'])
def get_cars_images_by_id(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars_images WHERE car_id = %s;", (id,))
    car = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(car) if car else jsonify({'error': 'Car not found'}), 404

@cars_images_bp.route('/api/cars_images/<int:id>', methods=['PUT'])
def update_cars_images(id):
    data = request.get_json()
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cars_images SET name = %s, description = %s WHERE id = %s;",
        (data['name'], data['description'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Cars image updated successfully'})

@cars_images_bp.route('/api/cars_images/<int:id>', methods=['DELETE'])
def delete_cars_images(id):
    conn = db_con.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars_images WHERE car_id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Car image deleted successfully'})


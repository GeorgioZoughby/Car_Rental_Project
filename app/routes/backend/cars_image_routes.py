from flask import Blueprint, request, jsonify
import connection as db_con
from werkzeug.utils import secure_filename
import os

cars_images_bp = Blueprint('car_images', __name__)

UPLOAD_FOLDER = 'static/images/cars/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
def create_cars_images(car_id):
    if 'images' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    conn = db_con.connect()
    cur = conn.cursor()
    uploaded_urls = []

    try:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                image_url = f'images/car/{filename}'
                cur.execute(
                    "INSERT INTO cars_images (car_id, image_url) VALUES (%s, %s);",
                    (car_id, image_url)
                )
                uploaded_urls.append(image_url)

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({
        'message': 'Car images uploaded successfully',
        'uploaded_images': uploaded_urls
    }), 201



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


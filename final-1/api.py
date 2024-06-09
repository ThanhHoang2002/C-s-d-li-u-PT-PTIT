from flask import Flask, request, jsonify
from Repository import Repository
from Service import Service
import mysql.connector
from flask_cors import CORS
from flask import send_file
from PIL import Image
app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="11102002",
    database="nature_image_data_2"
)
repository = Repository(db)
service = Service(repository)
images = service.get_all_image()
CORS(app)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        # Tên tệp mới bạn muốn sử dụng để thay thế tệp test.jpg
        new_filename = 'test.jpg'

        # Mở tệp hình ảnh bằng Pillow
        image = Image.open(file)

        # Resize ảnh thành 256x256
        image = image.resize((256, 256))

        # Lưu tệp với tên mới
        image.save(new_filename)
        
        # Gọi hàm search_image để tìm kiếm hình ảnh và nhận kết quả trả về
        output = service.search_image(new_filename, images)
        
        # Trả kết quả về cho frontend
        return jsonify(output)
    
    return jsonify({'error': 'Error occurred during upload'})
@app.route('/image/<path:image_path>', methods=['GET'])
def get_image(image_path):
    return send_file(image_path, mimetype='image/jpeg')
@app.route('/test', methods=['GET'])
def test():
    service.insert_image_from_folder('resize_image')
    return jsonify({'message': 'Test successful'})
if __name__ == '__main__':
    app.run(debug=True)

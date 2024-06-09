
class Repository:
    def __init__(self, db):
        self.db = db

    def get_all_image(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM image")
        images = cursor.fetchall()  # Lấy tất cả các hình ảnh từ kết quả của truy vấn
        cursor.close()
        return images

    def insert_image(self, color_histogram, hog, path):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO image (color_histogram, hog, path) VALUES (%s,%s,%s)", (color_histogram, hog, path))
        self.db.commit()
        cursor.close()
    # Thêm các hàm xử lý cơ sở dữ liệu khác tại đây

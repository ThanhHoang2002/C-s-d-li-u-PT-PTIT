from test import *
import os 
class Service:
    def __init__(self, repository):
        self.repository = repository

    def get_all_image(self):
        return self.repository.get_all_image()
    def insert_image_from_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            # Xác định đường dẫn đầy đủ đến tệp
            file_path = os.path.join(folder_path, filename)
            # Đảm bảo rằng tệp là một tệp ảnh
            if os.path.isfile(file_path) and any(filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                # Đọc ảnh và thêm vào danh sách
                bgr_image = cv2.imread(file_path)
                image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
                if image is not None:
                    # Trích xuất các đặc trưng từ ảnh
                    embedding, embedding_hog = feature_extraction(image)
                    color = ','.join(map(str, embedding))
                    hog = ','.join(map(str, embedding_hog))
                    # Lưu ảnh và các đặc trưng vào cơ sở dữ liệu
                    self.repository.insert_image( str(color), str(hog), file_path)
    def search_image(self, image_path, images):
        # Đọc ảnh và trích xuất các đặc trưng
        input_bgr_image = cv2.imread(image_path)
        resized_input_image = cv2.resize(input_bgr_image, (256, 256))
        input_rgb_image = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2RGB)
        color, hog = feature_extraction(input_rgb_image)
        
        # Tạo danh sách để lưu trữ độ tương tự và chỉ số của mỗi hình ảnh trong cơ sở dữ liệu
        similarity_list = []
        
        # Tính toán độ tương tự giữa ảnh truy vấn và các ảnh trong cơ sở dữ liệu
        for img in images:
            color_db = [float(x) for x in img['color_histogram'].split(',') ]
            hog_db = [float(x) for x in img['hog'].split(',') ]
            dis_color, dis_hog = compare(color, hog, color_db, hog_db)
            similarity_list.append((img['path'], dis_color, dis_hog))
        min_dis_color = min(similarity_list, key=lambda x: x[1])[1]
        max_dis_color = max(similarity_list, key=lambda x: x[1])[1]
        min_dis_hog = min(similarity_list, key=lambda x: x[2])[2]
        max_dis_hog = max(similarity_list, key=lambda x: x[2])[2]
        # Chuẩn hóa độ tương tự
        normalized_similarity_list = []
        for item in similarity_list:
            path, dis_color, dis_hog = item
            normalized_dis_color = (dis_color - min_dis_color) / (max_dis_color - min_dis_color) if max_dis_color != min_dis_color else 0
            normalized_dis_hog = (dis_hog - min_dis_hog) / (max_dis_hog - min_dis_hog) if max_dis_hog != min_dis_hog else 0
            normalized_similarity_list.append((path, normalized_dis_color, normalized_dis_hog))
        # Tính toán độ tương tự cuối cùng
        for i in range(len(normalized_similarity_list)):
            path, dis_color, dis_hog = normalized_similarity_list[i]
            similarity = 0.4 * dis_color + 0.6 * dis_hog
            normalized_similarity_list[i] = (path, similarity)
        # Sắp xếp danh sách độ tương tự từ thấp đến cao
        normalized_similarity_list.sort(key=lambda x: x[1])
        # Trả về 3 phần tử đầu tiên trong danh sách (có độ tương tự nhỏ nhất)
        top_3_indices = [path for path, similarity in normalized_similarity_list[:3]]
        return top_3_indices


    # Thêm các hàm xử lý logic kinh doanh khác tại đây

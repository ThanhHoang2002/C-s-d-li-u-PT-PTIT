import cv2
import os
import numpy as np
from skimage import feature
import math

# # Đọc tất cả ảnh trong file lưu trữ lại
# Đường dẫn tới thư mục chứa ảnh
def read_image(folder_path):
    # Khởi tạo một danh sách để lưu trữ các hình ảnh
    images = []
    
    # Lặp qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        # Xác định đường dẫn đầy đủ đến tệp
        file_path = os.path.join(folder_path, filename)
        # Đảm bảo rằng tệp là một tệp ảnh
        if os.path.isfile(file_path) and any(filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            # Đọc ảnh và thêm vào danh sách
            image = cv2.imread(file_path)
            if image is not None:
                images.append(image)
    return images

# # Hàm trích rút Color Histogram
def my_calcHist(image, channels, histSize, ranges):
    # Khởi tạo histogram với tất cả giá trị bằng 0
    hist = np.zeros(histSize, dtype=np.int64)
    # Lặp qua tất cả các pixel trong ảnh
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Lấy giá trị của kênh màu được chỉ định
            bin_vals = [image[i, j, c] for c in channels]
            # Tính chỉ số của bin
            bin_idxs = [(bin_vals[c] - ranges[c][0]) * histSize[c] // (ranges[c][1] - ranges[c][0]) for c in range(len(channels))]
            # Tăng giá trị của bin tương ứng lên 1
            hist[tuple(bin_idxs)] += 1
    return hist
def euclidean_distance(vector1, vector2):
    # Chuyển đổi list sang numpy array để sử dụng tính năng của numpy
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    
    # Tính khoảng cách Euclidean
    distance = np.sqrt(np.sum((vector1 - vector2)**2))
    return distance
def convert_image_rgb_to_gray(img_rgb):
    # Get the height (h), width (w), and number of channels (_) of the input RGB image
    h, w, _ = img_rgb.shape

    # Create an empty numpy array of zeros with dimensions (h, w) to hold the converted grayscale values
    img_gray = np.zeros((h, w), dtype=np.uint32)

    # Convert each pixel from RGB to grayscale using the formula Y = 0.299R + 0.587G + 0.114B
    for i in range(h):
        for j in range(w):
            r, g, b = img_rgb[i, j]
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            img_gray[i, j] = gray_value
            # Return the final grayscale image as a numpy array
    return np.array(img_gray)

def hog_feature(gray_img):  # default gray_image
    # Compute the HOG features and the HOG visualization image using the scikit-image "feature" module's hog() function.
    (hog_feats, hogImage) = feature.hog(
        gray_img,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        transform_sqrt=True,
        block_norm="L2",
        visualize=True,
    )

    return hog_feats
def feature_extraction(img):  # RGB image
    bins = [16, 16, 16]
    ranges = [[0, 256], [0, 256], [0, 256]]
    hist_my = my_calcHist(img, [0, 1, 2], bins, ranges)
    embedding = np.array(hist_my.flatten()) / (256*256)
    gray_image = convert_image_rgb_to_gray(img)
    embedding_hog = list(hog_feature(gray_image))
    return embedding,embedding_hog
def compare(color_hist_img1, hog_img1, color_hist_img2, hog_img2):
    # Tính khoảng cách Euclidean giữa các vector đặc trưng
    color_distance = euclidean_distance(color_hist_img1,color_hist_img2)

    hog_distance = euclidean_distance(hog_img1,hog_img2)
    #Trả về trung bình khoảng cách
    return color_distance, hog_distance
# bgr_image1 = cv2.imread('test.jpg')
# print("1")
# image1 = cv2.cvtColor(bgr_image1, cv2.COLOR_BGR2RGB)
# output = search_image(image1)
# for i, img in enumerate(output):
#     cv2.imwrite(f'output_image_{i}.jpg', img)
# print("end.")
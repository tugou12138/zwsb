import glob

from PIL import Image
import cv2
import numpy as np
from keras.applications.convnext import preprocess_input
import matplotlib.pyplot as plt

folder_path = r'C:\Users\ASUS\Desktop\c++\中华职教社\tree-master\static\images'
image_paths = glob.glob(folder_path + "\\*.png")

# 这里可能需要导入glob模块，以便使用glob.glob函数
# import glob

def ycl():
    print("获取文件夹中所有图像文件的路径", image_paths)
    print(len(image_paths))
    for i in range(len(image_paths)):
        image = Image.open(image_paths[i])
        image = image.resize((224, 224))
        image = preprocess_input(np.array(image))

        # 这里需要将图像从3通道BGR转换为灰度图像
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, dp=1, minDist=80,
                                   param1=10, param2=30, minRadius=10, maxRadius=400)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            max_circle = circles[0, np.argmax(circles[0, :, 2])]
            x, y, r = max_circle

            if x - r >= 0 and x + r < image.shape[1] and y - r >= 0 and y + r < image.shape[0]:
                stump_part = image[y - r:y + r, x - r:x + r + 1]
                if stump_part.size > 0:
                    print("Stump Part Shape:", stump_part.shape)
                    # cv2.imshow('Stump Part', stump_part)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    # 这里保存的应该是截取的树桩部分，而不是整个图像
                    cv2.imwrite('static/image/' + str(i) + ".png", stump_part)
                else:
                    print("截取的图像部分为空")
            else:
                print("截取范围超出图像边界")
        else:
            print("未找到树桩区域")
import sys
import time
import os

from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import glob
import os

import shuzhuangtiqu
from fenxi import calculate_similarity, extract_features

app = Flask(__name__)
# 配置静态文件的URL前缀和文件夹路径

app.static_url_path = '/static'
app.static_folder = './static'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'images' not in request.files:
        return 'No image uploaded'

    files = request.files.getlist('images')
    folder_path = r'static/images'  # 图像文件夹路径

    if not os.path.exists(folder_path):
        print("不存在")
        os.makedirs(folder_path)

    for file in files:
        # 保存图像到文件夹
        image_path = os.path.join(folder_path, file.filename)

        file.save(image_path)
    time.sleep(15)
    return redirect('analysis')


@app.route("/analysis", methods=["GET"])
def fenxi():
    duplicate_images = []  # 存储重复图像路径的列表
    # 获取文件夹中所有图像文件的路径
    folder_path = r"C:\Users\ASUS\Desktop\c++\中华职教社\tree-master\static\images"
    image_paths = glob.glob(folder_path + "/*.png")  # 指定图像文件类型

    print("获取文件夹中所有图像文件的路径", image_paths)

    # 阈值
    yuzhi = 0.80

    # 存储特征的集合
    tz_images = set()
    shuzhuangtiqu.ycl()
    # 批量处理图像并提取特征
    features = extract_features(image_paths)

    # 遍历图像文件路径列表
    for i in range(len(image_paths)):
        for j in range(i + 1, len(image_paths)):
            # 提取特征向量
            features1 = features[i]
            features2 = features[j]

            # 计算相似度
            similarity = calculate_similarity(features1, features2)

            # 判断是否重复
            if similarity > yuzhi:
                tz_images.add((image_paths[i], image_paths[j]))

    # 输出重复图像信息
    if len(tz_images) > 0:
        print("找到以下重复图像：")
        for image_pair in tz_images:
            img0 = image_pair[0]
            print("图像1：", img0)
            # file_name, extension = os.path.splitext(image_pair[0].replace("\\","/"))
            temp0 = '/static/images/'+img0.replace("\\","/").split('/')[-1]
            print(temp0)
            # duplicate_images.append(image_pair[0].replace("\\", "/"))
            duplicate_images.append(temp0)

            img1 = image_pair[1]
            print("图像2：", img1)
            temp1 = '/static/images/'+img1.replace("\\","/").split('/')[-1]
            # duplicate_images.append(image_pair[1].replace("\\", "/"))
            duplicate_images.append(temp1)
            print("---------------------")
    else:
        print("未找到重复图像。")
    print(duplicate_images)
    return render_template("result.html", duplicate_images=duplicate_images)


@app.route("/delete", methods=['DELETE'])
def delete():
    wait_dir = os.path.exists("./static/images")
    if wait_dir:
        for file in os.listdir("./static/images/"):
            os.remove("./static/images/" + file)
        return {"msg": '成功'}
    return {"msg": '找不到目录'}


if __name__ == '__main__':
    app.run(debug=True, threaded=False)

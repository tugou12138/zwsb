# coding=utf-8
from PIL import Image
import numpy as np
import glob
import os
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model

import tensorflow as tf
tf.config.run_functions_eagerly(True)

# 加载预训练的VGG16模型，并截断最后一层
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)
model.compile(run_eagerly=True)



def extract_features(image_paths):
    images = []
    for image_path in image_paths:
        # 读取图像
        image = Image.open(image_path)
        # 调整图像尺寸输入尺寸
        image = image.resize((224, 224))
        # 图像预处理
        image = preprocess_input(np.array(image))
        images.append(image)
    # 提取特征
    features = model.predict(np.array(images))
    return features



def calculate_similarity(features1, features2):
    # 计算余弦相似度
    similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    return similarity

import cv2
import exifread
import re

# GPS信息： {
# 'GPS GPSLatitude': '[32, 0, 597/20]',   纬度
# 'GPS GPSAltitude': '0', 高度
# 'GPS GPSLatitudeRef': 'N', 纬度参考
# 'GPS GPSAltitudeRef': '0', GPS高程参考
# 'GPS GPSProcessingMethod': '[67, 69, 76, 76, 73, 68]', GPS 处理方法
# 'GPS GPSLongitudeRef': 'E', GPS 经度基准
# 'GPS GPSTimeStamp': '[12, 52, 27]',  GPS时间戳
# 'GPS GPSLongitude': '[112, 4, 491/20]',
# 'GPS GPSDate': '2023:07:01', 'Image GPS Info': '931'} GPS 日期
# Date:

def find_gps_image(img_path):
    GPS = {}
    date = ''
    with open(img_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            # GPS纬度
            if 'GPS GPSTimeStamp' in tag:
                GPS[tag] = str(value)
            elif tag == 'EXIF原始日期时间':
                date = str(value)
        print("GPS信息：", GPS)
        print("Date:", date)

if __name__ == '__main__':
    # find_gps_image('static/images/1.jpg')
    cap = cv2.VideoCapture(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
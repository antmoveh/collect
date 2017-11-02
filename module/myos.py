import requests
import os
import time
import json


def file_name(file_dir):
    file_dict = {}
    for dirpath, dirnames, files in os.walk(file_dir):
        if len(files) == 0:
            continue
        for file in files:
            image_name = file.split(".")[0]
            file_dict[image_name] = os.path.join(dirpath, file)
    return file_dict


def file_post(url, file_dict):
    for f in file_dict:
        data = {"name": f}
        files = {'img': open(file_dict[f], 'rb')}
        response = requests.post(url, data=data, files=files)
        print(response.text)
        time.sleep(1)


if __name__ == '__main__':
    url = "http://192.168.40.131:9000/api/ubi"
    base_path = "E:\广州数字名城前瞻性研究\H5数据\历史建筑照片\第三批历史建筑图片"
    file_dict = file_name(base_path)
    print(len(file_dict))
    file_post(url, file_dict)
import os
import shutil
import xml.etree.ElementTree as ET

def is_xml_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() == '.xml'

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    class_name = root.find('object/name').text
    return class_name

# Example usage
data_folder = 'C:/Users/14869\Desktop\electronic_classification\hybrid'
output_folder = 'C:/Users/14869\Desktop\electronic_classification\class'

# 创建一个字典来存储类别对应的文件夹路径
class_folders = {}

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)

    # 筛查只读取图片文件和同名的XML文件
    if not is_xml_file(file_path):
        continue

    image_file = os.path.join(data_folder, f"{os.path.splitext(filename)[0]}.jpg")

    # 检查同名的图片文件是否存在
    if not os.path.isfile(image_file):
        continue

    # Parse XML file and extract class name
    class_name = parse_xml(file_path)

    # 检查该类别的文件夹是否已经创建，若未创建则创建该类别的文件夹
    if class_name not in class_folders:
        class_folder = os.path.join(output_folder, class_name)
        os.makedirs(class_folder, exist_ok=True)
        class_folders[class_name] = class_folder

    # 将图片移动到对应的文件夹
    shutil.copy(image_file, os.path.join(class_folders[class_name], os.path.basename(image_file)))

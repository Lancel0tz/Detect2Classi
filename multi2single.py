import os
import xml.etree.ElementTree as ET
from PIL import Image

def is_xml_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() == '.xml'

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    objects = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        objects.append((class_name, (xmin, ymin, xmax, ymax)))

    return objects

def crop_objects(image_file, bbox, output_folder, index):
    image = Image.open(image_file)
    cropped_image = image.crop(bbox)
    output_file = os.path.join(output_folder, f"{os.path.basename(image_file)[:-4]}_{index}.jpg")
    cropped_image.save(output_file)

    return cropped_image

def create_single_object_xml(original_xml_file, class_name, bbox, output_folder, index):
    tree = ET.parse(original_xml_file)
    root = tree.getroot()

    # Remove existing object elements
    for obj in root.findall('object'):
        root.remove(obj)

    # Add new object element with the current class name and bounding box
    obj_elem = ET.Element('object')
    name_elem = ET.Element('name')
    name_elem.text = class_name
    obj_elem.append(name_elem)

    bbox_elem = ET.Element('bndbox')
    xmin_elem = ET.Element('xmin')
    xmin_elem.text = str(bbox[0])
    ymin_elem = ET.Element('ymin')
    ymin_elem.text = str(bbox[1])
    xmax_elem = ET.Element('xmax')
    xmax_elem.text = str(bbox[2])
    ymax_elem = ET.Element('ymax')
    ymax_elem.text = str(bbox[3])
    bbox_elem.append(xmin_elem)
    bbox_elem.append(ymin_elem)
    bbox_elem.append(xmax_elem)
    bbox_elem.append(ymax_elem)
    obj_elem.append(bbox_elem)

    root.append(obj_elem)

    # Save the new XML file
    filename = os.path.splitext(os.path.basename(original_xml_file))[0]
    output_xml_file = os.path.join(output_folder, f"{filename}_{index}.xml")
    tree.write(output_xml_file)

# Example usage
data_folder = 'C:/Users/14869\Desktop\innerUAV'
output_folder = 'C:/Users/14869\Desktop/new'

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)

    # 筛查只读取图片文件和同名的XML文件
    if not is_xml_file(file_path):
        continue

    image_file = os.path.join(data_folder, f"{os.path.splitext(filename)[0]}.jpg")

    # 检查同名的图片文件是否存在
    if not os.path.isfile(image_file):
        continue

    # Parse XML file and extract objects (class name and bounding box)
    objects = parse_xml(file_path)

    # Crop objects from the image and save them to the output folder
    for i, (class_name, bbox) in enumerate(objects):
        cropped_image = crop_objects(image_file, bbox, output_folder, i)
        create_single_object_xml(file_path, class_name, bbox, output_folder, i)

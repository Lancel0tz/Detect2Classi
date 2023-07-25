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
data_folder = 'path to JPG with XML folder'   
output_folder = 'path to folder you want to store classification dataset'

class_folders = {}

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)

    # Screening only reads image files and XML files with the same name
    if not is_xml_file(file_path):
        continue

    image_file = os.path.join(data_folder, f"{os.path.splitext(filename)[0]}.jpg")

    # Check if an image file with the same name exists
    if not os.path.isfile(image_file):
        continue

    # Parse XML file and extract class name
    class_name = parse_xml(file_path)

    # Check whether the folder of this category has been created, if not, create a folder of this category
    if class_name not in class_folders:
        class_folder = os.path.join(output_folder, class_name)
        os.makedirs(class_folder, exist_ok=True)
        class_folders[class_name] = class_folder

    # Move the picture to the corresponding folder
    shutil.copy(image_file, os.path.join(class_folders[class_name], os.path.basename(image_file)))

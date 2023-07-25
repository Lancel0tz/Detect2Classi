# Detect2Classi
## Introduction
A tool can change the dataset of object detection to classification. 
Object detection dataset folders containing JPG and XML will be converted into folders containing JPG images 
corresponding to the object named and categorized by object name.
## Getting Started Guide
### Requirement
```
pip install os
pip install shutil
pip install xml
pip install PIL
```
### Instructions
If your dataset contains multiple objects in a single image so that their labels are all in one XML file, 
you must first use `multi2single.py` to break it into pieces, which will split your objects from the big images according to the position information in XML 
and separate it into a single object per XML. Because there must be a single target in the classified image. <br>
When your dataset is converted to per single object, use `detect2classi.py` to convert it into the final classification dataset form.



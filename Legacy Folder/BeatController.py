import os
from xml.etree import ElementTree
file_name ='project.xml'
full_file = os.path.abspath(os.path.join('XMLs', file_name))
print(full_file)
dom = ElementTree.parse(full_file)
print(dom)
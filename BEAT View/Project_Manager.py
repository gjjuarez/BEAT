import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

#might need to be rebuilt using minidom to format using toprettyxml

def all_projects(root):
    projects = root.findall('project/name')
    projectList = [] #the variable 'projectList' holds all the names of the projects found in the xml
    for child in projects:
        projectList.append(child.text) #put into a list not print
    #print(projectList) test line
#end of all_projects method

def add_project(projectName, projectDescription, projectPath, tree, file):
    projectelement = ET.Element("project") #add a new project
    root.append(projectelement)

    name = ET.SubElement(projectelement, "name")#add the name of the project as a child of project
    name.text = projectName

    description = ET.SubElement(projectelement, "description")#add the description of the project as a child of project
    description.text = projectDescription

    path = ET.SubElement(projectelement, "functionSource")#add the path of the projects binary file as a child of project
    path.text = projectPath

    tree.write(file)#write to the xml
#end of add_project method


#start of main
file = os.path.abspath(os.path.join('data', 'project.xml'))
tree = ET.parse(file)
root = tree.getroot()

#used to store the names of all projects
# method that puts all the projects into a list
all_projects(root)

# use these variables to write to the xml when adding a new project
projectName = 'project3'
projectDescription = 'project3 description'
projectPath = '[file path to the binary for project 3]'

#adds a new project to the xml (note it does not format the xml)
add_project(projectName, projectDescription, projectPath, tree, file)

all_projects(root)



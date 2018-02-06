# lib for xml tags
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ETIMPORT

def import_wireframe_xml(filename):
    parkinglots = []
    tree = ET.parse(filename)
    spaces = tree.getroot()
    # print('name of parkinglot: ',spaces.attrib['id'])
    parkinglotName=spaces.attrib['id']
    weather = spaces.attrib['weather']
    for space in spaces:
        # print( space.attrib['id'],space.attrib['occupied'])
        occupied = space.attrib['occupied'] == 'True'
        parkinglot = []
        for point in space.iter('point'):
            x = int(point.attrib['x'])
            y = int(point.attrib['y'])
            parkinglot.append([x, y])
        parkinglots.append([parkinglot,occupied])
    return parkinglots,weather

def get_crop_parmeter(parkinglot):
    xmin=99999999
    for x in parkinglot:
        if x[0]< xmin:
            xmin=x[0]
    ymin = 99999999
    for y in parkinglot:
        if y[1] < ymin:
            ymin = y[1]

    xmax = 0
    for x in parkinglot:
        if x[0] > xmax:
            xmax = x[0]
    ymax = 0
    for y in parkinglot:
        if y[1] > ymax:
            ymax = y[1]
    x=xmin
    y=ymin

    h=ymax-ymin
    w=xmax-xmin
    return x,y,h,w
import cv2
import numpy as np
import os
import csv
import datetime
import urllib.request
import socket
import traceback
import sys

# lib for xml tags
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ETIMPORT

def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def draw_parkinglot(path_to_current_frame, cv2, window_name, parkinglots, text,incompletespace=None):

        currentframe = cv2.imread(path_to_current_frame)
        text=''
        # add text
        fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        fontScale = 1
        thickness = 3
        color=(255,255,255)

        width, height = currentframe.shape[:2]
        xposition=int(width*0.1)
        yposition=int(height*0.7)
        cv2.putText(currentframe, text, (xposition, yposition), fontFace, 1,color)

        for parkinglot in parkinglots:

            pts = np.array(parkinglot, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(currentframe, [pts], True, (0, 255, 255))

        if incompletespace is not None:
            pts = np.array(incompletespace, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(currentframe, [pts], True, (0, 255, 255))

        cv2.imshow(window_name, currentframe)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def save_wireframe_xml(parkinglot_name,spaces,filepath):

    root = ET.Element("parking",id=parkinglot_name)

    for i in range(len(spaces)):
        space = spaces[i]
        spacexmltag = ET.SubElement(root, "space", id=str(i+1), occupied="bool")
        contour = ET.SubElement(spacexmltag, "contour")

        for point in space:
            point = ET.SubElement(contour, "point", x=str(point[0]), y=str(point[1]))

    xmlfile = open(filepath, "w")
    xmlfile.write(prettify(root))
    xmlfile.close()

def get_exsiting_space_drawn(filename):
    parkinglots = []
    print(filename)
    tree = ET.parse(filename)
    spaces = tree.getroot()
    # print('name of parkinglot: ',spaces.attrib['id'])

    for space in spaces:
        # print( space.attrib['id'],space.attrib['occupied'])
        parkinglot = []
        for point in space.iter('point'):
            x = int(point.attrib['x'])
            y = int(point.attrib['y'])
            parkinglot.append([x, y])
        parkinglots.append(parkinglot)

    return parkinglots

def get_listOfparkings(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders

def get_listOfFolders(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders

def get_listOfVideos(root):
    subfolders = [f.path for f in os.scandir(root) if '.mp4' in f.name]
    return subfolders

def get_listOfPictures(root):
    subfolders = [f.path for f in os.scandir(root) if '.jpg' in f.name]
    return subfolders

def format_string(unformatedString):
    if unformatedString.find('Ś') != -1:  # found
        formatString = unformatedString.replace("Ś", "S")
        unformatedString = formatString

    if unformatedString.find('ś') != -1:  # found
        formatString = unformatedString.replace("ś", "s")
        unformatedString = formatString

    if unformatedString.find('é') != -1:  # found
        formatString = unformatedString.replace("é", "e")
        unformatedString = formatString

    if unformatedString.find('ě') != -1:  # found
        formatString = unformatedString.replace("ě", "e")
        unformatedString = formatString

    if unformatedString.find('š') != -1:  # found
        formatString = unformatedString.replace("š", "s")
        unformatedString = formatString

    if unformatedString.find('á') != -1:  # found
        formatString = unformatedString.replace("á", "a")
        unformatedString = formatString

    if unformatedString.find('ž') != -1:  # found
        formatString = unformatedString.replace("ž", "z")
        unformatedString = formatString

    if unformatedString.find('a') != -1:  # found
        formatString = unformatedString.replace("å", "a")
        unformatedString = formatString

    if unformatedString.find('í') != -1:  # found
        formatString = unformatedString.replace("í", "i")
        unformatedString = formatString

    if unformatedString.find('ä') != -1:  # found
        formatString = unformatedString.replace("ä", "a")
        unformatedString = formatString

    if unformatedString.find('ð') != -1:  # found
        formatString = unformatedString.replace("ð", "o")
        unformatedString = formatString

    if unformatedString.find('ł') != -1:  # found
        formatString = unformatedString.replace("ł", "l")
        unformatedString = formatString

    if unformatedString.find('å') != -1:  # found
        formatString = unformatedString.replace("å", "l")
        unformatedString = formatString

    if unformatedString.find('ș') != -1:  # found
        formatString = unformatedString.replace("ș", "s")
        unformatedString = formatString

    if unformatedString.find('ä') != -1:  # found
        formatString = unformatedString.replace("ä", "a")
        unformatedString = formatString


    if unformatedString.find('å') != -1:  # found
        formatString = unformatedString.replace("å", "a")
        unformatedString = formatString

    if unformatedString.find('ě') != -1:  # found
        formatString = unformatedString.replace("ě", "e")
        unformatedString = formatString

    if unformatedString.find('ü') != -1:  # found
        formatString = unformatedString.replace("ü", "u")
        unformatedString = formatString

    if unformatedString.find('ß') != -1:  # found
        formatString = unformatedString.replace("ß", "b")
        unformatedString = formatString

    if unformatedString.find('ś') != -1:  # found
        formatString = unformatedString.replace("ś", "s")
        unformatedString = formatString

    if unformatedString.find('á') != -1:  # found
        formatString = unformatedString.replace("á", "a")
        unformatedString = formatString

    if unformatedString.find('í') != -1:  # found
        formatString = unformatedString.replace("í", "i")
        unformatedString = formatString

    if unformatedString.find('š') != -1:  # found
        formatString = unformatedString.replace("š", "s")

    return formatString
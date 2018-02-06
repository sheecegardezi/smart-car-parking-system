# lib for xml tags
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ETIMPORT

import cv2
import datetime
import numpy as np

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def extract_frames_from_video(filename,outputfolder,framerate=40):
    videoStream = cv2.VideoCapture(filename)
    totalFrames = int(videoStream.get(cv2.CAP_PROP_FRAME_COUNT))

    for x in range(0, totalFrames):
        ret, frame = videoStream.read()

        if x%framerate == 0:

            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')

            # save the current frame
            path=outputfolder+timestamp+'_'+str(x)+'.jpg'
            cv2.imwrite(path, frame)

    videoStream.release()

def import_wireframe_xml(filename):
    parkinglots = []
    tree = ET.parse(filename)
    spaces = tree.getroot()
    # print('name of parkinglot: ',spaces.attrib['id'])
    parkinglotName=spaces.attrib['id']
    # weather = spaces.attrib['weather']
    for space in spaces:
        # print( space.attrib['id'],space.attrib['occupied'])

        occupied = 0
        parkinglot = []
        for point in space.iter('point'):
            x = int(point.attrib['x'])
            y = int(point.attrib['y'])
            parkinglot.append([x, y])
        parkinglots.append([parkinglot,occupied])
    return parkinglots

def save_wireframe_xml(parkinglot_name,spaces,filepath):

    root = ET.Element("parking",id=parkinglot_name)

    for i in range(len(spaces)):
        space = spaces[i][0]
        spacexmltag = ET.SubElement(root, "space", id=str(i+1), occupied=str( spaces[i][1]))
        contour = ET.SubElement(spacexmltag, "contour")

        for point in space:
            point = ET.SubElement(contour, "point", x=str(point[0]), y=str(point[1]))

    xmlfile = open(filepath, "w")
    xmlfile.write(prettify(root))
    xmlfile.close()

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


def draw_parkinglot(path_to_current_frame, cv2, window_name, parkinglots):

        currentframe = cv2.imread(path_to_current_frame)

        for parkinglot in parkinglots:

            pts = np.array(parkinglot[0], np.int32)
            pts = pts.reshape((-1, 1, 2))
            print(parkinglot[1])
            if parkinglot[1] == True:
                cv2.polylines(currentframe, [pts], True, (0, 255, 255))
            else:
                cv2.polylines(currentframe, [pts], True, (255, 0, 255))

        cv2.imshow(window_name, currentframe)
        cv2.imwrite(path_to_current_frame,currentframe)


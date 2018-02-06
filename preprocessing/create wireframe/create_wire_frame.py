import logging
import os

from utils import *
from constants import *

parking_lot=[]
parking_lots=[]
drawing=False
currentframe='currentframe.jpg'
windowName='window'
# logging.basicConfig(filename='info.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

selectedSpace=-1


def draw_parking_spaces(event, x, y, flags, param):
    # grab references to the global variables
    global ix, iy, drawing, parking_lot, parking_lots,filled, drawing,selectedSpace
    ix, iy = x, y

    if event == cv2.EVENT_RBUTTONDOWN and not drawing:
        drawing=True
        parking_lot = []

        text="right click on four corners to draw a rectangle"
        draw_parkinglot(currentframe, cv2, windowName, parking_lots,text)
        logging.info('generate new rectangle')

    if event == cv2.EVENT_LBUTTONDOWN and drawing and len(parking_lot)<4:
        parking_lot.append([ix,iy])
        text="right click on "+ str(4-len(parking_lot))+" more corners to draw a rectangle"
        draw_parkinglot(currentframe, cv2, windowName, parking_lots,text,parking_lot)
        logging.info('new point added')

    if len(parking_lot)==4:
        parking_lots.append(parking_lot)
        parking_lot = []
        drawing=False
        logging.info('rectangle completed')
        text="left click to start drawing new rectangle"
        draw_parkinglot(currentframe, cv2, windowName, parking_lots,text)

    if not drawing and event == cv2.EVENT_LBUTTONDOWN:
        for i in range(len(parking_lots)):
            space=parking_lots[i]
            if point_inside_polygon(ix, iy ,space):
                selectedSpace=i
                logging.info('space selected at index '+str(selectedSpace))

cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName,draw_parking_spaces)

# root=os.path.join( dataPath, 'parkinglots' )
# ubuntu
# root=dircetoryPath = '/Users/sheeced/Desktop/csproj17s2/artefacts/data/parkinglots'
# windows

root=dircetoryPath = 'C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\parkinglots\\SSRLot'


dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]


for dir in dirlist:
    if dir not in ignoreParkinglots:
        # root = os.path.join(dataPath, 'parkinglots')
        root = os.path.join(dircetoryPath, dir)

        filelist = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and f.__contains__('.jpg')]
        nextParking=False

        if os.path.isfile(  os.path.join(root, 'wireframe.xml')) :
            parking_lots= get_exsiting_space_drawn( os.path.join(root, 'wireframe.xml'))
        for img in filelist:
            img=root+'/'+img
            logging.info('image loaded: ' + img)
            frame=cv2.imread(img)

            nextFrame = False

            if(frame is not None):
                # save the current frame
                cv2.imwrite(currentframe, frame)
                text = "left click to strat drawing new rectangle"
                draw_parkinglot(currentframe, cv2, windowName, parking_lots, text)

            else:
                nextFrame = True


            while not nextFrame:
                ch = cv2.waitKey()
                # Escape
                if ch == 27:# or cv2.getWindowProperty(windowName, 0) <= 0:
                    cv2.destroyAllWindows()
                    break

                #enter
                if ch==13:
                    logging.info('image deleted')
                    os.remove(img)
                    nextFrame = True

                # Space
                if ch == 32:
                    logging.info("get a new sample image")
                    nextFrame = True
                # backspace
                if ch == 8 or ch == 127:

                    if len(parking_lot) >= 1:
                        logging.info('last drawn space codinate deleted')
                        parking_lot = parking_lot[:-1]
                        text = "right click on " + str(4 - len(parking_lot)) + " more corners to draw a rectangle"
                        draw_parkinglot(currentframe, cv2, windowName, parking_lots, text,parking_lot)

                    elif len(parking_lots) >= 1:
                        logging.info('last drawn space deleted')
                        parking_lots = parking_lots[:-1]
                        text = "left click to start drawing new rectangle"
                        draw_parkinglot(currentframe, cv2, windowName, parking_lots, text)
                #d-key:
                if ch== 100:
                    logging.info('d key working')
                    if 0 <= selectedSpace < len(parking_lots):
                        del parking_lots[selectedSpace]
                        logging.info('space selected at index '+str(selectedSpace)+' deleted')
                        text = "left click to strat drawing new rectangle"
                        draw_parkinglot(currentframe, cv2, windowName, parking_lots, text)

                #n-key
                if ch == 110:
                    logging.info("drawing complete for current parking lot move to next")
                    nextParking=True
                    break

            if nextParking == True:
                break

        if (frame is not None):
            logging.info("wire frame saved")
            filepath = os.path.dirname(img)
            filepath=os.path.join(root, 'wireframe.xml')

            # sourse of conflict the parkinglot name is extracted from the floder conating the images
            save_wireframe_xml(dir, parking_lots, filepath)
        parking_lots = []



cv2.destroyAllWindows()
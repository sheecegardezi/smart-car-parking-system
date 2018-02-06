import os
from shutil import copyfile
import ntpath
from utils import *
import cv2
import sys

root='C:\\Users\\U5752631\\Desktop\\SSRLot'
output='C:\\Users\\U5752631\\Desktop\\SSRLotSegmented'
pathToCameras= [os.path.join(root, f.name) for f in os.scandir(root) if f.is_dir()]

# [f.name for f in os.scandir(root) if f.is_dir()]
#files=[f.path for f in os.scandir(pathTofiles) if '.jpg' in f.name]
# copyfile(src, des)
# os.path.join(root, 'test','Occupied',ntpath.basename(file))
cameras = [f.name for f in os.scandir(root) if f.is_dir()]

for camera in cameras:
    files = [f.path for f in os.scandir(os.path.join(root, camera) ) if '.xml' in f.name and  'wireframe' not in f.name]
    # print(len(files))
    for file in files:
        # print(file)

        filename=ntpath.basename(file).split('.')[0]
        parkinglot,date,time=filename.split('_')
        parkingspots, weather=import_wireframe_xml(file)
        imgFilePath=file.split('.')[0]+'.jpg'
        img = cv2.imread(imgFilePath)
        if img is None:
            print(imgFilePath)
            continue
        print(imgFilePath)

        # windowName = 'main'
        # cv2.namedWindow(windowName)
        #
        # cv2.imshow(windowName, img)
        # cv2.waitKey(0)

        for i in range(len(parkingspots)):
            # print(parkingspots[i])

            x, y, h, w = get_crop_parmeter(parkingspots[i][0])
            occupancy=''

            if parkingspots[i][1] == False:
                occupancy='Empty'
            else:
                occupancy = 'Occupied'

            try:
                crop_img = img[y: y + h, x: x + w]
            except TypeError:
                print(file)
                print(parkingspots[i])
                print(x, y, h, w)
                print(type(img))


            directory=os.path.join(output,camera, weather ,date,occupancy)
            if not os.path.exists(directory):
                os.makedirs(directory)

            filepath=os.path.join(directory,date+'_'+time+'_'+str(i)+'.jpg')
            cv2.imwrite(filepath, crop_img)
        #     windowName = 'window' + str(i)
        #     cv2.namedWindow(windowName)
        #     cv2.imshow(windowName, crop_img)
        #     cv2.waitKey(0)
        #
        # cv2.destroyAllWindows()

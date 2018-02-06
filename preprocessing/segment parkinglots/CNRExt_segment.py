import os
from shutil import copyfile
import ntpath
from utils import *
import cv2
import sys

labelpath='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\CNR-EXT\\LABELS\\all.txt'
imagespath='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\CNR-EXT\\PATCHES'

output='C:\\Users\\U5752631\\Desktop\\CNRParkSegmented'

totalLine = sum(1 for line in open(labelpath))

with open(labelpath) as infile:
    counter=0
    for line in infile:
        counter=counter+1
        print(counter,totalLine)
        weather=line.split('/')[0]
        date=line.split('/')[1]
        occupancy=line.split(' ')[1].strip()
        camera=line.split('/')[2]

        if occupancy =='1':
            occupancy='Occupied'
        else:
            occupancy='Empty'

        directory = os.path.join(output, camera, weather,date,occupancy)
        if not os.path.exists(directory):
            os.makedirs(directory)
        basefilename=ntpath.basename(line.split(' ')[0])
        time=basefilename.split('_')[2].replace('.','-')+'-00'
        id=basefilename.split('_')[4]
        des = os.path.join(directory, date + '_' + time + '_' + id + '.jpg')
        src= os.path.join(imagespath, line.split(' ')[0])
        copyfile(src, des)

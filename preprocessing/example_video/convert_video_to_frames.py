import datetime
import ntpath
import cv2
import os
from utils import *
import pickle

def segment_images_into_parkingspots(root,outputfolder):
    files = [f.path for f in os.scandir(root) if '.xml' in f.name and 'wireframe' not in f.name]
    print(len(files))
    for file in files:
        print(file)
        filename = ntpath.basename(file).split('.')[0]
        parkinglot='PUCPR'
        date = filename.split('_')[0]
        time= filename.split('_')[1:]
        time=time[0]+'-'+time[1]+'-'+time[2]
        parkingspots = import_wireframe_xml(file)
        imgFilePath = file.split('.')[0] + '.jpg'
        img = cv2.imread(imgFilePath)

        for i in range(len(parkingspots)):
            x, y, h, w = get_crop_parmeter(parkingspots[i][0])
            crop_img = img[y: y + h, x: x + w]
            cv2.imwrite(outputfolder + date + '_' + time + '#' + str(i) + '.jpg', crop_img)

def get_labels_for_segments():
    with open('C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\preprocessing\\example_video\\predictions.pickel',
              'rb') as handle:
        dic = pickle.load(handle)


    files = [f.path for f in os.scandir(root) if '.xml' in f.name and 'wireframe' not in f.name]

    for file in files:
        filename = ntpath.basename(file).split('.')[0]
        parkinglot = 'PUCPR'
        date = filename.split('_')[0]
        time = filename.split('_')[1:]
        time = time[0] + '-' + time[1] + '-' + time[2]
        parkingspots = import_wireframe_xml(file)
        imgFilePath = file.split('.')[0] + '.jpg'

        for i in range(len(parkingspots)):
            cropedImageName=date + '_' + time + '#' + str(i) + '.jpg'
            if dic[cropedImageName]==1:
                parkingspots[i][1]=True


        save_wireframe_xml(parkinglot, parkingspots, file)
        windowName = 'window'
        draw_parkinglot(imgFilePath, cv2, windowName, parkingspots)

        while True:
            ch = cv2.waitKey()
            if ch == 27:  # or cv2.getWindowProperty(windowName, 0) <= 0:
                cv2.destroyAllWindows()
                break
def create_video():
    files = [f.path for f in os.scandir(root) if '.jpg' in f.name]

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\preprocessing\\example_video\\out_video.avi', fourcc, 1, (1280, 720))

    c = cv2.VideoCapture('in_video.avi')

    for file in files:
        img=cv2.imread(file)

        out.write(img)  # write frame to the output video

    out.release()
    cv2.destroyAllWindows()
    c.release()


if __name__ == "__main__":

    root='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\preprocessing\\example_video\\video\\PUCPR'
    outputfolder='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\preprocessing\\example_video\\img\\'



    segment_images_into_parkingspots()
    print('Images segmented')
    get_labels_for_segments(root, outputfolder)
    print('Segmented Images Labeled')
    create_video()
    print('Video Made')
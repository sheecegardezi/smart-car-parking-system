import os
from shutil import copyfile
import ntpath
from utils import *

root='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\PKLot\\PKLotSegmented'
pathToCameras= [os.path.join(root, f.name) for f in os.scandir(root) if f.is_dir()]


typesOfWeather=['Cloudy','Rainy','Sunny']

countEmpty=0
countOcupid=0

train=[31420,29825]
val=[4488,4060]
test=[8978,8522]

root='PKlot'
for camera in pathToCameras:

    for weather in typesOfWeather:
       pathTodays = os.path.join(camera, weather)
       daysSubdirectory=[os.path.join(pathTodays, f.name) for f in os.scandir(pathTodays) if f.is_dir()]

       for day in daysSubdirectory:
           catagoriesSubdirectory = [f.name for f in os.scandir(day) if f.is_dir()]

           for catagory in catagoriesSubdirectory:
               if catagory =='Empty':
                   pathTofiles=os.path.join(day, catagory)
                   files=[f.path for f in os.scandir(pathTofiles) if '.jpg' in f.name]
                   countEmpty=countEmpty+len(files)

                   if train[0]>0:
                       train[0]=train[0]-len(files)
                       for file in files:
                            # print(file)
                            # print(ntpath.basename(file))
                            copyfile(file, os.path.join(root, 'train','Empty',ntpath.basename(file)))
                   elif val[0]>0:
                       val[0]=val[0]-len(files)
                       for file in files:
                            copyfile(file, os.path.join(root, 'val','Empty',ntpath.basename(file)))
                   else:
                       for file in files:
                            copyfile(file, os.path.join(root, 'test','Empty',ntpath.basename(file)))
               elif catagory == 'Occupied':
                   pathTofiles=os.path.join(day, catagory)
                   files=[f.path for f in os.scandir(pathTofiles) if '.jpg' in f.name]
                   countOcupid = countOcupid + len(files)

                   if train[1]>0:
                       train[1]=train[1]-len(files)
                       for file in files:
                            copyfile(file, os.path.join(root, 'train','Occupied',ntpath.basename(file)))
                   elif val[1]>0:
                       val[1]=val[1]-len(files)
                       for file in files:
                            copyfile(file, os.path.join(root, 'val','Occupied',ntpath.basename(file)))
                   else:
                       for file in files:
                            copyfile(file, os.path.join(root, 'test','Occupied',ntpath.basename(file)))
    print(countEmpty)
    print(countOcupid)


def get_listOfFolders(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders

def get_listOfVideos(root):
    subfolders = [f.path for f in os.scandir(root) if '.mp4' in f.name]
    return subfolders

train = 0.7
valid = 0.1
test = 0.2
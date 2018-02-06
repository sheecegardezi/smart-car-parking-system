import os
from shutil import copyfile
import ntpath

output='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\machinelearning'
root='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\parkinglotsSegmented'

parkinglots= [os.path.join(root, f.name) for f in os.scandir(root) if f.is_dir()]


TotalEmptyExamples=0
TotalOccupiedExamples=0

weathersets=['Sunny','Rainy']

countFiles={}

for weatherset in weathersets:
    print(weatherset)
    for parkinglot in parkinglots:
        print(parkinglot)
        cameras = [os.path.join(parkinglot, f.name) for f in os.scandir(parkinglot) if f.is_dir()]

        for camera in cameras:

            weathers = [os.path.join(camera, f.name) for f in os.scandir(camera) if f.is_dir()]

            for weather in weathers:

                days = [os.path.join(weather, f.name) for f in os.scandir(weather) if f.is_dir()]

                for day in days:

                    catagories = [os.path.join(day, f.name) for f in os.scandir(day) if f.is_dir()]

                    for catagory in catagories:

                        if weather.split('\\')[-1] == weatherset:

                            files = [f.path for f in os.scandir(catagory) if '.jpg' in f.name]

                            for file in files:

                                desfilename = os.path.join(output, weatherset, 'train', catagory.split('\\')[-1],ntpath.basename(file))
                                copyfile(file, desfilename)

                        else:
                            files = [f.path for f in os.scandir(catagory) if '.jpg' in f.name]

                            for file in files:
                                desfilename = os.path.join(output, weatherset, 'test', catagory.split('\\')[-1], ntpath.basename(file))
                                copyfile(file, desfilename)

#shift 10% of files in train ramdomly to valid
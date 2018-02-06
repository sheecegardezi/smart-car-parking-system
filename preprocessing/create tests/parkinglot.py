import os
from shutil import copyfile
import ntpath

output='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\machinelearning'
root='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data\\datasets\\parkinglotsSegmented'
parkinglots= [os.path.join(root, f.name) for f in os.scandir(root) if f.is_dir()]

trainset = 0.7
validset = 0.1
testset = 0.2

TotalEmptyExamples=0
TotalOccupiedExamples=0

countFiles={}
for parkinglot in parkinglots:

    cameras = [os.path.join(parkinglot, f.name) for f in os.scandir(parkinglot) if f.is_dir()]

    for camera in cameras:

        weathers = [os.path.join(camera, f.name) for f in os.scandir(camera) if f.is_dir()]

        for weather in weathers:

            days = [os.path.join(weather, f.name) for f in os.scandir(weather) if f.is_dir()]

            for day in days:

                catagories = [os.path.join(day, f.name) for f in os.scandir(day) if f.is_dir()]

                for catagory in catagories:

                    if catagory.split('\\')[-1] == 'Empty':
                        files = [f.path for f in os.scandir(catagory) if '.jpg' in f.name]
                        TotalEmptyExamples=TotalEmptyExamples+len(files)
                    elif catagory.split('\\')[-1] == 'Occupied':
                        files = [f.path for f in os.scandir(catagory) if '.jpg' in f.name]
                        TotalOccupiedExamples=TotalOccupiedExamples+len(files)


    train = [int(TotalEmptyExamples * trainset), int(TotalOccupiedExamples * trainset)]
    val = [int(TotalEmptyExamples * validset), int(TotalOccupiedExamples * validset)]
    test = [int(TotalEmptyExamples * testset), int(TotalOccupiedExamples * testset)]

    countFiles[parkinglot]={'train':train,'val':val,'test':test}






for parkinglot in parkinglots:

    cameras = [os.path.join(parkinglot, f.name) for f in os.scandir(parkinglot) if f.is_dir()]

    for camera in cameras:

        weathers = [os.path.join(camera, f.name) for f in os.scandir(camera) if f.is_dir()]

        for weather in weathers:

           days = [os.path.join(weather, f.name) for f in os.scandir(weather) if f.is_dir()]

           for day in days:

               catagories = [os.path.join(day, f.name) for f in os.scandir(day) if f.is_dir()]

               for catagory in catagories:

                   if catagory.split('\\')[-1] == 'Empty':

                       files=[f.path for f in os.scandir(catagory) if '.jpg' in f.name]

                       if countFiles[parkinglot]['train'][0]>0:
                           countFiles[parkinglot]['train'][0]=countFiles[parkinglot]['train'][0]-len(files)
                           for file in files:
                               directory=os.path.join(output,ntpath.basename(parkinglot), 'train','Empty')

                               filename=    ntpath.basename(file)
                               copyfile(file, os.path.join(directory,filename))


                       elif countFiles[parkinglot]['val'][0]>0:
                           countFiles[parkinglot]['val'][0]=countFiles[parkinglot]['val'][0]-len(files)
                           for file in files:
                               directory = os.path.join(output, ntpath.basename(parkinglot), 'val', 'Empty')

                               filename = ntpath.basename(file)
                               copyfile(file, os.path.join(directory, filename))

                       else:
                           for file in files:
                               directory = os.path.join(output, ntpath.basename(parkinglot), 'test', 'Empty')

                               filename = ntpath.basename(file)
                               copyfile(file, os.path.join(directory, filename))

                   elif catagory.split('\\')[-1] == 'Occupied':

                       files = [f.path for f in os.scandir(catagory) if '.jpg' in f.name]

                       if countFiles[parkinglot]['train'][1]>0:
                           countFiles[parkinglot]['train'][1]=countFiles[parkinglot]['train'][1]-len(files)
                           for file in files:
                               directory = os.path.join(output, ntpath.basename(parkinglot), 'train', 'Occupied')

                               filename = ntpath.basename(file)
                               copyfile(file, os.path.join(directory, filename))

                       elif countFiles[parkinglot]['val'][1]>0:
                           countFiles[parkinglot]['val'][1]=countFiles[parkinglot]['val'][1]-len(files)
                           for file in files:
                               directory = os.path.join(output, ntpath.basename(parkinglot), 'val', 'Occupied')

                               filename = ntpath.basename(file)
                               copyfile(file, os.path.join(directory, filename))
                       else:
                           for file in files:
                               directory = os.path.join(output, ntpath.basename(parkinglot), 'test', 'Occupied')

                               filename = ntpath.basename(file)
                               copyfile(file, os.path.join(directory, filename))
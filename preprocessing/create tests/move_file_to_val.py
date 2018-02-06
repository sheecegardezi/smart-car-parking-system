#shift 10% of files in train ramdomly to valid

import os
import ntpath
import shutil
from random import randint

#for empty slots move 1

root = 'C:/Users/U5752631/Desktop/csproj17s2/artefacts/data/machinelearning/Sunny/'

catagories=['Empty','Occupied']
for catagory in catagories:
    files =  [os.path.join(root,'train',catagory, f.name) for f in os.scandir(os.path.join(root,'train',catagory)) if '.jpg' in f.name]

    noOfValFiles=int(len(files)*0.2)
    # noOfTestFiles=int(len(files)*0.1)


    for i in range(noOfValFiles):
        file=files.pop(randint(0, len(files)-1))
        shutil.move(file, os.path.join(root,'valid',catagory,ntpath.basename(file)))


    # for i in range(noOfTestFiles):
    #     file = files.pop(randint(0, len(files)-1))
    #     shutil.move(file, os.path.join(root, 'test', catagory, ntpath.basename(file)))


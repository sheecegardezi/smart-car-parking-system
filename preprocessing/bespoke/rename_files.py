import os
import unicodedata
import csv
import re



def rename_folders(dircetoryPath):
    subfolders = [f.name for f in os.scandir(dircetoryPath) if f.is_dir()]

    for foldername in subfolders:
        oldFolderPath=os.path.join(dircetoryPath, foldername)
        foldername=unicodedata.normalize('NFKD', foldername).encode('ascii', 'ignore')
        foldername=foldername.decode('unicode_escape')
        newFolderPath=os.path.join(dircetoryPath, foldername)
        os.rename(oldFolderPath, newFolderPath)

def rename_files(dircetoryPath):
    #rename the files in each folder
    for foldername in os.scandir(dircetoryPath):
        if foldername.is_dir():
            for file in os.scandir(foldername):

                oldFilePath = file.path

                filename = unicodedata.normalize('NFKD', file.name).encode('ascii', 'ignore')
                filename = filename.decode('unicode_escape')
                newFilePath=os.path.join(dircetoryPath, foldername,filename)

                os.rename(oldFilePath, newFilePath)

#edit name in wireframe file
def edit_metadatafile(dircetoryPath):
    for foldername in os.scandir(dircetoryPath):

        if foldername.is_dir():
            metadatafilepath=os.path.join(dircetoryPath,foldername, 'meta_data.csv')
            if os.path.isfile(metadatafilepath):

                # read csv file
                with open(metadatafilepath, 'r', encoding="utf8") as csvFile:
                    reader = csv.DictReader(csvFile)
                    for record in reader:
                        # remove all non ascii charactars
                        place = unicodedata.normalize('NFKD', record['place']).encode('ascii', 'ignore').decode(
                            'unicode_escape')
                        # replace all non alpha chacters with -
                        record['place'] = re.sub('[^0-9a-zA-Z]+', '-', place)

                # write updated data to csv file
                with open(metadatafilepath, 'w') as f:
                    fieldnames = ['place', 'longitude', 'latitude', 'offset', 'url', 'details']
                    writer = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(record)


if __name__ == '__main__':
    # rename the folders
    dircetoryPath = 'C:\\Users\\U5752631\\Desktop\\data'

    rename_folders(dircetoryPath)
    rename_files(dircetoryPath)
    edit_metadatafile(dircetoryPath)

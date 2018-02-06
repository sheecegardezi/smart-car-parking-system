import os


def replace(fpath, old_str, new_str):
    for path, subdirs, files in os.walk(fpath):
        for name in files:
            if(old_str in name):
                os.rename(os.path.join(path,name), os.path.join(path, name.replace(old_str,new_str)))



# root='C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\data'
# replace(root, '.jpg.jpg','.jpg')

datasets=['CNRExtSegmented','PKLotSegmented','SSRLotSegmented']
print(datasets[0][:-9])
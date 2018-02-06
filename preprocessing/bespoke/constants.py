import os

#define operating system level constants

#define paths
dir_path = os.path.dirname(os.path.realpath(__file__))
dataPath=dir_path.split('\preprocessing')[0]+'\data'

ignoreParkinglots=['BIAR-Akureyri-Flight-School','30-Years-Of-Great-Victory-Square','Borgarfjarðar-College','Hauptplatz-from-Stadt-Cafe','Hiruzen-Bear-Valley-Ski-Area','Libra-&-Långnäsvägen','Lotus-Square','Monino-Central Airforce-Museum','Nakabiraki-Car-Park','Place-Centrale-Monthey']

#define the parking lots to use
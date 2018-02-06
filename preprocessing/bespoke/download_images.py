import csv
import os
import datetime
import socket
import urllib
import traceback
import sys

def get_metadata(filename):

    with open( filename, 'r' ) as csvFile:
        reader = csv.DictReader(csvFile)
        for record in reader:
            place=record[ 'place' ]
            longitude=float(record[ 'longitude' ])
            latitude=float(record[ 'latitude' ])
            offset= int(record[ 'offset' ])
            url=record['url']

    return place,longitude,latitude,offset,url


def get_listOfparkings(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders


def get_timestamp(offset):

    adjusted_time = datetime.datetime.now() + datetime.timedelta(hours=offset, minutes=0)
    timestamp = adjusted_time.strftime('%Y-%m-%d_%H-%M-%S')

    return timestamp

def save_image(url,filepath):
    socket.setdefaulttimeout(10)
    try:
        urllib.request.urlretrieve(url, filepath)
        #open saved image
        resize_image(filepath)
    except socket.timeout:
        print('caught a timeout')
    except urllib.error.HTTPError:
        print('caught a HTTPError')
    except Exception as e:
        print(traceback.format_exception(*sys.exc_info()))

def resize_image(filepath):
    #open image
    #check the lengths and check if the image is to be enlarged or smalled
    print('')
    
def main():
    root = '/home/sheece/Desktop/capture_live_stream/data/'

    parkingnames = get_listOfparkings(root)

    for parkingname in parkingnames:
        print("caputing: " + parkingname)
        metadata_filename = '/home/sheece/Desktop/capture_live_stream/data/' + parkingname + '/meta_data.csv'
        place, longitude, latitude, offset, url = get_metadata(metadata_filename)
        timestamp = get_timestamp(offset)
        image_filepath = '/home/sheece/Desktop/capture_live_stream/data/' + parkingname + '/' + parkingname + '_' + timestamp + '.jpg'
        save_image(url, image_filepath)

if __name__ == '__main__':
    main()
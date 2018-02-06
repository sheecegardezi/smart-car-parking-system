import cv2
import numpy as np
import os
import csv
import datetime
import urllib.request
import socket
import traceback
import sys



def get_listOfparkings(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders

def get_listOfFolders(root):
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    return subfolders

def get_listOfVideos(root):
    subfolders = [f.path for f in os.scandir(root) if '.mp4' in f.name]
    return subfolders

def get_listOfPictures(root):
    subfolders = [f.path for f in os.scandir(root) if '.jpg' in f.name]
    return subfolders

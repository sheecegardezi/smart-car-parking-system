#### Create Wire Frame ####

python create_wire_frame.py

Features:

 * draw rectangles on a picture
 * press space key to go to new picture of the same parking lot
 * press n key to save generate xml of the rectangles drawn and move to next parking lot
 * press enter to delete the current picture
 * press esc key to close the application without saving progress of current paring lot
 * right click to start drawing the rectangle
 * while not dawning click in any rectangle to select it and delete it using d key
 * if a wire frame already exists it will load it automatically


Run:
 * open and edit the value for varable root, it expects the path to the folder of a dataset of parking lots 
 * parkinglots->parkinglot1,parkinglot2.......
 * it expects that each subfolder will contain multiple pictues of same parking lot
 * this tool is used to create a four dimentional shape identifing a parkinlot
 * if you press 'n' key it will save the wireframe.xml file (this file is used by the labeling tool) and move to the next parking lot.
 * if you press space it will move to the next picture of the same parking lot
 * if you click in a drawn shape and press 'd' key it will delete that shape
 * if you press backspace it will delete the last drawn shape

#### Create Tests ####

* This collection of scriptes are used to create the test cases. they used the data from datasets of the file structure:
datasets
* * parkinglot
* * * empty
* * * * 1.jpg
* * * * 2.jpg
* * * occupied
* * * * 5.jpg
* * * * 3.jpg

and dived the data usind defined rules into
* test-case
* * train
* * * empty
* * * * 1.jpg
* * * * 2.jpg
* * * occupied
* * * * 5.jpg
* * * * 3.jpg
* * valid
* * * empty
* * * * 1.jpg
* * * * 2.jpg
* * * occupied
* * * * 5.jpg
* * * * 3.jpg
* * * test
* * * empty
* * * * 1.jpg
* * * * 2.jpg
* * * occupied
* * * * 5.jpg
* * * * 3.jpg

this data is used by the deep learning notebooks to evaluate the preformance of algorithums

#### Create Training and Test datasets ####

These scripts use the output of label data software, to segment each into parkingspots(each indevidual parking space) into a standard file structure. for weach of the databases PKLot, SSRLot and CNRPark-Ext this standard file strucure was created.

* parkinglotsSegmented
* * parkinglot-1-LotSegmented
* * * camera-1
* * * * weather_condition
* * * * * date
* * * * * * empty 
* * * * * * occupied
* * * camera-2
* * * * weather_condition
* * * * * date
* * * * * * empty 
* * * * * * occupied
* * parkinglot-2-LotSegmented
* * * camera-1
* * * * weather_condition
* * * * * date
* * * * * * empty 
* * * * * * occupied
* * * camera-2
* * * * weather_condition
* * * * * date
* * * * * * empty 
* * * * * * occupied

#### Downlaod Live Images ####

* This script requires a path to a folder that contains cameras as subfolder. Tt expects that each folder of the camera will contain a file meta_data.csv which will have the following details:
* place,longitude,latitude,offset,url,details
* This script uses url to extract a picture and save it into that folder, it also use the offset to adjust the time of the local clock to save the time according to the correct time zone. it also uses the place varable to save the name of the file.

#### Example Video ####

* This script reverse the entire processes it takes in a video parse it into frames.
* Wireframe tool is use to create a wire frame
* Then each picture is segmented
* It is given to a NN to generate predictions
* Its gets back a python dictonary:{"name of picture#id":label}
* It uses this dictonary to correctly identify the "unsegmented image" and then use id to identify the parking space and then use the label to draw green or red rectangle over it, 
* These images are saved
* Then another script merges these images into a avi video.

#### Label Images ####

This is a GUI used to label images.
To run use: 
python label_images.py

#### Segment Parkinglots ####

These scripts are used to segment PKLot and CNRPark-Ext

## Smart Car Parking System using Deep Learning

* Contract
Contains a copy of study contract signed

* Data
Contains datasets colllected and created. Required to run the CNNs
* Deep Learning
Contains python notebooks demostrating the appication of vgg16, vgg19, resnet50 and inception_v3 to identify empty car parking spots
* Demo Website
Demonstrates how the parking spots will be created on google maps
* Ethical Clearance
Contains copies of documents submitted for ethical clearance
* Preprocessing
Contains scripts to aquire and modifies the datasets to allow machine learning, it contains information on how to run each script.
* Report
Contains raw data used to create the report

### Instalation ###



* Download and install Anaconda Distribution for Python 3.6 from https://www.anaconda.com/download/

* Install OpenCV: conda install -c conda-forge opencv

* Download and install Cuda version 8 from https://developer.nvidia.com/cuda-80-ga2-download-archive
* Download and install cudnn version 5 from https://developer.nvidia.com/rdp/cudnn-download ,  you will have to register first.

Prerequist for theono:

* conda install numpy scipy mkl nose sphinx pydot-ng

* Install theano using commond: conda install theano pygpu
else try: conda install -c conda-forge theano 

* Install Keras: conda install -c conda-forge keras
else try: conda install -c anaconda keras

* setting hyperprameters for theano: Find the default ".theanorc.txt" file created on your system at install time. Replace its contents by the ".theanorc.txt" file in artifacts
Note: I ran into problems because theano want able to detect where nvidia and cuda drivers where installed, I have commented out my local paths if you run into issue with drivers not found you will have to give the location of the drivers manully in the file.

* Setting hyperprameters for keras: Find the folder .keras it will contain a file keras.json Replace it with the file provided in folder artefacts

### Running ###

Python notebook:

* Run python notebook using command: jupyter notebook
* This will start a local server. If a web browser in not opened automaticly type this address in web browers: localhost:8888
* If this donst work check bash where you entered the commond it will tell you the address of the local server and the port.

* Either copy+paste the notebooks in the directory that has been opened. You will have to figure out the folder location on you system judging by the files that you could see.
Else change the default folder opened by using the following command:
* jupyter notebook --generate-config
* A directory .jupyter/ should have created in your home with a file jupyter_notebook_config.py
uncomment and edit the field c.NotebookApp.notebook_dir to the path where you want to save the python notebooks

* Once the notebooks are opened you can view the results as they had run on my machine.
* You can run each block of code by clicking "run cell" button Or you can run all the cells at once by clicking cell->Run all


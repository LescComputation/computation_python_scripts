#!/usr/bin/env python
"""
Author: Shyue Ping Ong
Modified by: Devin Cela
             Dan Davies
"""
#script can be used to re-run tests using the contcar file as the poscar file

import subprocess
import os
import shutil

class cd:
    """
    Context manager for changing the current working directory in Python.
    E.g. with cd(path/to/new/directory):
            subprocess.call("Do something", shell=True)
         Outside of the with statement we are back to the original directory.
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

"""
this function just finds the top-level folders that we need to change into to find the results.
WARNING - this will not work if your directory structure is even a little bit complicated, and will only go down one level. 
http://stackoverflow.com/questions/141291/how-to-list-only-top-level-directories-in-python
puts the folders into a list that we can iterate through 
"""
folders = os.walk('.').next()[1] #

# Loop through different folders.
for folder in folders:

    #go into folder
    with cd(folder):
        #read the contcar file
        contcar_string = open("CONTCAR").read()

        #write the contcar file to the poscar file
        with open("POSCAR", "w") as f:
            f.write(contcar_string)
            
        #run VASP
        subprocess.call("sbatch SUBMIT", shell=True)

    #Print some status messages.
    print("Running from folder  %s" % (folder))

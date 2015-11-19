#!/usr/bin/env python 

"""
Author: Shyue Ping Ong
Modified by: Devin Cela
             Dan Davies
"""

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

# Load the template file as a template.
with open("KPOINTS_template") as f:
    kpoints_template = f.read()

with open("SUBMIT_template") as f:
    submit_template = f.read()

with open("INCAR_template") as f:
    incar_template = f.read()

# Loop through different k-points / encuts / whatever you define.

for k in range(1, 9, 1):
    #make a jobname
    jobname = "LMO_ENCUT_Test_%s" % (value)
    kpoints_string = kpoints_template.format(k=k) #This generates a string from the template with the parameters in {} replaced 
    #by the values that you specify
    SUBMIT_string = submit_template.format(job_name=jobname ) #same here
    INCAR_string = incar_template.format(ENCUT_value=350) #and here

    # Write the actual input file.
    with open("KPOINTS", "w") as f:
            f.write(kpoints_string)
    with open("SUBMIT", "w") as f:
        f.write(SUBMIT_string)
    with open("INCAR", "w") as f:
        f.write(INCAR_string)

    #Print some status messages.
    print("Running with value = %s..." % (value))

    # Make a folder with the unique jobname
    subprocess.call("mkdir {jobname}".format(jobname=jobname), shell=True)
    #Copy input files to new directory
    subprocess.call("cp INCAR POSCAR POTCAR KPOINTS SUBMIT {jobname}".format(jobname=jobname), shell=True)

    #Run VASP
    with cd("{jobname}".format(jobname=jobname)):
        subprocess.call("sbatch SUBMIT", shell=True) 
    
    #Let us know when it is finished
    print("Done. Output file is %s.out." % jobname)


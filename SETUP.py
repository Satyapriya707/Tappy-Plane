# THIS SCRIPT SHOULD BE CALLED SETUP.PY
import cx_Freeze

import sys

base = None
if (sys.platform == "win32"):
    base = "Win32GUI" 

import os

os.environ['TCL_LIBRARY'] = r"C:\Users\satya\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll"
os.environ['TK_LIBRARY'] = r"C:\Users\satya\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"

executables = [cx_Freeze.Executable("main.py", base = base)] 
cx_Freeze.setup( 
        name = "Tappy Plane",
        version = "22.99",
        options = {"build_exe": {"packages":["pygame","os","sys"],
                  "include_files":['img','snd','highscore.txt']}},
        description = "Tappy Plane game tutorial", 
        executables = executables)


#python setup.py build
#python setup.py bdist_msi
# first e: then cd 'location'

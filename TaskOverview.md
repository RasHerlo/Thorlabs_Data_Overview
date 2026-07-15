
TASK OVERVIEW:

- Consider uploading the data-examples from a connected GoogleDrive instead of 
having to commit via bash (which takes a loooong time)

- Also, consider much smaller data set for testing

- In Main_Folder_Walk.py, check if stack is actually made, instead of just checking
 if the folder is empty
 
 

OVERALL RUNNING ISSUES:

- Align the interpreters on the various work-stations (How?)
(see the fundamental issues in Notion: )

- How to establish an environment with the repo, which also uploads/downloads through GitHub?

- 

TRACKING:

- Delete early shape reports of tifs
- Delete "Yes, tiffile exist: xxxxxxxxx.tif"

- Inform about processes and steps for each walk branch
    - Record the time to assess the most time-consuming steps

TROUBLESHOOTING:

- consider implementing cProfile, line profiler of pdb to get an overview of why certain modules are stalling:

import cProfile

def my_slow_function():
    # Your code here

cProfile.run('my_slow_function()') 

---

from line_profiler import LineProfiler

def my_slow_function():
    # Your code here

profiler = LineProfiler()
profiler.add_function(my_slow_function)
profiler.run('my_slow_function()')
profiler.print_stats() 

---

import pdb

def my_slow_function():
    pdb.set_trace() 
    # Your code here

my_slow_function()


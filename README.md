# PyProfile: Memory Consumption and Runtime Tracker for Python

`Memory Consumption and Runtime Tracker for Python` is an application 
which focuses on memory and time data visualization for Python programmers.


### Setup

We prefer to do the setup in `Pycharm`, which is an ide for python.
But setting up through command line can also do the tricks

#### Pycharm
Download `pycharm` through here: https://www.jetbrains.com/pycharm/
and let `pycharm` automatically install all dependencies

#### Command Line setup
run `pip install astor`

#### Setup for React.js visualization
```shell
cd path/to/my-app && npm install
```

### Run
Hit the run button in pycharm or run 
```shell
python path/to/main.py
```
Then in the `pyprofile` shell, type:
```shell
profile path/to/file_for_profile.py
```

The profiling for file and visualization will be generated

### Note for running:
When the profiler is started, only `profile` and `quit` commands are
permitted. Other command will result in `invalid command`, `quit` will
simply end the app process. 

### Design Notes  
  
#### Motivation
Every program consumes different amounts of memory when it is running. Programmer may encounter memory bottleneck that they do not expect and find it hard to find out the cause of a memory issue. Our project is to help them to identify the memory bottlenecks and solve memory related issues.

#### Scope
We plan to dynamically analyse the execution of a python program, including keeping track of the memory consumption in each stack frame with time and heap memory profiling. We’ll implement the dynamic program analysis by instrumenting source code. In terms of visualization, we are planning to use a Flame Graph to represent the memory consumption in each stack frame with time, and use pie charts for representing variables allocated on heap (with type and the number of allocations).

#### Use case
Provide straightforward visualization graphs for programmers who want to measure/optimize memory consumption of each methods in their program, for example, if their resources are limited or they are paying a lot of attention to the performance of their program.


### Clarification

1. We have a loading page, which includes the links to the "FlameGraph" page and the "Top 10 Memory consuming methods" page
2. For the "FlameGraph" page, the x-axis of the flamegraph refers to runtime, and the color refers to the degree of memory consumption (the greener, the lower memory consumption; the redder, the higher memory consumption). (it should be noted that the length of a parent frame is longer than the total length of its children. It is because that the runtime of a parent method not only includes the runtime of the child calls, but also includes the runtime of some other statements like print("123") and a = 1 + 2)
    
   When we click on any frame in the flame graph, a pie chart which represents different types of variables allocated on heap will be shown.
   When we hover over a sector of the pie chart, the heap allocation of each local variable (sorted by size) under that type will be shown
3. For the "Top 10 Memory consuming methods" page, the top 10 memory consumption methods are shown (sorted by size) so that users can easily find out how to optimize their program

### Changes based on user studies and development experience

1. We change our backend to only have 1 json file generated instead of our original plan to generate 2 json files. This makes it easier for the backend to simply update a global dictionary that store all the memory info
2. Do note that, for memory consumption data in one stack frame, we do not include the memory consumption in any child frame (basically all function call )

### Implementation details
ASTInstrumenterConsumptionTracker instruments the initial source code,
and keeps tracking the consumption of CPU usage 
(time elapsed) and Memory usage (heap allocation) 
for each function call as a frame record. 
When the program runs and terminates, 
it generates all frame records to stacks.json file. 
The stacks.json is the input for flame graph and pie chart.

### Restrictions
1. The profiler can only process one single python module (i.e. one .py file), the module dependency is not solved in this project
2. Keep in mind, all initial source code must have a main function and run from it as an entry because this restriction really simplifies the AST instrumentation.
3. Our consumption tracker cannot track external library calls because there is no access to their function definitions. (eg. print)

### Good source samples for testing
```shell
profile ./source_samples/custom_class.py
profile ./source_samples/merge_sort.py
```

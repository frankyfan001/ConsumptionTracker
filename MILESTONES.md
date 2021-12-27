# Milestone 1

## Candidate ideas

1. Draw a UML diagram for project dependencies\
*Use case:*\
From previous co-op experience, we found that a project usually has many dependencies, even circular dependencies, making it hard for a new developer to get started on the project, and also difficult for refactoring. It would be useful to visualize the dependencies to make the project more accessible to new devs.\
*Description:* \
We plan to statically analyse a java program’s source code and visualize the structure of a system, including its classes, class attributes, operations (or methods), and the relationships among objects.

2. Resource Consumption Tracker (Performance Profiler): Flamegraph, Memory data visualization with time (stack and heap memory)\
*Use case:*  
Provide a straightforward visualization graph for programmers who want to measure/optimize their program, for example, if their resources are limited or they are paying a lot of attention to the performance of their program\
*Description:* \
We plan to analyse the execution of a java program, including the memory consumption of stack and heap. Moreover, we will keep track of the memory consumption in each stack frame and each heap allocation, as well as the runtime for each stack frame. We are planning to use a Flame Graph visualization for the stack data and a line chart for variables allocated on heap (with type, the number of allocations and memory consumption)

3. Metrics: VisualVM, \
*Use case:*\
users may want to monitor the measures of numbers of classes, threads, etc., other than just tracking for the CPU, memory, or other systematic usages. Users may also want to analyze the stability of some web apps by measuring different server statuses or even counting the log messages.\
*Description:* \
Firstly, we plan to count the number of classes, routers, and other statically checkable data before the execution of the real program. Then, we will run the input program, says some web apps, multiple times by accessing the specific routers(like postman) while measuring the status code, responding messages, and so on.

4. Code complexity analysis\
*Use case:*  
users may want to know how the performance of their program is bound to some extent when they want to optimize their logic.\
*Description:* \
We plan to run their program dynamically many times and fit with different sizes of input while plotting and fitting the data to some potential bounded complexity. In this case, we may be able to get closer to the actual time complexity by estimating the best fit.

## TA feedback
Idea1: I would not consider it a program analysis idea. UML is a very meta-level thing. Moreover, generate such a UML diagram does not really need to “analyze” the code, just went through each component of the code and categorize them. I would suggest not think along this line.

Idea2: performance-related analysis is ok, but from your description, I didn’t see much about how you gonna actually analyze a target program. (Or more specifically, what’s **your** action items for this project?) There are already a set of toolchains for generating flame graphs. What are the specific program analysis you will be doing in this process? Which part of the code will be statically analyze? Which part of the code will be dynamically analyzed? How will you do the static analysis and dynamic analysis? What do you mean by “use a flame graph visualization for ….”? Are you going to use existing flame graph tools, or will you make some extension to flame graph?
Overall, performance analysis may not be a bad idea, but it’s very unclear to me what you want to do in your project. It would be a good idea to pick a smaller scope and find some real examples.

Idea3: Are you referring to https://visualvm.github.io/ this project? Or it’s just you happened to think of the same project name? This one reads more or less the same as idea2. A few existing issues I’ve noticed:
	1. Your current plan involves no static analysis (counting classes, routers, etc. are not analysis).
	2. This is mostly due to I’m unsure if you are referring to the other visualvm project. Most of the things you mentioned here are already somewhat offered in visualVM. Are you planning to do the project based on VisualVM? If so, what’s the exact part you will be doing? If not, are you going to visualize all those profiling data? It would be better to have a more detailed plan, so I can make sure this is a project manageable within less than 5 weeks.

Idea4: Doesn’t look like a well-baked idea to me, because I fail to see the analysis part of it. A few problems with the idea:
	1. It seems what you eventually want to do is just run a regression on all the collected run-time data. But even if you get a really accurate bounded complexity, how does that help programers to optimize their program? Do they gain any knowledge about what cause the performance bottle neck? How can you achieve this goal?
	2. Like I mentioned in the summary, I personally doesn’t consider running a program a few times as dynamic analysis. But I surely didn’t see anything related to static analysis. Therefore based on the requirement for project 2, you need to have a substantial visualization part, which I also didn’t see in this idea.

## Follow-up tasks for the next week
1. settle on a specific idea
2. determine the specific action items for this project, including what program analysis we will be doing, which part of the code will be statically and dynamically analyzed, respectively, how we will do the static analysis and dynamic analysis, and what graph tools we will be using.
3. plan division of main responsibilities between team members.


&nbsp;

&nbsp;

&nbsp;

&nbsp;



# Milestone2

## Brief description of our planned program analysis idea
###### Resource Consumption Tracker: Memory data visualization with time
*Use case:* \
Provide a straightforward visualization graph for programmers who want to measure/optimize their program, for example, if their resources are limited or they are paying a lot of attention to the performance of their program.

*Description:* \
We plan to dynamically analyse the execution of a java program, including keeping track of the memory consumption in each stack frame and each heap allocation (and also the runtime of each method, if time permits). We’ll implement the dynamic program analysis by instrumenting source code. In terms of visualization, we are planning to use a Flame Graph visualization for the stack data and a line chart for variables allocated on heap (with type, the number of allocations and memory consumption)


## Notes of important feedback from TA discussion
Our idea 1 is quite meta-level. We need to add some interesting features to idea1 if we would like to work on it, like aliasing and polymorphism analysis => we have decided to abandon this idea and settle on idea2

For idea2, we can record the data we want by instrumenting source code. We can also add some interesting features like analysing the stack consumption of specific targets, e.g. loops, recursive functions.


## Any planned follow-up tasks or features still to design
Figure out how to instrument the source code in order to get records of memory allocation and runtime.

Mockup of how our project is planned to operate (as used for our first user study). Include any sketches/examples/scenarios.

Notes about first user study results.

Timeline of our project


## Planned division of main responsibilities between team members
Our initial plan is to have 3 people work on instrumenting source code, and 2 people work on visualization. 

## Progress so far.
We have settled on a specific idea and started working on designing the features.



&nbsp;

&nbsp;

&nbsp;

&nbsp;


# Milestone 3


## Description

Our project is called "Consumption Tracker", which focuses on memory data visualization with time. 

#### Motivation
Every program consumes different amounts of memory when it is running. Programmer may encounter memory bottleneck that they do not expect and find it hard to find out the cause of a memory issue. Our project is to help them to identify the memory bottlenecks and solve memory related issues.


#### Scope
We plan to dynamically analyse the execution of a python program, including keeping track of the memory consumption in each stack frame with time and heap memory profiling. We’ll implement the dynamic program analysis by instrumenting source code. In terms of visualization, we are planning to use a Flame Graph to represent the memory consumption in each stack frame with time, and use pie charts for representing variables allocated on heap (with type and the number of allocations).


#### Use case
Provide straightforward visualization graphs for programmers who want to measure/optimize memory consumption of each methods in their program, for example, if their resources are limited or they are paying a lot of attention to the performance of their program.

## Backend
by Jerry Liu, Kehong Liu, and Franky Fan

![](https://i.imgur.com/t4f2hLO.png)

The current version of backend is composed of 2 parts:
    1. A profiler component which is capable of getting information of memory consumption from libraries (tracemalloc, heapy)
    2. A AST Instrumenter, which will visit the `ast` and inject code for recording the memory consumption based on the `profiler` in 1.
    

## Frontend

by Chen Hang, Eric Lyu

![](https://i.imgur.com/70FmGzz.png)

Frontend is supposed to process the data generated by the Backend and draw the graph:

    1. Get the data in form of JSON (an example is shown below)
    2. Parse JSON and separate the memory data for drawing the flame graph and heap graghs
    3. Generate different input JSON files for the frontend library
    4. Draw the graph
    
### Json Example
`name` refers to the method name, and `value` refers to the running time of that method. `heapAlloc` refers to the heap allocation of the corresponding method(including the total allocation, the allocation of each data type, and the allocation of each variable)

    {
      "name": "main.py",
      "value": 89,

      "children": [
        {
          "children": [
            {
              "children": [
                {
                  "name": "method1",
                  "value": 20,
                  "heapAlloc": {
                    "total" : {
                      "total_memory": xxx,
                      "typed_memory":[
                        {
                            "type": "str",
                            "value": 10
                        },
                        ...
                      ]
                    },
                    "vars": [
                      {"name": ...,
                      "type": ...,
                      "value": ...},
  
  
                      {"name": ...,
                      "type": ...,
                      "value": ...},
                    ]
                  }
                }
              ],
              "name": "metho2",
              "value": 20,
              "heapAlloc": {
                "total" : {
                  "total_memory": xxx,
                  "typed_memory":[
                    {
                        "type": "str",
                        "value": 10
                    },
                    ...
                  ]
                },
                "vars": [
                  {"name": ...,
                  "type": ...,
                  "value": ...},


                  {"name": ...,
                  "type": ...,
                  "value": ...},
                ]
              }
            }
          ],
          "name": "method3",
          "value": 20,
          "heapAlloc": {
            "total" : {
              "total_memory": xxx,
              "typed_memory":[
                {
                    "type": "str",
                    "value": 10
                },
                ...
              ]
            },
            "vars": [
              {"name": ...,
              "type": ...,
              "value": ...},


              {"name": ...,
              "type": ...,
              "value": ...},
            ]
          }
        }
      ]
    }

    
### Visualization Examples
An example of the flame graph is shown below. The horizontal axis refers to the runing time, and the vertical axis refers to the stack frame.
The color of each frame is based on the memory consumption of that frame(e.g. the higher memory consumption, the redder in this graph)
![](https://i.imgur.com/UM5s34j.png)


When we hover over any method name, a pie chart which represents the heap memory usage of that method will be shown, as well as the names of the objects which consumes the highest memory in each data type.
![](https://i.imgur.com/vKVzwTj.jpg)


If we are intereted in one of the methods, we can zoom that part by clicking it. 
![](https://i.imgur.com/fYLaD4E.png)


### First user study results
1. General thoughts about our resource consumption tracker, like types of data provided, visualization components...? 
> Answers: 
> - It seems pretty interesting and data provided are useful.
> - The diagram and graphs provided are intuitive and may be helpful for analyzing and optimizing my code.
> - Generally speaking, the dynamic consumption tracker can help me with analyzing my program related to each timestamp. The overall idea is good.
> - Though the flame graph idea is good and has been persisted for a long time, new features provided like hovering above each frame providing more information or dynamically showing memory consumption of collections of variables in each frame can really help me with optimizing my code.
> - I think if there is a section shows how much time each function spends on (or proportion) that would be really helpful.
2. In what kinds of situations will you most likely use our application for gathering the information you need? 
> Answers:
> - It can be useful for practicing programming contest questions, as in these scenarios memory is very limited and it's good to know what takes up the memory.
> - Can help me optimize the memory used for programming exercise on LeetCode or determine the wasted allocated variables that are not longer needed.
> - Whenever there is a limited resources available to develop and I cannot find the place that I can keep track of for a better performace, I may use it. By using this application, I can easily find out where there is a list in my implementation that takes much more memory than expected. Then, I can come up with plans for optimization.
> - When I was stuck into some unterminated loop or terminated but time-consuming loop, I will use debugger to find out the place. However, debugger may not be able to determine the memory or heap consumption on some specific variables within some loops or recursions. I will use this instead.
> - I generally use a resource tracker when I write parallel code and try to find out which part of the code can be parallized.
3. Will you use our application when trying to optimize your program or to perform analysis? If not, what parts of visualization or data prevent you from conducting the analysis? Any unclear stated data/graph confuses you?
> Answers: 
> - The pie chart is straight forward but the flame graph is a bit confusing. May be some labels on the axis can help.
> - Yes, the overall visualization on frame heap is intuitive. However, it is much more userful if it can break down the flame graph into more sub-graph under the specific frame with each variables labelled with their memory consumption for each timestamp or interval.
> - Yes, but the graph seems get a bit blurrer with ... if going deeper. Not sure but better expand the tab.
> - Not really, the declaration or definition of the memory consumption for each frame seems vague to me. It is helpful if it can provide more details under the bottem of above each diagram/graph.
> - I'm not too sure what the flame graph represents. Maybe a legend of something similar can help clarify it a bit.
4. Any functionality that you would consider useful but not be included in our tracker?
> Answers: 
> - Adding the ability to click on the pie chart and see the memory consumption of each individual variable would be useful
> - Can add a feature like comparing the memory usage or other metrices between two tiny modified codes. That would be useful for me to find a way to optimize my program as a start point.
> - Provide a more intuitive color representations of the memory consumption can help me determine where should I zoom in without actually going to click or hover the tab.
> - May expand the dimension to 3D representation with extra measurement other than time like classes, etc. to provide more data. For examples, measure in different unit like class, method, or loop.
> - Maybe add a tool for tracking memory access would be helpful.
5.  If we have a score range from 1 to 5, 1 is very difficult to use and 5 is very easy to use, what would be the score?
> Answers: 
> - 2, need to understand flame graph
> - 1, more tutorials are needed. Overall is easy to understand.
> - 3, lack of many lables and more comments should be added.
> - 2, need more clarifications.
> - 3
6. Any comment or ideas for improvements that you want to remark beside the previous 5 questions
> Answers: 
> - Seems pretty good to me.
> - Could add features to analyze many versions of the program.
> - Overall is good.
> - Nah



# Milestone 4

### Status of implementation so far

Based on TA's feedback, we did several changes to our project planning (under Milestone3):
1. Added motivation, scope and use cases to our planning
2. Let the pie graph provide more detailed information (i.e. when we hover over a sector of the pie chart, the heap allocation of each local variable under that type will be shown), so that the user can know the outstanding object which takes a relatively big chunk of the memory and can do some optimization around it.
2. Modified the JSON format. It now includes the name, running time, total memory allocation, heap allocation of each data type, heap allocation of each local variable of each method.


We divided the implementation into backend and frontend. We’ve completed half of the total implementation. We plan to complete the first version of our project by the end of this week, and then do some code cleaning & refactoring.

For the backend implementation, we divided it into three parts. Franky, Jerry, and Kevin are working on this.
1. Franky set up the scaffolding / template of the instrumentation for the back-end project:
Details: 
He implemented ASTInstrumenterTrackTime that instruments AST of a program and produces a JSON file as the input for the front-end flame graph. In the final flame graph, the x-axis will show the stack profile population for the time elapsed.
ASTInstrumenterTrackTime impl details: for each function definition in the original source, a decorator (function wrapper) is inserted, so we can track the stack frame records of each function call. Currently the record of time is already done.
2. Kevin is responsible for getting the size of each local variable:
Details:
For each Assignment() AST node, insert sys.getsizeof() and type()statement to get the size and type of the variable, and record it in the heapAlloc dictionary of the current frame. If the right side of the assignment operator is a variable name, that means the newly defined variable is just a reference to the variable on the right side of the assignment operator, thus no additional memory is taken up by the var on the LHS, and it bears no signifance to the record of local variable sizes. Therefore its size and type will not be computed and will not be inserted into the heapAllloc dictionary. If a variable is reassigned a new value, then compute the size and type of the new value, and update the corresponding entry in heapAlloc.
3. Jerry is responsible for getting the total memory allocation of each frame
Details:
He implements the methods for calculating the memory consumption for each stack frame. This includes a wrapper which will take the wrapped function and calling the library to get memory details before and after the function call. Then the difference between the memory data before and after the function call is recorded into the JSON file so that the user will be able to know how much memory in total is spent in one stack frame


For the frontend implementation, we are using REACT to build user interfaces.We have completed the representation of the flamegraph and pie charts and we are still working on showing the heap allocation of each local variable under a certain type when a user hovers over a sector of the pie chart. We also plan to add some figures which can provide more straightforward visualization of the methods which have the largest memory consumption as well as the memory allocation of its local variables so that the users can easily find out how to optimize their program. Chen and Eric are responsible for this part.

### Plans for final user study
We will be conducting the study with a different set of users. Since we have done some changes to our project planning, we would also like the old users to test our application and ask about if the change we made is working for them.


### Planned timeline for the remaining days.
We plan to complete the first version by the end of this week, and then do some code cleaning/refactoring nect week.
We also plan to start working on the final video next week and get a draft version by the end of next week.



# Milestone 5

### changes

Added the "Top 10 Memory consuming methods" page. On this page, the top 10 memory consumption methods are shown (sorted by size) so that users can easily find out how to optimize their program

### Final User Study
1. General thoughts about our resource consumption tracker, like types of data provided, visualization components...? 
> Answers: 
> - I think it's rather useful because I can easily find out what variables/methods consumes a large amount of memory
> - The breakdown of variable sizes is useful, as I can pin point where the most memory is used
> - It's quite intuitive to have the the coloured flame graph representation, can easily see memory usage at a glance

2. In what kinds of situations will you most likely use our application for gathering the information you need? 
> Answers:
> - When I'm insterested in how the frames are built or when I have limited memory.
> - When I'm building applications for a resource-limited system, such as embedded systems
> - When I'm trying to keep track of memory for LeetCode questions, if I get a MLE I can pin point where it happened

3. Will you use our application when trying to optimize your program or to perform analysis? If not, what parts of visualization or data prevent you from conducting the analysis? Any unclear stated data/graph confuses you?
> Answers: 
> - Yes, I think the flame graph is quite straightforward. I can find the target methods just from the color
> - Yes, the pie chart is a clear representation of the relative sizes of local variables
> - Yes, clicking on the corresponding frame to see its variable sizes is pretty intuitive

4. Any functionality that you would consider useful but not be included in our tracker?
> Answers: 
> - Maybe show the corresponding code when I hover over a frame in the flame graph? 
> - Show memory consumption at each line can be useful
> - It would be good if it can also track of system allocated bytes on heap

5.  If we have a score range from 1 to 5, 1 is very difficult to use and 5 is very easy to use, what would be the score?
> Answers: 
> - 5, straightforward flame graph, and useful pie charts 
> - 5, graphs are clear
> - 5, intuitive and easy to use

6. Any comment or ideas for improvements that you want to remark beside the previous 5 questions
> Answers: 
> - for me, it's already quite useful
> - nothing to add, it's pretty good in my opinion
> - pretty good as an memory resource tracker


### Plans for final video
Complete the draft version by Saturday, and complete the final version by next Tuesday

### Planned timeline for the remaining days
Complete all our implementation by Friday (including debugging and refactoring)

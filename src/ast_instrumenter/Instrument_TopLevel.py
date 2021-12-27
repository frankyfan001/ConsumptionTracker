import functools
import time
import sys

"""
stack that will be pushed & popped with frames during function calls, just like stack-based memory allocation.
These frames are the records in our stacks.json to generate a flame graph.
"""
stack = []
"""
When root function call (ie. main()) finishes, its frame is assigned to root_frame_reference.
Then program terminates and stacks.json is generated based on the content of root_frame_reference.
"""
root_frame_reference = None
"""
consumption_tracker function here is a function wrapper, also knows as decorator.
A decorator wraps a function to extend the behavior of the wrapped function, without permanently modifying it.
In the decorator, a function is taken as the argument and then called inside the wrapper function.
Reference: https://www.geeksforgeeks.org/function-wrappers-in-python/
"""


def consumption_tracker(func):
    """
    Record the CPU usage (time elapsed) of the frame in stack during a function call.
    The record of Memory usage (heap allocation) is done in ASTInstrumenterConsumptionTracker.visit_Assign() separately.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Push a frame onto stack before function call starts."""
        frame = {'children': [], 'name': func.__name__, 'value': 0.0,
                 'heapAlloc': {'vars': []}}
        stack.append(frame)
        """Function call runs and record the run time of the frame in stack."""
        start_time = time.time_ns() / (10 ** 9)
        value = func(*args, **kwargs)
        end_time = time.time_ns() / (10 ** 9)
        run_time = end_time - start_time
        frame['value'] = run_time
        """Pop the frame from stack after function call finishes."""
        stack.pop()
        if func.__name__ != 'main':
            """Associate the frame (callee) with its parent frame (caller)"""
            parent_frame = stack[-1]
            parent_frame['children'].append(frame)
        else:
            """
            When root function call (ie. main()) finishes, its frame is assigned to root_frame_reference.
            Then program terminates and stacks.json is generated based on the content of root_frame_reference.
            """
            global root_frame_reference
            root_frame_reference = frame
        return value

    return wrapper

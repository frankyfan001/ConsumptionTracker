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
        start_time = time.time_ns() / 10 ** 9
        value = func(*args, **kwargs)
        end_time = time.time_ns() / 10 ** 9
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


@consumption_tracker
def merge(array, left_index, right_index, middle):
    if True:
        left_copy = array[left_index:middle + 1]
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'left_copy':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(left_copy
                    ).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    left_copy)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name': 'left_copy',
                'type': type(left_copy).__name__, 'value': sys.getsizeof(
                left_copy)})
    if True:
        right_copy = array[middle + 1:right_index + 1]
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'right_copy':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(right_copy
                    ).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    right_copy)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name': 'right_copy',
                'type': type(right_copy).__name__, 'value': sys.getsizeof(
                right_copy)})
    if True:
        left_copy_index = 0
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'left_copy_index':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                    left_copy_index).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    left_copy_index)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name':
                'left_copy_index', 'type': type(left_copy_index).__name__,
                'value': sys.getsizeof(left_copy_index)})
    if True:
        right_copy_index = 0
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'right_copy_index':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                    right_copy_index).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    right_copy_index)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name':
                'right_copy_index', 'type': type(right_copy_index).__name__,
                'value': sys.getsizeof(right_copy_index)})
    sorted_index = left_index
    while left_copy_index < len(left_copy) and right_copy_index < len(
        right_copy):
        if left_copy[left_copy_index] <= right_copy[right_copy_index]:
            array[sorted_index] = left_copy[left_copy_index]
            if True:
                left_copy_index = left_copy_index + 1
                reassign_var = False
                for i in range(len(stack[-1]['heapAlloc']['vars'])):
                    if stack[-1]['heapAlloc']['vars'][i]['name'
                        ] == 'left_copy_index':
                        reassign_var = True
                        stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                            left_copy_index).__name__
                        stack[-1]['heapAlloc']['vars'][i]['value'
                            ] = sys.getsizeof(left_copy_index)
                if not reassign_var:
                    stack[-1]['heapAlloc']['vars'].append({'name':
                        'left_copy_index', 'type': type(left_copy_index).
                        __name__, 'value': sys.getsizeof(left_copy_index)})
        else:
            array[sorted_index] = right_copy[right_copy_index]
            if True:
                right_copy_index = right_copy_index + 1
                reassign_var = False
                for i in range(len(stack[-1]['heapAlloc']['vars'])):
                    if stack[-1]['heapAlloc']['vars'][i]['name'
                        ] == 'right_copy_index':
                        reassign_var = True
                        stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                            right_copy_index).__name__
                        stack[-1]['heapAlloc']['vars'][i]['value'
                            ] = sys.getsizeof(right_copy_index)
                if not reassign_var:
                    stack[-1]['heapAlloc']['vars'].append({'name':
                        'right_copy_index', 'type': type(right_copy_index).
                        __name__, 'value': sys.getsizeof(right_copy_index)})
        if True:
            sorted_index = sorted_index + 1
            reassign_var = False
            for i in range(len(stack[-1]['heapAlloc']['vars'])):
                if stack[-1]['heapAlloc']['vars'][i]['name'] == 'sorted_index':
                    reassign_var = True
                    stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                        sorted_index).__name__
                    stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                        sorted_index)
            if not reassign_var:
                stack[-1]['heapAlloc']['vars'].append({'name':
                    'sorted_index', 'type': type(sorted_index).__name__,
                    'value': sys.getsizeof(sorted_index)})
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        if True:
            left_copy_index = left_copy_index + 1
            reassign_var = False
            for i in range(len(stack[-1]['heapAlloc']['vars'])):
                if stack[-1]['heapAlloc']['vars'][i]['name'
                    ] == 'left_copy_index':
                    reassign_var = True
                    stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                        left_copy_index).__name__
                    stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                        left_copy_index)
            if not reassign_var:
                stack[-1]['heapAlloc']['vars'].append({'name':
                    'left_copy_index', 'type': type(left_copy_index).
                    __name__, 'value': sys.getsizeof(left_copy_index)})
        if True:
            sorted_index = sorted_index + 1
            reassign_var = False
            for i in range(len(stack[-1]['heapAlloc']['vars'])):
                if stack[-1]['heapAlloc']['vars'][i]['name'] == 'sorted_index':
                    reassign_var = True
                    stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                        sorted_index).__name__
                    stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                        sorted_index)
            if not reassign_var:
                stack[-1]['heapAlloc']['vars'].append({'name':
                    'sorted_index', 'type': type(sorted_index).__name__,
                    'value': sys.getsizeof(sorted_index)})
    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        if True:
            right_copy_index = right_copy_index + 1
            reassign_var = False
            for i in range(len(stack[-1]['heapAlloc']['vars'])):
                if stack[-1]['heapAlloc']['vars'][i]['name'
                    ] == 'right_copy_index':
                    reassign_var = True
                    stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                        right_copy_index).__name__
                    stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                        right_copy_index)
            if not reassign_var:
                stack[-1]['heapAlloc']['vars'].append({'name':
                    'right_copy_index', 'type': type(right_copy_index).
                    __name__, 'value': sys.getsizeof(right_copy_index)})
        if True:
            sorted_index = sorted_index + 1
            reassign_var = False
            for i in range(len(stack[-1]['heapAlloc']['vars'])):
                if stack[-1]['heapAlloc']['vars'][i]['name'] == 'sorted_index':
                    reassign_var = True
                    stack[-1]['heapAlloc']['vars'][i]['type'] = type(
                        sorted_index).__name__
                    stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                        sorted_index)
            if not reassign_var:
                stack[-1]['heapAlloc']['vars'].append({'name':
                    'sorted_index', 'type': type(sorted_index).__name__,
                    'value': sys.getsizeof(sorted_index)})


@consumption_tracker
def merge_sort(array, left_index, right_index):
    if left_index >= right_index:
        return
    if True:
        middle = (left_index + right_index) // 2
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'middle':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(middle
                    ).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    middle)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name': 'middle', 'type':
                type(middle).__name__, 'value': sys.getsizeof(middle)})
    merge_sort(array, left_index, middle)
    merge_sort(array, middle + 1, right_index)
    merge(array, left_index, right_index, middle)


@consumption_tracker
def main():
    if True:
        array = [33, 42, 9, 37, 8, 47, 5, 29, 49, 31, 4, 48, 16, 22, 26, 1,
            2, 4, 3, 5, 9, 3, 3, 8, 7, 6, 10, 11, 100, 99]
        reassign_var = False
        for i in range(len(stack[-1]['heapAlloc']['vars'])):
            if stack[-1]['heapAlloc']['vars'][i]['name'] == 'array':
                reassign_var = True
                stack[-1]['heapAlloc']['vars'][i]['type'] = type(array
                    ).__name__
                stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(
                    array)
        if not reassign_var:
            stack[-1]['heapAlloc']['vars'].append({'name': 'array', 'type':
                type(array).__name__, 'value': sys.getsizeof(array)})
    merge_sort(array, 0, len(array) - 1)
    print(array)


main()

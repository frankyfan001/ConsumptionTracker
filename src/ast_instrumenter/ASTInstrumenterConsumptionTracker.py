import ast
from ast import *
from typing import Any

INSTRUMENT_CODE_PATH = "./ast_instrumenter/"

"""ASTInstrumenterConsumptionTracker instruments the initial source code, and keeps tracking the consumption of CPU 
usage (time elapsed) and Memory usage (heap allocation) for each function call as a frame record. When the program 
runs and terminates, it generates all frame records to stacks.json file. The stacks.json is the input for flame graph 
and pie chart. More documentation for detailed implementation is in Instrument_TopLevel.py. 

Important Note:

1. Keep in mind, all initial source code must have a main function and run from it as an entry because this restriction 
really simplifies the AST instrumentation.

2. Reading the inserted AST nodes in ASTInstrumenterConsumptionTracker is not straightforward to understand what code 
is inserted or its functionalities. It might be more convenient to go to /src/data and directly compare 
initial_source.py vs instrumented_source.py, to gain a better understanding.
"""


class ASTInstrumenterConsumptionTracker(NodeTransformer):
    @staticmethod
    def instrument_top_level(file_path):
        f = open(INSTRUMENT_CODE_PATH + file_path)
        code_instrument = f.read()
        f.close()
        return parse(code_instrument)

    def visit_Module(self, node: Module) -> Any:
        """
        If a node have children, visit child nodes first, since NodeTransformer is post-order traversal (modification).
        Reference: documentation of NodeTransformer
        """
        for i in range(len(node.body)):
            child_node: stmt = node.body[i]
            node.body[i] = self.visit(child_node)

        top_level_module: ast.Module = ASTInstrumenterConsumptionTracker.instrument_top_level("Instrument_TopLevel.py")
        top_level_module.body.reverse()
        for sub_node in top_level_module.body:
            node.body.insert(0, sub_node)
        return node

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        """
        If a node have children, visit child nodes first, since NodeTransformer is post-order traversal (modification).
        Reference: documentation of NodeTransformer
        """
        for i in range(len(node.body)):
            child_node: stmt = node.body[i]
            node.body[i] = self.visit(child_node)

        """The following code is inserted at the beginning of each function definition."""
        # @consumption_tracker
        # def foo():
        #     ...
        node.decorator_list.append(Name(id='consumption_tracker'))

        return node

    def visit_Assign(self, node: Assign) -> Any:
        """if left child of assignment is not a variable, don't count it in (eg. x[0] = 1)"""
        if type(node.targets[0]).__name__ != "Name":
            return node

        """if right child of assignment is a variable, don't count it in (eg. x = a)"""
        if type(node.value).__name__ == "Name":
            return node

        """The inserted node is equivalent to the following code after an Assign statement (eg. a = 666)."""
        # a = 666
        # reassign_var = False
        # for i in range(len(stack[-1]['heapAlloc']['vars'])):
        #     if stack[-1]['heapAlloc']['vars'][i]['name'] == 'a':
        #         reassign_var = True
        #         stack[-1]['heapAlloc']['vars'][i]['type'] = type(a).__name__
        #         stack[-1]['heapAlloc']['vars'][i]['value'] = sys.getsizeof(a)
        # if not reassign_var:
        #     stack[-1]['heapAlloc']['vars'].append({'name': 'a', 'type': type(a).__name__, 'value': sys.getsizeof(a)})
        replacement_body = [
            node,
            Assign(targets=[Name(id='reassign_var')], value=Constant(value=False, kind=None), type_comment=None),
            For(target=Name(id='i'),
                iter=Call(func=Name(id='range'),
                          args=[
                              Call(func=Name(id='len'),
                                   args=[
                                       Subscript(
                                           value=Subscript(
                                               value=Subscript(value=Name(id='stack'),
                                                               slice=UnaryOp(op=USub(),
                                                                             operand=Constant(value=1, kind=None))),
                                               slice=Constant(value='heapAlloc', kind=None)),
                                           slice=Constant(value='vars', kind=None))],
                                   keywords=[])],
                          keywords=[]),
                body=[
                    If(
                        test=Compare(
                            left=Subscript(
                                value=Subscript(
                                    value=Subscript(
                                        value=Subscript(
                                            value=Subscript(value=Name(id='stack'),
                                                            slice=UnaryOp(op=USub(),
                                                                          operand=Constant(value=1, kind=None))),
                                            slice=Constant(value='heapAlloc', kind=None)),
                                        slice=Constant(value='vars', kind=None)),
                                    slice=Name(id='i')),
                                slice=Constant(value='name', kind=None)),
                            ops=[Eq()],
                            comparators=[Constant(value=node.targets[0].id, kind=None)]),
                        body=[
                            Assign(targets=[Name(id='reassign_var')],
                                   value=Constant(value=True, kind=None),
                                   type_comment=None),
                            Assign(
                                targets=[
                                    Subscript(
                                        value=Subscript(
                                            value=Subscript(
                                                value=Subscript(
                                                    value=Subscript(value=Name(id='stack'),
                                                                    slice=UnaryOp(op=USub(), operand=Constant(value=1,
                                                                                                              kind=None))),
                                                    slice=Constant(value='heapAlloc', kind=None)),
                                                slice=Constant(value='vars', kind=None)),
                                            slice=Name(id='i')),
                                        slice=Constant(value='type', kind=None))],
                                value=Attribute(
                                    value=Call(func=Name(id='type'), args=[node.targets[0]], keywords=[]),
                                    attr='__name__'),
                                type_comment=None),
                            Assign(
                                targets=[
                                    Subscript(
                                        value=Subscript(
                                            value=Subscript(
                                                value=Subscript(
                                                    value=Subscript(value=Name(id='stack'),
                                                                    slice=UnaryOp(op=USub(), operand=Constant(value=1,
                                                                                                              kind=None))),
                                                    slice=Constant(value='heapAlloc', kind=None)),
                                                slice=Constant(value='vars', kind=None)),
                                            slice=Name(id='i')),
                                        slice=Constant(value='value', kind=None))],
                                value=Call(func=Attribute(value=Name(id='sys'), attr='getsizeof'),
                                           args=[node.targets[0]],
                                           keywords=[]),
                                type_comment=None)],
                        orelse=[])],
                orelse=[],
                type_comment=None),
            If(test=UnaryOp(op=Not(), operand=Name(id='reassign_var')),
               body=[
                   Expr(
                       value=Call(
                           func=Attribute(
                               value=Subscript(
                                   value=Subscript(
                                       value=Subscript(value=Name(id='stack'),
                                                       slice=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))),
                                       slice=Constant(value='heapAlloc', kind=None)),
                                   slice=Constant(value='vars', kind=None)),
                               attr='append'),
                           args=[
                               Dict(
                                   keys=[Constant(value='name', kind=None),
                                         Constant(value='type', kind=None),
                                         Constant(value='value', kind=None)],
                                   values=[Constant(value=node.targets[0].id, kind=None),
                                           Attribute(
                                               value=Call(func=Name(id='type'), args=[node.targets[0]], keywords=[]),
                                               attr='__name__'),
                                           Call(func=Attribute(value=Name(id='sys'), attr='getsizeof'),
                                                args=[node.targets[0]],
                                                keywords=[])])],
                           keywords=[]))],
               orelse=[])
        ]

        """
        We are appending multiple statements to the initial single Assign statement, but NodeTransformer's visit 
        functions only allow to return a single AST node. Therefore, we wrap all statements into an If statement 
        which always run. Basically, this If statement only serves as a wrapper and does not change any behaviours.
        """
        # if True:
        #     a = 666    // initial single Assign statement
        #     ...        // instrumented multiple statements
        return If(
            test=Constant(value=True, kind=None),
            body=replacement_body,
            orelse=[]
        )

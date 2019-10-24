import os
import ast
from glob import glob


class Analyzer(ast.NodeVisitor):
    def __init__(self, obj):
        self.function = obj
        self.fargs = 0
        self.stats = {'args': 0, 'kargs': 0}

    # def visit_FunctionDef(self, node):
    #     print(node.name)
    #     # if node.name == self.function:
    #     self.generic_visit(node)

    # def visit_Name(self, node):
    #     # print(node.id)
    #     if node.id == self.function:
    #         print(ast.dump(node))
    #     self.generic_visit(node)

    # def visit_Expr(self, node):
    #     # if node.name == self.function:
    #     self.generic_visit(node)

    # def visit_Assign(self, node):
    #     # if node.name == self.function:
    #     for child in ast.walk(node):
    #         if child.value.func.id
    #         print(ast.dump(child))
    #         print(' '.join(10 * ['*']))
    #     self.generic_visit(node)

    def visit_Call(self, node):
        try:
            if node.func.id == self.function:
                print(ast.dump(node))
                print(' '.join(10 * ['*']))
                self.stats['args'] += len(node.args)
                self.stats['kargs'] += len(node.keywords)
        except Exception as e:
            pass
        self.generic_visit(node)

    # def visit_Attribute(self, node):
    #     print(node.attr)
    #     if node.attr == self.function:
    #         print(ast.dump(node))
    #     self.generic_visit(node)

    # def visit_Function(self, node):
    #     self.generic_visit(node)



# repo = '/home/srg/tmp/davidbp-python_tutorials-c2199fc'
# repo = '/home/srg/tmp/srikanthumich-machine-learning-9825c75'
# files = glob(os.path.join(repo, '**', '*py'), recursive=True)
# print(files)

# file = os.path.join(repo ,'predicting-housing-prices/visuals_test.py')
# file = os.path.join(repo ,'predicting-housing-prices/visuals.py')
file = "/home/srg/Documents/Projects/scikit-positional-args-stats/my-scikit-analysis/data/joel-repos/foresighters/lg-electronics-lecture-master/class_a/Day_1_Python_강의자료/Ch_4_Lambda, Map, Reduce/1. function, lambda, map, reduce.py"
# func = 'learning_curve'
func = 'validation_curve'
# func = 'DecisionTreeRegressor'

node_args = ast.arguments()
node_func = ast.FunctionDef()

with open(file,  'r') as fp:
    tree = ast.parse(fp.read())

# for elem in tree.body:
#     print(elem)

print(' '.join(30 * ['-']))
out = Analyzer(func)
out.visit(tree)
print(out.stats)
print(' '.join(30 * ['-']))

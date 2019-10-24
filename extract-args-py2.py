import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import os
import ast
import random
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=DeprecationWarning)
    from sklearn.utils.testing import all_estimators
from argparse import ArgumentParser

class Analyzer(ast.NodeVisitor):
    def __init__(self, obj):
        self.function = obj
        self.fargs = 0
        self.stats = {'args': 0, 'kargs': 0}

    def visit_Call(self, node):
        try:
            if node.func.id == self.function:
                self.stats['args'] += len(node.args)
                self.stats['kargs'] += len(node.keywords)
        except Exception as excp:
            pass
        self.generic_visit(node)


myparser = ArgumentParser()
myparser.add_argument(
    '--file', default=None,help='file path', required=True, type=str
)
argss = myparser.parse_args()

pyfile = argss.file
sk_objects = [x for x in all_estimators()]

# try:
with open(pyfile, 'r') as fp:
    tree = ast.parse(fp.read())

for elem in sk_objects:
    obj = elem[0]
    output_an = Analyzer(obj)
    output_an.visit(tree)

    if output_an.stats['args'] > 0:
        print ','.join([
            obj,
            str(output_an.stats['args']),
            str(output_an.stats['kargs'])
        ])

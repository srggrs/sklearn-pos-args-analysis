import warnings

import os
import subprocess
import ast

from glob import glob
from argparse import ArgumentParser

import pandas as pd
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=DeprecationWarning)
    from sklearn.utils.testing import all_estimators
from dask import delayed, compute
import dask.bag as db
import random


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


def analyze_file(pyfile):
    data = []

    repo = os.path.relpath(pyfile, DATA_PATH).split('/')[0]
    # try processing with python 3
    try:
        with open(pyfile, 'r') as fp:
            tree = ast.parse(fp.read())

        for elem in sk_objects:
            obj = elem[0]
            output = Analyzer(obj)
            output.visit(tree)

            if output.stats['args'] > 0:
                data.append(
                    [repo, os.path.relpath(pyfile, DATA_PATH), obj, output.stats['args'], output.stats['kargs']]
                )
    except Exception as err:
        # print(f'Python 3 error: {err}')
        # try processing with python 2
        cmdstr = [PY2EXEC,'extract-args-py2.py','--file',f'{pyfile}']
        out = subprocess.run(cmdstr, capture_output=True)
        if out.returncode == 0:
            output = out.stdout.decode()
            output = [
                [repo, os.path.relpath(pyfile, DATA_PATH)] + sub.split(',') for sub in output.split('\n')[:-1]
            ]
            data.extend(output)
        # else:
        #     error = out.stderr.decode()
        #     print(f'cannot process file:\n{pyfile}\nreason:\n{error}')
        #     print(' '.join(30*['-']))

    # if data:
    #     # tmpdf = pd.DataFrame(data, columns=data_cols)
    #     # tmpdf.to_csv(result_file, index=False, header=False, mode='a')
    #     # print(data)
    #     return data
    # # return ['test', 'tst', 't', random.randint(1, 10), random.randint(55, 77)]
    # else:
    #     return [len(data_cols) * [None]]
    # print(pyfile)
    # print(data)
    return data


def get_py_files(repo):
    repo = os.path.join(WORK_PATH, 'data', 'joel-repos', repo)
    return glob(os.path.join(repo, '**', '*.py'), recursive=True)


def check_nr_cols(data, file):
    for subdata in data:
        if len(subdata) > len(data_cols):
            print('issues with extracting this')
            print(file)
            print(data)
    pass


myparser = ArgumentParser()
myparser.add_argument(
    '--debug',
    action='store_true',
    help='set the Dask scheduler to synchronous for debugging'
)
myparser.add_argument(
    '--data-folder',
    type=str,
    required=True,
    help='Folder with the repos to analyse'
)
myparser.add_argument(
    '--py2-exec',
    type=str,
    required=True,
    help='Python2 interpreter location'
)
argss = myparser.parse_args()

def_scheduler = 'synchronous' if argss.debug else 'processes'
# def_scheduler = 'synchronous'

WORK_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.abspath(argss.data_folder)
OUTPUT_PATH = os.path.join(WORK_PATH, 'out')
PY2EXEC = os.path.realpath(argss.py2_exec)
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

RESULT_FILE = os.path.join(OUTPUT_PATH, 'data-summary.csv')
data_cols = ['repo', 'file','class','nr_pos_args','nr_kargs']
# df = pd.DataFrame(
#     columns=data_cols
# )
# if not os.path.exists(RESULT_FILE):
#     df.to_csv(RESULT_FILE, index=False)

# get the scikit learn classes
sk_objects = [x for x in all_estimators()]

repos = os.listdir(DATA_PATH)
repo_bag = db.from_sequence(repos)
all_py = repo_bag.map(get_py_files).flatten()
args_stats = all_py.map(analyze_file).filter(lambda x: len(x) > 0).flatten()
# checking = args_stats.map(check_nr_cols, file=all_py)
# compute(checking)
starttm = pd.Timestamp('now')
dataframe = args_stats.to_dataframe(columns=data_cols).compute(scheduler=def_scheduler)
stoptm = pd.Timestamp('now') - starttm
print(f'Computantion time: {stoptm}')
# # dataframe = args_stats.flatten().to_dataframe(columns=data_cols).dropna().compute()
# nrfiles = compute(args_stats, scheduler=def_scheduler)
# print(f'--------\nnr of processed files: {len(nrfiles)}')

print(f'data size: {dataframe.shape}')
print(dataframe.head())
print(dataframe.tail())
dataframe.to_csv(RESULT_FILE, index=False)

# print('done')



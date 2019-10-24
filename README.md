# sklearn-pos-args-analysis
This code analyse the usage of arguments and keyword arguments in the scikit classes (e.g. `RandomForestClassifier`) used from other repositories.

The code use Python AST to find the numer of `args` and `kargs` for a specific Scikit-learn object.


# Installation
Install a `Python >= 3.6` environment  with `requirements-py3.txt` and a `Python == 2.7` environment with `requirements-py2.txt`.


# Usage
After dowloading the python repos in a folder, activate the `Python3` environment and run the main code:

```bash
python extract-pos-args.py --data-folder PATH_TO_PY_REPOS --py2-exec PATH_TO_PY2_INTERPRETER
```

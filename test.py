import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.join(current_dir, 'packages')

if os.path.exists(packages_dir):
    sys.path.insert(0, packages_dir)


import numpy
import pandas
import seaborn
import matplotlib.pyplot as plt

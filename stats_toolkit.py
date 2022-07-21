import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def significance_test(p):
    '''
    Assumes an alpha of .05. Takes in a value, p, and returns a string stating whether or not that p value indicates sufficient evidence
    to reject a null hypothesis.
    '''
    α = 0.05
    if p < α:
        print("Sufficient evidence -> Reject the null hypothesis.")
    else:
        print("Insufficient evidence -> Fail to reject the null hypothesis.")


        
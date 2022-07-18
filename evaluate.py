from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression 
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

import wrangle as wr

def plot_residuals(df, y, y_hat):
    '''
    Takes in a DataFrame, as well as the columns serving as y 
    and y_hat, and returns a scatterplot that shows the residual 
    for each entry based on the provided variables.
    '''
    plt.figure(figsize = (12,8))
    residual = y - y_hat
    sns.scatterplot(data = df, x = y_hat, y = residual).set(title = 'Visualizing Residuals')
    plt.axhline(y = 0, ls = ':')
    plt.xlabel('Actual Value')
    plt.ylabel('Model Residual')

#Copying a classmate's (Cayt Schlichting) code to streamline:

#Individual calculations
def residuals(y,y_hat):
    return (y - y_hat)

def sse(y,y_hat):
    return sum(residuals(y,y_hat)**2)

def rmse(y,y_hat):
    return sqrt(mean_squared_error(y,y_hat))

def ess(y,y_hat):
    return sum((y_hat-y.mean())**2)

def tss(y,y_hat):
    return ess(y,y_hat) + sse(y,y_hat)

def regression_errors(y, y_hat):
    '''
    Takes in the values serving as y 
    (actual value) and y_hat (model's prediction), and returns 
    a list of error values for the dataset.
    '''
    #set index name for dataframe
    if isinstance(y_hat,pd.Series): ind=y_hat.name
    else: ind='y_hat'
    #Create DataFrame with performance stats as columns
    df = pd.DataFrame({
        'sse': [sse(y,y_hat)],
        'ess': [ess(y,y_hat)],
        'tss': [tss(y,y_hat)],
        'mse': [mean_squared_error(y,y_hat)],
        'rmse': [rmse(y,y_hat)],
        },index=[ind])
    return df

#Back to my own code:

def better_than_baseline(baseline_sse, model_sse):
    '''
    Takes in the SSE values for two models (note that the baseline or initial model
    must be entered as the first of the two arguments) and returns a statement declaring whether the alternative
    model beats the baseline, and by what percentage. If the model does not beat baseline, 
    the statement will list the percentage for how much worse the model performed relative
    to the baseline.'''
    #Calculating the difference between the baseline SSE and the model SSE:
    sse_diff = baseline_sse - model_sse
    if sse_diff > 0:
        #Determining the percentage improvement for the model over baseline:
        sse_diff_pct = round(((sse_diff / baseline_sse) * 100), 2)
        #Generating a format string that includes the percentage by which the model beat baseline:
        return print(f'The model performed better than the baseline and produced {sse_diff_pct}% less error.')
    elif sse_diff < 0:
        #Calculating the percentage increase in error the model produced over baseline:
        sse_diff_pct = abs(round(((sse_diff / baseline_sse) * 100), 2))
        #Generating a format string that includes the percentage by which the model increased error over baseline:
        return print(f'The model performed worse than the baseline and produced {sse_diff_pct}% more error.')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
from sklearn.feature_selection import SelectKBest, f_regression

def select_k_features(X_df, y_df, k):
    '''
    Takes in the X and y sets of a modeling DataFrame,
    as well as the number, k, of most important features
    to be selected. 
    '''
    #Creating the selector object:
    f_selector = SelectKBest(f_regression, k=k)

    #Finding the top k features correlated with y:
    f_selector.fit(X_df, y_df)

    # boolean mask of whether the column was selected or not:
    feature_mask = f_selector.get_support()

    #get list of top K features:
    f_feature = X_df.iloc[:, feature_mask].columns.tolist()

    #Returning list of features:
    return f_feature

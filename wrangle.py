import os
from env import get_db_url
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def get_zillow_data():
    '''
    First checks for a CSV containing the Zillow data for homes
    sold during 2017. If no CSV exists, queries the Codeup database 
    to retrieve relevant Zillow data, returns a DataFrame of the 
    information, and then creates a CSV file to cache the data for 
    future use.
    '''
    
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col = 0)
    else:
        # read the SQL query into a dataframe
        df = pd.read_sql('''SELECT
        bathroomcnt AS bathrooms,
        bedroomcnt AS bedrooms,
        taxvaluedollarcnt AS value,
        calculatedfinishedsquarefeet AS square_feet, 
        yearbuilt AS year_built,
        fips, 
        latitude,
        longitude,
        lotsizesquarefeet AS lot_size
        FROM properties_2017 
        LEFT JOIN predictions_2017 USING (parcelid) 
        LEFT JOIN propertylandusetype USING (propertylandusetypeid)
        WHERE propertylandusedesc IN ('Single Family Residential',
        'Inferred Single Family Residential') 
        AND YEAR(transactiondate) = 2017;''', get_db_url('zillow'))

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv(filename)

        # Return the dataframe to the calling code
        return df

def clearing_fips(df):
    '''This function takes in a DataFrame of unprepared Zillow information and generates a new
    'county' column, with the county name based on the FIPS code. Drops the 'fips' column and returns
    the new DataFrame.
    '''
    # create a list of our conditions
    fips = [
        (df['fips'] == 6037.0),
        (df['fips'] == 6059.0),
        (df['fips'] == 6111.0)
        ]
    # create a list of the values we want to assign for each condition
    counties = ['Los Angeles County', 'Orange County', 'Ventura County']
    # create a new column and use np.select to assign values to it using our lists as arguments
    df['county'] = np.select(fips, counties)
    df = df.drop(columns = 'fips')
    return df

def add_zillow_features(df):
    #Adding column that displays ration of bedrooms to bathrooms:
    df['bath_bed_ratio'] = df.bathrooms / df.bedrooms
    return df

def wrangle_zillow():
    '''Function to import zillow data from database and create a CSV cache of the file. 
    Function runs the clearing_fips function to generate counties and drop fips column, 
    then drops rows containing nulls, as well as rows with 0 bathrooms, 0 bedrooms, and 
    less than 12 sqft. Finally, converts 'bedroomcnt' and 'yearbuilt' columns to integers.
    Return wrangled DataFrame.
    '''
    #Acquire Data:
    df = get_zillow_data()
    #Run clearing_fips function:
    df = clearing_fips(df)
    #Drop Null Values:
    df = df.dropna()
    #Add bedroom-to-bathroom ratio column:
    df = add_zillow_features(df)
    #Drop listings that have 0.0 bathrooms, 0.0 bedrooms, are under the 120 sqft legal minimum as required by California to be considered a residence, are over 10,000 square feet, or are priced over $2.5 million:
    df = df.drop(df[(df.bedrooms == 0.0) | (df.bathrooms == 0.0) | (df.square_feet < 120.0) | (df.square_feet > 10000) | (df.value > 1600000) | (df.lot_size > 100000)].index)
    #Fixing the format of the latitude and longitude values:
    df['latitude'] = df.latitude * (10 ** -6)
    df['longitude'] = df.longitude * (10 ** -6)
    #Converting 'bedrooms' and 'year_built' columns to 'int' type:
    df = df.astype({'bedrooms' : int, 'year_built': int})
    return df

def split_zillow_data(df):
    '''
    Takes in a DataFrame containing the Zillow data, and splits the data into train, validate, and test sets.
    Returns the train, validate, and test sets.
    '''
    #Sets 20% of the data aside as the test set:
    train_and_validate, test = train_test_split(df, test_size = .2, random_state=456)
    #Sets 30% of the remaining 80% (24% of the total) aside as the validate set:
    train, validate = train_test_split(train_and_validate, test_size = .3, random_state = 456)
    return train, validate, test

def scale_zillow_data(train, validate, test):
    
    '''
    Takes in train, validate, and test sets, creates copies of those sets, and
    scales the copies. Returns train_scaled, validate_scaled, and test_scaled 
    DataFrames in which the county values are one-hot encoded and the numerical 
    values are scaled.
    '''
    
    #Defining the columns that need to be scaled:
    scaled_columns = ['bedrooms', 'bathrooms', 'square_feet', 'bath_bed_ratio', 'lot_size', 'year_built']
    
    #Creating scalable copies of the train, validate, and test sets:
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    #Creating the scaler object:
    scaler = MinMaxScaler()
    scaler.fit(train[scaled_columns])
    
    #Applying the scaler to the scalable colums within the train, validate, test copies:
    train_scaled[scaled_columns] = scaler.transform(train[scaled_columns])
    validate_scaled[scaled_columns] = scaler.transform(validate[scaled_columns])
    test_scaled[scaled_columns] = scaler.transform(test[scaled_columns])

    #Returning scaled dataframes:
    return train_scaled, validate_scaled, test_scaled

def encode_zillow_data(df, column_names = ['county']):
    '''
    Takes in the Zillow DataFrame and returns a version
    in which the county values are one-hot encoded for modeling.
    '''
    #Making the dummy columns for the encoded variable:
    dummy_df = pd.get_dummies(df[column_names], drop_first = True)

    #Concatenating dummy columns onto original dataframe:
    df = pd.concat([df, dummy_df], axis=1).drop(columns = column_names)
    
    #Returning DataFrame With Encoded Values:
    return df
    


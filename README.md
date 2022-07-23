# Predicting Home Prices With Regression
__Greg Maggard__ <br>
July 22, 2022

=========================================================================================================

## General Overview:
This project aims to use regression models to predict home values from the Zillow dataset containing listings from 2017.

### Main Goals:
- Use regression machine learning models to make predictions regarding housing prices. 
- Identify key features that can be used to create an effective predictive model.
- Use findings to make recommendations and establish a foundation for future work to improve model's performance. 

=========================================================================================================

### So What and Why?
- Improving this model provides significant opportunity for Zillow to increase their ability to accurately predict the valuation/sale price of a home, which is integral to its ability to attract customer, generate leads, and earn commissions on sales. 

=========================================================================================================

### Executive Summary:
- This project aims to improve upon an existing model to predict home prices for Zillow listings from 2017.
- Data was acquired by querying 2017 home data from the Zillow database. 
- Exploration was done to test some hypotheses about relationships between features. 
- Multiple regression models were run, ultimately finding Linear Regression to be the most effect, reducing the model's error by ~19.44%.
- I recommend deploying this model over the original for the time being, given that there is a 20% increase in model performance.
- Given more time, I'd like to continue to refine the model with current features, while also trying to add more home features and data into the dataset.

=========================================================================================================

## Project Plan:

### Acquisition:
- Querying data from the Zillow database for use in the model.
```SQL
SELECT 
    bathroomcnt AS bathrooms,
    bedroomcnt AS bedrooms,
    taxvaluedollarcnt AS value,
    calculatedfinishedsquarefeet AS square_feet,
    yearbuilt AS year_built,
    fips,
    latitude,
    longitude,
    lotsizesquarefeet AS lot_size
FROM
    properties_2017
        LEFT JOIN
    predictions_2017 USING (parcelid)
        LEFT JOIN
    propertylandusetype USING (propertylandusetypeid)
WHERE
    propertylandusedesc IN ('Single Family Residential' , 'Inferred Single Family Residential')
        AND YEAR(transactiondate) = 2017;
``` 

52,441 rows are returned, with the above 9 columns.

#### Data Dictionary: 

| Column/Feature | Description |
|--- | --- |
| __bathrooom__ | The number of bathrooms in the home. |
| __bedrooms__ | The number of bedrooms in the home. |
| __value__ | The tax-assessed value of the home. <br> __Not__ the home's ultimate sale price. |
| __square_feet__ | The home's square footage. |
| __year_built__ | The year the home was built. |
| __fips__ | "Federal Information Process System" code, used to <br> identify zip codes in the U.S. |
| __latitude__ | The latitude of the home. |
| __longitude__ | The longitude of the home. |
| __lot_size__ | The square footage of the lot on which <br> the home is built. |

=========================================================================================================

### Wrangling:

#### - General Data Format Cleaning:
- Converting moving decimal left 6 places on latitude and longitude.

#### - Assigning county names to each home, based on the fips code one the record:  
- 60370: Los Angeles County
- 60490: Orange County
- 61110: Ventura County

#### - Homes Dropped:
- Having 0 bedrooms
- Having 0 bathrooms
- Having less than 120 square feet
    - These homes to not meet the CA minimum to classify as a residence.
- Having more than 10,000 square feet
    - These homes make up a small portion of the set and could skew the model.
- Home value over 1.6 million dollars
    - These homes make up a small portion of the set and could skew the model.
- Having more than 100,000 square footage of lot size.
    - These homes make up a small portion of the set and could skew the model.
- Home records containing null values in any column.
    
#### - Columns Created:
- Column displaying the ratios of bedrooms to bathrooms.

#### Notes on Wrangling:
- All of these cleaning steps are carried out in the wrangle script, and leave 94.3\% of the data remaining. 
- I feel comfortable with the omission of this data, as I want to ensure that I'm not excluding too large a chunk of my total set, but do want to be sure that I'm focusing my model on homes that comprise the bulk of Zillow's business.

=========================================================================================================

### Exploration:

#### Key Questions Answered:
- Is there a significant relationship between square footage and home value?
    - __Statistical Finding: There is sufficient evidence to reject the null and assert that there is a significant relationship between square footage and the assessed value.__
- Is there a significant relationship between lot_size and home value?
    - __Findings: There is sufficient evidence to reject the null and assert that there is a significant relationship between lot size and the assessed value.__
- Is there a relationship between the county in which a home is built and its value?
    - __Statistical Finding: There is sufficient evidence to reject the null and assert that there is a meaningful relationship between home values and county.__
- Is there a relationship between the year a home is built and the square footage of a home?
    - __Statistical Finding: There is sufficient evidence to reject the null and assert that there is a meaningful relationship between home values and county.__

=========================================================================================================

### Modeling:
#### Baseline Model:
- Created a baseline model that uses no features, and simply takes the mean home value as the estimate.
- It's important to note here that there is no "machine learning" happening with this model; all it is doing is finding the mean assessed home value and saving that to a new column in the DataFrame.

#### Regression Model:
- Created and OLS linear regression model with 9 features to attempt to predict house values. 

#### Modeling Takeaways:
- The OLS Regression model beats the baseline by ~19.81% on the test set.

=========================================================================================================

## Conclusion:

### Key Findings:
- Home square footage, lot size, county, and build year all proved to be significant drivers of home value.
- The OLS Linear Regression model, with the features provided, was able to improve upon the baseline model by ~19.81%. I would expect that this will be the case on further out-of-sample data.

### Recommendations:
- I recommend deploying this linear regression model for now, as an improvement of nearly %20 over the current model means there is substantial financial benefit on the line.
- I'd also recommend perhaps doing more qualitative research to understand what factors customers look for in estimating a home's value.

### Next Steps:
- With the luxury of more time, I would like to further explore the variables in the dataset and see if I could find a better combination to refine the model.
- It would likely be worthwhile to look into acquiring more data on the homes to see if there are other factors that could be drivers of home value. 
    - There are factors like how recently a home has been renovated, proximity to quality schools or greenspaces, or myriad other aspects that could be considered.

=========================================================================================================

## Steps to Reproduce:
- Ensure that you have an env.py file that includes relevant database credentials to query the data.
- Download wrangle.py, evaluate.py, and explore.py files.
- Download and run the zillow_final_report.ipynb file.

=========================================================================================================

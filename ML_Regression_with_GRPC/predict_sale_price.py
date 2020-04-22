

import pandas as pd
import numpy as np



# Read the data and store in a dataframe called training_set
train_data_path ='train.csv'
training_set = pd.read_csv(train_data_path)

# Select the target variable and call it y
y = training_set.SalePrice

# Create a list of the predictor variables
predictors = ["MSSubClass","LotArea", "YearBuilt","BedroomAbvGr", "TotRmsAbvGrd"]

# Create a new dataframe with the predictors list
X = training_set[predictors]

# Import DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor

# Define the first model
tree_model = DecisionTreeRegressor()

# Fit model
tree_model.fit(X, y)


def predict_sale_price(MSSubClass, LotArea, YearBuilt, BedroomAbvGr, TotRmsAbvGrd):
    prediction = tree_model.predict([[MSSubClass, LotArea, YearBuilt, BedroomAbvGr, TotRmsAbvGrd]])
    return (prediction)













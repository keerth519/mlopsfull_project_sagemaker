"""data inspection and validation"""
#importing the pandas library
import pandas as pd 
#reading the raw csv file and  stroing it in  Datafram as df
df=pd.read_csv('data/raw/ai4i2020.csv')
#checking the how many rows and coluns in data set(10000rX14C)
print(df.shape)
#it will fetch the column name in data set 
print(df.columns.tolist())
#it will check the any missing values in every column 
print(df.isnull().sum())
#checking the number of  C and R in dataset 
print("Rows:", df.shape[0])
print("columns:", df.shape[1])

""" 
python src/data_Inspection.py

###  output  ####
HDF                        0
PWF                        0
OSF                        0
RNF                        0
dtype: int64
Rows: 10000
columns: 14 
"""
### Expected columns validation ###
Expected_columns = [
    "UDI",
    "Product ID",
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure",
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF"
]
print("actual columns:", list(df.columns))
print("Expected columns:", Expected_columns)
if list(df.columns)==Expected_columns:
    print("column validation pass")
else:
    print("column validation failed")
"""Data Preprocessing"""
### importing the pandas for data manipulation ###
import pandas as pd 
###  load the RAW CSV as  DATAframe as dF in Memory ###
df=pd.read_csv("data/raw/ai4i2020.csv")
###rows and columns check###
print(df.shape)
###fetch the first 5 records)
print(df.head())
"""removing the unneccessary columns  - UID  and 
product id in ML those are not direct usefull features """
df = df.drop(columns=["UDI", "Product ID"])
print("after removing unnecessary columns:")
print(df.shape)
###converting categorical(L,M,H) data to numerical data(0,1,2) 
df = pd.get_dummies(df, columns=["Type"], dtype=int)
print("after encoding Type")
print(df.head)
print(df.shape)
### separating the target varibales/OUTPUT from feature/input
Y = df["Machine failure"]  # input/features
X = df.drop(columns=["Machine failure"])  # input , Target
print("Feature shape:", X.shape)
print("Target shape:", Y.shape)


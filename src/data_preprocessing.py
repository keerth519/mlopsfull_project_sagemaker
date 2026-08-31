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
###converting categorical(L,M,H) data to numerical data(0,1,2)  #  ml algorithms 
df = pd.get_dummies(df, columns=["Type"], dtype=int)
print("after encoding Type")
print(df.head)
print(df.shape)
### separating the target varibales/OUTPUT from feature/input

Y = df["Machine failure"]  # output/Target 
X = df.drop(columns=["Machine failure"])  # input/feature 
print("Feature shape:", X.shape)
print("Target shape:", Y.shape)

""" processed data need to be save in data/processed 
and it have x and y both data """

df.to_csv("data/processed/processed_data.csv", index=False) ## cleaned and Encoded data 

print("processed data saved successfully")

""" when the raw features data is in Different ranges 
to provide the common scale algorithm we are going to do 
 feature enginerring  for example  air Temperature 208 ,
 process temperature 308 the values are different"""
 ### SPlit Data Set 
# Train_test_split is function is provided by Scikit(sklearn)
from sklearn.model_selection import train_test_split  
# Splitting the Data to Train and Test  of X and y 
X_train, X_test, Y_train, Y_test = train_test_split(
X,
Y,
test_size=0.2, # 20% test
random_state=42, # reproducible results
stratify=Y # maintain class distribution
)
print("X_train Shape:", X_train.shape)
print("X_test  shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)

##SAve and slipt the data
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
Y_train.to_csv("data/processed/Y_train.csv", index=False)
Y_test.to_csv("data/processed/Y_test.csv", index=False)
print("Train and Test datasets saved successfully.")





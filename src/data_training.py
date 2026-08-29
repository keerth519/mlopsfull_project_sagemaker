""" it need to verify the what columns /types 
are actually insode out current X_train.csv  and Y_train.csv"""
"""import pandas as pd
x=pd.read_csv('data/processed/X_train.csv')
y=pd.read_csv('data/processed/Y_train.csv')
print(x.dtypes)
print('X:', x.shape)
print ('Y:', y.shape)
print(y.head())"""
""" Output is X has 8000 recordes and 13features
 and Y have 8000 c and 1 target """
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
import joblib
import os 
import mlflow # to Track the Experiment 
import mlflow.sklearn 

# Load the Training data 
X = pd.read_csv("data/processed/X_train.csv") # it contains features used by model
y = pd.read_csv("data/processed/Y_train.csv") # it contains target that the model need to predict 
#convert traget from dataframe
# (8000, 1)(rows and columns) to series (8000,)(target values)  
y = y.squeeze()
print("X Shape:", X.shape)
print("Y Shape:", y.shape)
##an mlflow experiment groups realted model training runs 
mlflow.set_experiment("machine_failures_prediction")
### create the random forest model  and mlflow run 
""" Use a fixed random seed. 
Create the trees using random sampling, 
but ensure that the same random sampling is 
used in every run. This is what random_state=42 
helps achieve.
    """
#MLFLOW TRAIning RUn
with mlflow.start_run():
    # define model parameters
    n_estimators=100 # 100 experts (100 trees) - 100-decision-tree ,
    # max_depth=10, # Each tree can grow only up to 10 levels. 
    random_state=42 # While creating the trees, perform random selections.But use the same random selections every time the model is run. 
model = RandomForestClassifier(
    n_estimators=n_estimators,
    random_state=random_state,
    n_jobs=-1
)
#log parameters to mlflow
#these parameters will be visible in the MLFLOW UI:
mlflow.log_param("n_estimators", n_estimators)
mlflow.log_param("random_state", random_state)
### Train the model 
model.fit(X,y)
print("model Training is completed")
#Create a model Directory 
os.makedirs("models", exist_ok=True)
#save the Trained model
joblib.dump(model,"models/model.pkl")
 # joblib.dump() = "save the trained model into a file/path(directory)
print("model save successfully")
#log the trainind model to mlflow
#mlflow stores the model as an artifiact associated 
#with this particular training run.
mlflow.sklearn.log_model(
    model,
    "model"
)
print("model logged to mlflow")








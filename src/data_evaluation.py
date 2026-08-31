import pandas as pd
import joblib
##Using metrics from Sklearn library
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
# 1.load the Data Set 
#X_test contains the features used for evaluation 
X_test = pd.read_csv("data/processed/X_test.csv")
#Y_test contains the actual target values
Y_test = pd.read_csv("data/processed/Y_test.csv")
# 2.Load Trained model
# Load the model that we save During training
model = joblib.load("models/model.pkl")
#3.generate predictions
#use the trained modle to predict the target values
Y_pred = model.predict(X_test)
#4.calculate evaluation metrics
accuracy = accuracy_score(Y_test, Y_pred)
Precision = precision_score(Y_test, Y_pred , zero_division=0)
recall = recall_score(Y_test, Y_pred, zero_division=0)
f1 = f1_score(Y_test, Y_pred , zero_division=0)
# 5. Display Results
"""print("model evalluation Results")
print("_____________________")
print("Accuracy:", accuracy)
print("precision:", Precision)
print("recall:", recall)
print("f1score:", f1)"""
#in this file we have mertics we need to to log the mlflow
#Log evaluation metrics to mlflow
#start a new mlflow run for model evaluation
import mlflow
#Used the same mlflow experiment used for model training 
mlflow.set_experiment("machine_failures_prediction")
with mlflow.start_run():
    #log the model performance metrics
    mlflow.log_metric("Accuracy", accuracy)
    mlflow.log_metric("precision", Precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1score", f1)
    print("evaluation metrics logged to mlflow ")
## QUALITY GATE
ACCURACY_THRESHOLD = 0.8
PRECISION_THRESHOLD = 0.8
RECALL_THRESHOLD = 0.8
F1_THRESHOLD = 0.8
if (
    accuracy >= ACCURACY_THRESHOLD 
    and Precision >= PRECISION_THRESHOLD 
    and recall >= RECALL_THRESHOLD
    and f1 >= F1_THRESHOLD
):
    print("Quality Gate Passed")
else:
    print("Quality Gate Failed")
    raise SystemExit(1) # jenkins sees that as a failure and stops the pipeline deployment.
""" suppose evaluation metrics gives >=0.8 
Quality Gate Passed  python exits successfully --> 
jenkins can continue even one metrics will  the quality gate will be failed"""

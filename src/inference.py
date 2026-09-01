import os 
import io 
import joblib 
import pandas as pd

def model_fn(model_dir): 
##Load the trained Random Forest model from the SageMaker model directory.
    model_path = os.path.join(model_dir, "model.pkl")
    model = joblib.load(model_path)
    return model

def input_fn(request_body, request_content_type): 
# Convert incoming CSV request data into a pandas DataFrame. """
    if request_content_type == "text/csv":
       feature_name = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
        "TWF",
        "HDF",
        "PWF",
        "OSF",
        "RNF"
        "Type_H",
        "Type_L",
        "Type_M"
       ]
       data = pd.read_csv(io.StringIO(request_body), header=None) 
       data.columns = feature_name

       return data
    raise ValueError(
        f"Unsupported content type: {request_content_type}"
    )

def predict_fn(input_data, model):
#Run prediction using the trained model. """
    predictions = model.predict(input_data)
    return predictions

def output_fn(prediction, accept):
# Convert predictions into CSV response. """
    if accept == "text/csv":
        output = io.StringIO()
        for value in prediction:
            output.write(f"{value}\n")
        return output.getvalue(), accept
    raise ValueError(
         f"Unsupported accept type: {accept}"
       )

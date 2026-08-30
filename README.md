# mlopsfull_project_sagemaker
============================================================
first part 

  our workflow 

  github
    ||
Data collection --> validation -->preprocessing --> feature engineering --> Train/test split --> Dvc--s3
--------------
Terraform installation : wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
---------------
AWS CLI installation : 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
---------------

==============================================================
second part 
   model training --> we are here
   || 
   --> MLflow --> Evaluation   --->sagemaker model registry 
   --->s3 model artifacts+ECR container ---> sagemaker endpoint--< inference.py--> predictions 
    --> monitoring -->cloud watch --> Teams alert --> retraining --> jenkin ci/cd
==============================================================
Training the model (data_training.py)
==============================================================
Reminder 
x= input/feature 
y=target/output

=============
 data/processed/ --? x_train.cdv --> x_test.csv  -->y_tain.csv  -->y_test.csv
==============
 so Training uses  -->  x_train+y_train --> AL algorithm --> Trained model 
 and ---> x_test+y_test are not used for Training  they kept aside for evaluation
============
   x_test+y_test  --> Trained Model --> predictions --> compare with y_test
=============
 What model will we use ?
  our data set is the AI4I2020 predictive maintainence dataset.
  The Target is whether a machine Experiences a failure .
  so this is a classification problem for our model lets use : RANDOM FOREST Classifier
==============
  Classification:  it will decide which the category or       class or classification that model should be 
      it will represe as class or category 
  example :   Email --> Spam ?
             Output --> Yes / No
Regression : in Regression the Output is not a category it is numeric value 

Examples:
    House Features
       Predicted Price = ₹52,30,000
========================
Trees in Randomeforstclassifires :

 "If I have 8000 records and Random Forest with 100 trees, each tree learns patterns from random samples of those 8000 records. During prediction, all 100 trees vote, and the majority vote becomes the final prediction."

 100 trees = 100 decision-makers (100 Decision Trees)
        Example
            Tree 1 -> 8000 records nundi random sample
            Tree 2 -> 8000 records nundi random sample
            Tree 3 -> 8000 records nundi random sample
            Tree 100 -> 8000 records nundi random sample
==========================
## squeeze : it used to clean the data shape in NumPy/Pandas 
      Many machine learning algorithms (such as RandomForestClassifier) expect the target variable y to be a 1-dimensional Series, not a 2-dimensional DataFrame.
          Example : (100,)  - one dimentsional  series 
=============
load the Data 
=============
create a randomforest  model 
============
traing the model buy using .fit
===========
create model directory with os.makedirs
==============
save the Training model byusing joblib with dump action 
=============================================================
Tracking the Experiment 
=============================================================
--->pip install mlflow
---> Mflow UI  (like - http://127.0.0.1:5000)  - directly click on this - don't open it manually copy and paste

1.Experiment  - it will group the Related training runs of Machine failure prediction 
2.Run - one training execution  i will automatically generate the Run name 
parameters 
3.Metrics : for to track the model performance (accuracy)
Arttifacrs : Model. Plots , files Etc,
4.model Logging  : by using sklearn 
5.mlflow UI - compating the runs (parameters, metrics, artifacts)
6.Model Registry - versioning +model lifecyscle management 

We use mlflow tracking for Experiment tracking - logging training parameters , evaluation metrics and model artifacts so that  different training runs can be compared and Reproduced 

==============================================================
DATA EVALUATION(data_evaluation.py)
==============================================================
    1. load X_test.csv 
    2. laod Y_test.csv
    3. load model/model.pkl
    4. generate predictions
    5. calculate evaluation metrics  through MLFLOW
    6.Used the same mlflow experiment used for model training 
    7. save the metrics  for MLFLOE
    8.#log the model performance metrics MLFLOw
     so later jenkins CI?cd can automatically check whether the model is good enough
     
work flow

  data --> datavalidation-->model Training --> mlflow -->parameters
       ||
          -->n_estimators =100 ; random_state=42
    -->model evaluation 
         || --> MLflow
                   ||
                     ---> Accuracy , precision , recall , f1
we use primarily for experiment tracking --Logging parameters and evaluation metrics. model registration is handled by sagemaker 
==============================================================
sagemaker model Registry
==============================================================
architecture 
model.pkl-artifacts --> s3  --> sagemaker model package group --> model version 1
============

-->  need to store the artifacts to s3 
     we have already configure the AWS cli in our machine so check the data  access keys 
        "aws sts get-caller-identity"
    chekcing correct region in Terminal
         "aws configure get region"
        move to cd infrastructure 
          terraform plan --> terraform apply
          Bucket has been created in AWS 
        Terraform output
        terraform state list
     terraform state show aws_s3_bucket.mlops_data | head -20
--> " find models -type f " --> this will exactly what inside the  models
---> " ls -lh models/model.pkl "  --> it will verify to  show the first file size and permission 
========
we are pushing the data through DVC 
  dvc remote list
  dvc status
  dvc add models/model.pkl
----------------
git status 
dvc add models/model.pkl
git  add models/model.pkl
las -la models
Git status
DVC push
git status 
git add .
git coomit -m "second commit"
git push origin miam
-----------------------

mlflow.db --> mlruns we should not put in git  and  as well 
model.pkl --> dvc  --model.pkl.dvc --github
    model.pkl --> s3/dvc remote
-------
without dvc directly pushing to s3
---> aws s3 cp models/model.pkl s3://mlops-full-project-sagemaker-data-2026/model.pkl   ---> it will upload the file to s3 bucket 
===============
sagemaker model registry 
===================
s3 model.pkl --> sagemaker model --> model package -> modle Package group --> version 1
s3 --> model.tar.gz / model artifacts
ecr --> inference container 
            || --> sagemaker model registry --> model Vesrion 
NOTE: creating the model package group = creating the container/group in registry then actual mode registration step





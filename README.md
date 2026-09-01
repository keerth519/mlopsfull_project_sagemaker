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

TO install in Docker and root as jenkins 

docker exec -u root jenkins bash -c "apt-get update && apt-get install -y wget gpg && wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo 'deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com bookworm main' > /etc/apt/sources.list.d/hashicorp.list && apt-get update && apt-get install -y terraform"
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



    #### we can't we maintain metrics for training data 

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

### suggestion is inference.yaml file --> s3  and  
#### docker file  ---> ecr --> sagemaker studio those file for the endpoint 
### FAST API Training face itself

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
---------------
Sage maker model package group : 
NOTE: creating the model package group = creating the container/group in registry then actual mode registration step
after creating the infra about the package group then need to register the model vesrion 
------------------------
s3 --> model.tar.gz / model artifacts
----------
-- tar -czvf models/model.tar.gz -C models model.pkl  --  converting  .pkl to model.tar.gc (sagemaker - friendly packaged model artifact)
----------
---ls -lh models/
--- aws s3  ls s3://mlops-full-project-sagemaker-data-2026/ (view the list )
---aws s3 cp models/model.tar.gz s3://mlops-full-project-sagemaker-data-2026/model.tar.gz  (for to upload the tar file in s3 )
----------------
sagemkaer model Registry 
      will create the modelversion in model registry 
    sagemaker model registry registration required iamrole+image URL

--- infra code in terraform/main.tf ( for sagenaker package group and model registry(inference container))  

-- pip install sagemaker (src/importsagemaker.py)
## run this code as project root
    python -c "import sklearn, joblib; print('sklearn:', sklearn.__version__); print('joblib', jobli
b.__vesrion__)"   ## it will which sagemaker image tag to put in main.tf 
###  
  pip show joblib | grep Version   --(To show the version of joblib)

  now we got the vesion of sagemaker and joblib to update in main.tf 

#### Important :  sagemaker container version mainly depends on scikit-learn compatability and we can't decide the sagemaker maker by using joblib version 

pip install scikit-learn==1.4.2  
###  sagemaker support the scikit-learn framework  version 1.4.2 , aws lists it as the current supported version.  out trained modek has was created with scikitlearn 1.9.0, we shodn't to register this 1.90 model inside a 1.4.2 container , that can be model-loading/version - compatability problems 
### aws says the 1.4.2 container requires python 3.1o+joblin >-1.5.2  , now our joblib already satisfies that requiremnent 
      ------  current --> sklearn 1.9.0 -- change to sklearn 1.4.2 ---> train again --> model.pkl ---> model.tar.gz --> s3 --> sagemaker model Registry 
retraining the model 
           again we need to run the data_training.py -->  remove existing Tar.gz file --> create and convert already trained .mkl file to tar.gz ---> push to s3 --> execute the Evaluation.py file --> o/p -- evalauation ,etrics logged to mlflow

check the packages before register the model 
### aws sagemaker list-model-packages --model-package-group-name mlops-full-proejct-models --region ap-southeast-2
To check the Repositories 
### aws ecr describe-repositories --region ap-southeast-2
if not container image has been dispayed import the eaxt IMAGE URI from that specifi region
### pythin -c import sys; print (sys.version)
To check the Sagemaker version 
###  python -c "import importlib.metadata; print(importlib.metadata.version('sagemaker'))"
sagamker version --> 3.21.0  and scikit-learn - 19.0 and joblib - 1.5.3 sagemaker sklearn container 1.4-2

Model has been registered so we can retirve through command line as of now so visualise and from console or UI representation we need to setup the infra for sagemaker studio by creating domain and user by applying the iam policies and roles 

 "ModelPackageGroupName": "mlops-full-project-models",
            "ModelPackageGroupArn": "arn:aws:sagemaker:ap-southeast-2:129898827031:model-package-group/mlops-full-project-models",
            "ModelPackageGroupDescription": "Model Registry for Machine Failure Prediction models",
            "CreationTime": "2026-08-29T19:03:27.738000+00:00",
            "ModelPackageGroupStatus": "Completed"

=================================================================================================
CI/CD pipeline :
=================================================================================================
it containes -- >github -->jenkins-->
                              ||
                               -----> 1. checkout the code 
                               ------> 2. install dependencies
                               -------> 3. runtests
                               -------> 4. data validation /preprocessing 
                               -----> 5. Train model
                               -----> 6.evaluate model
                              ------> 7.log experiment --> Mlflow
                              ------->8. package the model
                               ------>9.push artifacts--> s3
                               -----> 10.register model --> sagemaker model registry
                              -------> 11. Quality gate
                                             ||
                                              ----> FAIL --> STOP
                                              ----> Pass --> continue
                              ------->12. deploy --> sagemaker endpoint
                              ------> 13. cloudwatch monitoring
                               -----> SNS ---> email alerts
-----------------------------------
JENKINS -->  jenkins controller --> jenkins agents/workers --> ephemeral build agents 
----------------------------------
we use jenkins to orchestrate the ml pipeline .it check out the code from git , installs dependencies , runs tests and validation , triggers model training and evaluation , logs experiments to mlflow , stores the model artifacts in s3 , register the model in sagemaket model registry , applies a metric -based quality gate , and if the model passes , deploy it to a sagemaker endpoint . cloudwatch monitors the endpoint and SNS send alerts
-------------------------------

I am building the jenkins through Docker container without ec2 instances
     --> docket -- version (to check the docker is present are not in current environment )
     pulling the Jenkins image 
      ---> docker pull jenkins/jenkins:lts-jdk21
    Starts the jenkins container 
      ---->    docker run -d \
               --name jenkins \
               -p 8080:8080 -p 50000:50000 \
               -v jenkins_home:/var/jenkins_home \
                jenkins/jenkins:lts-jdk21
    check the container  --> docker ps 
    check the password by using ---> docker logs jenkins
--------------------------------------
  NOTE : if  the port is not farwading to browser cntrl+shft+p --  type ports: forward port --> enter 
  it will ask for port ot it will another tab beside of terminal
  like 8080 click it will open the jenkins page 
--------------------------------------
   pip freeze  
   it will give the  dependent libraries
   pip freeze | grep -Ei "boto3|sagemaker|mlflow|scikit-learn|pandas|numpy|joblib|dvc|dvc-s3"
-----------------
   pipeline has been created for venv, checkout, install dependencies , validate , train , evalaute(Jenkinsfile)
---------------
      to go to the jenkins container as root in your terminal 
        docker  exec -u 0 -it jenkins bash
        python has been installed and moved to main branch
------------------
     dependency conflicts has been occured while running requirement.txt file so fixed 
-----------------
   df -h
   du -sh /var/jenkins_home/* 2>/dev/null | sort -h
   du -sh /var/jenkins_home/workspace/* 2>/dev/null | sort -h
   we seapeareted the requirement.txt and requirement-ci.txt for light weight image for libraries to avoid the space issue 
   and we have missed to add the preprocessing stage in pipeline that is also added with mkdir 
   and finnaly pipeline successfully executed 
   then setupthe webhook in github to trigger the pipeline automatically when code changes and push to main branch 
     -- added the trigger in job - configure 
     gihub --> setting --> actions --> webhooks --> create --> added the jenkins url as playload url  and content type as json and enable SSL 
------------------------
URL for payload - https://verbose-giggle-x5wjwq6rg9p4fp4j-8080.app.github.dev/github-webhook/ -- jenkins url - https://verbose-giggle-x5wjwq6rg9p4fp4j-8080.app.github.dev/job/mlops-full-project/
we are removing the from job to end and adding the github-webhook in that place 
---------------------
aws sts get-caller-identity
 ps  aux | grep jenkins
history | grep -i jenkins | tail -20
docker ps -a 
docker start  jenkins
 grep -r "awscc" infrastructure
 docker exec jenkins terraform version
 docker exec jenkins aws --version
 docker exec -u root jenkins bash -c "apt-get update && apt-get install -y awscli"
 --------------------
 successfully registered the model in sagemkaer registery as package model(AWScc) 
 =====================================
 QUALITy GATES (data_evaluation.py)
 =====================================
    is model performance meets our minimum acceptable cireria ? --> cd continue . if no --> deployment STOP.
    metrics will be logged to the mloflow and jenkins direct will tell pass or fail
    step 1 --> decide quality thresholds
            accuracy >=0.00 , precision >=0.00 , recall >=0.00 , f1 >=0.00
    step2 --> modify evalauation / quantity-gate logic 
    step3 --> jenkins reads the result 
    step 4 -->PASS --> deployment 
    STEP5 --> FAIL --> exits 1 and jenkins stops

Sage maker need i am execution role 
in our project --> iam user --> access keys     --> jenkins/terraform -->aws
    sage maker execution role                   ---> sagemaker --> s3/ecr/cloudwatch
  --> created the iam role thorugh Infra
  next : sagemaker model  creation
  next : endpoint configuration
  next : sage maker endpoint
                  S3
                 │
          model.tar.gz
                 │
                 ▼
         SageMaker Model
                 │
                 ▼
      Endpoint Configuration
         │             │
      Model       ml.t2.medium
         │             │
         └──────┬──────┘
                ▼
      SageMaker Endpoint
                │
                ▼
         Live inference
  error while creating sagemaker endpoint 
     Error: waiting for SageMaker AI Endpoint (mlops-failure-prediction-endpoint) create: unexpected state 'Failed', wanted target 'InService'. last error: The primary container for production variant primary did not pass the ping health check. Please check CloudWatch logs for this endpoint.
│  for that we have chekced cloudwatch logs from we that have decided to write the inference.py
  ======================================================
  inference code tells the container how to load the model and process request . 
  -----------------------------------------------------------
  python -c "import joblib; m=joblib.load('models/model.pkl'); print(type(m))" python -c "import joblib;

     aws sagemaker describe-endpoint  --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --query 'endpointStatus'
     
      aws sagemaker describe-endpoint  --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --query 'EndpointStatus'
      aws sagemaker describe-endpoint  --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --query 'EndpointStatus' --output text
  INFERENCE prediction command throufh cli

     aws sagemaker-runtime invoke-endpoint --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --content-type text/csv --body fileb://test_request.csv /tmp/predictions.txt
INFERENCE REsPONSe 
aws sagemaker-runtime invoke-endpoint --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --content-type text/csv --accept text/csv --body fileb://../test.csv ./response.json

     to show the log stream 
       aws logs describe-log-streams --log-group-name "/aws/sagemaker/Endpoints/mlops-failure-prediction-endpoint" --region ap-southeast-2 --order-by LastEventTime --descending --max-items 1
       aws logs get-log-events --log-group-name "/aws/sagemaker/Endpoints/mlops-failure-prediction-endpoint" --log-stream-name "primary/i-0299588a1433c8aa4" --region ap-southeast-2 --limit 50
    aws sagemaker describe-endpoint --endpoint-name mlops-failure-prediction-endpoint --region ap-southeast-2 --query '{Status:EndpointStatus,Config:EndpointConfigName}'

The sage maker endpoint configuration and sagemaker endpoint with inference Request and Resposne has been configured through terraform 
Predictions has been provided and got the Repdections as well 
---------------------------------
building the pipeline from Quality gate to sagemaker endpoint to get the predection from new data 

----------------
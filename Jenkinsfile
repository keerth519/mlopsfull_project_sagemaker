pipeline {
    agent any

    environment {
        PYTHON_ENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                git branch: 'main',
                    url: 'https://github.com/keerth519/mlopsfull_project_sagemaker.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing dependencies..."
                sh '''
                    python3 -m venv ${PYTHON_ENV}
                    . ${PYTHON_ENV}/bin/activate
                    python -m pip install --no-cache-dir -r requirements-ci.txt
                '''
            }
        }

        stage('Validate') {
            steps {
                echo "Validating dataset and code..."
                sh '''
                    . ${PYTHON_ENV}/bin/activate
                    python src/data_validation.py
                '''
            }
        }
        stage('preprocess') {
            steps {
                echo "preprocessing dataset and code..."
                sh '''
                    mkdir -p data/processed
                    . ${PYTHON_ENV}/bin/activate
                    python src/data_preprocessing.py
                '''
            }
        }
        stage('Train') {
            steps {
                echo "Training Model..."
                sh '''
                    . ${PYTHON_ENV}/bin/activate
                    python src/data_training.py
                '''
            }
        }

        stage('Evaluate') { steps { echo "Evaluating Model..."

            script {
                 env.EVAL_STATUS = sh(
                script: '''
                . ${PYTHON_ENV}/bin/activate
                python src/data_evaluation.py
            ''',
            returnStatus: true
        ).toString()
    }
}
}

        stage('Quality Gate') { steps { script { echo "Checking model quality..."

             if (env.EVAL_STATUS == '0') {
                echo "Quality Gate PASSED"
                echo "All model metrics meet the required thresholds."
             } 
            else {
                echo "Quality Gate FAILED"
                echo "Model does not meet the required thresholds."
                error("Pipeline stopped because Quality Gate failed.")
        }
    }
}
}
        stage('Register Model') {
            steps {
                echo "Registering model in sagemaker model registry..."
                  sh '''
                    echo " packaging trained model .."
                    tar -czvf models/model.tar.gz -C models model.pkl
                '''
                script {
                withCredentials([
                    usernamePassword(

                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]){
                   sh '''
                    echo "uploading files to s3"
                    aws s3 cp models/model.tar.gz s3://mlops-full-project-sagemaker-data-2026/model.tar.gz
                    echo " registering model in sagemaker modle registry .."
                    cd infrastructure
                    terraform init 
                    terraform import aws_s3_bucket.mlops_data mlops-full-project-sagemaker-data-2026 || true
                    terraform import aws_sagemaker_model_package_group.mlops_model_group arn:aws:sagemaker:ap-southeast-2:129898827031:model-package-group/mlops-full-project-models || true
                    terraform import aws_iam_role.sagemaker_execution_role mlops-sagemaker-execution-role || true
                    terraform import aws_sagemaker_model.mlops_model mlops-failure-prediction-model || true
                    terraform import aws_sagemaker_endpoint_configuration.mlops_endpoint_config mlops-failure-prediction-endpoint-config || true
                    terraform import aws_sagemaker_endpoint.mlops_endpoint mlops-failure-prediction-endpoint || true
                    terraform plan
                    terraform apply -auto-approve
                '''
                }  
              
            }
         }
     }
        stage('Endpoint Test') {
             steps { 
                echo "Testing SageMaker endpoint..."

                script {
                withCredentials([
                    usernamePassword(
                         credentialsId: 'aws-credentials',
                         usernameVariable: 'AWS_ACCESS_KEY_ID',
                         passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                      )
                   ]) {
                    sh '''
                        echo "Creating test data..."
                        echo "5.1,3.5,1.4,0.2" > test.csv
                    '''
                    sh '''
                        set -e

                        export AWS_DEFAULT_REGION=ap-southeast-2

                        ENDPOINT_NAME="mlops-failure-prediction-endpoint"

                        echo "Checking SageMaker endpoint status..."

                        for i in $(seq 1 20); do

                            STATUS=$(aws sagemaker describe-endpoint \
                                --endpoint-name "$ENDPOINT_NAME" \
                                --region "$AWS_DEFAULT_REGION" \
                                --query 'EndpointStatus' \
                                --output text)

                            echo "Endpoint status: $STATUS"

                           if [ "$STATUS" = "InService" ]; then
                              break
                           fi

                           if [ "$STATUS" = "Failed" ]; then
                              echo "ERROR: SageMaker endpoint deployment failed."
                              exit 1
                           fi

                            echo "Waiting for endpoint..."
                            sleep 30

                        done

                        if [ "$STATUS" != "InService" ]; then
                            echo "ERROR: Endpoint did not become InService."
                            exit 1
                       fi

                       echo "Endpoint is InService."
                       echo "Invoking endpoint with test data..."

                       aws sagemaker-runtime invoke-endpoint \
                            --endpoint-name "$ENDPOINT_NAME" \
                            --region "$AWS_DEFAULT_REGION" \
                            --content-type text/csv \
                            --accept text/csv \
                            --body fileb://test.csv \
                            prediction.txt

                        echo "Prediction received:"
                        cat prediction.txt

                        if [ ! -s prediction.txt ]; then
                            echo "ERROR: Prediction file is empty."
                            exit 1
                        fi

                        echo "Endpoint integration test PASSED."
                   '''
        }
    }
}
}
  }
}


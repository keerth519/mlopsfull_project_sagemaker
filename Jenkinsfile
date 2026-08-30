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

        stage('Evaluate') {
            steps {
                echo "Evaluating Model..."
                sh '''
                    . ${PYTHON_ENV}/bin/activate
                    python src/data_evaluation.py
                '''
            }
        }
        stage('Register Model') {
            steps {
                echo "Registering model in sagemaker model registry..."
                sh '''
                    echo " packaging trained model .."
                    tar -czvf models/model.tar.gz -C models model.pkl

                    echo " registering model in sagemaker modle registry .."
                    
                    cd infrastructure
                    terraform init 
                    terraform apply -auto-approve
                '''
            }
        }
    }

}
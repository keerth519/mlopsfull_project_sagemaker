pipeline {
    agent any

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
                   
                    pip install --upgrade pip
                    pip install -r requirement.txt
                '''
            }
        }

        stage('Validate') {
            steps {
                echo "Validating dataset and code..."
                sh '''
                    python src/data_validation.py
                '''
            }
        }

        stage('Train') {
            steps {
                echo "Training Model..."
                sh '''
                
                    python src/data_training.py
                '''
            }
        }

        stage('Evaluate') {
            steps {
                echo "Evaluating Model..."
                sh '''
                 
                    python src/data_evaluation.py
                '''
            }
        }
    }

}
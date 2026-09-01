#terraform Declaration

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

#providers
provider "aws" {
  region = "ap-southeast-2" # Sydney
}
provider "awscc" {
  region = "ap-southeast-2" # Sydney
}
## i am role for sagemaker 

resource "aws_iam_role" "sagemaker_execution_role" {
  name = "mlops-sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_s3_bucket" "mlops_data" {
  bucket = "mlops-full-project-sagemaker-data-2026"
}
resource "aws_s3_object" "model" {
  bucket = aws_s3_bucket.mlops_data.id
  key    = "model.tar.gz"
  source = "../models/model.tar.gz"
  etag = filemd5("../models/model.tar.gz)
}
  #sagemaker model registry
  #this creates a model package Group where different versions of out trained ml model can be registered  and managed
resource "aws_sagemaker_model_package_group" "mlops_model_group" {
  model_package_group_name        = "mlops-full-project-models"
  model_package_group_description = "Model Registry for Machine Failure Prediction models"

  tags = {
    Environment = "dev"
    Project     = "MLops"
    managed     = "Terraform"
  }
}
   # Regestring the model version in Sagemaker Ai
resource "awscc_sagemaker_model_package" "mlops_model" {
  model_package_group_name  = aws_sagemaker_model_package_group.mlops_model_group.model_package_group_name
  model_package_description = "Machine Failure Prediction Model Version 1"
  depends_on                = [aws_s3_object.model]
  inference_specification = {
    containers =[
      {
        image          =  "783357654285.dkr.ecr.ap-southeast-2.amazonaws.com/sagemaker-scikit-learn:1.4-2-cpu-py3"
        model_data_url = "s3://mlops-full-project-sagemaker-data-2026/model.tar.gz"
      }
    ]

    supported_content_types       = ["text/csv"]
    supported_response_mime_types = ["text/csv"]
  }
}
resource "aws_iam_role_policy_attachment" "sagemaker_execution_policy" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
   #Sagemaker model 
resource "aws_sagemaker_model" "mlops_model" {
  name               = "mlops-failure-prediction-model"
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn
  primary_container {
    image          = "783357654285.dkr.ecr.ap-southeast-2.amazonaws.com/sagemaker-scikit-learn:1.4-2-cpu-py3"
    model_data_url = "s3://mlops-full-project-sagemaker-data-2026/model.tar.gz"
    environment = {
      SAGEMAKER_PROGRAM = "inference.py"
      SAGEMAKER_SUBMIT_DIRECTORY = "s3://mlops-full-project-sagemaker-data-2026/model.tar.gz"
    }
  }
}
   #Awssagemakerendpoint configuration
resource "aws_sagemaker_endpoint_configuration" "mlops_endpoint_config" {
  name = "mlops-failure-prediction-endpoint-config"
  production_variants {
    variant_name           = "primary"
    model_name             = aws_sagemaker_model.mlops_model.name
    initial_instance_count = 1
    instance_type          = "ml.t2.medium"
  }
}
  #Sagemaker endpoint
resource "aws_sagemaker_endpoint" "mlops_endpoint" {
  name                 = "mlops-failure-prediction-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.mlops_endpoint_config.name
}



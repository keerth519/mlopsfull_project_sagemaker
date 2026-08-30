#terraform Declaration

terraform {
required_version = ">= 1.5"
required_providers {
aws = {
source = "hashicorp/aws"
version = "~> 5.0"
       }
   }
}

#providers
provider "aws" {
region = "ap-southeast-2" # Sydney
}

resource "aws_s3_bucket" "mlops_data" {
bucket = "mlops-full-project-sagemaker-data-2026"
}
resource "aws_s3_object" "model" {
  bucket = aws_s3_bucket.mlops_data.id
  key = "model.tar.gz"
  source = "../models/model.tar.gz"
}
#sagemaker model registry
#this creates a model package Group where different versions of out trained ml model can be registered  and managed
resource "aws_sagemaker_model_package_group" "mlops_model_group" {
  model_package_group_name        = "mlops-full-project-models"
  model_package_group_description = "Model Registry for Machine Failure Prediction models"

  tags = {
    Environment = "dev"
    Project     = "MLops"
    managed = "Terraform"
  }
}
# Regestring the model version in Sagemaker Ai
resource "awscc_sagemaker_model_package" "mlops_model" {
  model_package_group_name = aws_sagemaker_model_package_group.mlops_model_group.model_package_group_name
  model_package_description = "Machine Failure Prediction Model Version 1"
  depends_on = [aws_s3_object.model]
  inference_specification = {
    containers = [
      {
      image = "783357654285.dkr.ecr.ap-southeast-2.amazonaws.com/sagemaker-scikit-learn:1.4-2-cpu-py3"
      model_data_url = "s3://mlops-full-project-sagemaker-data-2026/model.tar.gz"
    }
  ]
  
    supported_content_types = ["text/csv"]
    supported_response_mime_types = ["text/csv"]
}
}


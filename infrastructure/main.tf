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

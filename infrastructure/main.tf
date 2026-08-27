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

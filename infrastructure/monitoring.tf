
#SNS Topic for MLOps Alerts

resource "aws_sns_topic" "mlops_alerts" {
  name = "mlops-sagemaker-alerts"
}


#SNS Email Subscription

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.mlops_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

#CloudWatch Log Metric Filter DETECTS error message from Sagemaker LOGs

resource "aws_cloudwatch_log_metric_filter" "sagemaker_errors" {
  name           = "mlops-sagemaker-errors"
  log_group_name = "/aws/sagemaker/Endpoints/mlops-failure-prediction-endpoint"
  pattern        = "ERROR"

  metric_transformation {
    name      = "InferenceErrors"
    namespace = "MLOps/SageMaker"
    value     = "1"
  }
}

#ALARM -1 Application / inference Errors CloudWatch Alarm

resource "aws_cloudwatch_metric_alarm" "sagemaker_error_alarm" {
  alarm_name        = "mlops-sagemaker-inference-errors"
  alarm_description = "Alert when SageMaker inference errors occur"

  namespace   = "MLOps/SageMaker"
  metric_name = "InferenceErrors"

  statistic          = "Sum"
  period             = 60
  evaluation_periods = 1

  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 1

  alarm_actions = [
    aws_sns_topic.mlops_alerts.arn
  ]
}

# Alarm 2: SageMaker 5XX Errors Detect failed endpoint invocations

resource "aws_cloudwatch_metric_alarm" "sagemaker_5xx_alarm" {
  alarm_name        = "mlops-sagemaker-5xx-errors"
  alarm_description = "Alert when SageMaker endpoint returns 5XX errors"

  namespace   = "AWS/SageMaker"
  metric_name = "Invocation5XXErrors"

  dimensions = {
    EndpointName = "mlops-failure-prediction-endpoint"
    VariantName  = "primary"
  }

  statistic          = "Sum"
  period             = 60
  evaluation_periods = 1

  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 1

  alarm_actions = [
    aws_sns_topic.mlops_alerts.arn
  ]
}

# Alarm 3: High Model Latency SageMaker ModelLatency is measured in microseconds 2,000,000 microseconds = 2 seconds

resource "aws_cloudwatch_metric_alarm" "sagemaker_latency_alarm" {
  alarm_name        = "mlops-sagemaker-high-latency"
  alarm_description = "Alert when SageMaker model latency exceeds 2 seconds"

  namespace   = "AWS/SageMaker"
  metric_name = "ModelLatency"

  dimensions = {
    EndpointName = "mlops-failure-prediction-endpoint"
    VariantName  = "primary"
  }

  statistic          = "Average"
  period             = 60
  evaluation_periods = 1

  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 2000000

  alarm_actions = [
    aws_sns_topic.mlops_alerts.arn
  ]
}
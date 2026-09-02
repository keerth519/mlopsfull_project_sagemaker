#adding the email varibale to get alert from clouwatch based on metric and cloudwatch filter

variable "alert_email" {
  description = "Email Address for MLOPS CLoud watch alerts"
  type        = string
}


resource "aws_sns_topic" "project_alerts" {
  name = "DistriTask-alerts"

  tags = {
    Name        = "DistriTask Alerts"
    Environment = "production"
  }
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.project_alerts.arn
  protocol  = "email"
  endpoint  = "mustafa09402@gmail.com"
}

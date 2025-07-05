# قائمة بالـ instances الفعالة حالياً
locals {
  active_instances = {
    public_instance_1_az1  = aws_instance.public_instance_1_az1.id
    private_instance_1_az1 = aws_instance.private_instance_1_az1.id

    # public_instance_2_az1  = aws_instance.public_instance_2_az1.id
    # public_instance_3_az1  = aws_instance.public_instance_3_az1.id
    # public_instance_1_az2  = aws_instance.public_instance_1_az2.id
    # private_instance_1_az2 = aws_instance.private_instance_1_az2.id
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_alarms" {
  for_each = local.active_instances

  alarm_name          = "high-cpu-${each.key}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "CPU utilization alarm for ${each.key}"
  alarm_actions       = [aws_sns_topic.project_alerts.arn]
  ok_actions          = [aws_sns_topic.project_alerts.arn]

  dimensions = {
    InstanceId = each.value
  }

  tags = {
    Name = "CPU-Alert-${each.key}"
  }
}

resource "aws_cloudwatch_metric_alarm" "health_alarms" {
  for_each = local.active_instances

  alarm_name          = "health-check-${each.key}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Maximum"
  threshold           = "0"
  alarm_description   = "Health check alarm for ${each.key}"
  alarm_actions       = [aws_sns_topic.project_alerts.arn]

  dimensions = {
    InstanceId = each.value
  }

  tags = {
    Name = "Health-Alert-${each.key}"
  }
}

resource "aws_cloudwatch_metric_alarm" "network_alarms" {
  for_each = local.active_instances

  alarm_name          = "high-network-${each.key}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "NetworkIn"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "10000000" # 10MB
  alarm_description   = "High network usage for ${each.key}"
  alarm_actions       = [aws_sns_topic.project_alerts.arn]

  dimensions = {
    InstanceId = each.value
  }

  tags = {
    Name = "Network-Alert-${each.key}"
  }
}

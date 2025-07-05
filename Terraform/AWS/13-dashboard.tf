resource "aws_cloudwatch_dashboard" "project_dashboard" {
  dashboard_name = "ProjectInstancesDashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 24
        height = 6

        properties = {
          metrics = [
            for instance_name, instance_id in local.active_instances : [
              "AWS/EC2", "CPUUtilization", "InstanceId", instance_id
            ]
          ]
          period = 300
          stat   = "Average"
          region = "us-east-1"
          title  = "CPU Utilization - All Active Instances"
        }
      }
    ]
  })
}

output "public_instance_1_az1" {
  value       = aws_instance.public_instance_1_az1.public_ip
  description = "Public IP of the first EC2 instance in the public subnet (AZ1)"
}

# output "public_instance_2_az1" {
#   value       = aws_instance.public_instance_2_az1.public_ip
#   description = "Public IP of the second EC2 instance in the public subnet (AZ1)"
# }

# output "public_instance_3_az1" {
#   value       = aws_instance.public_instance_3_az1.public_ip
#   description = "Public IP of the third EC2 instance in the public subnet (AZ1)"
# }

output "private_instance_1_az1" {
  value       = aws_instance.private_instance_1_az1.private_ip
  description = "Private IP of the first EC2 instance in the private subnet (AZ1)"
}

# output "public_instance_1_az2" {
#   value       = aws_instance.public_instance_1_az2.public_ip
#   description = "Public IP of the first EC2 instance in the public subnet (AZ2)"
# }

# output "private_instance_1_az2" {
#   value       = aws_instance.private_instance_1_az2.private_ip
#   description = "Private IP of the first EC2 instance in the private subnet (AZ2)"
# }


# output "alb_dns_name" {
#   value = aws_lb.app_alb.dns_name
# }

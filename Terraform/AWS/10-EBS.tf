# Persistent EBS volume for MySQL data


# resource "aws_ebs_volume" "mysql_volume_az1" {
#   availability_zone = aws_instance.private_instance_1_az1.availability_zone
#   size              = 5
#   type              = "gp3"

#   tags = {
#     Name = "mysql-db-volume-az1"
#   }

#   # lifecycle {
#   #   prevent_destroy = true # Prevent accidental deletion
#   # }
# }

# # Attach EBS volume to the private database instance
# resource "aws_volume_attachment" "mysql_attach_az1" {
#   device_name  = "/dev/sdf"
#   volume_id    = aws_ebs_volume.mysql_volume_az1.id
#   instance_id  = aws_instance.private_instance_1_az1.id
#   force_detach = true
# }

#####################################################################################

# Create a persistent EBS volume in AZ2 for the second DB instance


# resource "aws_ebs_volume" "mysql_volume_az2" {
#   availability_zone = aws_instance.private_instance_1_az2.availability_zone
#   size              = 5
#   type              = "gp3"

#   tags = {
#     Name = "mysql-db-volume-az2"
#   }

#   lifecycle {
#     prevent_destroy = true # Ensure volume is not deleted accidentally
#   }
# }



# Attach the EBS volume to the second DB instance in AZ2
# resource "aws_volume_attachment" "mysql_attach_az2" {
#   device_name  = "/dev/sdf"
#   volume_id    = aws_ebs_volume.mysql_volume_az2.id
#   instance_id  = aws_instance.private_instance_1_az2.id
#   force_detach = true
# }



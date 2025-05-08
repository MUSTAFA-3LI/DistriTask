# resource "aws_eip" "public_instance_1_az1" {
#   domain = "vpc"
# }

# resource "aws_eip" "public_instance_2_az1" {
#   domain = "vpc"
# }

# resource "aws_eip" "public_instance_3_az1" {
#   domain = "vpc"
# }

# resource "aws_eip" "private_instance_1_az1" {
#   domain = "vpc"
# }

# resource "aws_eip" "public_instance_1_az2" {
#   domain = "vpc"
# }

# resource "aws_eip" "private_instance_1_az2" {
#   domain = "vpc"
# }



resource "aws_key_pair" "SSH_key" {
  key_name   = "SSH_key"
  public_key = file("/home/mustafa/.ssh/SSH_key.pub")
}


# EC2 instances in public subnet in AZ1
resource "aws_instance" "public_instance_1_az1" {
  ami                    = "ami-04a81a99f5ec58529"
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.SSH_key.key_name
  subnet_id              = aws_subnet.public_subnet_a.id
  vpc_security_group_ids = [aws_security_group.public_sg.id]

  tags = {
    Name = "public_instance_1_az1"
  }

  associate_public_ip_address = true
}

resource "aws_instance" "public_instance_2_az1" {
  ami                    = "ami-04a81a99f5ec58529"
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.SSH_key.key_name
  subnet_id              = aws_subnet.public_subnet_a.id
  vpc_security_group_ids = [aws_security_group.public_sg.id]

  tags = {
    Name = "public_instance_2_az1"
  }

  associate_public_ip_address = true
}

# resource "aws_instance" "public_instance_3_az1" {
#   ami                    = "ami-04a81a99f5ec58529"
#   instance_type          = "t3.medium"
#   key_name               = aws_key_pair.SSH_key.key_name
#   subnet_id              = aws_subnet.public_subnet_a.id
#   vpc_security_group_ids = [aws_security_group.public_sg.id]

#   tags = {
#     Name = "public_instance_3_az1"
#   }

#   associate_public_ip_address = true
# }

# EC2 instance in private subnet in AZ1
# Mount the EBS volume and persist it
resource "aws_instance" "private_instance_1_az1" {
  ami                    = "ami-04a81a99f5ec58529"
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.SSH_key.key_name
  subnet_id              = aws_subnet.private_subnet_a.id
  vpc_security_group_ids = [aws_security_group.private_sg.id]

  associate_public_ip_address = false

  user_data = <<-EOF
              #!/bin/bash
              while [ ! -e /dev/nvme1n1 ]; do
                sleep 1
              done
              if ! blkid /dev/nvme1n1; then
                mkfs -t ext4 /dev/nvme1n1
              fi
              VOLUME_UUID=$(blkid -s UUID -o value /dev/nvme1n1)
              mkdir -p /data/mysql
              mount UUID=$VOLUME_UUID /data/mysql
              grep -q '/data/mysql' /etc/fstab || echo "UUID=$VOLUME_UUID /data/mysql ext4 defaults,nofail 0 2" >> /etc/fstab
              EOF

  tags = {
    Name = "private_instance_1_az1"
  }
}



# EC2 instance in public subnet in AZ2
resource "aws_instance" "public_instance_1_az2" {
  ami                    = "ami-04a81a99f5ec58529"
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.SSH_key.key_name
  subnet_id              = aws_subnet.public_subnet_b.id
  vpc_security_group_ids = [aws_security_group.public_sg.id]

  tags = {
    Name = "public_instance_1_az2"
  }

  associate_public_ip_address = true
}

# EC2 instance in private subnet in AZ2
# Configure the instance to mount the volume automatically on boot

resource "aws_instance" "private_instance_1_az2" {
  ami                    = "ami-04a81a99f5ec58529"
  instance_type          = "t3.medium"
  key_name               = aws_key_pair.SSH_key.key_name
  subnet_id              = aws_subnet.private_subnet_b.id
  vpc_security_group_ids = [aws_security_group.private_sg.id]

  associate_public_ip_address = false

  user_data = <<-EOF
              #!/bin/bash
              while [ ! -e /dev/nvme1n1 ]; do
                sleep 1
              done
              if ! blkid /dev/nvme1n1; then
                mkfs -t ext4 /dev/nvme1n1
              fi
              VOLUME_UUID=$(blkid -s UUID -o value /dev/nvme1n1)
              mkdir -p /data/mysql
              mount UUID=$VOLUME_UUID /data/mysql
              grep -q '/data/mysql' /etc/fstab || echo "UUID=$VOLUME_UUID /data/mysql ext4 defaults,nofail 0 2" >> /etc/fstab
              EOF

  tags = {
    Name = "private_instance_1_az2"
  }
}



# resource "aws_eip_association" "public_instance_1_az1_eip_association" {
#   instance_id   = aws_instance.public_instance_1_az1.id
#   allocation_id = aws_eip.public_instance_1_az1.id
# }

# resource "aws_eip_association" "public_instance_2_az1_eip_association" {
#   instance_id   = aws_instance.public_instance_2_az1.id
#   allocation_id = aws_eip.public_instance_2_az1.id
# }

# resource "aws_eip_association" "public_instance_3_az1_eip_association" {
#   instance_id   = aws_instance.public_instance_3_az1.id
#   allocation_id = aws_eip.public_instance_3_az1.id
# }


# resource "aws_eip_association" "private_instance_1_az1_eip_association" {
#   instance_id   = aws_instance.private_instance_1_az1.id
#   allocation_id = aws_eip.private_instance_1_az1.id
# }


# resource "aws_eip_association" "public_instance_1_az2_eip_association" {
#   instance_id   = aws_instance.public_instance_1_az2.id
#   allocation_id = aws_eip.public_instance_1_az2.id
# }


# resource "aws_eip_association" "private_instance_1_az2_eip_association" {
#   instance_id   = aws_instance.private_instance_1_az2.id
#   allocation_id = aws_eip.private_instance_1_az2.id
# }

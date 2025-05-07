resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.distritask_vpc.id

  tags = {
    Name = "igw"
  }
}

# should i create another igw for the second az?


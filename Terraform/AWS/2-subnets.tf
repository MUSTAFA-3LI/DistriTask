resource "aws_subnet" "public_subnet_a" {
  vpc_id            = aws_vpc.distritask_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-a"
  }
}

# resource "aws_subnet" "public_subnet_b" {
#   vpc_id            = aws_vpc.distritask_vpc.id
#   cidr_block        = "10.0.3.0/24"
#   availability_zone = "us-east-1b"

#   map_public_ip_on_launch = true

#   tags = {
#     Name = "public-subnet-b"
#   }
# }

resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.distritask_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-a"
  }
}

# resource "aws_subnet" "private_subnet_b" {
#   vpc_id            = aws_vpc.distritask_vpc.id
#   cidr_block        = "10.0.4.0/24"
#   availability_zone = "us-east-1b"

#   tags = {
#     Name = "private-subnet-b"
#   }
# }

resource "aws_route_table" "public_rt_az1" {
  vpc_id = aws_vpc.distritask_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table-az1"
  }
}

resource "aws_route_table" "public_rt_az2" {
  vpc_id = aws_vpc.distritask_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table-az2"
  }
}




resource "aws_route_table" "private_rt_az1" {
  vpc_id = aws_vpc.distritask_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw_az1.id
  }

  tags = {
    Name = "private-route-table-az1"
  }
}

resource "aws_route_table" "private_rt_az2" {
  vpc_id = aws_vpc.distritask_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw_az2.id
  }

  tags = {
    Name = "private-route-table-az2"
  }
}

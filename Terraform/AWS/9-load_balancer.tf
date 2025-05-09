resource "aws_lb" "app_alb" {
  name               = "distritask-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets = [
    aws_subnet.public_subnet_a.id,
    # aws_subnet.public_subnet_b.id
  ]

  tags = {
    Name = "distritask-alb"
  }
}



resource "aws_lb_target_group" "app_tg" {
  name     = "distritask-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = aws_vpc.distritask_vpc.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200-399"
  }

  tags = {
    Name = "distritask-tg"
  }
}


resource "aws_lb_listener" "app_listener" {
  load_balancer_arn = aws_lb.app_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}


resource "aws_lb_target_group_attachment" "ec2_attachment_1" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.public_instance_1_az1.id
  port             = 8000
}

resource "aws_lb_target_group_attachment" "ec2_attachment_2" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.public_instance_2_az1.id
  port             = 8000
}

# resource "aws_lb_target_group_attachment" "ec2_attachment_3" {
#   target_group_arn = aws_lb_target_group.app_tg.arn
#   target_id        = aws_instance.public_instance_3_az1.id
#   port             = 8000
# }

# resource "aws_lb_target_group_attachment" "ec2_attachment_4" {
#   target_group_arn = aws_lb_target_group.app_tg.arn
#   target_id        = aws_instance.public_instance_1_az2.id
#   port             = 8000
# }

resource "aws_instance" "nginx_server" {
  count          = var.instance_count
  ami            = var.ami_id
  instance_type  = var.instance_type
  security_groups = [aws_security_group.nginx_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install nginx1.12 -y
              systemctl start nginx
              systemctl enable nginx
              EOF

  tags = {
    Name        = "${var.environment}_NginxServer-${count.index}"
    Environment = var.environment
  }
}

resource "aws_security_group" "nginx_sg" {
  name        = var.security_group_name
  description = "Allow inbound traffic for Nginx and SSH"

  # Ingress rule for HTTP (port 80)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Ingress rule for SSH (port 22)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "public_ips" {
  value       = aws_instance.nginx_server[*].public_ip
  description = "The public IPs of the Nginx servers"
}
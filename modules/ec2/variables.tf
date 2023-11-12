variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "The type of the EC2 instance"
  type        = string
}

variable "environment" {
  description = "Environment for the infrastructure, e.g. dev, prod"
  type        = string
}

variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
}

variable "security_group_name" {
  description = "Name of the security group for Nginx instances"
  type        = string
}

variable "aws_region" {
  description = " Name of the region to create resources"
  type        = string
}

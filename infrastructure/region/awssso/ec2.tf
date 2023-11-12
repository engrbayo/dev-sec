module "dev_nginx_servers" {
  source              = "../../..//modules/ec2"
  environment         = "dev"
  instance_type       = "t2.micro"
  instance_count      = "2"
  ami_id              = "ami-041feb57c611358bd"
  security_group_name = "dev-nginx"
  aws_region          = "us-east-1"
}

module "prod_nginx_servers" {
  source              = "../../..//modules/ec2"
  environment         = "prod"
  instance_type       = "t2.micro"
  instance_count      = "3"
  ami_id              = "ami-041feb57c611358bd"
  security_group_name = "prod-nginx"
  aws_region          = "us-east-1"
}

module "cloudsentrics" {
  source = "../../..//modules/ec2"

  environment         = "sandbox"
  instance_type       = "t2.micro"
  instance_count      = "6"
  ami_id              = "ami-041feb57c611358bd"
  security_group_name = "cloudsentrics"
  aws_region          = "us-east-1"
}

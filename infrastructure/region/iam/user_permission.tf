provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "admin_user" {
  name = "admin_user"
}

resource "aws_iam_policy" "admin_policy" {
  name        = "admin_policy"
  description = "An admin policy that grants full access"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "*",
        Effect   = "Allow",
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_user_policy_attachment" "admin_attach" {
  user       = aws_iam_user.admin_user.name
  policy_arn = aws_iam_policy.admin_policy.arn
}

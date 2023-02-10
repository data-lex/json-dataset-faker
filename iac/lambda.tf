resource "aws_lambda_function" "json_dataset_faker" {
  function_name = "json-dataset-faker"
  image_uri     = var.aws_ecr_uri
  memory_size   = 256
  package_type  = "Image"
  role          = aws_iam_role.json_dataset_faker_role.arn
  timeout       = 30
}

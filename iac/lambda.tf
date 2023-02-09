resource "aws_lambda_function" "json_dataset_faker" {
  image_uri     = var.aws_ecr_image_uri
  package_type  = Image
  function_name = "json-dataset-faker"
  role          = aws_iam_role.json_dataset_faker_role.arn
  handler       = "main.handler"
  timeout       = 30
}

resource "null_resource" "package_lambda_command" {
  # Use local-exec to create a ZIP package of the lambda function
  provisioner "local-exec" {
    command = <<EOF
      rm -rf lambda_function_payload.zip package
      mkdir -p package
      pip install \
        --platform manylinux2014_aarch64 \
        --target=package \
        --implementation cp \
        --python-version 3.11 \
        --only-binary=:all: --upgrade \
        -r requirements.txt
      zip lambda_function_payload.zip app.py lambda_function.py
      pushd package
      zip -ur ../lambda_function_payload.zip ./*
      popd
    EOF
  }

  # Add a file trigger to ensure the zip is recreated if the function changes
  triggers = {
    function_code_sha = filebase64sha256("app.py")
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "local_file" "lambda_zip" {
  filename = "${path.module}/lambda_function_payload.zip"
  depends_on = [null_resource.package_lambda_command]
}

resource "aws_lambda_function" "example" {
  function_name = "example_lambda"
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda_exec.arn
  timeout       = 10
  memory_size   = 128  # Minimum memory allocation

  filename         = data.local_file.lambda_zip.filename
  source_code_hash = data.local_file.lambda_zip.content_base64sha256

  environment {
    variables = {
      # Add any environment variables here
    }
  }
}

resource "aws_lambda_function_url" "example" {
  function_name = aws_lambda_function.example.function_name
  authorization_type = "NONE"
}

output "lambda_function_url" {
  value = aws_lambda_function_url.example.function_url
}

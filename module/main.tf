# S3 bucket resource
resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
}

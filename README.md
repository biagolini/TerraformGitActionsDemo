# Terraform GitHub Actions Pipeline Demo

This repository demonstrates a minimal and secure CI/CD pipeline for deploying AWS infrastructure using Terraform and GitHub Actions. It leverages **OpenID Connect (OIDC)** for authentication, avoiding the use of static AWS credentials.

**Enhanced Pipeline Features:**
- Manual approval gates for infrastructure changes
- AI-powered Terraform plan summaries using AWS Bedrock
- Automated comments on pull requests and commits

**Step-by-Step Tutorials:**
1. [Creating a Secure and Modular Terraform Pipeline Using GitHub Actions](https://blog.devops.dev/creating-a-secure-and-modular-terraform-pipeline-using-github-actions-43abfa2723cf)
2. [Implementing Manual Approval in GitHub Terraform Pipelines](https://medium.com/@biagolini/implementing-manual-approval-in-github-terraform-pipelines-7c01e6946ead)

**More AWS, AI & Security Tutorials:** [https://medium.com/@biagolini](https://medium.com/@biagolini)

---

## Project Structure

```
├── module/                       # Reusable Terraform module (e.g., defines an S3 bucket)
│   ├── main.tf
│   └── variables.tf
│
├── environments/                 # Environment-specific configurations
│   └── dev/
│       ├── main.tf              # Module instantiation with environment-specific inputs
│       ├── variables.tf         # Variable declarations expected by this environment
│       ├── terraform.tfvars     # Values for variables (e.g., bucket_name)
│       └── providers.tf         # AWS provider and backend S3/DynamoDB config
│
├── .github/
│   ├── workflows/
│   │   └── main.yml             # GitHub Actions workflow to run Terraform
│   └── generate_ai_summary.py   # Python script for AI-powered plan summaries
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## How It Works

* **Terraform** manages AWS infrastructure, using modules to promote reuse and clarity.
* **GitHub Actions** is triggered on a push to a branch (e.g., `dev`, `main`), and authenticates to AWS using OIDC.
* **Terraform state** is stored in an S3 bucket, and locking is managed by a DynamoDB table.
* **Environment-specific values** (like instance size, resource count, or naming) are passed via `.tfvars` files.

---

## Local Testing Instructions

To test the `dev` environment locally:

```bash
# 1. Navigate to the environment directory
cd environments/dev

# 2. Initialize Terraform (loads backend config and checks state locking)
terraform init

# 3. Validate the configuration
terraform validate

# 4. Review the planned changes
terraform plan -var-file=terraform.tfvars

# 5. Apply the changes
terraform apply -auto-approve -var-file=terraform.tfvars
```

Ensure that AWS credentials are configured in your local environment (via `aws configure`, environment variables, or assumed role) before running these commands.

---

## Bootstrap: Creating the Remote Backend Resources

Before running `terraform init`, you must ensure that the S3 bucket and DynamoDB table exist.

You can create them manually using the AWS CLI:

```bash
# Create the S3 bucket (adjust the region and bucket name as needed)
aws s3api create-bucket \
  --bucket tutorial-terraform-tfstate \
  --region us-east-1 \
  --create-bucket-configuration LocationConstraint=us-east-1

# Create the DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-lock-table \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

These resources must exist before `terraform init` can succeed.

---

## CI/CD Usage

1. **Configure AWS IAM Role**: Create an IAM role with trust relationship for GitHub's OIDC provider, and necessary permissions (e.g., `s3`, `dynamodb`, `ec2`).
2. **Set Secrets**: In your GitHub repository, define the following secrets:

   * `AWS_ROLE_ARN`: ARN of the IAM role to assume
   * `AWS_REGION`: AWS region (e.g., `us-east-1`)
3. **Trigger the Pipeline**: Push changes to the desired branch (`dev`, `main`, etc.) and the GitHub Actions workflow will automatically:

   * Checkout the code
   * Configure AWS credentials via OIDC
   * Run `terraform init`, `validate`, `plan`, and `apply`

---

## Notes

* Each environment should use a unique `key` in the `backend "s3"` block to isolate state.
* Avoid provisioning the backend resources (e.g., the DynamoDB lock table) from the same Terraform project that uses them.
* Use branch-based workflows to deploy to different environments (e.g., `dev` branch for development, `main` for production).

---

Feel free to extend this project by adding more modules or environments as needed.

# Shortly's cloud pieces as code (task 12), created on Floci, the local AWS from the cloud lab.
# Run OpenTofu from shortly/: tofu -chdir=infra init, then plan, apply and destroy.

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # TODO(task 12): pin the provider version from the kit's VERSIONS.md.
    }
  }
}

# TODO(task 12): the aws provider for Floci, as in card 5: the region from var.region, the fake
#   keys, the skip settings, path-style S3, and endpoints for s3, sqs, iam, sts and budgets,
#   all at http://localhost:4566.
# TODO(task 13): remove access_key and secret_key from the provider. It then reads
#   AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from the environment.

# TODO(task 12): an aws_s3_bucket named shortly-backups-${var.env}.
# TODO(task 12): an aws_sqs_queue named shortly-clicks-${var.env}.
# TODO(task 12): an aws_iam_role named shortly-api that EC2 may assume.
# TODO(task 12): an aws_iam_role_policy on that role that allows only s3:PutObject on the bucket's
#   objects and sqs:SendMessage on the queue. Use the resources' arn attributes, never "*".
# TODO(task 12): an aws_budgets_budget: COST, MONTHLY, a limit of var.budget_usd in USD,
#   account_id = var.account_id, and an email alert to var.alert_email at 80% of actual spend.

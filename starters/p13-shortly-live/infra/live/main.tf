# Shortly's one real server (task 10), on your real AWS account. P11's infra/ stays on Floci;
# this folder is separate. Run OpenTofu in shortly/infra/live/, in one Git Bash window:
#   eval "$(aws configure export-credentials --profile shortly --format env)"
#   tofu init, tofu fmt, tofu validate, then tofu plan -out live.tfplan and tofu apply live.tfplan
# The state file (terraform.tfstate) stays on your laptop. Your P11 .gitignore keeps it out of Git.

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # TODO(task 10): pin the provider version from the kit's VERSIONS.md.
    }
  }
}

provider "aws" {
  region = var.region

  # Every resource gets the tag project = "shortly", so you can find them all by tag.
  default_tags {
    tags = {
      project = "shortly"
    }
  }
}

# The newest Ubuntu Server 24.04 image in this region. Canonical publishes its id here.
# Use data.aws_ssm_parameter.ubuntu.insecure_value as the instance's ami.
data "aws_ssm_parameter" "ubuntu" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}

# TODO(task 10): an aws_key_pair with key_name "shortly-key" and the public key read from
#   ~/.ssh/shortly-key.pub (use file() and pathexpand()). The private key never leaves ~/.ssh.

# TODO(task 10): an aws_security_group with name "shortly-web". Leave out vpc_id, so it is made in
#   the default VPC. Write no ingress or egress blocks inside it: the rules below are their own
#   resources, and the two styles must not be mixed.

# TODO(task 10): aws_vpc_security_group_ingress_rule resources: TCP 80 and TCP 443 from 0.0.0.0/0,
#   and TCP 22 from var.my_ip_cidr only. Each needs security_group_id, ip_protocol, from_port,
#   to_port and cidr_ipv4.

# TODO(task 10): one aws_vpc_security_group_egress_rule that allows all outbound traffic
#   (ip_protocol "-1" to 0.0.0.0/0). Without it the server cannot download Docker.

# TODO(task 10): an aws_instance "shortly": t3.small, the Ubuntu image above, the key pair and the
#   security group, user_data from file("../../ops/user-data.sh") with
#   user_data_replace_on_change = true, a 20 GiB gp3 root_block_device, and the tag Name = "shortly".

# Inputs for infra/live/main.tf (task 10).

variable "region" {
  description = "The AWS region of Shortly's server: Asia Pacific (Mumbai)"
  type        = string
  default     = "ap-south-1"
}

# TODO(task 10): declare my_ip_cidr: a string with no default, your laptop's public IPv4 address
#   followed by /32. The SSH rule allows only this address. tofu plan gets it with
#   -var "my_ip_cidr=$(curl -s https://checkip.amazonaws.com)/32".

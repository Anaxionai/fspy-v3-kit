#!/bin/bash
# EC2 user data for Shortly's server (task 10). cloud-init runs it once, as root, at first boot.
# It must keep LF line endings: with Windows line endings it fails and Docker is never installed.
set -euxo pipefail

# TODO(task 10): install Docker with Docker's install script (get.docker.com).
# TODO(task 10): add the user ubuntu to the docker group, so docker runs without sudo.

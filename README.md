# AWS Lambda experiment, Python cachetools

This is an experiment aimed at showcasing cachetools in AWS Lambda

It comes from a conversation with Engineer Megan List.

I Asserted that AWS Lambda can:

- [ ] cache values for more than 15 minute maximum runtime
- [ ] take memory snapshots of VM to get faster warm boot times
- [ ] I was wrong when I said it reaps warm lambdas over 1 hour old.


## Pre-requisites

- Curl 8.6+
- Terraform 1.5+
- cli `zip` command compatible with:
  - `zip <zipfile-path.zip> <list of file names>`
  - `zip -ur ../<zipfile-path.zip> ./*`

## Usage

1. Initialize terraform and apply
```
terraform init
terraform apply
```


# EC2 & S3 Debugger CLI Tool

This Python-based CLI tool allows secure debugging of EC2 instances and S3 buckets by assuming an IAM role. It provides key diagnostics without SSH access using AWS Systems Manager.

## Features

- Assume AWS IAM roles via STS for secure access
- List and inspect EC2 instances (ID, state, type)
- Retrieve basic diagnostics (running services, logs) using SSM
- List and inspect S3 buckets and policies
- CLI interface using click for ease of use
- Modular Python codebase

## Project Directory

├── aws_session.py # Handles STS role assumption

├── ec2_debugger.py # EC2 utilities

├── s3_debugger.py # S3 utilities

├── cli.py # Main CLI entry point

├── roles_config.json # Alias-to-ARN mapping

├── requirements.txt

├── README.md

## Setup

```bash
1.**Install dependencies**

pip install -r requirements.txt

2. **Configure your AWS CLI credentials**


aws configure   # add access key and secret key

3. **Update the roles_config.json with valid IAM role ARNs**

{
        "ec2": "arn:aws:iam::11111111111:role/EC2DebugRole",
        "s3": "arn:aws:iam::111111111111:role/S3DebugRole"
}

4. **Usage**

Run the CLI and choose the role/environment:

python3 cli.py --role ec2 --debug ec2







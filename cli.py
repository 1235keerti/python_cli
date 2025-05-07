import click
import json
from aws_session import assume_role
from ec2_debugger import print_instance_status
from s3_debugger import print_bucket_info

@click.command()
@click.option('--role', prompt='Choose a role (e.g., dev, prod)', help='Role alias to assume.')
@click.option('--debug', type=click.Choice(['ec2', 's3', 'both']), default='both', help='What to debug.')
@click.option('--region', default='eu-north-1', help='AWS region to use.')  # New region option
def main(role, debug, region):
    with open("roles_config.json") as f:
        roles = json.load(f)

    if role not in roles:
        print(f"Role {role} not found.")
        return

    print(f"Assuming role: {role}")
    session = assume_role(roles[role])
    ec2 = session.client("ec2", region_name=region)
    s3 = session.client("s3", region_name=region)

    if debug in ['ec2', 'both']:
        print("\n--- EC2 Instances ---")
        print_instance_status(ec2,region)

    if debug in ['s3', 'both']:
        print("\n--- S3 Buckets ---")
        print_bucket_info(s3)

if __name__ == "__main__":
    main()


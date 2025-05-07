import boto3
import paramiko  # For SSH access to EC2 instances (ensure the private key is available)

# List EC2 Instances
def list_instances(ec2_client):
    instances = []
    response = ec2_client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "Type": instance["InstanceType"]
            })
    return instances

# Fetch running services and logs
def get_running_services(instance_id, region):
    # Use SSH to get running services or system logs
    # Here you can add logic to connect via SSH and get services information
    # Ensure you have the private key for SSH access to the EC2 instance
    
    # Example using paramiko (SSH) to run a command on the EC2 instance
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
    private_key_path = '/home/keerti/.ssh/Debug.pem'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(public_ip, username='ec2-user', key_filename=private_key_path)
        stdin, stdout, stderr = ssh_client.exec_command('systemctl list-units --type=service')
        services = stdout.read().decode('utf-8')
        return services
    except Exception as e:
        return str(e)
    finally:
        ssh_client.close()

# Get logs for the EC2 instance
def get_instance_logs(instance_id, region):
    logs_client = boto3.client('logs', region_name=region)
    log_group_name = '/aws/ec2/instance/' + instance_id

    try:
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )
        log_streams = response['logStreams']
        if log_streams:
            log_stream_name = log_streams[0]['logStreamName']
            log_events = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                limit=5
            )
            return [event['message'] for event in log_events['events']]
        else:
            return ["✅ Log group found but no log streams available."]
    except logs_client.exceptions.ResourceNotFoundException:
        return [f"⚠️ Log group '{log_group_name}' not found."]
    except Exception as e:
        return [f"❌ Error fetching logs: {str(e)}"]

# Print EC2 Instance Debugging Information
def print_instance_status(ec2_client, region):
    instances = list_instances(ec2_client)
    total_instances = len(instances)  # Count the total number of instances
    print(f"Total Instances: {total_instances}")
    
    for inst in instances:
        print(f"id : {inst['InstanceId']} | status : {inst['State']} | type : {inst['Type']}")
        
        # Fetch Running Services (SSH approach)
        services = get_running_services(inst['InstanceId'], region)
        print(f"Running Services on {inst['InstanceId']}:\n{services}")
        
        # Fetch Logs (CloudWatch approach)
        logs = get_instance_logs(inst['InstanceId'], region)
        print(f"Logs for {inst['InstanceId']}:\n{logs}")

# Example usage
region = 'eu-west-1'  # Replace with your EC2 region
ec2_client = boto3.client('ec2', region_name=region)
print_instance_status(ec2_client, region)

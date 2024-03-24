#!/usr/bin/python3

import boto3
import subprocess
import os
import requests
import sys
import tmpfile

AWS_ENV_FILE_PATH = '/etc/aws-iot-device-client/thing/aws-environment.env'
AWS_DEVICE_ENV_FILE_PATH = '/etc/aws-iot-device-client/thing/device-environment.env'

# Set this to your desired image updater
IMAGE_UPDATER = "rauc"
IMAGE_UPDATE_FILE_COMMAND = []
IMAGE_UPDATE_STREAM_COMMAND= []

if IMAGE_UPDATER == "rauc"
    IMAGE_UPDATE_FILE_COMMAND = ['/usr/bin/rauc','install']

if IMAGE_UPDATER == "fwup":
    IMAGE_UPDATE_STREAM_COMMAND = ['/usr/bin/fwup', '-a', '-U', '-d', '/dev/mmcblk0', '-t', 'upgrade']

def add_env_vars(env_file : str):
    """
    Load environment variables from a bash environment file.

    Args:
        env_file (str): Path to the bash environment file.

    Returns:
        dict: Dictionary containing the environment variables.
    """
    env_vars = {}
    try:
        with open(env_file, 'r') as file:
            for line in file:
                # Ignore comments and empty lines
                if line.strip() and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Remove quotes from value
                    value = value.strip('"')
                    env_vars[key.strip()] = value
                for key, value in env_vars.items():
                    if key not in os.environ:
                        os.environ[key] = value
    except Exception as e:
        print(f"Error opening {env_file} for reading: {e}")


def obtain_temporary_credentials():
    """
    Obtain temporary credentials to an S3 bucket using the sequence described in [1]
    1: https://fanchenbao.medium.com/access-aws-s3-bucket-from-aws-iot-thing-in-python3-1ca828456e55

    Returns:
        Tuple with access key, secret access key, and session token
    """
    credential_provider_endpoint = f"https://{os.environ.get('AWS_CREDENTIALS_ENDPOINT')}/role-aliases/{os.environ.get('AWS_S3_ACCESS_ROLE_ALIAS')}/credentials"
    resp = requests.get(
        credential_provider_endpoint,
        headers={'x-amzn-iot-thingname': os.environ.get('AWSIOT_THING_NAME')},
        cert=(os.environ.get('AWSIOT_DEVICE_CERT_PATH'), os.environ.get('AWSIOT_DEVICE_PRIVATE_KEY_PATH')),
    )

    if resp:  # check whether https request succeeds
        credentials = resp.json()
        access_key_id = credentials['credentials']['accessKeyId']
        secrete_access_key = credentials['credentials']['secretAccessKey']
        session_token = credentials['credentials']['sessionToken']
        return access_key_id, secrete_access_key, session_token
    else:
        print('error requesting temporary access to AWS S3')
        return '', '', ''

def stream_s3_download_to_image_updater(bucket_file : str):
    """
    Stream an S3 object download into an image update command.

    Args:
        bucket_file (str): The S3 URI for the bucket file.

    Returns:
        subprocess.CompletedProcess: Completed process object.
    """
    # Create an S3 client
    print(f'Obtaining temp credentials for file {bucket_file}')
    access_key_id, secrete_access_key, session_token = obtain_temporary_credentials()

    temp_dir = tempfile.mkdtemp()

    bucket, key = bucket_file.replace("s3://", "").split("/", 1)
    temp_file_path = os.path.join(temp_dir, os.path.basename(key))
    process = None
    update_command = IMAGE_UPDATE_STREAM_COMMAND
    update_command.append(temp_file_path)
    print(f"Obtaining file from {bucket}/{key} and passing to {' '.join(update_command)}")
    
    s3_cli = boto3.client(  # access S3 with obtained credentials
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secrete_access_key,
            aws_session_token=session_token,
        )
    # Stream the S3 object content into the shell command
    s3_cli.download_file(bucket, key, temp_file_path)
    print(f"File downloaded successfully to {temp_file_path}")
    # Run the shell command, appending the temp file path
    try:
        process = subprocess.Popen(update_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()
    except Exception as e:
        print(f"Failed to download file from {bucket}/{key} to {temp_file_path} : {e}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file deleted: {temp_file_path}")
    return process

def download_s3_and_update_image(bucket_file : str):
    """
    Download an S3 object to temp directory and use this to update the image

    Args:
        bucket_file (str): The S3 URI for the bucket file.

    Returns:
        subprocess.CompletedProcess: Completed process object.
    """
    # Create an S3 client
    print(f'Obtaining temp credentials for file {bucket_file}')
    access_key_id, secrete_access_key, session_token = obtain_temporary_credentials()
    update_command = 

    bucket, key = bucket_file.replace("s3://", "").split("/", 1)
    print(f"Obtaining file from {bucket}/{key} and passing to {' '.join(update_command)}")

    s3 = boto3.client('s3')
    # Start streaming the S3 object content into the shell command
    with subprocess.Popen(update_command, stdin=subprocess.PIPE) as process:
        s3_cli = boto3.client(  # access S3 with obtained credentials
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secrete_access_key,
            aws_session_token=session_token,
        )

        # Stream the S3 object content into the shell command
        s3_cli.download_fileobj(bucket, key, process.stdin)

        # Wait for the shell command to finish
        process.communicate()

        # Return the completed process object
        return process


if __name__ == "__main__":
    # Load environment variables from the file
    add_env_vars(AWS_ENV_FILE_PATH)
    add_env_vars(AWS_DEVICE_ENV_FILE_PATH)

    if len(sys.argv) < 2:
        print("Please specify a single argument with path to file")
        sys.exit(1)

    download_image = sys.argv[1]
    if not download_image.startswith("s3://"):
        print(f"Please specify a path to the download image in s3.  Path {download_image} in {sys.argv} and arg list length {len(sys.argv)} does not include an s3:// prefix")
        sys.exit(1)

    if len(IMAGE_UPDATE_STREAM_COMMAND):
        process = stream_s3_download_to_image_updater(download_image)
    else:
        process = downlad_s3_and_update_image(download_image)

    if process.returncode == 0:
        print("Rebooting to the new image in 1 minute")
        subprocess.run(['/sbin/shutdown', '-r', '1'])
    sys.exit(process.returncode)

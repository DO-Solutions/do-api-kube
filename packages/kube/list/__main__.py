import json
import os
from kubernetes import client, config
import boto3
import yaml

SPACES_REGION = "nyc3"  # Change to your region (e.g., sgp1, ams3)
SPACES_BUCKET = "kubefiles"  # Your Space name
KUBECONFIG_FILE = "config" 

SPACES_ACCESS_KEY = os.getenv("SPACES_ACCESS_KEY")
SPACES_SECRET_KEY = os.getenv("SPACES_SECRET_KEY")

def main(args):
    if not SPACES_ACCESS_KEY or not SPACES_SECRET_KEY:
        return {"error": "Missing DigitalOcean Spaces credentials."}
    try:
        # Initialize DigitalOcean Spaces client
        session = boto3.session.Session()
        s3_client = session.client(
            "s3",
            region_name=SPACES_REGION,
            endpoint_url=f"https://{SPACES_REGION}.digitaloceanspaces.com",
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY,
        )

        # Retrieve kubeconfig file from Spaces
        response = s3_client.get_object(Bucket=SPACES_BUCKET, Key=KUBECONFIG_FILE)
        kubeconfig_content = response["Body"].read()

        # Load kubeconfig from retrieved content
        kubeconfig_dict = yaml.safe_load(kubeconfig_content)
        config.load_kube_config_from_dict(kubeconfig_dict)

        # Create Kubernetes API client
        v1 = client.CoreV1Api()

        # List all pods across all namespaces
        pod_list = v1.list_pod_for_all_namespaces(watch=False)

        pods_info = []
        for pod in pod_list.items:
            pods_info.append({
                "namespace": pod.metadata.namespace,
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "ip": pod.status.pod_ip or "None"
            })

        return {
            "body": {
                "pods": json.dumps(pods_info),
                "count": len(pods_info),
                "status": "success"
            }
        }

    except Exception as e:
        return {
            "body": {
                "pods": json.dumps([]),
                "count": 0,
                "status": "error",
                "error": str(e)
            }
        }

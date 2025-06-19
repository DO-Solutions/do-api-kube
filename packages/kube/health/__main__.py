import json
import os
from kubernetes import client, config
from kubernetes.client.rest import RESTClientObject
from kubernetes.client import Configuration, ApiClient
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
        c = Configuration()
        rest_client = RESTClientObject(ApiClient(configuration=c))
        
        ### 1. Node Health
        node_list = v1.list_node()
        nodes_info = []
        for node in node_list.items:
            for condition in node.status.conditions:
                if condition.type == "Ready":
                    nodes_info.append({
                        "name": node.metadata.name,
                        "status": "Ready" if condition.status == "True" else "NotReady"
                    })

        # ### 2. Component Status
        # component_list = v1.list_component_status()
        # components_info = []
        # for comp in component_list.items:
        #     healthy = all(c.status == "True" for c in comp.conditions)
        #     components_info.append({
        #         "name": comp.metadata.name,
        #         "healthy": healthy
        #     })

        # # ### 3. API Server /healthz
        # # response = rest_client.GET('/healthz', _preload_content=False)
        # # apiserver_health = response.data.decode().strip()

        # ### 4. kube-system Pods Health
        # kube_system_pods = v1.list_namespaced_pod(namespace="kube-system")
        # ks_pods_info = []
        # for pod in kube_system_pods.items:
        #     ks_pods_info.append({
        #         "name": pod.metadata.name,
        #         "status": pod.status.phase
        #     })


        return {
            "body": {
                "status": "success",
                "node_health": json.dumps(nodes_info)
                # "components_health": json.dumps(components_info),
                # "apiserver_health": apiserver_health,
                # "kube_system_pods": json.dumps(ks_pods_info)
            }
        }

    except Exception as e:
        return {
            "body": {
                "status": "error",
                "pods": json.dumps([]),
                "count": 0,
                "node_health": json.dumps([]),
                "components_health": json.dumps([]),
                "apiserver_health": "unknown",
                "kube_system_pods": json.dumps([]),
                "error": str(e)
            }
        }
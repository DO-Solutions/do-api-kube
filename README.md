A serverless function example built for DigitalOcean Functions that retrieves your Cluster's information from the DigitalOcean API. This function demonstrates how to create API-connected serverless functions that can be integrated with GenAI platforms for function calling capabilities. Built using Python 3.11, it leverages the [kubernetes](https://github.com/kubernetes-client/python) client to interact with DOKS along with [boto3](https://pypi.org/project/boto3/) for interacting with Spaces..

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [GenAI Integration Use Cases](#genai-integration-use-cases)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup \& Installation](#setup--installation)
  - [Environment Variables](#environment-variables)
  - [Python Dependencies](#python-dependencies)
- [Deployment](#deployment)
  - [Deploying to DigitalOcean Functions](#deploying-to-digitalocean-functions)
- [Sample Package](#sample-package)

---

## Introduction

The **do-api** function is a practical example of creating serverless functions on [DigitalOcean Functions](https://docs.digitalocean.com/products/functions/). It retrieves a Cluster Pod information from the DigitalOcean API and is structured to be easily integrated as a function calling endpoint for GenAI platforms and Large Language Models (LLMs).

This function supports fetching details for a specific cluster by supplying a `kubeconfig` stored in Spaces. The function returns key details such as pod name, the namespace, pod status and its IP.

### GenAI Integration Use Cases

This function can be used as:
- A function calling endpoint for LLMs to retrieve real-time infrastructure information
- An API connector for AI agents managing cloud resources
- A data source for AI-powered cloud management dashboards


---

## Features

- **Retrieve Specific Pod:** Get information on a single pod.
- **List Pods:** Retrieve a list all  pods on your cluster.
- **List Namespaces:** Retrieve a list all namespaces on your cluster.
- **List Pod Status and Ips:** Retrieve the pod Status and IPs
- **Web-Enabled Function:** Configured to be deployed as a web-accessible function with an associated web secure token.

---

## Directory Structure

```
do-api/
├── project.yml                         # Project configuration file for deployment
└── packages/
    ── kube/
      └── list/
         ├── __main__.py             # Main API function script
         ├── build.sh                # Build script for dependency installation
         └── requirements.txt        # Python dependencies (kubernetes==32.0.1)

```

- **project.yml**
  Defines package parameters, function configuration (runtime, web settings, resource limits, etc.) including the secure token for web access.

- **packages/do-api/api/__main__.py**
  Contains the API logic to connect to DigitalOcean, retrieve droplet information, and format the API response.

- **packages/do-api/api/build.sh**
  A shell script to set up a virtual environment and install required Python packages targeting the correct runtime directory.

---

## Setup & Installation

### Environment Variables

Before running the API function, you need to set the "SPACES_ACCESS_KEY" and "SPACES_SECRET_KEY" environment variables.


### Python Dependencies

The function uses Python 3.11. The required dependency is specified in `packages/do-api/api/requirements.txt`:

```
kubernetes==32.0.1
```

To install the dependencies in your local environment, you can use the provided build script.

---
### Code Changes
Update the values for SPACES_REGION, SPACES_BUCKET and KUBECONFIG_FILE as needed.
```
SPACES_REGION = "nyc3"  #The region of your Spaces bucket
SPACES_BUCKET = "kubefiles"  # Spaces bucket name
KUBECONFIG_FILE = kubeconfig # The name of the kubeconfig file in Spaces BUcket 
```
## Deployment

The project is configured via `project.yml` for deployment on [DigitalOcean Functions](https://docs.digitalocean.com/products/functions/). Key points from the configuration include:

- **Runtime:** Python 3.11 (supported by DigitalOcean Functions)
- **Function Name:** `api`
- **Resource Limits:** Memory 512 MB, Timeout 5000 ms (within DigitalOcean Functions limits)

Make sure to integrate your deployment pipeline with the `project.yml` configuration. The environment variables are injected automatically into the function runtime.

### Deploying to DigitalOcean Functions

1. Install the DigitalOcean CLI (`doctl`)
2. Configure your DigitalOcean API token
3. Deploy the function:
   ```bash
   doctl serverless deploy .
   ```

---




Happy coding!

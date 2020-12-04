import logging
import sys, os
import time

from kubernetes import client, config, utils
import kubernetes.client
from kubernetes.client.rest import ApiException


class K8s(object):
    """
    This class handles creation and deletion of jobs in a kubernetes cluster.
    """
    def __init__(self):
        # Set logging
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        # Setup K8 configs
        # config.load_kube_config() # if running locally
        config.load_incluster_config()
        self.configuration = kubernetes.client.Configuration()
        self.api_instance = client.BatchV1Api()

    def generate_job_name(self):
        time_split = str(time.time()).split('.')
        name = "job-" + time_split[0] + "-" + time_split[1]
        return name


    def create_job_object(self, name, image, labels, backoff_limit, env):
        # Configureate Pod template container
        container = client.V1Container(
            name=name,
            image=image,
            env=env
        )
        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=labels),
            spec=client.V1PodSpec(restart_policy="Never", service_account_name="gke-app", containers=[container]))
        # Create the specification of deployment
        spec = client.V1JobSpec(template=template, backoff_limit=backoff_limit)
        # Instantiate the job object
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=name),
            spec=spec)
        return job

    def create_job(self, namespace, name, image, labels, backoff_limit, env_vars):
        # env variables are passed as a tuple. This creates one from the dictionary
        env =[]
        for i in env_vars.keys():
            env.append(client.V1EnvVar(name=i, value=env_vars[i]))

        api_response = self.api_instance.create_namespaced_job(
            body=self.create_job_object(name, image, labels, backoff_limit, env),
            namespace=namespace)
        return str(api_response)

    def get_jobs(self, namespace):
        api_response = self.api_instance.list_namespaced_job(
            namespace=namespace)
        jobs = []
        for i in range(len(api_response.items)):
            job = {}
            job['job_name'] = api_response.items[i].metadata.name
            job['status'] = api_response.items[i].status.conditions[0].type
            jobs.append(job)
        return jobs

    def get_job(self, namespace, name):
        api_response = self.api_instance.read_namespaced_job(
            name=name,
            namespace=namespace
        )
        return api_response.status.conditions[0].type

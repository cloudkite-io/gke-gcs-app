import uuid

from flask_api import FlaskAPI
from flask import request, jsonify

from gke import K8s


app = FlaskAPI(__name__)
k8s = K8s()


@app.route('/jobs', methods = ['POST'])
def create():
    image = "gcr.io/cloudkite-dev/gcs-app"
    job_name = request.data.get('job_name', f"gcs-uploader-{str(uuid.uuid4())[:4]}")
    namespace = request.data.get('namespace', 'demo')
    num_of_jobs = request.data.get('num_of_jobs', 5)
    try:
        # Alternatives for job parallelism logic is to
        # use spec.completions or spec.parallelism. See:
        # https://kubernetes.io/docs/concepts/workloads/controllers/job/#parallel-jobs
        env_vars = {
            "JOB_NAME": job_name,
            "BUCKET": "bucket-upload-test-script",
        }
        labels =  {
            "job": job_name
        }
        k8s.create_job(
            namespace=namespace,
            name=job_name,
            image=image,
            labels=labels,
            completions=num_of_jobs,
            backoff_limit=5,
            env_vars=env_vars
        )
        payload = {
            "message": f"Inserted {num_of_jobs} job(s)",
            "job_name": job_name
        }
    except Exception as e:
        payload = {
            "message": "Something went wrong data processing",
            "reason": str(e)
        }
    return jsonify(payload)

@app.route('/jobs/<namespace>', methods = ['GET'])
def list_jobs(namespace):
    try:
        payload = k8s.get_jobs(namespace)
    except Exception as e:
        payload = {
            "message": "Something went wrong data processing",
            "reason": e.__dict__['body']
        }

    return jsonify(payload)

@app.route('/jobs', methods = ['GET'])
def get_job():
    job_name = request.args.get('job_name')
    namespace = request.data.get('namespace', 'demo')
    try:
        job_status = k8s.get_job(namespace=namespace, name=job_name)
        payload = {
            "job_name": job_name,
            "job_status": job_status
        }

    except Exception as e:
        payload = {
            "message": "Something went wrong data processing",
            "reason": str(e)
        }
    return jsonify(payload)

@app.route('/health', methods = ['GET'])
def healthCheck():
    payload = {"status": "Up and running"}
    return payload


if __name__ == "__main__":
    app.run(debug=False)

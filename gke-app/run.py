from flask_api import FlaskAPI
from flask import request, jsonify

from gke import K8s

app = FlaskAPI(__name__)
k8s = K8s()


@app.route('/jobs', methods = ['POST'])
def create():
    namespace = 'test'
    image = "gcr.io/cloudkite-dev/gcs-app"
    labels = {
        "env": "development"
    }
    env_vars = {
        "BUCKET": "bucket-upload-test-script"
    }
    num_of_jobs = request.data.get('number_of_jobs')
    backoff_limit = 4
    job_name =[]

    try:
        for job_num in range(num_of_jobs):
            name=k8s.generate_job_name()
            env_vars['JOB_NAME'] = name
            job = k8s.create_job(
                namespace=namespace,
                name=name,
                image=image,
                labels=labels,
                backoff_limit=backoff_limit,
                env_vars=env_vars)
            job_name.append(name)
            payload = {
                "message": "The jobs have been created successfully",
                "job_names": job_name
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
    namespace = "test"
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

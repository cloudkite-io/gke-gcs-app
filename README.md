# gke-gcs-app

This is a 2 part demo. 
The 1st part, `gke-app`, shows how to use the kubernetes python client to create a job.
The 2nd part, `gcs-app`, is a simple script to create and upload a file to GCS bucket.

This demo is deployed [here](https://www.gke-app.gcp.dev.cloudkite.io/health)

## gke-app
The app is a small Flask API with 3 routes:

- `/jobs` : this is a `POST`. It takes in one variable `number_of_jobs` which specifies how many jos to create.
```bash
curl -XPOST -d "num_of_jobs=5" https://www.gke-app.gcp.dev.cloudkite.io/jobs
{
  "job_name": "gcs-uploader-140a",
  "message": "Inserted 5 job(s)"
}
```

- `/jobs?job_name=<JOB NAME>`: This is a `GET`. It returns the specified job and it's status.

```bash
curl "https://www.gke-app.gcp.dev.cloudkite.io/jobs?job_name=gcs-uploader-f220"
{
  "job_name": "gcs-uploader-f220",
  "job_status": {
    "active": null,
    "completion_time": "Tue, 08 Dec 2020 21:37:31 GMT",
    "failed": null,
    "start_time": "Tue, 08 Dec 2020 21:37:07 GMT",
    "succeeded": 5
  }
}
```


- `/jobs/<NAMESPACE>` : This is a `GET`. It returns a list of all the jobs in a namespace and their status.
```bash

curl "https://www.gke-app.gcp.dev.cloudkite.io/jobs/test"
[
  {
    "job_name": "gcs-uploader-7a92",
    "status": "Complete"
  },
  {
    "job_name": "gcs-uploader-7b2b",
    "status": "Complete"
  }
]
```


## gcs-app
The `POST` method in the `gke-app` creates a job with the image of the `gcs-app`.
This app creates a file and uploads this file to a GCS bucket.

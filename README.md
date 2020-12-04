# gke-gcs-app

This is a 2 part demo. 
The 1st part, `gke-app`, shows how to use the kubernetes python client to create a job.
The 2nd part, `gcs-app`, is a simple script to create and upload a file to GCS bucket.

This demo is deployed [here](https://www.gke-app.gcp.dev.cloudkite.io/health) 

## gke-app
The app is a small Flask API with 3 routes:

- `/jobs` : this is a `POST`. It takes in one variable `number_of_jobs` which specifies how many jos to create.
- `/jobs/<NAMESPACE>` : This is a `GET`. It returns a list of all the jobs in a namespace and their status.
- `/jobs?JOB_NAME=<JOB NAME>`: This is a `GET`. It returns the specified job and it's status.

## gcs-app
The `POST` method in the `gke-app` creates a job with the image of the `gcs-app`.
This app creates a file and uploads this file to a GCS bucket.

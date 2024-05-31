
# GCP Datastore Lookup API
This repository is designed as a Cloud Run Service which retrieves 1+ entities from a specified Datastore cache 

# Local Development
### 1. Build and Run Local Test
```commandline
docker-compose -f docker-compose-local.yml build gcp-datastore-lookup-api-local && docker-compose -f docker-compose-local.yml up gcp-datastore-lookup-api-local
```
**_NOTE:_**  There is a postman collection in the repo which can be used to test the endpoints, but 
you need to add your IP address in to the compose file for it to work


### 2. Build and Run Unit and Integration Tests
```commandline
docker-compose -f docker-compose.yml up --build 
```

#### Integration Tests
With the Docker Compose dev instance running:
```commandline
docker exec gcp-datastore-lookup-api-dev /bin/sh -c "poetry run pytest /home/appuser/tests/integration_tests/"
```

#### Unit Tests
With the Docker Compose dev instance running:
```commandline
docker exec gcp-datastore-lookup-api-dev /bin/sh -c "poetry run pytest /home/appuser/tests/unit_tests/"
```

#### Deploy to GCP Dev
For actually deploying to the dev environment
```
gcloud run deploy gcp-datastore-lookup-api-<your-name> \
 --image europe-west2-docker.pkg.dev/<GAR_NAME>:<VERSION_NUMBER> \
 --platform managed \
 --project <PROJECT_ID> \
 --region europe-west2 \
 --ingress=internal-and-cloud-load-balancing \
 --no-allow-unauthenticated \
 --service-account=<SA>.iam.gserviceaccount.com \
 --set-env-vars "GCP_PROJECT_ID=<PROJECT_ID>" --set-env-vars "TARGET_PROJECT_ID=<PROJECT_ID>" --set-env-vars "TARGET_BUCKET=<PROJECT_ID>-dummy_bucket" \
 --min-instances=3 \
 --max-instances=10 \
 --concurrency=100 \
 --memory=2Gi \
 --cpu=4 \
 --vpc-connector serverless-conn-ew2 --vpc-egress all-traffic
 
 
```
### API Model Updates
```commandline
datamodel-codegen  --input openapi/gcp_datastore_lookup_api.yaml --output src/pydantic_model/api_model.py
```

# AI-Watchdog-Smart-Cloud-Security-Monitoring
Project
================================================================================================================================================================================================


What is AI-Watchdog?
AI-Watchdog is a lightweight cloud-ready service that analyzes server logs with an anomaly-detection model and sends alerts when something looks suspicious. It’s a practical way to move your Colab prototype into a real, always-on service.

Highlights:
Small FastAPI app with an /analyze POST endpoint.
Put your trained model files under models/ and the app will load them at startup.
Dockerized for easy local testing and cloud deployment.
GitHub Actions workflow to build, push to ECR and deploy to ECS Fargate.
CloudWatch logging friendly out of the box.

Repo layout
bash
Copy
Edit
/ (repo root)
├─ app/
│  └─ main.py         # FastAPI app
├─ models/            # put your model files here
├─ requirements.txt
├─ Dockerfile
├─ ecs/task-def.json  # template, replace IMAGE_URI
└─ .github/workflows/deploy.yml

Quick start — run locally

Build the Docker image:
bash
Copy
Edit
docker build -t ai-watchdog:local .

Run it:
bash
Copy
Edit
docker run --rm -p 8080:8080 ai-watchdog:local

Test the endpoint:
bash
Copy
Edit
curl -s -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"logs":["login fail from 1.2.3.4"]}' | jq
If you get JSON back, the service is running.

Deploy summary (AWS Fargate)

This repo contains everything to deploy to AWS Fargate. High-level steps:
Create an ECR repo and push your image.
Create an ECS Fargate cluster, task execution role, and a service (or use the provided task-def template).

Add these GitHub Secrets in your repo:
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID, AWS_REGION
ECR_REPOSITORY, ECS_CLUSTER, ECS_SERVICE
Push to main — the GitHub Actions workflow will build and deploy.
If you want, I can write Terraform to automate steps 1–3.
Environment & secrets

Keep secrets out of code. Use:
GitHub Secrets for CI (AWS creds, account id, region, repo/service names).
AWS Secrets Manager for API keys or tokens, and pass those ARNs into the task definition as env vars.
The ECS Task Execution Role needs permissions to pull from ECR and write CloudWatch logs. Also allow iam:PassRole for the role.

How to add your model
Put your trained model in models/ (e.g., models/anomaly_model.joblib).
Update app/main.py to load and run your model. Keep model loading outside the request handler (load once on startup).
If your model is large or needs GPU, consider SageMaker or EC2 GPU instances — Fargate is best for small to medium CPU models.

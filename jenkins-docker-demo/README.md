# Jenkins -> Docker Hub Demo

A simple CI/CD project: a push to GitHub triggers a Jenkins pipeline that tests a Python script, builds it into a Docker image, and pushes the image to Docker Hub.

```
GitHub push --> Jenkins --> Test --> Build image --> Smoke test --> Push to Docker Hub
```

## Project structure

| File | Purpose |
|------|---------|
| `app.py` | Python script ("DevOps Tip Bot"): prints a random tip, time, hostname, Python version |
| `test_app.py` | Unit tests, run in the Test stage |
| `Dockerfile` | Builds the image from `python:3.12-slim` |
| `.dockerignore` | Keeps unneeded files out of the image |
| `Jenkinsfile` | Declarative pipeline definition |
| `README.md` | This file |

## Prerequisites

- A GitHub account and repository
- A Docker Hub account
- A Jenkins server with:
  - Docker installed
  - Python 3 installed
  - Plugins: Pipeline, Git, Credentials Binding (installed by default with suggested plugins)

## Setup

### 1. Push the project to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Allow Jenkins to use Docker
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 3. Create a Docker Hub access token
Docker Hub > Account Settings > Security > New Access Token (Read & Write).

### 4. Add the credential in Jenkins
Manage Jenkins > Credentials > Global > Add Credentials:
- Kind: **Username with password**
- Username: your Docker Hub username
- Password: the access token
- ID: `dockerhub-creds`

### 5. Edit the Jenkinsfile
Set `DOCKERHUB_USER` to your Docker Hub username:
```groovy
DOCKERHUB_USER = 'your-dockerhub-username'
```

### 6. Create the pipeline job
New Item > Pipeline > under Pipeline choose **Pipeline script from SCM**:
- SCM: Git
- Repository URL: your GitHub repo
- Branch: `*/main`
- Script Path: `Jenkinsfile`

### 7. (Optional) Trigger builds on every push
- GitHub repo > Settings > Webhooks > Add webhook
  - Payload URL: `http://<jenkins-url>/github-webhook/`
  - Content type: `application/json`
- In the Jenkins job, tick **GitHub hook trigger for GITScm polling**.

### 8. Run it
Click **Build Now**. On success, the image appears on Docker Hub as
`<your-username>/devops-tip-bot` with tags `<build-number>` and `latest`.

## Run the image

```bash
docker run --rm <your-username>/devops-tip-bot:latest
```

Example output:
```
==================================================
DevOps Tip Bot
==================================================
Time      : 2026-11-04T10:15:00+00:00
Host      : 3f2a9c1d7b44
Python    : 3.12.x
Build tag : devops-tip-bot-1
--------------------------------------------------
Tip: Tag images with build numbers, not just 'latest'.
```

## Run locally (without Jenkins)

```bash
python3 app.py
python3 -m unittest -v
docker build -t devops-tip-bot .
docker run --rm devops-tip-bot
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `permission denied ... /var/run/docker.sock` | Add the `jenkins` user to the `docker` group and restart Jenkins (step 2) |
| `denied: requested access to the resource is denied` | Check `DOCKERHUB_USER` matches your Docker Hub username and the token has Read & Write |
| `python3: not found` in Test stage | Install Python 3 on the Jenkins agent |
| Credential not found | The credential ID must be exactly `dockerhub-creds` |
| Webhook does not trigger | Jenkins must be reachable from the internet; check the webhook's "Recent Deliveries" in GitHub |

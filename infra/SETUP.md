# Azure Infrastructure Setup

This pipeline deploys to Azure Container Apps.
Infrastructure was provisioned manually via Azure CLI.
Azure resources have been torn down after project completion to avoid charges.

## Architecture

    GitHub (code) -> Azure DevOps (3-stage pipeline) -> ACR (image) -> Azure Container Apps (runtime)

    Stage 1: Test   -> pytest runs on self-hosted agent
    Stage 2: Build  -> docker buildx build --platform linux/amd64 -> push to ACR
    Stage 3: Deploy -> az containerapp update -> new revision live

## Resources Provisioned

| Resource | Name | Purpose |
|---|---|---|
| Resource Group | rg-azure-devops-cicd | Container for all resources |
| Container Registry | jackiedevops4acr | Stores Docker images |
| Container App Environment | cae-devops-cicd | Hosts Container Apps |
| Container App | ca-devops-cicd | Runs FastAPI (port 8000) |
| Azure DevOps Project | azure-devops-cicd | Hosts pipeline and repo mirror |

## Bootstrap Commands

    # 1. Resource group
    az group create --name rg-azure-devops-cicd --location southeastasia

    # 2. Container Registry
    az acr create --name jackiedevops4acr --resource-group rg-azure-devops-cicd --sku Basic --admin-enabled true

    # 3. Container App Environment
    az containerapp env create --name cae-devops-cicd --resource-group rg-azure-devops-cicd --location southeastasia

    # 4. Container App (initial placeholder)
    az containerapp create --name ca-devops-cicd --resource-group rg-azure-devops-cicd --environment cae-devops-cicd --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest --target-port 8000 --ingress external

## Azure DevOps Setup

    # 5. Create service connection in Azure DevOps
    # Project Settings -> Service connections -> New -> Azure Resource Manager
    # Name: Azure-ServiceConnection (must match azure-pipelines.yml)

    # 6. Register self-hosted agent (laptop)
    mkdir myagent && cd myagent
    # Download agent from Azure DevOps -> Project Settings -> Agent pools -> Default -> New agent
    ./config.sh --url https://dev.azure.com/{org} --auth pat --token {PAT}
    ./run.sh

## Pipeline Variables (non-sensitive, defined in azure-pipelines.yml)

| Variable | Value | Notes |
|---|---|---|
| acrName | jackiedevops4acr | ACR instance name |
| acrLoginServer | jackiedevops4acr.azurecr.io | Full ACR URL |
| imageName | azure-devops-cicd | Image repository name |
| imageTag | $(Build.BuildId) | Auto-incrementing integer per run |
| containerAppName | ca-devops-cicd | Container App to update |
| resourceGroup | rg-azure-devops-cicd | Resource group name |

## Why Not Terraform Here?

Repo 1 (azure-fastapi-project) demonstrates full Terraform IaC with remote state backend.
This repo focuses on the Azure DevOps 3-stage pipeline pattern (Test -> Build -> Deploy)
and self-hosted agent setup. In production both would use Terraform.

## Teardown

    az group delete --name rg-azure-devops-cicd --yes --no-wait

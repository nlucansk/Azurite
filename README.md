# Azurite

## Introduction
Azurite is a "helper tool" designed to help you manage your Azure resources. <br>
It's using TerraformCDK to create and manage the resources.

## Goal
Is to make management of infrastructure easier and more efficient. Using only 1 config to drive the deployment logic<br>
Tool can be used "standalone" or as a part of a CI/CD pipeline

## Prerequisites
- [TerraformCDK](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install)

## Getting Started
1. Clone the repository
2. Export your Azure credentials as environment variables / use Azure cli etc ...
    ```bash
    export TENANT_ID="XXXXXXXXXXX"
    export SUBSCRIPTION_ID="XXXXXXXXXXX"
    export CLIENT_ID="XXXXXXXXXXX"
    export CLIENT_SECRET="XXXXXXXXXXX"
    ```
3. Create and fill the `config/config.yml` file (use the `config/config_template.yml` as an example)
4. Run the following commands
    ```bash
    pipenv shell
    cdktf plan ... 
    cdktf deploy / cdktf deploy "stack_name"
    ```
5. To destroy the resources, run the following command
    ```bash
   ...
   cdktf destroy
    ```

## Capabilities
- [x] Create Resource group
- [ ] Create Storage account
- [ ] Create App Service Plan
- [ ] Create App Service
- [ ] Create SQL Database
- [ ] Create SQL Server
- [ ] Create Key Vault
- [ ] Create Virtual Network
- [ ] Create Virtual Machine
- [ ] Create Kubernetes Cluster
- [ ] Create CosmosDB
- [ ] Create Function App
- [ ] Create Logic App
- [ ] Create Service Bus
- [ ] Create Redis Cache
- [ ] Create CDN
- [ ] Create Traffic Manager
- [ ] Create API Management
- [ ] Create Event Grid
- [ ] Create Event Hub
- [ ] Create Front Door
- [ ] Create Mysql Database
- [ ] Create Postgres Database
- [ ] Create Container Registry
- [ ] Generate Infrastructure Diagram
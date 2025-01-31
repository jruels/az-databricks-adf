### **Lab: Setting Up CI/CD for Azure Data Factory Using Azure DevOps**

#### **Objective**
By the end of this lab, you will:
- Set up a CI/CD pipeline for Azure Data Factory (ADF) using Azure DevOps.
- Integrate Azure Data Factory with Git for source control.
- Deploy ADF resources automatically to a test environment using a release pipeline.

---

### **Prerequisites**
1. An active **Azure Subscription**.
2. Access to **Azure Data Factory**.
3. An **Azure DevOps Organization** (create one [here](https://dev.azure.com) if needed).
4. Basic familiarity with Azure and DevOps (we’ll provide step-by-step instructions).

---

### **Step 1: Integrate Azure Data Factory with Git**

1. **Navigate to Azure Data Factory Studio**:
   - Go to the Azure portal.
   - Open your Data Factory instance.
   - Click on **Launch Studio** to open the ADF Studio.

2. **Set Up Git Integration**:
   - In ADF Studio, click on the **Manage** tab (wrench icon).
   - Under **Git configuration**, click **Configure**.
   - Select **Azure DevOps Git** and sign in to your Azure DevOps account.
   - Choose:
     - **Azure DevOps organization**: Select your organization.
     - **Project name**: Choose or create a project in Azure DevOps.
     - **Repository name**: Create or select a repository to store your ADF code.
     - **Collaboration branch**: Use `main` or create a new branch.
   - Save the configuration.

3. **Publish to Git**:
   - Open a pipeline in ADF Studio.
   - Save your work to Git by clicking **Save All** and then **Publish**.

📘 **Resource**: [Microsoft Docs: Source control in ADF](https://learn.microsoft.com/en-us/azure/data-factory/source-control).

---

To find or create the Azure service connection (`azureSubscription`) in Azure DevOps, follow these steps:

### **Step-by-Step Guide to Create an Azure Service Connection**

1. **Navigate to Azure DevOps Project**:
   - Go to your Azure DevOps project.
   - Select **Project Settings** (found at the bottom left corner).

2. **Service Connections**:
   - Under **Pipelines**, select **Service connections**.
   - Click **Create service connection**.

3. **Choose Azure Resource Manager**:
   - In the list of service connection types, select **Azure Resource Manager**.
   - Click **Next**.

4. **Authentication Method**:
   - Choose the authentication method. The most common method is **App registration (automatic)**.
   - Click **Next**.

5. **Configure the Service Connection**:
   - **Scope level**: Choose **Subscription**.
   - **Subscription**: Select your Azure subscription from the dropdown.
   - **Resource Group**: You can leave this blank to allow access to all resource groups or specify a particular resource group.
   - **Service connection name**: Provide a name for the service connection (e.g., `MyAzureServiceConnection`).
   - **Security**: Optionally, grant access permissions to all pipelines.

6. **Create the Service Connection**:
   - Click **Save** to create the service connection.

### **Using the Service Connection in Your Pipeline**

Once the service connection is created, you can reference it in your pipeline YAML file. Replace `<Your Azure Service Connection>` with the name of your service connection.



### **Step 2: Create an Azure DevOps Build Pipeline**

1. **Go to Azure DevOps**:
   - Navigate to your DevOps project.
   - Select **Pipelines > New Pipeline**.

2. **Connect to Your Repository**:
   - Choose your repository connected to ADF.
   - Select the source branch (`main` or collaboration branch).

3. **Configure the Build Pipeline**:
   - Choose **Starter Pipeline** or **Existing YAML**.
   - Use the following YAML to create a build pipeline:

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'windows-latest'

steps:
  - task: UseDotNet@2
    inputs:
      packageType: sdk
      version: '3.1.x'
      installationPath: $(Agent.ToolsDirectory)/dotnet

  - task: AzureCLI@2
    inputs:
      azureSubscription: 'MyAzureServiceConnection'
      scriptType: 'ps'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az datafactory pipeline create --resource-group rg-adf-<your name> --factory-name adf-<your name> --name "MyPipeline" --output $(Build.ArtifactStagingDirectory)/adf/adf-pipeline.json

  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: '$(Build.ArtifactStagingDirectory)/adf'
      ArtifactName: 'adf-pipeline'
    
```

4. **Save and Run the Pipeline**:
   - Click **Save and Run** to save and test the pipeline.

📘 **Resource**: [Microsoft Docs: CI/CD with ADF](https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-deployment).

---

### **Step 3: Create an Azure DevOps Release Pipeline**

1. **Navigate to Releases**:
   - Go to **Pipelines > Releases** and click **New Pipeline**.

2. **Add an Artifact**:
   - Click **Add an artifact** and select the build pipeline you created earlier.
   - Select the latest version as the default source.

3. **Define Stages**:
   - Click **Add a stage** and select **Empty Job**.
   - Rename it as **Test Environment**.

4. **Configure Deployment Task**:
   - In the Test Environment stage:
     - Click **Tasks** > **Agent Job**.
     - Add an **Azure CLI** task.
     - Use the following inline script to deploy ADF resources:

       ```bash
       az datafactory pipeline create \
         --resource-group <ResourceGroup> \
         --factory-name <ADFName> \
         --name "<PipelineName>" \
         --pipeline $(System.DefaultWorkingDirectory)/adf-pipeline.json
       ```

     - Replace `<ResourceGroup>`, `<ADFName>`, and `<PipelineName>` with your actual resource details.

5. **Add Post-Deployment Validation**:
   - Add another **Azure CLI** task to validate pipeline deployment by triggering a test run:
     ```bash
     az datafactory pipeline run \
       --resource-group <ResourceGroup> \
       --factory-name <ADFName> \
       --pipeline-name "<PipelineName>"
     ```

---

### **Step 4: Test and Validate**

1. **Trigger the Release**:
   - Manually trigger the release pipeline or configure a schedule.
2. **Monitor the Deployment**:
   - Check the **Release Logs** for deployment progress and success.
3. **Test Deployed Pipeline**:
   - Verify the pipeline in the ADF Test environment by running a test execution.

---

### **Step 5: Implement Logging**

1. **Add Logging to Release Pipeline**:
   - Use Azure Monitor or Log Analytics for tracking pipeline runs.
   - Add additional CLI tasks to log success/failure messages to a central logging system or database.

2. **Set Up Alerts**:
   - In Azure DevOps or Monitor, set up alerts for failed deployments.

📘 **Resource**: [Azure Monitor for ADF](https://learn.microsoft.com/en-us/azure/data-factory/monitor-using-azure-monitor).

---

### **Expected Outcome**

- **Build Pipeline**: A build pipeline in Azure DevOps that packages and uploads ADF pipelines to an artifact.
- **Release Pipeline**: A release pipeline that deploys ADF resources to a test environment and validates the deployment.
- **Git Integration**: Azure Data Factory integrated with Git for source control.

# Lab 1 to 3 Using Python Notebooks

Below are detailed instructions to replicate Labs 1, 2, and 3 via Python notebooks instead of the Azure Portal. This approach uses:
- Python 3+ (You can check if Python is installed by running `python --version` in Powershell)
- Azure CLI (invoked from a notebook)  (You can check if it's installed by running `az --version`)
- Jupyter or any IPython-based environment  

> **Tip:** If you do not have Python or Jupyter installed, see [Python Downloads](https://www.python.org/downloads/) and install Jupyter via `pip install jupyter` Make sure to add python to the PATH environment variable during installation.

---
## 1. Set Up Your Development Environment


1. Download and install the [Azure CLI](https://azcliprod.blob.core.windows.net/msi/azure-cli-2.64.0-x64.msi)
2. Open a terminal (on Windows, “Command Prompt” or “PowerShell”).  

```bash
# Install Azure CLI (if not already installed)
pip install azure-cli

# (Re)Login to Azure
az login
```

---

## Lab 1: Create ADF and Resource Group

**Objective:** Create a resource group and an Azure Data Factory instance from Python notebook cells.

1. **Create Resource Group**  
   Replace `<your-name>`, `<location>`, and `<subscription-id>` as needed:
   ```bash
   # Create resource group
   $env:resourceGroup="rg-adf-<your-name>"
   $env:location="<location>"
   $env:subscriptionId=az account show --query id --output tsv
   $env:datafactory="<data-factory-name>"
   az group create --name $env:resourceGroup --location $env:location --subscription $env:subscriptionId
   ```


2. **Create Data Factory**
   The name of your data factory resource must be globally unique.
   When prompted to install the data factory extension, type **y** to continue
   ```python
   # Create ADF instance
   az datafactory create --resource-group $env:resourceGroup --factory-name $env:datafactory --location $env:location
   ```

4. **Verify Creation**  
   ```bash
   # List all Data Factories in the resource group
   az datafactory list --resource-group $env:resourceGroup
   ```

---

## Lab 2: Create Pipeline with Azure Database for PostgreSQL

**Objective:** Provision Azure Database for PostgreSQL, create a Storage account, upload CSV, and connect them via a pipeline.

### 2.1 Create a Storage Account
```bash
# Create a globally  unique storage account
$env:storageAccount="<replace-with-storage-account-name>"
az storage account create --resource-group $env:resourceGroup --name $env:storageAccount --location $env:location --sku Standard_LRS
```

### 2.2 Create Container & Upload CSV
```python
# Create a container
az storage container create --account-name $env:storageAccount --name inputcontainer

# Upload lab2data.csv
az storage blob upload --account-name $env:storageAccount --container-name inputcontainer --name lab2data.csv --file 'c:/path/to/lab2data.csv'
```

### 2.3 Create Azure Database for PostgreSQL

With PowerShell, you must ensure Get-ExecutionPolicy is not Restricted. We suggest using Bypass to bypass the policy to get things installed or AllSigned for quite a bit more security.

Run `Get-ExecutionPolicy`. If it returns Restricted, then run `Set-ExecutionPolicy AllSigned` or `Set-ExecutionPolicy Bypass -Scope Process`.

Run the following command to install chocolatey:
```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Run the following command to install `psql`:
```bash
choco install postgresql
```
When prompted to add your client IP address, type **y**:
`Detected current client IP : 20.83.210.238
Do you want to enable access to client 20.83.210.238 (y/n):`

```bash
# Create Azure Database for PostgreSQL flexible server
$env:postgresServer="<your-postgres-server>"
$env:adminUser="<admin-user>"
$env:adminPassword="<admin-password>"
$env:postgresVersion="16"
$env:postgresTier="GeneralPurpose"
$env:postgresSku="Standard_D2s_v3"
$env:postgresStorage="128"

az postgres flexible-server create --subscription $env:subscriptionId --resource-group $env:resourceGroup --name $env:postgresServer --location $env:location --version $env:postgresVersion --admin-user $env:adminUser --admin-password $env:adminPassword --tier $env:postgresTier --sku-name $env:postgresSku --storage-size $env:postgresStorage

```
Copy the text from the command output and save it somewhwere. 

### 2.4 Create Table and Insert Example Data
Use a local PostgreSQL client or psql from the notebook (install psql or use Python drivers), for example:
```bash
# Example using psql if installed locally: 
psql "sslmode=require host=$env:postgresServer.postgres.database.azure.com user=$env:adminUser password=$env:adminPassword dbname=postgres" -c "CREATE TABLE public.sample_data (id SERIAL PRIMARY KEY, name VARCHAR(100), value INT);"

```
```bash
# Insert data rows
psql "sslmode=require host=$env:postgresServer.postgres.database.azure.com user=$env:adminUser password=$env:adminPassword dbname=postgres" -c "INSERT INTO public.sample_data(name, value) VALUES ('Test1',123),('Test2',456);"
```

### 2.5 Create Pipeline using Python SDK

**Prerequisites (as defined in the provided document):**

1.  **Python 3.x:** You need Python 3 installed on your system.
2.  **Azure CLI:** The Azure CLI must be installed and you must be logged in with `az login`.
3.  **Jupyter/IPython:**  You should be working in a Jupyter notebook environment or similar.

**Python Package Installation**

First, ensure you have the necessary Azure Python SDK packages and Azure Developer CLI installed by running the following command in the terminal:

```python
choco install winget
pip install azure-mgmt-datafactory azure-identity
winget install microsoft.azd
```

**Lab 2.5 - Create Pipeline in ADF (Programmatically)**

This section will replace the manual steps in the original lab instructions with Python code to create a pipeline within ADF.

1. Open a terminal (on Windows, “Command Prompt” or “PowerShell”).  
2. Run `jupyter notebook` or open your notebook in VS Code.
3. Create a new Notebook and give it a name
4. Add the code below to your notebook cells

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import (
    LinkedServiceResource,
    AzureStorageLinkedService,
    AzurePostgreSqlLinkedService,
    DatasetResource,
    DelimitedTextDataset,
    PostgreSqlTableDataset,
    CopyActivity,
    PipelineResource,
    DatasetStorageFormat,
    DatasetCompression,
    LinkedService,
    Dataset,
    Activity
    )
import json

# 1. Configure Credentials and Clients
credential = DefaultAzureCredential()

# Replace with your actual values
subscription_id = "<subscription-id>"
resource_group = "rg-adf-<your-name>"
factory_name = "<your-adf-name>"
storage_account_name = "<uniqueStorageAccountName>"
postgres_server_name= "<your-postgres-server>.postgres.database.azure.com"
postgres_admin_user = "<admin-user>"
postgres_admin_password = "<admin-password>"
storage_container_name = "inputcontainer"
storage_file_name = "lab2data.csv"
table_name = "public.sample_data"
location = "<location>"



df_client = DataFactoryManagementClient(credential, subscription_id)



# 2. Create Linked Services

# 2.1 Create Azure Storage Linked Service
storage_linked_service = LinkedServiceResource(
    properties=AzureStorageLinkedService(
    connection_string={
        "type": "SecureString",
        "value": f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};EndpointSuffix=core.windows.net;"
    }
    ))
print("Creating storage linked service...")
ls_storage = df_client.linked_services.create_or_update(resource_group,factory_name, "AzureStorageLinkedService", storage_linked_service)

print(f"storage linked service created {ls_storage.name}")

# 2.2 Create Azure PostgreSQL Linked Service
postgres_linked_service = LinkedServiceResource(
    properties=AzurePostgreSqlLinkedService(
        server = postgres_server_name,
        database = "postgres",
        username = postgres_admin_user,
        password = {
            "type": "SecureString",
            "value": postgres_admin_password
        }
    ))
print("Creating postgres linked service...")
ls_postgres = df_client.linked_services.create_or_update(resource_group, factory_name, "AzurePostgreSqlLinkedService", postgres_linked_service)
print(f"postgres linked service created {ls_postgres.name}")


# 3. Create Datasets
# 3.1 Create Azure Storage CSV Dataset
storage_dataset = DatasetResource(
        properties=DelimitedTextDataset(
        linked_service_name=LinkedService(
            reference_name="AzureStorageLinkedService",
            type="LinkedServiceReference",
        ),
         folderPath=storage_container_name,
        fileName=storage_file_name,
        compression= DatasetCompression(type="none"),
        location_type="AzureBlobStorageLocation",
        columnDelimiter = ",",
        rowDelimiter="\n",
        first_row_as_header = True
    ))
print("Creating CSV dataset...")
ds_csv = df_client.datasets.create_or_update(resource_group, factory_name, "AzureBlobCSVDataset", storage_dataset)
print(f"csv dataset created {ds_csv.name}")


# 3.2 Create Azure PostgreSQL Table Dataset
postgres_dataset = DatasetResource(
    properties=PostgreSqlTableDataset(
        linked_service_name=LinkedService(
            reference_name="AzurePostgreSqlLinkedService",
            type="LinkedServiceReference"
        ),
       table_name = table_name
    ))
print("Creating postgres dataset...")
ds_postgres = df_client.datasets.create_or_update(resource_group, factory_name, "AzurePostgreSqlDataset", postgres_dataset)
print(f"postgres dataset created {ds_postgres.name}")

# 4. Create Copy Activity
from azure.mgmt.datafactory.models import CopyActivity, PipelineResource, DatasetReference, DelimitedTextSource, AzurePostgreSqlSink,BlobSource
copy_activity = CopyActivity(
    name="CopyDataFromBlobToPostgres",
    inputs=[DatasetReference(reference_name="AzureBlobCSVDataset",type="DatasetReference")],
    outputs=[DatasetReference(reference_name="AzurePostgreSqlDataset",type="DatasetReference")],
    source=DelimitedTextSource(),
    sink=AzurePostgreSqlSink(write_batch_timeout="00:05:00", write_batch_size=10000)
)

# Create a pipeline with the copy activity
pipeline_name = "copyPipeline"
params_for_pipeline = {}
pipeline_obj = PipelineResource(activities=[copy_activity], parameters=params_for_pipeline)
pipeline = df_client.pipelines.create_or_update(resource_group, factory_name, pipeline_name, pipeline_obj)
print(f"Pipeline created: {pipeline.name}")
```

**Key Points and Explanations:**

*   **Azure SDK:** The code uses the `azure-mgmt-datafactory` library, which provides a Pythonic way to interact with the Data Factory service.
*   **Credentials:** We're using `AzureCliCredential()` which uses the credentials from your already logged-in Azure CLI session.
*   **Linked Services:** These define the connection information for the data stores (Azure Storage, PostgreSQL). We create linked services for both the storage account where the CSV is located and the PostgreSQL flexible server.
*   **Datasets:** These define the specific data you're working with within the linked services. For example, the "AzureBlobCSVDataset" refers to the `lab2data.csv` within the storage container and the `AzurePostgreSqlDataset` points to your table in postgres.
*   **Copy Activity:** This activity is the core of the pipeline. It copies data from the source dataset to the target dataset.
*   **Pipeline:**  The pipeline ties together the activities, and this creates a pipeline called `PostgreSQLCopyPipeline`.
*   **`create_or_update()`:** We use this method for all resources, allowing you to update existing ones if they already exist, or create new ones if they don't.
*   **Error Handling**:  You can add exception handling around API calls to gracefully manage errors.

## Lab 3: Run the Pipeline & Monitor

**Objective:** Execute the newly created pipeline and monitor its run status—still from Python if desired (REST or CLI calls).

1. **Trigger Pipeline via REST API**  
   - Obtain a bearer token via `az account get-access-token`.  
   - Send a POST request to ADF’s pipeline create-run endpoint. Example:
     ```python
     import json
     import requests
     
     # Replace with your details
     subscription_id = "<subscription-id>"
     resource_group = "rg-adf-<your-name>"
     factory_name = "<your-adf-name>"
     pipeline_name = "PostgreSQLCopyPipeline"
     
     token = !az account get-access-token --query accessToken --output tsv
     headers = {
         "Authorization": f"Bearer {token[0]}",
         "Content-Type": "application/json"
     }
     
     url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.DataFactory/factories/{factory_name}/pipelines/{pipeline_name}/createRun?api-version=2018-06-01"
     resp = requests.post(url, headers=headers, json={})
     print("Run pipeline response:", resp.json())
     ```

2. **Monitor Pipeline Run**
   ```python
   # Check pipeline runs
   url_runs = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.DataFactory/factories/{factory_name}/queryPipelineRuns?api-version=2018-06-01"
   payload = {"lastUpdatedAfter": "2023-01-01T00:00:00Z", "lastUpdatedBefore": "2024-01-01T00:00:00Z"}
   runs_resp = requests.post(url_runs, headers=headers, json=payload)
   print("Pipeline runs:", runs_resp.json())
   ```

3. **Validate Output**
   - Confirm pipeline run status is "Succeeded."  
   - Check PostgreSQL table for data using psql or a SQL tool:
     ```python
     !psql -h <your-postgres-server>.postgres.database.azure.com \
         -U <admin-user> \
         -d postgres \
         -c "SELECT COUNT(*) FROM public.sample_data;"
     ```

---

## Conclusion
Using a Python notebook, you have:
1. Created Azure resources (Resource Group, ADF, Storage, PostgreSQL).  
2. Deployed a pipeline from the Azure Portal or via REST.  
3. Triggered the pipeline and monitored runs with Python code.  
4. Validated data movement in PostgreSQL.

Experiment with different data formats, advanced copy settings, and pipeline configurations to deepen your mastery of Azure Data Factory.  


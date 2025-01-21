# Lab 1 to 3 Using Python Notebooks

Below are detailed instructions to replicate Labs 1, 2, and 3 via Python notebooks instead of the Azure Portal. This approach uses:
- Python 3+  
- Azure CLI (invoked from a notebook)  
- Jupyter or any IPython-based environment  

> **Tip:** If you do not have Python or Jupyter installed, see [Python Downloads](https://www.python.org/downloads/) and install Jupyter via `pip install jupyter`.

---
## 1. Set Up Your Development Environment

```python
# filepath: /Labs/Day1/ADF_Full_Labs.ipynb

# Install Azure CLI (if not already installed)
!pip install azure-cli
# Optionally install Azure CLI interactive extension
!az extension add --name interactive

# (Re)Login to Azure
!az login
```
1. Open a terminal (on Windows, “Command Prompt” or “PowerShell”).  
2. Run `jupyter notebook` or open your notebook in VS Code.  
3. Copy the lines above into a notebook cell and run it.

---

## Lab 1: Create ADF and Resource Group

**Objective:** Create a resource group and an Azure Data Factory instance from Python notebook cells.

1. **Create Resource Group**  
   Replace `<your-name>`, `<location>`, and `<subscription-id>` as needed:
   ```python
   # Create resource group
   !az group create --name rg-adf-<your-name> --location <location> --subscription <subscription-id>
   ```

2. **Create Data Factory**  
   ```python
   # Create ADF instance
   !az datafactory create \
       --resource-group rg-adf-<your-name> \
       --factory-name <your-adf-name> \
       --location <location>
   ```

3. **Verify Creation**  
   ```python
   # List all Data Factories in the resource group
   !az datafactory list --resource-group rg-adf-<your-name>
   ```

---

## Lab 2: Create Pipeline with Azure Database for PostgreSQL

**Objective:** Provision Azure Database for PostgreSQL, create a Storage account, upload CSV, and connect them via a pipeline.

### 2.1 Create a Storage Account
```python
# Create a storage account
!az storage account create \
    --resource-group rg-adf-<your-name> \
    --name <uniqueStorageAccountName> \
    --location <location> \
    --sku Standard_LRS
```

### 2.2 Create Container & Upload CSV
```python
# Create a container
!az storage container create \
    --account-name <uniqueStorageAccountName> \
    --name inputcontainer

# Upload lab2data.csv
!az storage blob upload \
    --account-name <uniqueStorageAccountName> \
    --container-name inputcontainer \
    --name lab2data.csv \
    --file c:/path/to/lab2data.csv
```

### 2.3 Create Azure Database for PostgreSQL

Use the CLI parameters to specify configuration details for the PostgreSQL flexible server:

- subscription: Sets which Azure subscription to use.
- resource-group: Specifies the resource group for the new server.
- name: Gives the server a unique name.
- location: Chooses the Azure region.
- version: Defines the PostgreSQL version.
- zone: Selects the availability zone.
- password-auth: Enables password-based authentication.
- admin-user / admin-password: Sets admin credentials for the server.
- tier / sku-name: Chooses the pricing tier and compute size.
- storage-type / storage-size: Picks the storage type and size.
- performance-tier: Configures the server performance tier.
- storage-auto-grow: Automatically increases storage as needed.
- high-availability: Enables or disables regional HA.
- public-access: Allows or restricts public connections.

You can learn more about the parameters here: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server?tabs=cli-create-flexible%2Cportal-get-connection%2Cportal-delete-resources

```python
# Create Azure Database for PostgreSQL flexible server
!az postgres flexible-server create --subscription <subscription> --resource-group rg-adf-<your-name> --name <name> --location <region> --version <version> --zone <zone> --password-auth <password-auth> --admin-user <admin-user> --admin-password <admin-password> --tier <tier> --sku-name <sku-name> --storage-type <storage-type> --storage-size <storage-size> --performance-tier <performance-tier> --storage-auto-grow <storage-auto-grow> --high-availability <high-availability> --standby-zone <standby-zone> --backup-retention <backup-retention> --geo-redundant-backup <geo-redundant-backup> --public-access <public-access> --tags <tags>
```

Configure firewall to allow Azure services and your client IP:
```python
!az postgres flexible-server firewall-rule create \
    --resource-group rg-adf-<your-name> \
    --name <your-postgres-server> \
    --rule-name AllowAll \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 255.255.255.255
```

### 2.4 Create Table and Insert Example Data
Use a local PostgreSQL client or psql from the notebook (install psql or use Python drivers), for example:
```python
# Example using psql if installed locally: 
!psql "sslmode=require host=<your-postgres-server>.postgres.database.azure.com user=<admin-user> password=<admin-password> dbname=postgres" -c "CREATE TABLE public.sample_data (id SERIAL PRIMARY KEY, name VARCHAR(100), value INT);"

```
```python
# Insert data rows
!psql "sslmode=require host=<your-postgres-server>.postgres.database.azure.com user=<admin-user> password=<admin-password> dbname=postgres" -c "INSERT INTO public.sample_data(name, value) VALUES ('Test1',123),('Test2',456);"
```

### 2.5 Create Pipeline using Python SDK

**Prerequisites (as defined in the provided document):**

1.  **Python 3.x:** You need Python 3 installed on your system.
2.  **Azure CLI:** The Azure CLI must be installed and you must be logged in with `az login`.
3.  **Jupyter/IPython:**  You should be working in a Jupyter notebook environment or similar.

**Python Package Installation**

First, ensure you have the necessary Azure Python SDK packages installed:

```python
!pip install azure-mgmt-datafactory azure-identity
```

**Lab 2.5 - Create Pipeline in ADF (Programmatically)**

This section will replace the manual steps in the original lab instructions with Python code to create a pipeline within ADF.

```python
from azure.identity import AzureCliCredential
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
    DatasetTextFormat,
    LinkedService,
    Dataset,
    Activity
    )
import json


# 1. Configure Credentials and Clients
credential = AzureCliCredential()

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
copy_activity = Activity(
        name = "CopyDataFromBlobToPostgres",
        type = "Copy",
        inputs = [Dataset(reference_name = "AzureBlobCSVDataset")],
        outputs=[Dataset(reference_name = "AzurePostgreSqlDataset")],
        type_properties = {
            "source": {
                "type": "DelimitedTextSource"
             },
             "sink": {
                "type": "PostgreSqlSink",
                 "writeBatchTimeout": "00:05:00",
                 "writeBatchSize": 10000
            }
        }
)


# 5. Create Pipeline
pipeline = PipelineResource(
    properties = {
        "activities": [copy_activity]
    }
)
print("Creating Pipeline...")
pipeline_result = df_client.pipelines.create_or_update(resource_group, factory_name, "PostgreSQLCopyPipeline", pipeline)
print(f"Pipeline created {pipeline_result.name}")
print("Pipeline creation complete.")
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


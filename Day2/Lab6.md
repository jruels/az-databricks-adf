### **Lab: Building Complex Data Workflows with Azure Data Factory and Azure Databricks**

This lab includes detailed step-by-step instructions for creating the required Azure resources, building a pipeline with Azure Data Factory (ADF), integrating with Azure Databricks, and leveraging advanced control flow features. Assume no prior knowledge of the tools.

---

### **Step 1: Prerequisites**

#### **1.1 Install Azure CLI (Optional)**
- Follow this guide to install the Azure CLI: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

#### **1.2 Download Sample Datasets**
1. Download the datasets:
   - [Happiness Data (CSV)]
   - [Population Data (CSV)]
2. Save these files locally; you’ll upload them to Azure Blob Storage.

---

### **Step 2: Create Azure Resources**

#### **2.1 Create Azure Storage Account**
1. Log in to the [Azure Portal](https://portal.azure.com).
2. If you already have an existing storage account you can skip this step and go to step 7
3. Search for **Storage Accounts** in the search bar.
4. Click **+ Create**.
5. In the **Basics** tab:
   - Subscription: Choose your subscription.
   - Resource Group: Click **Create New** and name it (e.g., `ADF-Lab-Group`).
   - Storage Account Name: Enter a unique name (e.g., `adflabstorage`).
   - Region: Select a region close to you.
   - Performance: Standard.
   - Redundancy: Locally-redundant storage (LRS).
6. Click **Review + Create**, then **Create**.
7. Once deployed, go to the **Storage Account**, and under **Containers**, create a new container (e.g., `inputdata`).

#### **2.2 Upload Files to Blob Storage**
1. In the Azure portal, navigate to your storage account.
2. Open the **Containers** blade and select your container (`inputdata`).
3. Click **Upload** and add the downloaded CSV files.

#### **2.3 Create Azure Data Factory**
1. You can skip this step if you have an existing Data Factory instance otherwise open the Azure Portal and,
2. Search for **Data Factory** in the search bar and click **+ Create**.
3. In the **Basics** tab:
   - Subscription: Choose your subscription.
   - Resource Group: Select the one you created earlier.
   - Name: Provide a name (e.g., `ADF-Lab`).
   - Region: Same as your storage account.
4. Click **Review + Create**, then **Create**.

#### **2.4 Create Azure Databricks Workspace**
1. Open the Azure Portal and search for **Azure Databricks** in the search bar and click **+ Create**.
2. In the **Basics** tab:
   - Subscription: Choose your subscription.
   - Resource Group: Select your existing resource group.
   - Workspace Name: Enter a name (e.g., `Databricks-Lab`).
   - Region: Same as other resources.
3. Click **Review + Create**, then **Create**.
4. Once deployed, go to the resource and click **Launch Workspace**.
5. In the databricks workspace on the Compute tab click Create
6. Set to Terminate after 60 minutes of inactivity
7. Click Create compute
---

### **Step 3: Build the ADF Pipeline**

#### **3.1 Create Linked Services**
1. In ADF Studio, click on **Manage** (gear icon).
2. Under **Linked Services**, click **+ New**.
3. Create the following linked services:
   - **Azure Blob Storage**:
     - Type: Azure Blob Storage.
     - Name: `AzureBlobStorage_LinkedService`.
     - Connection: Select your storage account.
   - **Azure Databricks**:
     - Type: Azure Databricks. You can find Databricks under the "Compute" tab.
     - Name: `AzureDatabricks_LinkedService`.
     - Provide the workspace URL (from the Databricks resource) and authentication details. You can follow the instructions here to get the access token: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/pat
     - Choose any cluster version, cluster node and choose Python 3.
     - Click on "Test connection"
     - Click on the "Create" button

#### **3.2 Create Datasets**
1. Go to **Author**, then click **+** > **Dataset**.
2. Create datasets for:
   - **Input Files**:
     - Dataset Name: `HappinessInput`.
     - Linked Service: `AzureBlobStorage_LinkedService`.
     - Container Path: Point to `inputdata` container.
   - **Output Location**:
     - Dataset Name: `ProcessedData`.
     - Linked Service: `AzureBlobStorage_LinkedService`.
     - File Path: Provide a new container name (e.g., `outputdata/`). Please note, the container must be created in Blob Storage first.

---

### **Step 4: Add Activities to the Pipeline**

#### **4.1 Create a New Pipeline**
1. In ADF Studio, click **+ Pipeline**.

#### **4.2 Add Get Metadata Activity**
1. Drag the **Get Metadata** activity to the canvas.
2. Configure:
   - **Dataset**: Select the dataset pointing to your `happiness.csv` file (e.g., `HappinessInput`).
   - **Field list**: Select `Structure` to get the schema of the CSV file.

#### **4.3 Add Lookup Activity**
1. Drag a **Lookup** activity onto the canvas.
2. Connect the **Get Metadata** activity to the **Lookup** activity.
3. Configure:
   - **Dataset**: Select the same dataset (`HappinessInput`).
   - **First row only**: Set to `false` to retrieve all rows.

#### **4.4 Add Filter Activity**
1. Drag a **Filter** activity onto the canvas.
2. Connect the **Lookup** activity to the **Filter** activity.
3. Configure:
   - **Items**: Use the output from the **Lookup** activity:
     ```json
     @activity('Lookup').output.value
     ```
   - **Condition**: Use the expression to filter rows with `Happiness_Score > 6`:
     ```json
     @greater(item().Happiness_Score, 6)
     ```
   - Click on "Debug" the pipeline and monitor the pipeline
   - Do all the activities succeed? Fix any errors that might occur and proceed

#### **4.5 Add ForEach Activity**
1. Drag a **ForEach** activity onto the canvas.
2. Connect the **Filter** activity to the **ForEach** activity.
3. Configure:
   - **Items**: Use the filtered array from the **Filter** activity:
     ```json
     @activity('Filter').output
     ```
   - **Activities inside ForEach**:
     1. Add a **Copy Activity** to copy each filtered row to the output folder or another destination.
     2. Configure the **Copy Activity**:
        - **Source**: Use the same dataset (`HappinessInput`).
        - **Sink**: Configure the destination dataset (e.g., another CSV file or a database table).


### **Step 5: Debug and Validate**
1. Use the **Debug** function to test your pipeline.
2. Check the output of each activity to ensure the data is being processed correctly.
3. Verify that the filtered rows are copied to the specified output destination.


---

### **Step 5: Integrate Azure Databricks**

#### **5.1 Create Databricks Notebook**
1. Open the Azure Cloud Shell and run the following command to assign the **Storage Blob Data Contributor** role to yourself. Remember to replace the placeholders `{}` with your actual resource values.
   ```bash
   az role assignment create --role "Storage Blob Data Contributor" --assignee {user@domain.com} --scope "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/{storage-account-name}
   ```
2. Get a SaS token value of your storage container using the following command. Copy the value down.
   ```bash
   az storage container generate-sas \
    --account-name <storage-account-name> \
    --name <container-name> \
    --permissions rwl \
    --expiry <expiry-date> \
    --account-key <storage-account-key>
   ```
      Replace the placeholders:

    `<storage-account-name>`: Your Azure Storage account name.
    `<container-name>`: The name of the container.
    `<permissions>`: The access permissions (e.g., r for read, w for write, l for list).
    `<expiry-date>`: The expiry date of the SAS token in UTC (e.g., 2025-01-31T23:59:59Z).
    `<storage-account-key>`: The storage account key
3. Create a new Azure Key Vault resource in your resource group
   ```bash
   az keyvault create --name {key-vault-name} --resource-group {resource-group-name} --location eastus
   ```
4. Next create a secret to store the Azure Storage Acccount access key. If you can't create the key, assign yourself the "Key Vault Administrator" role under the Access Control menu of the key vault resource in the Azure Portal.
   ```bash
   az keyvault secret set --vault-name {key-vault-name} --name storageContainerSaSToken --value "value of your SAS token"
   ```
5. Create a key vault backed secret scope for your Databricks workspace by following the instructions found here: https://docs.azure.cn/en-us/databricks/security/secrets/secret-scopes
6. Launch Databricks workspace and create a new notebook.
7. Paste and adapt the following Spark code:
   ```python
    if not any(mount.mountPoint == '/mnt/<container-name>' for mount in dbutils.fs.mounts()):
        dbutils.fs.mount(
            source = "wasbs://<container-name>@<storage-account-name>.blob.core.windows.net",
            mount_point = "/mnt/<container-name>",
            extra_configs = {"fs.azure.sas.<container-name>.<storage-account-name>.blob.core.windows.net":dbutils.secrets.get(scope = "<scope-you-set-in-step-5>", key = "<secret-name-in-step-5>")}
        )

    df_happiness = spark.read.csv("/mnt/<container-name>/happiness.csv", header=True)
    df_population = spark.read.csv("/mnt/<container-name>/population.csv", header=True)

    joined = df_happiness.join(df_population, df_happiness.Country == df_population.Country)

    dbutils.notebook.exit(joined.toJSON().collect())
   ```
8. Save the notebook.

#### **5.2 Add Databricks Notebook Activity**
1. In ADF, add a **Databricks Notebook** activity.
2. Configure:
   - Linked Service: `AzureDatabricks_LinkedService`.
   - Notebook Path: Path to your Databricks notebook.
   - Parameters: Input file paths.

---

### **Step 6: Create and Use an Azure Function**

#### **6.1 Create an Azure Function**
1. **Set Up Azure Function App**
   - In the Azure Portal, create a new **Function App**.
   - Choose **Python** as the runtime stack.
   - Configure other settings as needed and create the Function App.

2. **Create the Python Function**
   - Follow the instructions here to setup and create an Azure Function with VS Code: https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python
   - In the Function App, create a new function using the **HTTP trigger** template.
   - Replace the default code with the following to read from the Databricks output and write to Azure Database for PostgreSQL:
   - You can test the function locally by using the Postman tool to post the output from the Databricks activity to the function

   ```python
    import azure.functions as func
    import logging
    import json
    import psycopg2

    app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

    @app.route(route="ProcessData")
    def ProcessData(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python HTTP trigger function processed a request.')

        data = req.get_json()

        # PostgreSQL connection details
        host = os.getenv('POSTGRES_HOST')
        dbname = os.getenv('POSTGRES_DBNAME')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        port = os.getenv('POSTGRES_PORT', 5432)

        # Connect to PostgreSQL
        try:
            conn = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port,
                sslmode='require'
            )
            cursor = conn.cursor()
            logging.info("Connected to PostgreSQL successfully")
        except Exception as e:
            logging.error(f"Failed to connect to PostgreSQL: {e}")
            return func.HttpResponse(f"Failed to connect to PostgreSQL: {e}", status_code=500)

        # Create table if it does not exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS public.happiness_population (
            Region VARCHAR(255),
            Country VARCHAR(255),
            Happiness_Score FLOAT,
            Population INT
        )
        '''
        cursor.execute(create_table_query)
        conn.commit()

        if data:
            run_output = data["runOutput"]
            parsed_data = [json.loads(record) for record in run_output]
            for row in parsed_data:
                if row["Region"] == "Europe":
                    cursor.execute(
                        "INSERT INTO public.happiness_population (Region, Country, Happiness_Score, Population) VALUES (%s, %s, %s, %s)",
                        (row['Region'], row['Country'], row['Happiness_Score'], row['Population'])
                    )
                    conn.commit()
            return func.HttpResponse(f"Data processed successfully: {parsed_data}")
        
        
        cursor.close()
        conn.close()
   ```

3. **Configure Environment Variables**
   - In the Function App settings, add the following environment variables:
     - `POSTGRES_HOST`
     - `POSTGRES_DBNAME`
     - `POSTGRES_USER`
     - `POSTGRES_PASSWORD`
     - `POSTGRES_PORT` (optional, default is 5432)

#### **6.2 Add Azure Function Activity in ADF**
1. In ADF, add an **Azure Function** activity.
2. Configure:
   - **Linked Service**: Create a linked service pointing to your Azure Function App.
   - **Function Name**: Select the function you created.
   - **Method**: POST
   - **Body**: Pass the output from the Databricks notebook to the function. `@activity('Notebook1').output`

---

### **Step 7: Debug and Validate**
1. Use the **Debug** function to test your pipeline.
2. Check the output of each activity to ensure the data is being processed correctly.
3. Verify that the data is inserted into the Azure Database for PostgreSQL.

```



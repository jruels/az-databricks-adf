### **Lab Exercise: Transforming a Dataset from Azure Blob Storage to Azure PostgreSQL with Data Flow in Azure Data Factory**

---

### **Objective**
This lab demonstrates how to transform a dataset stored in Azure Blob Storage using a Data Flow in Azure Data Factory (ADF). The transformed data will be loaded into Azure Database for PostgreSQL. You will apply transformations such as filtering, joining, and aggregations in the data flow.

---

### **Prerequisites**

Before starting, ensure you:
1. Have an [Azure account](https://azure.microsoft.com/free/).
2. Completed labs 1 to 4
3. Lab Datasets
4. Set up Azure resources:
   - **Azure Blob Storage**: Upload the dataset.
   - **Azure Database for PostgreSQL**: Create a target table.
5. Set up **Azure Data Factory**: Create an ADF instance.

---

### **Scenario**

You will process two CSV files:
1. `happiness.csv` (World Happiness Report).
2. `population.csv` (Population data for countries).

The goal is to:
1. Filter records for a specific year (e.g., 2021).
2. Join the happiness dataset with population data.
3. Calculate the average happiness score and total population for each region.
4. Load the transformed data into a PostgreSQL table.

---

### **Step-by-Step Instructions**

---

### **Part 1: Set Up Azure Resources**

#### 1. **Azure Blob Storage**
1. Use an existing storage account from previous labs or create a new **Storage Account** in the [Azure Portal](https://portal.azure.com).
   - Follow the instructions: [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create).
2. Create a **Container** (e.g., `datasets`).
3. Upload the `happiness.csv` and `population.csv` files into the container.

#### 2. **Azure Database for PostgreSQL**
1. Use the existing PostgresSQL server from previous labs or create an **Azure Database for PostgreSQL** server: 
   - Follow instructions: [Create a PostgreSQL database](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server?tabs=portal-create-flexible%2Cportal-get-connection%2Cportal-delete-resources#create-an-azure-database-for-postgresql-flexible-server-instance).
2. Connect to your server using pgAdmin 4 then right click Databases and click on Create -> Database
3. Enter "analytics" as the name of the database
4. Right click on the "analytics" database and open the Query Tool and run the query below to create a table 
   ```sql
   CREATE TABLE transformed_data (
       region VARCHAR(100),
       avg_happiness_score FLOAT,
       total_population BIGINT
   );
   ```

---

### **Part 2: Build the Data Factory Pipeline**

#### 1. **Create Azure Data Factory**
1. Use an existing Data Factory or in the Azure Portal, create an **Azure Data Factory** instance:
   - Follow instructions: [Create an Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal).

2. Open **Data Factory Studio**.

---

### **Part 3: Set Up Linked Services and Datasets**

#### 1. **Set Up Linked Services**
1. Navigate to **Manage > Linked Services > New**:
   - **Blob Storage**:
     - Select **Azure Blob Storage** and authenticate with your Storage Account containing the happiness and population csv files. Remember to give your linked service a unique name.
   - **PostgreSQL**:
     - Click on `+ New` then select **Azure Database for PostgreSQL** and provide server details (host, username, password, database). Remember to give your linked service a unique name. DO NOT FORGET TO SELECT SSL FOR ENCRYPTION METHOD.

#### 2. **Create Datasets**
1. **Blob Storage Dataset** (Source):
   - Go to **Author > Datasets > New Dataset**.
   - Select **Azure Blob Storage**
   - Select **Delimited Text**.
   - Link it to your Blob Storage linked service.
   - Configure a dataset and the file paths for `happiness.csv` and name it `HappinessDataset`.
   - Schema > Import schema > From connection/store
   - Repeat the process for `population.csv` and name `PopulationDataset`.

2. **PostgreSQL Dataset** (Sink):
   - Go to **Author > Datasets > New Dataset**.
   - Select **Azure Database for PostgreSQL Table**.
   - Link it to your PostgreSQL linked service.
   - Select the `transformed_data` table.
   - name the dataset `TransformedDataset`.

---

### **Part 4: Create and Configure Data Flow**

#### 1. **Create a Data Flow**
1. Go to **Author > Data Flows > New Data Flow**.
2. Name it `TransformDataFlow`.
3. Enable `Data Flow Debug` so that you can test the data flow and preview the output of each step.

---

#### 2. **Add a Source for Happiness Data**
1. Add a **Source** onto the canvas and configure:
   - **Source Dataset**: Select the `HappinessDataset` dataset.
   - **Projection**: Allow schema inference or manually define columns.
2. Rename the source as `HappinessData`.

---

#### 3. **Add a Source for Population Data**
1. Add another **Source** onto the canvas and configure:
   - **Source Dataset**: Select the `population.csv` dataset `PopulationDataset`
   - **Projection**: Define columns like `Country`, `Year`, and `Population`.
2. Rename the source as `PopulationData`.

---

#### 4. **Filter the Data**
1. Add a **Filter** transformation to `HappinessData`:
   - Click the "+" on the `HappinessData` and add a **Filter** onto the canvas.
   - Configure the condition:
     ``` 
     Year == 2021
     ```
   - Rename it to `FilteredHappiness`.

---

#### 5. **Join the Data**
1. Add a **Join** transformation onto the canvas and connect it to `FilteredHappiness` as the Left Stream and `PopulationData` as the Right Stream. You can a a transformation by clicking the "+" button on the `FilteredHappiness` filter.
2. Configure the join:
   - **Join Condition**: Match `Country` in both datasets.
   - **Join Type**: Inner join.
   - Rename it to `JoinedData`.

---

#### 6. **Aggregate Data**
1. Add a **Cast** transformation to the `JoinedData` transformation to convert the Happiness_Score and Population columns to the float and integer data types respectively.
2. Name it `CastedData`
3. Add an **Aggregate** transformation:
   - Connect it to `CastedData`.
   - Configure the aggregations:
     - **Group By**: `Region`.
     - **Aggregates**:
       - `round(avg(Happiness_Score),2)` as `AvgHappinessScore`.
       - `sum(Population)` as `TotalPopulation`.
   - Rename it to `AggregatedData`.

---

#### 7. **Sink the Data**
1. Add a **Sink** transformation by clicking "+" on to connect it to `AggregatedData`.
   - Configure:
     - **Sink Dataset**: Select the PostgreSQL dataset.
     - **Write Behavior**: Choose `Allow Insert` for the update method under settings.
     - **Mapping**: Map the transformed columns to the PostgresSQL table columns
   - Rename it to `LoadToPostgreSQL`.

#### 8. **Debugging transformations**

You can preview the output data for each transformation by enabling the `Data flow debug` option.

---

### **Part 5: Build the Pipeline**

1. Create a new **Pipeline** and drag the `TransformDataFlow` onto the canvas.
2. Validate the pipeline to ensure there are no errors.
3. Click Publish All

---

### **Part 6: Run, Monitor, and Verify**

#### 1. **Run the Pipeline**
1. Trigger the pipeline by clicking **+ Add Trigger** -> **Trigger Now**.
2. Monitor the run in the **Monitor** tab.

#### 2. **Verify the Data**
1. Open the `analytics` database using pgAdmin 4 or a PostgresSQL admin tool of choice
2. Open the query tool then,
3. Query the `transformed_data` table in PostgreSQL to verify the results:
   ```sql
   SELECT * FROM transformed_data;
   ```

---

### **Resources and References**
1. [Azure Blob Storage Documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/)
2. [Azure Database for PostgreSQL Documentation](https://learn.microsoft.com/en-us/azure/postgresql/)
3. [Azure Data Factory Documentation](https://learn.microsoft.com/en-us/azure/data-factory/)


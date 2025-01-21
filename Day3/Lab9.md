### **Lab Exercise: Migrating Data from PostgreSQL to Azure SQL Database with Azure Data Factory (ADF)**

---

### **Objective**
This lab demonstrates how to migrate data from a PostgreSQL database to an Azure SQL Database using Azure Data Factory (ADF). You will learn to set up a pipeline, configure source and sink datasets, perform both full and incremental data loads, and implement transformations to handle insert and update operations during migration.

---

### **Prerequisites**

Before starting, ensure you:
1. Have an [Azure account](https://azure.microsoft.com/free/).
2. Set up the following Azure resources:
   - **Azure SQL Database**: Create an SQL Database and a target table.
   - **PostgreSQL Database**: Set up the PostgreSQL database with source data.
   - **Azure Data Factory**: Create an ADF instance.

---

### **Scenario**
You have an existing PostgreSQL database with a table `employee_data` that holds employee records. The task is to:
1. Migrate the data to an Azure SQL Database.
2. Implement full load and incremental load strategies for migrating data.
3. Handle insert and update operations on the Azure SQL database.
4. Implement data validation post-migration.

---

### **Step-by-Step Instructions**

---

### **Part 1: Set Up Azure Resources**

#### 1. **Azure PostgreSQL Database (Source)**
1. Use the existing PostgreSQL instance or create a new **Azure Database for PostgreSQL**.
   - Follow instructions: [Create a PostgreSQL database](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server).
2. Connect to your PostgreSQL database using a tool like **pgAdmin** or **psql**.
3. Create a table named `employee_data` using the following SQL script:
   ```sql
   CREATE TABLE employee_data (
       employee_id SERIAL PRIMARY KEY,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       department VARCHAR(50),
       hire_date DATE,
       salary DECIMAL
   );
   ```
4. Populate the `employee_data` table with sample records (you can use insert queries or import sample data).

#### 2. **Azure SQL Database (Sink)**
1. Use an existing **Azure SQL Database** or create one.
   - Follow instructions: [Create an Azure SQL Database](https://learn.microsoft.com/en-us/azure/sql-database/sql-database-get-started-portal).
2. Create a table named `employee_data` in the Azure SQL Database using the following SQL script:
   ```sql
   CREATE TABLE employee_data (
       employee_id INT PRIMARY KEY,
       first_name NVARCHAR(50),
       last_name NVARCHAR(50),
       department NVARCHAR(50),
       hire_date DATE,
       salary DECIMAL
   );
   ```

---

### **Part 2: Create the Azure Data Factory Pipeline**

#### 1. **Set Up Azure Data Factory**
1. Use an existing Data Factory or create a new **Azure Data Factory** instance:
   - Follow instructions: [Create an Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal).
2. Open **Data Factory Studio**.

---

### **Part 3: Set Up Linked Services and Datasets**

#### 1. **Create Linked Services**
1. **PostgreSQL Linked Service (Source)**:
   - Navigate to **Manage > Linked Services > New**.
   - Choose **Azure Database for PostgreSQL** and authenticate with your PostgreSQL server.
   - Provide connection details (server name, username, password, and database name).

2. **Azure SQL Linked Service (Sink)**:
   - Navigate to **Manage > Linked Services > New**.
   - Choose **Azure SQL Database** and authenticate with your Azure SQL server.
   - Provide connection details (server name, username, password, and database name).

#### 2. **Create Datasets**
1. **PostgreSQL Dataset (Source)**:
   - Go to **Author > Datasets > New Dataset**.
   - Choose **Azure Database for PostgreSQL** and select the PostgreSQL linked service.
   - Select the `employee_data` table from the source PostgreSQL database.

2. **Azure SQL Dataset (Sink)**:
   - Go to **Author > Datasets > New Dataset**.
   - Choose **Azure SQL Database** and select the Azure SQL linked service.
   - Select the `employee_data` table from the target Azure SQL database.

---

### **Part 4: Create and Configure the Data Pipeline**

#### 1. **Create a New Pipeline**
1. Go to **Author > Pipelines > New Pipeline**.
2. Name the pipeline `MigrateEmployeeData`.

#### 2. **Configure Copy Activity for Full Load**
1. Add a **Copy Data** activity to the pipeline.
2. Configure the **Source**:
   - Choose the **PostgreSQL Dataset**.
   - Set the **Source Query** to fetch all records:
     ```sql
     SELECT * FROM employee_data;
     ```
3. Configure the **Sink**:
   - Choose the **Azure SQL Dataset**.
   - Set the **Write Behavior** to `Insert` (to load data for the first time).

#### 3. **Configure Incremental Load (CDC)**
1. **Change Data Capture (CDC)**: 
   - Create a **Stored Procedure** in PostgreSQL to identify the changed records based on `last_modified` date or other logic.
     ```sql
     SELECT * FROM employee_data WHERE last_modified > 'last_checkpoint_date';
     ```
2. Use **Stored Procedure Activity** or a **Copy Activity** with dynamic query for incremental load in the pipeline. You can set a parameter for `last_checkpoint_date` that will be passed each time the pipeline runs.

#### 4. **Configure Data Transformations (Upsert Logic)**
1. For handling **Insert, Update, and Upsert** operations:
   - Create a **Stored Procedure** in Azure SQL Database to perform upsert logic (combining `INSERT` and `UPDATE` operations):
     ```sql
     MERGE INTO employee_data AS target
     USING (SELECT employee_id, first_name, last_name, department, hire_date, salary FROM staging_employee_data) AS source
     ON target.employee_id = source.employee_id
     WHEN MATCHED THEN
         UPDATE SET target.first_name = source.first_name, target.last_name = source.last_name, 
                    target.department = source.department, target.hire_date = source.hire_date, 
                    target.salary = source.salary
     WHEN NOT MATCHED THEN
         INSERT (employee_id, first_name, last_name, department, hire_date, salary)
         VALUES (source.employee_id, source.first_name, source.last_name, source.department, source.hire_date, source.salary);
     ```
2. Use a **Stored Procedure Activity** in the pipeline to call the upsert procedure after the data copy.

---

### **Part 5: Debugging and Running the Pipeline**

#### 1. **Debugging the Pipeline**
1. In the pipeline, click **Debug** to run the pipeline in test mode and review any errors.

#### 2. **Run the Pipeline**
1. Trigger the pipeline using **Trigger Now**.
2. Monitor the execution in the **Monitor** tab to ensure the pipeline runs successfully.

---

### **Part 6: Verifying the Data**

1. Query the `employee_data` table in Azure SQL Database to verify that data has been copied and transformed correctly:
   ```sql
   SELECT * FROM employee_data;
   ```

2. Ensure that both full and incremental loads are working as expected, and that upserts are updating existing records and inserting new ones.

---

### **Expected Outcome**
After completing this lab, you should be able to:
- Migrate data from PostgreSQL to Azure SQL Database using ADF.
- Set up full and incremental load strategies.
- Handle insert, update, and upsert operations during data migration.
- Use ADF to automate data migrations with proper validation.
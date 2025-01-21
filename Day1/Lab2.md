# Lab 2: Create a Pipeline with Azure Database for PostgreSQL

**Objective:**
Create a simple Azure Data Factory pipeline that copies data from an Azure Storage account to an Azure Database for PostgreSQL table.

**Pre-requisites:**
* An Azure subscription.
* The resource group created in **Lab 1**.

**Detailed Steps:**
1. **Create a Storage Account (in the Lab1 Resource Group):**
   - In the Azure portal, search for "Storage accounts," select "+ Create," use the same resource group from Lab1, and provide a unique name.  
   - Choose region/replication, then click "Review + Create" → "Create."  
   - Click "Go to Resource" to navigate to the storage account.
   - Go to "Data storage" then click on "Containers". Create a container (e.g., "inputcontainer") to store the data file (CSV or JSON).
   - Create a new csv file `lab2data.csv ` and paste the following text:
```csv
id,name,value
1,Name1,100
2,Name2,200
3,Name3,300
4,Name4,400
5,Name5,500
6,Name6,600
7,Name7,700
8,Name8,800
9,Name9,900
10,Name10,1000
11,Name11,1100
12,Name12,1200
13,Name13,1300
14,Name14,1400
15,Name15,1500
16,Name16,1600
17,Name17,1700
18,Name18,1800
19,Name19,1900
20,Name20,2000
21,Name21,2100
22,Name22,2200
23,Name23,2300
24,Name24,2400
25,Name25,2500
26,Name26,2600
27,Name27,2700
28,Name28,2800
29,Name29,2900
30,Name30,3000
```
    - Copy the lab2data.csv file and upload it to the inputcontainer
2. **Create an Azure Database for PostgreSQL (in the Lab1 Resource Group):**
   - Search for " Azure Database for PostgreSQL Flexible server," select "+ Create" and choose "Single server" (or "Flexible server").  
   - Assign the same resource group from Lab1, provide server name, admin username, password, location, and pricing tier.  
   - Select "PostgreSQL authentication only" for Authentication method
   - After creation, enable access by configuring firewall rules under "Connection security."
   - Click "Go to Resource" to open the database overview page
   - Click on Connect and choose a connect method, for this exercise you can select pgAdmin 4 and follow the instructions. (You can download and install pgAdmin from this url: https://www.pgadmin.org/download/)

3. **Prepopulate the Database with Example Data:**
   - Right click databases then click "Create" → "Database"
   - Give the database a name e.g. "lab2db"  
   - Right click the database you created above and click "Query Tool"
   - Paste the code below to create a new table
     ```sql
     CREATE TABLE public.sample_data (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       value INT
     );
     ```
   - Insert some rows:
     ```sql
     INSERT INTO public.sample_data (name, value)
     VALUES ('Test1', 123), ('Test2', 456);
     ```

4. **Open ADF Studio:**
   - In the portal, go to your Data Factory instance (also created in Lab1) and click "Launch Studio" to open ADF Studio.

5. **Author a New Pipeline:**
   - In ADF Studio, click the "Author" tab, then “+” → "Pipeline."  
   - Rename it (e.g., "PostgreSQLCopyPipeline").

6. **Add Copy Activity:**
   - Search for "Copy" in the Activities panel and drag "Copy data" onto the canvas.

7. **Configure Source and Sink for the Copy Activity:**
   - **Source**: Create/select a linked service pointing to your storage account and a dataset referencing your input file. 
   - To create a new linked service, click "+ New" in the Source tab
   - Select Azure Blob Storage from the data store options and press Continue
   - Choose Excel for the data format
   - Click "+ New" under linked service
   - Give the linked service a name for example "AzureBlobStorageSource"
   - Select the subscription containing your storage account
   - Select your storage account name from the drop down options and click "Create"
   - Under file path, browse to the location of the csv file in the storage account and select it
   - Click "Ok"
   - Click "Preview data" to check if connection to the storage account was successful
   - **Sink**: Create/select a linked service pointing to your PostgreSQL server and choose a table dataset pointing to "public.sample_data."
   - Click on "+ New" in the Sink tab
   - Select "Azure Database for PostgreSQL"
   - Click "+ New" under linked service
   - Select name of the server you created in Step 2 above
   - Enter your server user name and password
   - Select SSL as encyption method
   - Click on test connection
   - If you get an error message for example `Failed to connect to your instance of Azure Database for PostgreSQL flexible server.
28000: no pg_hba.conf entry for host "20.42.3.136", user "adfadmin", database "lab2db", no encryption`, go to the Networking settings of the database server in Azure and allow the IP Address through the firewall.
   - Click on "Create"
   - Select the `public.sample_data` table
   - Press "OK"


8. **Publish Changes:**
   - Click "Publish all" to save and deploy the pipeline.

**Expected Output:**
Your pipeline copies data from the storage file into the Azure Database for PostgreSQL table.

**Troubleshooting:**
* Verify firewall settings for PostgreSQL.
* Check that your linked services and datasets use correct credentials.
* Ensure storage container and PostgreSQL table names match your setup.